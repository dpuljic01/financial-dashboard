<template>
  <div class="allocation-grid">
    <div class="allocation-chart">
      <h3 class="allocation-title">Holdings</h3>
      <Doughnut :data="holdingsChartData" :options="chartOptions" />
    </div>
    <div class="allocation-chart">
      <h3 class="allocation-title">Sector</h3>
      <Doughnut :data="sectorChartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script>
import { Doughnut } from 'vue-chartjs';
import {
  Chart as ChartJS, ArcElement, Tooltip, Legend,
} from 'chart.js';
import { groupBy } from '../../utils';

ChartJS.register(ArcElement, Tooltip, Legend);

const PALETTE = ['#116468', '#0f9d70', '#00aaad', '#d1435c', '#8c6dfd', '#e8873a', '#3a86ff', '#c9a227'];

export default {
  name: 'Allocation',
  components: {
    Doughnut,
  },
  props: ['portfolio'],
  data() {
    return {
      holdingsChartData: { labels: [], datasets: [{ data: [], backgroundColor: [] }] },
      sectorChartData: { labels: [], datasets: [{ data: [], backgroundColor: [] }] },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 10,
              boxHeight: 10,
              padding: 16,
              font: { family: "'IBM Plex Sans', sans-serif", size: 12 },
            },
          },
        },
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
    calculatePortfolioAlloc() {
      const holdingsPerStock = Object.values(groupBy(this.portfolio.holdings, 'stock_id'));
      const labels = [];
      const values = [];
      holdingsPerStock.forEach((holdings) => {
        values.push(this.calcHoldingsWorth(holdings));
        labels.push(this.getCompanyTicker(holdings[0].stock_id));
      });
      this.holdingsChartData = {
        labels,
        datasets: [{ data: values, backgroundColor: labels.map((label, i) => PALETTE[i % PALETTE.length]) }],
      };
      this.mapIndustries();
    },
    mapIndustries() {
      // Was previously `break`-ing out of the whole loop on the first
      // sector-less stock, silently dropping every stock after it from the
      // sector chart entirely - now just buckets each one as "Other" and
      // keeps going.
      const labels = [];
      const counts = [];
      this.portfolio.stocks.forEach((stock) => {
        const sector = (stock.company_info && stock.company_info.sector) || 'Other';
        const index = labels.indexOf(sector);
        if (index === -1) {
          labels.push(sector);
          counts.push(1);
        } else {
          counts[index] += 1;
        }
      });
      this.sectorChartData = {
        labels,
        datasets: [{ data: counts, backgroundColor: labels.map((label, i) => PALETTE[i % PALETTE.length]) }],
      };
    },
  },
  watch: {
    portfolio() {
      this.calculatePortfolioAlloc();
    },
  },
};
</script>

<style scoped>
.allocation-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 32px;
  justify-content: center;
  max-width: 100%;
}
.allocation-chart {
  /* chart.js's responsive resizing needs a relatively-positioned parent
     with a resolvable size, or the canvas can render at its own default
     intrinsic size instead of shrinking to fit a narrow flex item. */
  position: relative;
  flex: 1 1 260px;
  min-width: 0;
  max-width: 380px;
}
.allocation-title {
  text-align: center;
  margin: 0 0 12px;
  font-size: 15px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.7);
}
</style>
