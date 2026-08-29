<template>
  <div class="compare card-surface" :class="{ 'compare--single': !multiple }">
    <h2 v-if="multiple" class="md-heading compare-heading">Compare multiple tickers and analyze their movement.</h2>

    <div v-if="multiple" class="compare-input">
      <p class="compare-input-label">Enter exact ticker symbols</p>
      <md-chips
        v-model="localSymbols"
        :md-auto-insert="true"
        :md-format="toUppercase"
        @md-insert="compare"
        @md-delete="delayedCompare"
      >
      </md-chips>
    </div>

    <div v-else-if="loaded" class="compare-price-header">
      <span class="compare-price fin-figure">{{ formattedPrice }}</span>
      <span
        class="compare-change fin-figure"
        :class="trend === 'up' ? 'fin-gain' : 'fin-loss'"
      >{{ formattedChange }}</span>
    </div>

    <div class="compare-toolbar">
      <TabBar variant="pill" :tabs="periodTabs" v-model="activeTab" @change="onTabChange" />
    </div>

    <div class="chart">
      <Area v-if="loaded" :options="options" :series="series" />
      <md-progress-spinner
        v-else
        :md-diameter="50"
        :md-stroke="4"
        style="margin-top: 50px;"
        md-mode="indeterminate"
      ></md-progress-spinner>
    </div>
  </div>
</template>

<script>
import moment from 'moment';
import Area from './charts/Area.vue';
import TabBar from './TabBar.vue';
import { QUOTE_OPTIONS } from '../consts';
import { setQuoteSeries, setYAxis, percentChange } from '../utils';

export default {
  name: 'Compare',
  props: {
    multiple: {
      type: Boolean,
      default: true,
    },
    symbols: {
      type: Array,
      default: () => ['GOOG', 'TSLA'],
    },
  },
  components: {
    Area,
    TabBar,
  },
  computed: {
    formattedPrice() {
      return this.latestPrice != null ? `$${(+this.latestPrice).toFixed(2)}` : '';
    },
    formattedChange() {
      if (this.changePercent == null) return '';
      const sign = this.changePercent > 0 ? '+' : '';
      return `${sign}${this.changePercent.toFixed(2)}%`;
    },
  },
  data() {
    return {
      localSymbols: [...this.symbols],
      period: '1d',
      interval: '5m',
      options: QUOTE_OPTIONS,
      series: [],
      loaded: false,
      latestPrice: null,
      trend: 'flat',
      changePercent: null,
      activeTab: 'tab-1d',
      periodTabs: [
        { id: 'tab-1d', label: '1D' },
        { id: 'tab-5d', label: '5D' },
        { id: 'tab-1mo', label: '1M' },
        { id: 'tab-6mo', label: '6M' },
        { id: 'tab-1y', label: '1Y' },
        { id: 'tab-5y', label: '5Y' },
        { id: 'tab-max', label: 'MAX' },
      ],
    };
  },
  mounted() {
    this.compare();
  },
  methods: {
    onTabChange(tabId) {
      [, this.period] = tabId.split('-');
      switch (this.period) {
        case '1d':
          this.interval = '5m';
          break;
        case '5d':
          this.interval = '30m';
          break;
        case '1mo':
          this.interval = '1h';
          break;
        case '6mo':
          this.interval = '1d';
          break;
        case '1y':
          this.interval = '1d';
          break;
        case '5y':
          this.interval = '1wk';
          break;
        case 'max':
          this.interval = '1mo';
          break;
        default:
          this.period = '1d';
          this.interval = '5m';
      }
      this.compare();
    },
    toUppercase(str) {
      const newStr = str.toUpperCase();
      return newStr;
    },
    async compare() {
      if (this.localSymbols.length > 0) {
        this.loaded = false;
        await this.getQuoteHistory();
        if (!this.multiple) {
          this.updateSingleSymbolStats();
        }
        this.options = {
          ...this.options,
          ...{
            xaxis: {
              type: 'datetime',
            },
            yaxis: setYAxis(this.series),
            legend: {
              show: this.multiple,
              position: 'top',
              horizontalAlign: 'left',
            },
            colors: this.multiple ? undefined : [this.trend === 'down' ? '#d1435c' : '#0f9d70'],
            tooltip: {
              x: {
                formatter: function f(val) {
                  return moment(val).format('LLL');
                },
                tooltip: {
                  shared: true,
                },
              },
              y: {
                formatter: function f(val) {
                  return +val.toFixed(4);
                },
              },
            },
            chart: {
              animations: {
                enabled: false,
              },
              toolbar: { show: false },
              zoom: { enabled: false },
              height: 'auto',
            },
          },
        };
        this.loaded = true;
      }
    },
    updateSingleSymbolStats() {
      const [serie] = this.series;
      if (!serie || serie.data.length === 0) {
        this.latestPrice = null;
        this.changePercent = null;
        this.trend = 'flat';
        return;
      }
      const [, openPrice] = serie.data[0];
      const [, latestPrice] = serie.data[serie.data.length - 1];
      this.latestPrice = latestPrice;
      this.changePercent = percentChange(openPrice, latestPrice);
      if (this.changePercent > 0) {
        this.trend = 'up';
      } else if (this.changePercent < 0) {
        this.trend = 'down';
      } else {
        this.trend = 'flat';
      }
    },
    async getQuoteHistory() {
      const resp = await this.$store.dispatch('getStockHistoryData', {
        symbols: this.localSymbols.join(),
        interval: this.interval,
        period: this.period,
        include_info: false,
      });
      this.series = setQuoteSeries(resp.data);
      this.$store.commit('setLoading', false);
    },
    async delayedCompare() {
      await this.compare();
    },
  },
  watch: {
    localSymbols() {
      this.onTabChange('1d');
    },
    symbols(val) {
      const unchanged = val.length === this.localSymbols.length
        && val.every((symbol, i) => symbol === this.localSymbols[i]);
      if (!unchanged) {
        this.localSymbols = [...val];
      }
    },
  },
};
</script>

<style scoped>
.compare {
  padding: 24px 28px 12px;
}
.compare--single {
  max-width: 820px;
  margin: 0 auto;
}
.compare-heading {
  margin-top: 0;
}
.compare-input-label {
  margin: 0 0 8px;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.6);
}
.compare-input {
  margin-bottom: 8px;
}
.compare-price-header {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 16px;
}
.compare-price {
  font-size: 28px;
  font-weight: 700;
  color: #0a2f31;
}
.compare-change {
  font-size: 15px;
  font-weight: 600;
}
.compare-toolbar {
  margin-bottom: 16px;
}
.chart {
  margin: 0 auto;
  width: 100%;
  height: 100%;
  max-width: 800px;
}
</style>
