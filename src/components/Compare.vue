<template>
  <div>
    <h2 v-if="multiple" class="md-heading">Compare multiple tickers and analyze their movement.</h2>
    <div class="chart">
      <p v-if="multiple" class="md-body-2" style="text-align:left;">Enter exact ticker symbols:</p>
      <md-chips
        v-if="multiple"
        v-model="symbols"
        :md-auto-insert="true"
        :md-format="toUppercase"
        @md-insert="compare"
        @md-delete="delayedCompare"
      >
      </md-chips>

      <h3 v-if="multiple">COMPARISON CHART</h3>
      <md-tabs
        class="tabs md-elevation-2"
        style="overflow-x: auto; margin-bottom: 15px;"
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
import { QUOTE_OPTIONS } from '../consts';
import { setQuoteSeries, setYAxis } from '../utils';

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
  },
  data() {
    return {
      period: '1d',
      interval: '5m',
      options: QUOTE_OPTIONS,
      series: [],
      loaded: false,
      activeTab: 'tab-1d',
    };
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
      if (this.symbols.length > 0) {
        this.loaded = false;
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
              height: 'auto',
            },
          },
        };
        this.loaded = true;
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
  watch: {
    symbols(val) {
      this.symbols = val;
      this.onTabChange('1d');
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
