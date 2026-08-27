<template>
  <div>
    <h2 v-if="multiple" class="md-heading">Compare multiple tickers and analyze their movement.</h2>
    <div class="chart">
      <p v-if="multiple" class="md-body-2" style="text-align:left;">Enter exact ticker symbols:</p>
      <md-chips
        v-if="multiple"
        v-model="localSymbols"
        :md-auto-insert="true"
        :md-format="toUppercase"
        @md-insert="compare"
        @md-delete="delayedCompare"
      >
      </md-chips>

      <h3 v-if="multiple">COMPARISON CHART</h3>
      <TabBar
        class="tabs md-elevation-2"
        style="overflow-x: auto; margin-bottom: 15px;"
        :tabs="periodTabs"
        v-model="activeTab"
        @change="onTabChange"
      />
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
    TabBar,
  },
  data() {
    return {
      localSymbols: [...this.symbols],
      period: '1d',
      interval: '5m',
      options: QUOTE_OPTIONS,
      series: [],
      loaded: false,
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
