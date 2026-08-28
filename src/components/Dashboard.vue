<template>
  <div v-if="loaded" class="page-container">
    <div class="page-section">
      <Search @search="searchQuote($event)"></Search>
    </div>

    <div class="page-section">
      <h2 v-if="marketOverviewLoaded" class="md-heading">Market overview</h2>
      <TrendChart @loaded="marketOverviewLoaded = $event" />
    </div>

    <div v-if="Object.keys(portfolio).length !== 0" class="page-section card-surface summary-card">
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
      marketOverviewLoaded: false,
      hasHoldings: false,
      portfolios: [],
      portfolio: {},
      portfolioTabs: [
        { id: 'tab-allocation', label: 'Allocation' },
        { id: 'tab-performance', label: 'Performance' },
      ],
      activeTab: 'tab-allocation',
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
