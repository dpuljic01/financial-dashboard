<template>
  <div v-if="loaded">
    <search />
    <trend-chart></trend-chart>
    <h3>PORTFOLIO SUMMARY</h3>
    <md-tabs @md-changed="onPortfolioSummaryTabChange" :md-active-tab="activeTab">
      <md-tab id="tab-allocation" md-label="Allocation">
        <div class="md-layout allocation">
          <div class="md-layout-item md-size-30">
            <doughnut class="md-layout-item" :chart-data="chartData" :options="options"></doughnut>
          </div>
          <div class="md-layout-item md-size-30">
            <doughnut class="md-layout-item" :chart-data="chartData" :options="options"></doughnut>
          </div>
        </div>
        <md-empty-state v-if="!this.hasHoldings" md-label="You don't have any holdings in your portfolio">
          <router-link :to="`/portfolios/${portfolio.id}/holdings`">
            <md-button class="md-primary md-raised"><md-icon>add</md-icon> Add holdings</md-button>
          </router-link>
        </md-empty-state>
      </md-tab>

      <md-tab id="tab-performance" md-label="Performance">
        <!--<portfolio-news :portfolioId="portfolioId"></portfolio-news>-->
        <md-empty-state v-if="!this.hasHoldings" md-label="You don't have any holdings in your portfolio">
          <router-link :to="`/portfolios/${portfolio.id}/holdings`">
            <md-button class="md-primary md-raised"><md-icon>add</md-icon> Add holdings</md-button>
          </router-link>
        </md-empty-state>
      </md-tab>
    </md-tabs>
    <!--<portfolio v-if="hasPortfolio" :portfolioId="0" :portfolio="portfolio"></portfolio>-->
  </div>
</template>

<script>
import TrendChart from './charts/TrendChart.vue';
import Search from './Search.vue';
import Doughnut from './charts/Doughnut';

export default {
  name: 'Dashboard',
  components: {
    Doughnut,
    TrendChart,
    Search,
  },
  data() {
    return {
      loaded: false,
      hasHoldings: false,
      portfolio: [],
      chartData: {
        labels: ['MSFT', 'AAPL', 'TSLA', 'NIO'],
        datasets: [
          {
            borderWidth: 1,
            borderColor: [
              'rgba(255,99,132,1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
            ],
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
            ],
            data: [2000, 500, 1500, 1000],
          },
        ],
      },
      activeTab: 'tab-allocation',
      options: {
        legend: {
          display: true,
        },
        responsive: true,
        maintainAspectRatio: false,
      },
    };
  },
  async mounted() {
    this.$store.commit('setLoading', true);
    await this.$store.dispatch('getCurrentUser');
    await this.$store.dispatch('getPortfolios');
    if (this.$store.getters.listPortfolios.length > 0) {
      const primaryPortfolio = this.$store.getters.listPortfolios[0].name; // return name of "primary" portfolio here
      await this.$store.dispatch('getPortfolio', primaryPortfolio);
      this.hasHoldings = this.$store.getters.hasHoldings;
      this.portfolio = this.$store.getters.currentPortfolio;
    }
    this.$store.commit('setLoading', false);
    this.loaded = true;
  },
  methods: {
    onPortfolioSummaryTabChange(id) {
      this.activeTab = id;
    },
  },
};
</script>

<style scoped>
.md-drawer {
  max-width: 250px;
}
.md-menu.md-button {
  height: 100%;
}
h3 {
  text-align: left;
}
.allocation {
  display: flex;
  justify-content: space-around;
}
</style>
