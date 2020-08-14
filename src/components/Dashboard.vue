<template>
  <div>
    <search />
    <trend-chart></trend-chart>
    <portfolio v-if="hasPortfolio" :portfolioId="0" :portfolio="portfolio"></portfolio>
    <md-empty-state
      v-else
      md-icon="post_add"
      md-label="Create your first portfolio"
      md-description="By creating a portfolio, you'll be able to add your holdings and get valuable information."
    >
      <!--<md-button class="md-primary md-raised" @click="open = true">Create portfolio</md-button>-->
      <md-button class="md-primary md-raised" @click="open = true">Create portfolio</md-button>
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
      hasPortfolio: true,
      portfolio: [],
    };
  },
  async mounted() {
    this.$store.commit('setLoading', true);
    await this.$store.dispatch('getCurrentUser');
    this.hasPortfolio = this.$store.getters.hasPortfolio;
    this.portfolio = this.$store.getters.getPortfolios;
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
