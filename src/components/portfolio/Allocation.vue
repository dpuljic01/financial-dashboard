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
      <apexchart type="donut" :options="allocationChart" :series="allocationChart.series"></apexchart>
    </div>
    <div class="md-layout-item md-size-45 md-xsmall-size-80 md-medium-size-50 md-large-size-40 md-gutter" id="chart">
      <apexchart type="donut" :options="sectorChart" :series="sectorChart.series"></apexchart>
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
      allocationChart: this.initialChartValue('Holdings'),
      sectorChart: this.initialChartValue('Sector'),
      loaded: false,
    };
  },
  mounted() {
    this.loaded = false;
    this.copyAlloc = this.allocationChart;
    this.copySector = this.sectorChart;
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
      this.loaded = false;
      const holdingsPerStock = Object.values(groupBy(this.portfolio.holdings, 'stock_id'));
      this.mapIndustries();
      for (let i = 0; i < holdingsPerStock.length; i += 1) {
        const holdingPrice = this.calcHoldingsWorth(holdingsPerStock[i]);
        this.allocationChart.series.push(holdingPrice);
        this.allocationChart.labels.push(this.getCompanyTicker(holdingsPerStock[i][0].stock_id));
      }
      this.loaded = true;
    },
    mapIndustries() {
      for (let i = 0; i < this.portfolio.stocks.length; i += 1) {
        const { sector } = this.portfolio.stocks[i].company_info;
        if (!sector) {
          this.sectorChart.series.push(1);
          this.sectorChart.labels.push('Other');
          break;
        }
        const sectorIndex = this.sectorChart.labels.indexOf(sector);
        if (sectorIndex === -1) {
          this.sectorChart.series.push(1);
          this.sectorChart.labels.push(sector);
        } else {
          this.sectorChart.series[sectorIndex] += 1;
        }
      }
    },
    initialChartValue(title) {
      return {
        series: [],
        labels: [],
        legend: {
          show: true,
          position: 'bottom',
          horizontalAlign: 'center',
          floating: false,
        },
        title: {
          text: title,
        },
      };
    },
  },
  watch: {
    allocationChart(val) {
      this.allocationChart = val;
    },
    sectorChart(val) {
      this.sectorChart = val;
    },
    portfolio() {
      this.allocationChart = this.initialChartValue('Holdings');
      this.sectorChart = this.initialChartValue('Sector');
      this.calculatePortfolioAlloc();
    },
  },
};
</script>
