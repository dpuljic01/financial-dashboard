<template>
  <div class="market-overview">
    <div v-if="!loaded" class="futures noselect" aria-hidden="true">
      <div class="ticker-card ticker-card-skeleton" v-for="n in 9" :key="n">
        <div class="skeleton-line skeleton-label"></div>
        <div class="skeleton-line skeleton-price"></div>
        <div class="skeleton-block skeleton-chart"></div>
      </div>
    </div>
    <div v-else>
      <div class="market-overview-toolbar">
        <md-button class="md-icon-button md-dense" @click="fetchStockHistory(true)">
          <md-icon>refresh</md-icon>
        </md-button>
      </div>
      <div class="futures noselect">
        <router-link
          class="ticker-card"
          :class="`ticker-card--${value.trend}`"
          v-for="(value, index) in trendData"
          :key="index"
          :to="`/quote/${value.name}`"
        >
          <div class="ticker-card-header">
            <span class="ticker-label">{{ value.label }}</span>
            <span class="ticker-change fin-figure" :class="`ticker-change--${value.trend}`">{{ value.change }}</span>
          </div>
          <div class="ticker-price fin-figure">{{ value.price }}</div>
          <LightweightChart :series="value.lwcSeries" :height="110" sparkline />
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { setQuoteSeries, percentChange } from '../../utils';
import LightweightChart from './LightweightChart.vue';

// Matches the backend's yfinance history cache timeout, so the localStorage
// cache never holds data staler than what a fresh request would return anyway.
const TREND_CACHE_TTL_MS = 5 * 60 * 1000;

export default {
  name: 'TrendChart',
  components: {
    LightweightChart,
  },
  data() {
    return {
      symbols: ['EURUSD=X', '^gspc', '^dji', '^ixic', '^rut', 'cl=f', 'gc=f', 'si=f', '^vix'], // most popular indexes
      trendData: [],
      interval: '1m',
      period: '1d',
      loaded: false,
    };
  },
  mounted() {
    this.fetchStockHistory();
  },
  methods: {
    async fetchStockHistory(reload = false) {
      this.loaded = false;
      this.trendData = [];
      const data = await this.fetchTrendData(reload);
      const series = setQuoteSeries(data);
      this.setTrendData(series);
      this.loaded = true;
    },
    async fetchTrendData(reload) {
      const cached = reload ? null : JSON.parse(localStorage.getItem('_trendData'));
      const isFresh = cached && cached.timestamp && Date.now() - cached.timestamp < TREND_CACHE_TTL_MS;
      if (isFresh && Object.keys(cached.data).length > 0) {
        return cached.data;
      }
      const resp = await this.$store.dispatch('getStockHistoryData', {
        symbols: this.symbols.join(),
        interval: this.interval,
        period: this.period,
        include_info: false,
      });
      const { data } = resp;
      localStorage.setItem('_trendData', JSON.stringify({ data, timestamp: Date.now() }));
      return data;
    },
    setTrendData(series) {
      for (let i = 0; i < series.length; i += 1) {
        const serieLength = Object.keys(series[i].data).length;
        const symbol = this.nameFromSymbol(series[i].name);
        const latestPrice = series[i].data[serieLength - 1][1];
        const { openPrice } = series[i];
        const positiveTrend = openPrice < latestPrice;
        const changePercent = percentChange(openPrice, latestPrice);
        let trend = 'flat';
        if (changePercent) {
          trend = positiveTrend ? 'up' : 'down';
        }
        const { name } = series[i];
        /* eslint-disable-next-line no-param-reassign */
        series[i].name = symbol;
        const gain = trend !== 'down';
        const chartData = {
          name,
          label: symbol,
          price: `$${(+latestPrice).toFixed(2)}`, // last value is the newest
          trend,
          change: changePercent ? `${changePercent > 0 ? '+' : ''}${changePercent.toFixed(2)}%` : 'NA',
          lwcSeries: [
            {
              type: 'area',
              data: this.toLwcData(series[i].data),
              color: gain ? '#0f9d70' : '#d1435c',
              lineWidth: 1.5,
              topColor: gain ? 'rgba(15, 157, 112, 0.25)' : 'rgba(209, 67, 92, 0.25)',
              bottomColor: 'rgba(0, 0, 0, 0)',
            },
          ],
        };
        this.trendData.push(chartData);
      }
    },
    // apexcharts-era data shape ([isoDateString, value] pairs) into
    // lightweight-charts' {time (unix seconds), value} points - sorted and
    // deduped by second, since the library rejects out-of-order/duplicate
    // timestamps.
    toLwcData(pairs) {
      const bySecond = new Map();
      pairs.forEach(([isoDate, value]) => {
        if (value === null || value === undefined) return;
        const time = Math.floor(new Date(isoDate).getTime() / 1000);
        bySecond.set(time, value);
      });
      return [...bySecond.entries()]
        .sort((a, b) => a[0] - b[0])
        .map(([time, value]) => ({ time, value }));
    },
    nameFromSymbol(symbol) {
      const mapping = {
        '^gspc': 'S&P 500',
        '^dji': 'DOW 30',
        '^ixic': 'NASDAQ',
        '^rut': 'Russell 2000',
        'cl=f': 'Crude Oil',
        'gc=f': 'Gold',
        'si=f': 'Silver',
        'EURUSD=X': 'EUR/USD',
        '^vix': 'Vix',
      };
      return mapping[symbol];
    },
  },
};
</script>

<style scoped>
.market-overview-toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: -4px;
}
.futures {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  overflow-y: hidden;
  flex-direction: row;
  justify-content: flex-start;
  align-items: stretch;
  padding: 4px 4px 18px;
}
.ticker-card {
  position: relative;
  width: 240px;
  min-width: 240px;
  max-width: 240px;
  height: 210px;
  min-height: 210px;
  padding: 16px 18px 10px 22px;
  display: flex;
  flex-direction: column;
  text-decoration: none;
  background: var(--surface-color);
  border: 1px solid var(--surface-border);
  border-radius: 14px;
  box-shadow: var(--surface-shadow);
  overflow: hidden;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.ticker-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
}
.ticker-card--up::before {
  background: var(--gain-color);
}
.ticker-card--down::before {
  background: var(--loss-color);
}
.ticker-card--flat::before {
  background: rgba(0, 0, 0, 0.15);
}
.ticker-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(17, 40, 40, 0.14);
}
.ticker-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}
.ticker-label {
  font-size: 13px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.65);
  letter-spacing: 0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.ticker-change {
  font-size: 12px;
  font-weight: 700;
  padding: 2px 9px;
  border-radius: 999px;
  white-space: nowrap;
  flex-shrink: 0;
}
.ticker-change--up {
  color: var(--gain-color);
  background: var(--gain-tint);
}
.ticker-change--down {
  color: var(--loss-color);
  background: var(--loss-tint);
}
.ticker-change--flat {
  color: rgba(0, 0, 0, 0.5);
  background: rgba(0, 0, 0, 0.06);
}
.ticker-price {
  font-size: 23px;
  font-weight: 700;
  color: #0a2f31;
  margin: 8px 0 6px;
}

.ticker-card-skeleton {
  gap: 0;
}
.skeleton-line,
.skeleton-block {
  border-radius: 6px;
  background: linear-gradient(90deg, rgba(0, 0, 0, 0.06) 25%, rgba(0, 0, 0, 0.12) 37%, rgba(0, 0, 0, 0.06) 63%);
  background-size: 400% 100%;
  animation: skeleton-shimmer 1.4s ease infinite;
}
.skeleton-label {
  width: 60%;
  height: 13px;
}
.skeleton-price {
  width: 80%;
  height: 22px;
  margin: 8px 0 6px;
}
.skeleton-chart {
  flex: 1;
  width: 100%;
  border-radius: 8px;
}
@keyframes skeleton-shimmer {
  0% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0 50%;
  }
}
@media (prefers-reduced-motion: reduce) {
  .skeleton-line,
  .skeleton-block {
    animation: none;
  }
}

::-webkit-scrollbar {
  height: 5px;
}

/* Track */
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  -webkit-border-radius: 10px;
  border-radius: 10px;
}

/* Handle */
::-webkit-scrollbar-thumb {
  -webkit-border-radius: 10px;
  border-radius: 10px;
  background: rgba(85, 85, 85, 0.8);
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5);
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5);
}
::-webkit-scrollbar-thumb:window-inactive {
  background: rgba(144, 144, 144, 0.4);
}
</style>
