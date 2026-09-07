// NYSE/Nasdaq trading-session detection - client-side, no API call needed.
// Everything below is standard-hours logic (regular session 9:30-16:00 ET,
// with pre/post windows); it does not account for one-off intraday
// halts or ad hoc exchange closures, and treats the Thanksgiving/Christmas
// Eve early-close days as normal full sessions.

const ET_TIME_ZONE = 'America/New_York';

function partsInNewYork(date) {
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: ET_TIME_ZONE,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    weekday: 'short',
  }).formatToParts(date);
  const get = (type) => parts.find((p) => p.type === type).value;
  const hour = Number(get('hour')) % 24; // some locales report midnight as "24"
  return {
    year: Number(get('year')),
    month: Number(get('month')),
    day: Number(get('day')),
    minutesSinceMidnight: hour * 60 + Number(get('minute')),
    weekday: get('weekday'), // 'Mon' .. 'Sun'
  };
}

// Anonymous Gregorian algorithm for the date of Easter Sunday.
function easterSunday(year) {
  const a = year % 19;
  const b = Math.floor(year / 100);
  const c = year % 100;
  const d = Math.floor(b / 4);
  const e = b % 4;
  const f = Math.floor((b + 8) / 25);
  const g = Math.floor((b - f + 1) / 3);
  const h = (19 * a + b - d - g + 15) % 30;
  const i = Math.floor(c / 4);
  const k = c % 4;
  const l = (32 + 2 * e + 2 * i - h - k) % 7;
  const m = Math.floor((a + 11 * h + 22 * l) / 451);
  const month = Math.floor((h + l - 7 * m + 114) / 31);
  const day = ((h + l - 7 * m + 114) % 31) + 1;
  return { month, day };
}

function nthWeekday(year, month, weekday, n) {
  // weekday: 0=Sun..6=Sat
  const firstOfMonth = new Date(Date.UTC(year, month - 1, 1)).getUTCDay();
  const offset = (weekday - firstOfMonth + 7) % 7;
  return 1 + offset + (n - 1) * 7;
}

function lastWeekday(year, month, weekday) {
  const daysInMonth = new Date(Date.UTC(year, month, 0)).getUTCDate();
  const lastDayWeekday = new Date(Date.UTC(year, month - 1, daysInMonth)).getUTCDay();
  return daysInMonth - ((lastDayWeekday - weekday + 7) % 7);
}

// Sat -> observed the Friday before; Sun -> observed the Monday after.
function observedDay(year, month, day) {
  const weekday = new Date(Date.UTC(year, month - 1, day)).getUTCDay();
  if (weekday === 6) return day - 1;
  if (weekday === 0) return day + 1;
  return day;
}

function holidaysForYear(year) {
  const goodFriday = easterSunday(year);
  const goodFridayDate = new Date(Date.UTC(year, goodFriday.month - 1, goodFriday.day - 2));

  return [
    { month: 1, day: observedDay(year, 1, 1), name: "New Year's Day" },
    { month: 1, day: nthWeekday(year, 1, 1, 3), name: 'Martin Luther King Jr. Day' },
    { month: 2, day: nthWeekday(year, 2, 1, 3), name: "Washington's Birthday" },
    { month: goodFridayDate.getUTCMonth() + 1, day: goodFridayDate.getUTCDate(), name: 'Good Friday' },
    { month: 5, day: lastWeekday(year, 5, 1), name: 'Memorial Day' },
    { month: 6, day: observedDay(year, 6, 19), name: 'Juneteenth' },
    { month: 7, day: observedDay(year, 7, 4), name: 'Independence Day' },
    { month: 9, day: nthWeekday(year, 9, 1, 1), name: 'Labor Day' },
    { month: 11, day: nthWeekday(year, 11, 4, 4), name: 'Thanksgiving Day' },
    { month: 12, day: observedDay(year, 12, 25), name: 'Christmas Day' },
  ];
}

function holidayOn(year, month, day) {
  return holidaysForYear(year).find((h) => h.month === month && h.day === day) || null;
}

const SESSION = {
  PRE: {
    key: 'pre', label: 'Pre-Market', start: 4 * 60, end: 9 * 60 + 30,
  },
  REGULAR: {
    key: 'open', label: 'Market Open', start: 9 * 60 + 30, end: 16 * 60,
  },
  POST: {
    key: 'post', label: 'After-Hours', start: 16 * 60, end: 20 * 60,
  },
};

export function getMarketStatus(date = new Date()) {
  const {
    year, month, day, minutesSinceMidnight, weekday,
  } = partsInNewYork(date);

  const isWeekend = weekday === 'Sat' || weekday === 'Sun';
  const holiday = !isWeekend ? holidayOn(year, month, day) : null;

  if (!isWeekend && !holiday) {
    if (minutesSinceMidnight >= SESSION.PRE.start && minutesSinceMidnight < SESSION.PRE.end) {
      return { key: SESSION.PRE.key, label: SESSION.PRE.label, detail: 'Opens at 9:30 AM ET' };
    }
    if (minutesSinceMidnight >= SESSION.REGULAR.start && minutesSinceMidnight < SESSION.REGULAR.end) {
      return { key: SESSION.REGULAR.key, label: SESSION.REGULAR.label, detail: null };
    }
    if (minutesSinceMidnight >= SESSION.POST.start && minutesSinceMidnight < SESSION.POST.end) {
      return { key: SESSION.POST.key, label: SESSION.POST.label, detail: 'Regular session has closed' };
    }
  }

  if (holiday) {
    return { key: 'closed', label: 'Market Closed', detail: holiday.name };
  }
  if (isWeekend) {
    return { key: 'closed', label: 'Market Closed', detail: 'Weekend' };
  }
  return { key: 'closed', label: 'Market Closed', detail: 'Opens at 9:30 AM ET' };
}

// Yahoo/yfinance ticker suffix conventions: "-USD" (and similar) for crypto
// pairs, "=X" for FX pairs, "=F" for futures/commodities.
function isCryptoSymbol(symbol) {
  return /-(usd|usdt|eur|gbp|btc|eth)$/i.test(symbol);
}
function isForexOrFuturesSymbol(symbol) {
  return /=(x|f)$/i.test(symbol);
}

// FX and futures trade nearly continuously - open from Sunday 5pm ET
// through Friday 5pm ET, with just the one weekend gap. This doesn't model
// the daily short maintenance breaks futures exchanges take, but it's close
// enough for "is it worth polling right now".
function isForexOrFuturesOpen(date) {
  const { weekday, minutesSinceMidnight } = partsInNewYork(date);
  const SESSION_BREAK = 17 * 60; // 5:00 PM ET
  if (weekday === 'Sat') return false;
  if (weekday === 'Sun') return minutesSinceMidnight >= SESSION_BREAK;
  if (weekday === 'Fri') return minutesSinceMidnight < SESSION_BREAK;
  return true;
}

// Whether it's worth polling live prices for this symbol right now - crypto
// trades 24/7, FX/futures nearly so, and everything else (equities,
// indices) only actually moves during NYSE's pre/regular/post sessions.
export function isSymbolTrading(symbol, date = new Date()) {
  if (!symbol) return false;
  if (isCryptoSymbol(symbol)) return true;
  if (isForexOrFuturesSymbol(symbol)) return isForexOrFuturesOpen(date);
  return getMarketStatus(date).key !== 'closed';
}

export default getMarketStatus;
