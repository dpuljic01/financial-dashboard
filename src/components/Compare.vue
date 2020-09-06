<template>
  <div>
    <h3 class="md-title">Compare multiple tickers and analyze their movement.</h3>
    <md-chips class="md-primary" v-model="symbols" :md-auto-insert="true" @md-insert="compare">
      <label>Enter ticker symbols</label>
    </md-chips>
    <div v-if="!this.$store.getters.isLoading" class="chart">
      <Area :options="options" :series="series" />
    </div>
  </div>
</template>

<script>
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
      symbols: ['GOOGL', 'TSLA'],
      period: '1mo',
      interval: '1d',
      options: QUOTE_OPTIONS,
      series: [],
      categories: [],
    };
  },
  mounted() {
    this.compare();
  },
  methods: {
    async compare() {
      this.$store.commit('setLoading', true);
      if (this.symbols.length > 1) {
        await this.getQuoteHistory();
        this.options = {
          ...this.options,
          ...{
            xaxis: {
              type: 'datetime',
            },
            yaxis: setYAxis(this.series),
            title: {
              text: 'COMPARISON CHART',
            },
            legend: {
              position: 'top',
            },
          },
        };
      }
      this.$store.commit('setLoading', false);
    },
    async getQuoteHistory() {
      this.$store.commit('setLoading', true);
      const resp = await this.$store.dispatch('getStockHistoryData', {
        symbols: this.symbols.join(),
        interval: this.interval,
        period: this.period,
        include_info: false,
      });
      this.series = setQuoteSeries(resp.data);
      this.$store.commit('setLoading', false);
    },
  },
};
</script>
