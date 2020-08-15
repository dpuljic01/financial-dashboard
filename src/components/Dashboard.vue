<template>
  <div>
    <search />
    <trend-chart></trend-chart>
    <portfolio v-if="hasPortfolio" :portfolioId="0" :portfolio="portfolio"></portfolio>
    <md-empty-state
      v-else
      md-label="Create your first portfolio"
    >
      <router-link to="portfolios">
        <md-button class="md-primary md-raised">Go to portfolios</md-button>
      </router-link>
    </md-empty-state>
  </div>
</template>

<script>
// import Vue from 'vue';
import TrendChart from './charts/TrendChart.vue';
import Portfolio from './Portfolio.vue';
import Search from './Search.vue';

export default {
  name: 'Dashboard',
  components: {
    TrendChart,
    Portfolio,
    Search,
  },
  data() {
    return {
      showEmpty: false,
      hasPortfolio: false,
      portfolio: [],
    };
  },
  async mounted() {
    this.$store.commit('setLoading', true);
    await this.$store.dispatch('getCurrentUser');
    this.hasPortfolio = this.$store.getters.hasPortfolio;
    if (this.hasPortfolio) {
      const [firstPortfolio] = this.$store.getters.getPortfolios;
      this.portfolio = firstPortfolio;
    }
    this.showEmpty = this.hasPortfolio || true;
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
</style>
