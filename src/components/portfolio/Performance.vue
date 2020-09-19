<template>
  <div v-if="!loaded">
    <md-progress-spinner
      :md-diameter="50"
      :md-stroke="4"
      style="margin-top: 50px;"
      md-mode="indeterminate"
    ></md-progress-spinner>
  </div>
  <div v-else class="md-layout md-gutter">
    <div class="md-layout-item md-size-45 md-xsmall-size-90 md-medium-size-50 md-large-size-40 md-gutter" id="chart">
      {{ portfolioValue }}
    </div>
    <div class="md-layout-item md-size-45 md-xsmall-size-80 md-medium-size-50 md-large-size-40 md-gutter" id="chart">
      <!--<apexchart type="donut" :options="sectorChart" :series="sectorChart.series"></apexchart>-->
    </div>
  </div>
</template>

<script>
import { groupBy } from '../../utils';

export default {
  name: 'Performance',
  props: ['portfolio'],
  data() {
    return {
      allocationChart: {},
      sectorChart: {},
      loaded: false,
      portfolioValue: 0,
    };
  },
  mounted() {
    console.log(this.portfolio.holdings);
    this.portfolioValue = this.calcPortfolioValue(this.portfolio.holdings);
    this.loaded = true;
    // this.calcPortfolioReturns();
  },
  methods: {
    calcPortfolioValue(holdings) {
      let worth = 0;
      for (let i = 0; i < holdings.length; i += 1) {
        worth += holdings[i].shares * holdings[i].price;
      }
      return worth;
    },
    calcPortfolioReturns(stocks) {
      const holdingsPerStock = groupBy(this.portfolio.holdings, 'stock_id');
      console.log(JSON.stringify(holdingsPerStock));
      // The returns from the portfolio will simply be the weighted average of the returns from the two or more assets:
      // R = w1*R1 + w2*R2
      let r = 0;
      for (let i = 0; i < stocks.length; i += 1) {
        r += this.calcStockReturn(stocks[i]);
      }
      this.loaded = true;
      return r;
    },
    calcStockReturn() {
      return 30; // test
    },
  },
};
</script>
