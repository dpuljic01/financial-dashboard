<template>
  <div class="market-overview">
    <md-progress-spinner
      v-if="!loaded"
      :md-diameter="50"
      :md-stroke="4"
      style="margin-top: 50px;"
      md-mode="indeterminate"
    ></md-progress-spinner>
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
          <Area :series="[value.serie]" :options="value.options" />
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { setQuoteSeries, setYAxis, percentChange } from '../../utils';
import Area from './Area.vue';
import { QUOTE_OPTIONS } from '../../consts';

// Matches the backend's yfinance history cache timeout, so the localStorage
// cache never holds data staler than what a fresh request would return anyway.
const TREND_CACHE_TTL_MS = 5 * 60 * 1000;

export default {
  name: 'TrendChart',
  components: {
    Area,
  },
  emits: ['loaded'],
  data() {
    return {
      symbols: ['EURUSD=X', '^gspc', '^dji', '^ixic', '^rut', 'cl=f', 'gc=f', 'si=f', '^vix'], // most popular indexes
      trendData: [],
      interval: '1m',
      period: '1d',
      options: QUOTE_OPTIONS,
      loaded: false,
    };
  },
  mounted() {
    this.fetchStockHistory();
  },
  methods: {
    async fetchStockHistory(reload = false) {
      this.loaded = false;
      this.$emit('loaded', false);
      this.trendData = [];
      const data = await this.fetchTrendData(reload);
      const series = setQuoteSeries(data);
      this.setTrendData(series);
      this.loaded = true;
      this.$emit('loaded', true);
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
        const chartData = {
          name,
          label: symbol,
          price: `$${(+latestPrice).toFixed(2)}`, // last value is the newest
          trend,
          change: changePercent ? `${changePercent > 0 ? '+' : ''}${changePercent.toFixed(2)}%` : 'NA',
          serie: series[i],
          options: this.setOptions(series[i]),
        };
        this.trendData.push(chartData);
      }
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
    setOptions(serie) {
      const positiveTrend = serie.data[0][1] < serie.data[Object.keys(serie.data).length - 1][1];
      const yAxis = setYAxis(serie);
      return {
        ...this.options,
        ...{
          stroke: {
            curve: 'straight',
            width: 1,
          },
          xaxis: {
            type: 'datetime',
            floating: true,
            axisTicks: {
              show: false,
            },
            axisBorder: {
              show: false,
            },
            labels: {
              show: false,
              format: 'HH:MM',
            },
          },
          yaxis: yAxis,
          legend: {
            show: false,
          },
          tooltip: {
            x: {
              show: false,
              formatter: function f(val) {
                const formattedDate = new Date(val);
                return `${formattedDate.getHours()}:${formattedDate.getMinutes()}`;
              },
            },
            y: {
              show: false,
              formatter: function f(val) {
                return +val.toFixed(2);
              },
            },
          },
          grid: {
            show: false,
            padding: {
              left: 0,
              right: 0,
              top: 0,
              bottom: 0,
            },
          },
          colors: positiveTrend ? ['#0f9d70'] : ['#d1435c'],
          chart: {
            zoom: {
              enabled: false,
            },
            selection: {
              enabled: false,
            },
            width: '100%',
            height: 300,
            animations: {
              enabled: false,
            },
            toolbar: {
              maxHeight: 0,
              show: false,
            },
          },
        },
      };
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
