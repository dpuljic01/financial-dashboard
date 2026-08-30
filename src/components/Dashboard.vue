<template>
  <div v-if="loaded" class="page-container">
    <div class="page-section">
      <Search @search="searchQuote($event)"></Search>
    </div>

    <div class="page-section">
      <h2 class="md-heading">Market overview</h2>
      <TrendChart />
    </div>

    <div v-if="Object.keys(portfolio).length !== 0" class="page-section card-surface summary-card">
      <div class="summary-card-header">
        <h2 class="md-heading">Portfolio summary</h2>
        <md-menu v-if="portfolios.length > 1" :md-offset-x="0" :md-offset-y="4">
          <md-button class="portfolio-switcher" md-menu-trigger>
            <span class="portfolio-switcher-label">{{ portfolio.name }}</span>
            <md-icon>expand_more</md-icon>
          </md-button>
          <md-menu-content class="portfolio-switcher-menu">
            <md-menu-item
              v-for="p in portfolios"
              :key="p.id"
              class="portfolio-switcher-item"
              :class="{ 'portfolio-switcher-item--active': p.id === portfolio.id }"
              @click="switchPortfolio(p.id)"
            >
              {{ p.name }}
            </md-menu-item>
          </md-menu-content>
        </md-menu>
        <span v-else-if="portfolio.name" class="portfolio-switcher portfolio-switcher--static">
          {{ portfolio.name }}
        </span>
      </div>

      <TabBar :tabs="portfolioTabs" v-model="activeTab" @change="onPortfolioSummaryTabChange" />

      <div v-if="activeTab === 'tab-performance'">
        <md-empty-state v-if="!this.hasHoldings" md-label="You don't have any holdings in your portfolio">
          <router-link :to="`/portfolios/${portfolio.id}/holdings`">
            <md-button class="md-primary md-raised"><md-icon>add</md-icon> Add holdings</md-button>
          </router-link>
        </md-empty-state>
        <Performance v-else class="performance" :portfolio="portfolio" />
      </div>

      <div v-if="activeTab === 'tab-allocation'">
        <md-empty-state v-if="!this.hasHoldings" md-label="You don't have any holdings in your portfolio">
          <router-link :to="`/portfolios/${portfolio.id}/holdings`">
            <md-button class="md-primary md-raised"><md-icon>add</md-icon> Add holdings</md-button>
          </router-link>
        </md-empty-state>
        <Allocation v-else class="allocation" :portfolio="portfolio" />
      </div>
    </div>
    <div v-else-if="loaded" class="page-section card-surface welcome-card">
      <div class="welcome-icon" aria-hidden="true">&#128075;</div>
      <h2 class="welcome-title">Welcome{{ userFirstName ? `, ${userFirstName}` : '' }}!</h2>
      <p class="welcome-subtitle">Let's get your dashboard set up — it only takes a minute.</p>

      <ol class="welcome-steps">
        <li>
          <span class="step-index">1</span>
          <div>
            <strong>Create a portfolio</strong>
            <p>Give it a name — you can create as many as you like.</p>
          </div>
        </li>
        <li>
          <span class="step-index">2</span>
          <div>
            <strong>Add the symbols you hold</strong>
            <p>Search any ticker and add your shares to start tracking performance.</p>
          </div>
        </li>
      </ol>

      <router-link to="/portfolios">
        <md-button class="md-primary md-raised">
          <md-icon>add</md-icon> Create your first portfolio
        </md-button>
      </router-link>
    </div>
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
  computed: {
    userFirstName() {
      return this.$store.getters.getCurrentUser.first_name || '';
    },
  },
  data() {
    return {
      loaded: false,
      hasHoldings: false,
      portfolios: [],
      portfolio: {},
      portfolioTabs: [
        { id: 'tab-performance', label: 'Performance' },
        { id: 'tab-allocation', label: 'Allocation' },
      ],
      activeTab: 'tab-performance',
    };
  },
  async mounted() {
    this.$store.commit('setLoading', true);
    await this.$store.dispatch('getCurrentUser');
    // Always refetch rather than trusting the localStorage-cached list - it
    // goes stale the moment a portfolio is added/removed from another tab,
    // session, or device, and silently under-lists portfolios here.
    this.portfolios = await this.$store.dispatch('getPortfolios');
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
    searchQuote(event) {
      this.$router.push(`/quote/${event.symbol}/profile`);
    },
  },
};
</script>

<style scoped>
.summary-card {
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
  display: flex !important;
  align-items: center;
  gap: 6px;
  height: auto !important;
  min-width: 0 !important;
  margin: 0 !important;
  padding: 8px 14px !important;
  border-radius: 20px !important;
  background: rgba(17, 100, 104, 0.06) !important;
  box-shadow: none !important;
  color: #116468 !important;
  font-size: 13px;
  font-weight: 600;
  text-transform: none;
  cursor: pointer;
}
.portfolio-switcher:hover {
  background: rgba(17, 100, 104, 0.12) !important;
}
.portfolio-switcher .md-icon {
  margin: 0 !important;
  font-size: 18px !important;
  color: #116468 !important;
}
.portfolio-switcher-label {
  max-width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.portfolio-switcher--static {
  cursor: default;
}
@media (max-width: 480px) {
  .summary-card-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
.allocation {
  display: flex;
  justify-content: space-around;
}
.welcome-card {
  padding: 40px 36px;
  text-align: center;
  max-width: 640px;
  margin: 0 auto;
}
.welcome-icon {
  font-size: 40px;
  margin-bottom: 12px;
}
.welcome-title {
  margin: 0 0 8px;
  font-size: 24px;
}
.welcome-subtitle {
  margin: 0 0 28px;
  color: rgba(0, 0, 0, 0.6);
}
.welcome-steps {
  list-style: none;
  margin: 0 0 28px;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: left;
}
.welcome-steps li {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}
.step-index {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(17, 100, 104, 0.1);
  color: #116468;
  font-weight: 700;
  font-size: 14px;
}
.welcome-steps p {
  margin: 2px 0 0;
  color: rgba(0, 0, 0, 0.6);
  font-size: 14px;
}
</style>
