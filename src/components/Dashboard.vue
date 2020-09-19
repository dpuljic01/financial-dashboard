<template>
  <div v-if="loaded">
    <div>
      <Search @search="searchQuote($event)"></Search>
    </div>
    <h2 class="md-heading">Market overview</h2>
    <TrendChart />
    <div v-if="Object.keys(portfolio).length !== 0">
      <h2 class="md-heading">Portfolio summary</h2>
      <label style="text-align: left;"
        >Choose portfolio: <strong>{{ portfolio.name }}</strong></label
      >
      <md-menu style="text-align: left;" :md-offset-x="150" :md-offset-y="-50">
        <md-button class="md-icon md-accent" md-menu-trigger>
          keyboard_arrow_down
        </md-button>
        <md-menu-content>
          <md-menu-item v-for="p in portfolios" :key="p.id" @click="switchPortfolio(p.id)">
            {{ p.name }}
          </md-menu-item>
        </md-menu-content>
      </md-menu>
    </div>
    <md-tabs
      v-if="Object.keys(portfolio).length !== 0"
      @md-changed="onPortfolioSummaryTabChange"
      :md-active-tab="activeTab"
    >
      <md-tab id="tab-allocation" md-label="Allocation">
        <md-empty-state v-if="!this.hasHoldings" md-label="You don't have any holdings in your portfolio">
          <router-link :to="`/portfolios/${portfolio.id}/holdings`">
            <md-button class="md-primary md-raised"><md-icon>add</md-icon> Add holdings</md-button>
          </router-link>
        </md-empty-state>
        <Allocation v-else class="allocation" :portfolio="portfolio" />
      </md-tab>

      <md-tab id="tab-performance" md-label="Performance">
        <md-empty-state v-if="!this.hasHoldings" md-label="You don't have any holdings in your portfolio">
          <router-link :to="`/portfolios/${portfolio.id}/holdings`">
            <md-button class="md-primary md-raised"><md-icon>add</md-icon> Add holdings</md-button>
          </router-link>
        </md-empty-state>
        <Performance v-else class="performance" :portfolio="portfolio" />
      </md-tab>
    </md-tabs>
    <md-empty-state
      v-else-if="loaded"
      md-icon="post_add"
      md-label="No portfolios found"
      md-description="By creating a portfolio, you'll be able to add your holdings and get valuable information."
    >
      <router-link to="/portfolios">
        <md-button class="md-primary md-raised">Go to portfolios</md-button>
      </router-link>
    </md-empty-state>
  </div>
</template>

<script>
import Performance from './portfolio/Performance.vue';
import TrendChart from './charts/TrendChart.vue';
import Search from './Search.vue';
import Allocation from './portfolio/Allocation.vue';

export default {
  name: 'Dashboard',
  components: {
    Allocation,
    Performance,
    TrendChart,
    Search,
  },
  data() {
    return {
      loaded: false,
      hasHoldings: false,
      portfolios: [],
      portfolio: {},
      industrySeries: [30, 40, 30],
      series: [44, 55, 41, 17, 15],
      chartOptions: {
        chart: {
          type: 'donut',
        },
        responsive: [
          {
            breakpoint: 480,
            options: {
              chart: {
                width: '100%',
              },
              legend: {
                position: 'top',
              },
            },
          },
        ],
      },
      activeTab: 'tab-allocation',
      ploaded: false,
    };
  },
  async mounted() {
    this.$store.commit('setLoading', true);
    await this.$store.dispatch('getCurrentUser');
    this.portfolios = this.$store.getters.listPortfolios;
    if (this.portfolios.length === 0) {
      this.portfolios = await this.$store.dispatch('getPortfolios');
    }
    if (this.portfolios.length > 0) {
      this.portfolio = await this.getCurrentPortfolio();
      this.hasHoldings = this.$store.getters.hasHoldings;
    }
    this.$store.commit('setLoading', false);
    this.loaded = true;
  },
  methods: {
    async getCurrentPortfolio() {
      let { currentPortfolio } = this.$store.getters;
      if (Object.keys(currentPortfolio).length === 0) {
        currentPortfolio = await this.$store.dispatch('getPortfolio', this.portfolios[0].id);
      }
      return currentPortfolio;
    },
    onPortfolioSummaryTabChange(id) {
      this.activeTab = id;
    },
    async switchPortfolio(id) {
      if (this.portfolio.id !== id) {
        this.portfolio = await this.$store.dispatch('getPortfolio', id);
        this.hasHoldings = this.$store.getters.hasHoldings;
      }
    },
    toggleSubmenu() {
      this.submenuVisible = !this.submenuVisible;
    },
    searchQuote(event) {
      this.$router.push(`/quote/${event.symbol}/profile`);
    },
  },
};
</script>

<style scoped>
.allocation {
  display: flex;
  justify-content: space-around;
}
</style>
