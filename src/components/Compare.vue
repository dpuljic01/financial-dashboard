<template>
  <div>
    <h3 class="md-title">Compare multiple tickers and analyze their movement.</h3>
    <div class="chart">
      <md-chips
        class="md-accent"
        v-model="symbols"
        :md-auto-insert="true"
        :md-format="toUppercase"
        @md-insert="compare"
        @md-delete="delayedCompare"
      >
        <label>Enter ticker symbols</label>
      </md-chips>

      <h3>COMPARISON CHART</h3>
      <md-tabs
        class="tabs md-elevation-1"
        style="overflow-x: auto; margin-bottom: 10px;"
        :md-active-tab="activeTab"
        @md-changed="onTabChange"
      >
        <md-tab id="tab-1d" md-label="1D"></md-tab>
        <md-tab id="tab-5d" md-label="5D"> </md-tab>
        <md-tab id="tab-1mo" md-label="1M"> </md-tab>
        <md-tab id="tab-6mo" md-label="6M"> </md-tab>
        <md-tab id="tab-1y" md-label="1Y"> </md-tab>
        <md-tab id="tab-5y" md-label="5Y"> </md-tab>
        <md-tab id="tab-max" md-label="MAX"> </md-tab>
      </md-tabs>
      <Area v-if="loaded" :options="options" :series="series" />
    </div>
  </div>
</template>

<script>
import moment from 'moment';
import Area from './charts/Area.vue';
import { QUOTE_OPTIONS } from '../consts';
import { setQuoteSeries, setYAxis } from '../utils';

export default {
  name: 'Compare',
  components: {
    Area,
  },
  data() {
    return {
      symbols: ['GOOG', 'TSLA'],
      period: '1d',
      interval: '5m',
      options: QUOTE_OPTIONS,
      series: [],
      loaded: false,
      activeTab: 'tab-1d',
    };
  },
  async mounted() {
    await this.compare();
    this.$store.commit('setLoading', false);
    this.loaded = true;
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
          this.interval = '1d';
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
      if (this.symbols.length > 0) {
        this.$store.commit('setLoading', true);
        await this.getQuoteHistory();
        this.options = {
          ...this.options,
          ...{
            xaxis: {
              type: 'datetime',
            },
            yaxis: setYAxis(this.series),
            legend: {
              position: 'top',
              horizontalAlign: 'left',
            },
            tooltip: {
              x: {
                formatter: function f(val) {
                  return moment(val).format('LLL');
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
              height: 'auto',
            },
          },
        };
        this.$store.commit('setLoading', false);
      }
    },
    async getQuoteHistory() {
      const resp = await this.$store.dispatch('getStockHistoryData', {
        symbols: this.symbols.join(),
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
};
</script>

<style scoped>
.chart {
  margin: 0 auto;
  width: 100%;
  height: 100%;
  max-width: 800px;
}
</style>
