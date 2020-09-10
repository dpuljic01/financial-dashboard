<template>
  <div class="md-layout md-gutter">
    <div class="md-layout-item md-size-45 md-xsmall-size-100 md-gutter" id="chart">
      <apexchart type="donut" :options="allocationChart" :series="allocationChart.series"></apexchart>
    </div>
    <div class="md-layout-item md-size-45 md-xsmall-size-100 md-gutter" id="chart">
      <apexchart type="donut" :options="industryChart" :series="industryChart.series"></apexchart>
    </div>
  </div>
</template>

<script>
import { groupBy } from '../../utils';

export default {
  name: 'Allocation',
  props: ['portfolio'],
  data() {
    return {
      allocationChart: {
        series: [],
        labels: [],
      },
      industryChart: {
        series: [],
        labels: [],
      },
    };
  },
  mounted() {
    this.calculatePortfolioAlloc();
  },
  methods: {
    calcHoldingsWorth(holdings) {
      let holdingPrice = 0;
      for (let i = 0; i < Object.values(holdings).length; i += 1) {
        holdingPrice += holdings[i].price * holdings[i].shares;
      }
      return holdingPrice;
    },
    getCompanyTicker(stockId) {
      let name = '';
      for (let i = 0; i < this.portfolio.stocks.length; i += 1) {
        if (this.portfolio.stocks[i].id === stockId) {
          name = this.portfolio.stocks[i].ticker;
          break;
        }
      }
      return name;
    },
    calculateTotalPrice(holdings) {
      let price = 0;
      for (let i = 0; i < holdings.length; i += 1) {
        for (let j = 0; j < holdings[i].length; j += 1) {
          price += this.calcHoldingWorth(holdings[i][j]);
        }
      }
      return price;
    },
    calculatePortfolioAlloc() {
      const holdingsPerStock = Object.values(groupBy(this.portfolio.holdings, 'stock_id'));
      this.mapIndustries();
      for (let i = 0; i < holdingsPerStock.length; i += 1) {
        const holdingPrice = this.calcHoldingsWorth(holdingsPerStock[i]);
        this.allocationChart.series.push(holdingPrice);
        this.allocationChart.labels.push(this.getCompanyTicker(holdingsPerStock[i][0].stock_id));
      }
    },
    mapIndustries() {
      for (let i = 0; i < this.portfolio.stocks.length; i += 1) {
        this.industryChart.series.push(1);
        this.industryChart.labels.push(this.portfolio.stocks[i].company_info.sector);
      }
    },
  },
  watch: {
    allocationChart(val) {
      this.allocationChart = val;
    },
    industryChart(val) {
      this.industryChart = val;
    },
  },
};
</script>
