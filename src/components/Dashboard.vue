<template>
  <div v-if="loaded" class="dashboard">
    <div class="dashboard-section">
      <Search @search="searchQuote($event)"></Search>
    </div>

    <div class="dashboard-section">
      <h2 v-if="marketOverviewLoaded" class="md-heading">Market overview</h2>
      <TrendChart @loaded="marketOverviewLoaded = $event" />
    </div>

    <div v-if="Object.keys(portfolio).length !== 0" class="dashboard-section summary-card">
      <div class="summary-card-header">
        <h2 class="md-heading">Portfolio summary</h2>
        <div class="portfolio-switcher">
          <span>Portfolio: <strong>{{ portfolio.name }}</strong></span>
          <md-menu :md-offset-x="150" :md-offset-y="-50">
            <md-button class="md-icon-button md-dense" md-menu-trigger>
              <md-icon>keyboard_arrow_down</md-icon>
            </md-button>
            <md-menu-content>
              <md-menu-item v-for="p in portfolios" :key="p.id" @click="switchPortfolio(p.id)">
                {{ p.name }}
              </md-menu-item>
            </md-menu-content>
          </md-menu>
        </div>
      </div>

      <TabBar :tabs="portfolioTabs" v-model="activeTab" @change="onPortfolioSummaryTabChange" />

      <div v-if="activeTab === 'tab-allocation'">
        <md-empty-state v-if="!this.hasHoldings" md-label="You don't have any holdings in your portfolio">
          <router-link :to="`/portfolios/${portfolio.id}/holdings`">
            <md-button class="md-primary md-raised"><md-icon>add</md-icon> Add holdings</md-button>
          </router-link>
        </md-empty-state>
        <Allocation v-else class="allocation" :portfolio="portfolio" />
      </div>

      <div v-if="activeTab === 'tab-performance'">
        <md-empty-state v-if="!this.hasHoldings" md-label="You don't have any holdings in your portfolio">
          <router-link :to="`/portfolios/${portfolio.id}/holdings`">
            <md-button class="md-primary md-raised"><md-icon>add</md-icon> Add holdings</md-button>
          </router-link>
        </md-empty-state>
        <Performance v-else class="performance" :portfolio="portfolio" />
      </div>
    </div>
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
import TabBar from './TabBar.vue';

export default {
  name: 'Dashboard',
  components: {
    Allocation,
    Performance,
    TrendChart,
    Search,
    TabBar,
  },
  data() {
    return {
      loaded: false,
      marketOverviewLoaded: false,
      hasHoldings: false,
      portfolios: [],
      portfolio: {},
      portfolioTabs: [
        { id: 'tab-allocation', label: 'Allocation' },
        { id: 'tab-performance', label: 'Performance' },
      ],
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
.dashboard {
  max-width: 1180px;
  margin: 0 auto;
  text-align: left;
}
.dashboard-section {
  margin-bottom: 48px;
}
.dashboard-section:last-child {
  margin-bottom: 0;
}
.summary-card {
  background: var(--surface-color);
  border: 1px solid var(--surface-border);
  border-radius: 16px;
  box-shadow: var(--surface-shadow);
  padding: 28px 28px 8px;
}
.summary-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}
.summary-card-header .md-heading {
  margin: 0;
}
.portfolio-switcher {
  display: flex;
  align-items: center;
  gap: 4px;
  color: rgba(0, 0, 0, 0.65);
  font-size: 14px;
}
.allocation {
  display: flex;
  justify-content: space-around;
}
</style>
