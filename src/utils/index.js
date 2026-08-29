export function isValidJwt(jwt) {
  if (!jwt || jwt.split('.').length < 3) {
    return false;
  }
  const data = JSON.parse(atob(jwt.split('.')[1])); // atob decodes base64 encoded string
  const exp = new Date(data.exp * 1000); // JS deals with dates in milliseconds and in flask we had seconds
  const now = new Date();
  return now < exp;
}

export function isValidEmail(email) {
  /* eslint max-len: ["error", { "code": 200 }] */
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

export function getLastItem(path) {
  return path.substring(path.lastIndexOf('/') + 1);
}

export function formatDate(date) {
  return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
}

export function formatTime(date) {
  return `${date.getHours()}:${date.getMinutes()}`;
}

export function formatDateTime(date) {
  return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}  ${date.getHours()}:${date.getMinutes()}`;
}

export function isValidDate(d) {
  /* eslint-disable-next-line no-restricted-globals */
  return d instanceof Date && !isNaN(d);
}

// export function parseTuple(t) {
//   const newT = t
//     .replace(/'/g, '"')
//     .replace('(', '[')
//     .replace(')', ']');
//   return JSON.parse(newT);
// }

export function setQuoteSeries(data) {
  const series = [];
  const symbols = Object.keys(data);

  for (let i = 0; i < symbols.length; i += 1) {
    const symbol = symbols[i];
    const closeKeys = Object.keys(data[symbol].Close);
    const closeValues = Object.values(data[symbol].Close);

    if (closeValues.length > 0) {
      const quoteSeries = {
        name: symbol,
        openPrice: Object.values(data[symbol].Open)[0],
        data: [],
      };

      // this below fixes the problem where one line chart ends too soon
      for (let j = 0; j < closeValues.length; j += 1) {
        if (closeValues[j]) {
          quoteSeries.data.push([closeKeys[j], closeValues[j]]);
        }
      }
      series.push(quoteSeries);
    }
  }
  return series;
}

export function groupBy(xs, key) {
  return xs.reduce((rv, x) => {
    /* eslint-disable-next-line no-param-reassign */
    (rv[x[key]] = rv[x[key]] || []).push(x);
    return rv;
  }, {});
}

export function percentChange(first, last) {
  return ((last - first) / first) * 100;
}

export function percent(number, total) {
  return (number / total) * 100;
}

// Compacts large numbers for display, e.g. 12000000 -> "12M", 32248789 -> "32.25M".
export function formatCompactNumber(value) {
  if (value === null || value === undefined || value === '' || Number.isNaN(+value)) return null;
  const num = +value;
  const units = [
    { threshold: 1e12, suffix: 'T' },
    { threshold: 1e9, suffix: 'B' },
    { threshold: 1e6, suffix: 'M' },
    { threshold: 1e3, suffix: 'K' },
  ];
  const unit = units.find((u) => Math.abs(num) >= u.threshold);
  if (!unit) return num.toLocaleString('en-US');
  return `${(num / unit.threshold).toFixed(2).replace(/\.?0+$/, '')}${unit.suffix}`;
}
