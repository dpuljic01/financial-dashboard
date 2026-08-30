<template>
  <div class="page-container">
    <div v-if="!loaded" class="portfolio-loading">
      <FinancialLoader label="Loading portfolio…" />
    </div>
    <template v-else>
      <div class="page-section card-surface portfolio-card">
        <div class="portfolio-card-header">
          <h3 class="md-title portfolio-heading">
            Portfolio: <strong>{{ portfolio.name }}</strong>
          </h3>
          <md-button class="md-raised md-primary" @click="addSymbolOpen = true">
            <md-icon>add</md-icon> Add symbol
          </md-button>
        </div>
        <TabBar :tabs="portfolioTabs" :modelValue="'tab-' + path" @change="onPortfolioTabChange" />

        <md-empty-state
          v-if="portfolio.stocks.length === 0"
          md-icon="playlist_add"
          md-label="No symbols yet"
          md-description="Add a symbol to start tracking it in this portfolio."
        >
          <md-button class="md-primary md-raised" @click="addSymbolOpen = true">
            <md-icon>add</md-icon> Add symbol
          </md-button>
        </md-empty-state>

        <template v-else>
          <div v-if="path === 'summary'">
            <Summary :stocks="portfolio.stocks"></Summary>
          </div>
          <div v-if="path === 'holdings'">
            <Holdings @deletedSymbol="onDelete" :portfolio="portfolio"></Holdings>
          </div>
          <div v-if="path === 'news'">
            <News :tickers="tickers"></News>
          </div>
          <div v-if="path === 'performance'">
            <Performance :portfolio="portfolio"></Performance>
          </div>
        </template>
      </div>

      <Modal v-model="addSymbolOpen">
        <h3 class="modal-title">Add a symbol</h3>
        <p class="modal-subtitle">Search for a ticker to add it to this portfolio.</p>
        <Search
          @search="onAddSymbol($event)"
          :disabled="addingSymbol"
          placeholder="e.g. AAPL, MSFT..."
        ></Search>
        <div v-if="addingSymbol" class="add-symbol-status">
          <FinancialLoader size="small" :label="`Adding ${pendingSymbol}…`" />
        </div>
      </Modal>
    </template>
  </div>
</template>

<script>
import Search from './Search.vue';
import Holdings from './portfolio/Holdings.vue';
import Summary from './portfolio/Summary.vue';
import News from './portfolio/News.vue';
import Performance from './portfolio/Performance.vue';
import TabBar from './TabBar.vue';
import Modal from './Modal.vue';
import FinancialLoader from './FinancialLoader.vue';

export default {
  name: 'Portfolio',
  components: {
    Holdings,
    Summary,
    Search,
    News,
    Performance,
    TabBar,
    Modal,
    FinancialLoader,
  },
  data() {
    return {
      addSymbolOpen: false,
      addingSymbol: false,
      pendingSymbol: '',
      portfolio: {},
      loaded: false,
      tickers: [],
      path: 'summary',
      portfolioTabs: [
        { id: 'tab-summary', label: 'Summary' },
        { id: 'tab-holdings', label: 'Holdings' },
        { id: 'tab-performance', label: 'Performance' },
        { id: 'tab-news', label: 'News' },
      ],
    };
  },
  created() {
    this.portfolioId = this.$route.params.portfolioId;
    this.path = this.$route.path.split('/').pop();
  },
  async mounted() {
    this.$store.commit('setLoading', true);
    this.portfolio = await this.$store.dispatch('getPortfolio', this.portfolioId);
    this.getTickers();
    this.$store.commit('setLoading', false);
    this.loaded = true;
    // Refreshes the DB's cached quotes for next time - this render already
    // has the prices getPortfolio returned, so there's nothing to wait on.
    if (this.tickers.length > 0) {
      this.$store.dispatch('getLatestStockPrices', { symbols: this.tickers.join() });
    }
  },
  methods: {
    onPortfolioTabChange(tabId) {
      this.path = tabId.replace('tab-', '');
      this.$router.push(`/portfolios/${this.portfolio.id}/${this.path}`);
    },
    getTickers() {
      const tickers = this.portfolio.stocks.map((stock) => stock.ticker);
      this.tickers = tickers;
    },
    async onAddSymbol(payload) {
      this.addingSymbol = true;
      this.pendingSymbol = payload.symbol;
      this.$store.commit('setLoading', true);
      try {
        await this.$store.dispatch('addSymbol', {
          portfolio: this.portfolio.id,
          payload: {
            symbol: payload.symbol,
            short_name: payload.short_name,
          },
        });
        this.portfolio = await this.$store.dispatch('getPortfolio', this.portfolioId);
        this.getTickers();
        this.addSymbolOpen = false;
        this.$store.dispatch('successMessage');
      } finally {
        this.addingSymbol = false;
        this.$store.commit('setLoading', false);
      }
    },
    onDelete() {
      this.getTickers();
    },
  },
  watch: {
    portfolio: function portfolio(val) {
      this.portfolio = val;
    },
    tickers: function tickers(val) {
      this.tickers = val;
    },
  },
};
</script>
<style scoped>
.portfolio-loading {
  display: flex;
  justify-content: center;
  margin-top: 80px;
}
.portfolio-card {
  padding: 28px;
}
.portfolio-heading {
  margin-top: 0;
}
.portfolio-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 8px;
}
.portfolio-card-header .portfolio-heading {
  margin-bottom: 0;
}
.modal-title {
  margin: 0 0 4px;
}
.modal-subtitle {
  margin: 0 0 16px;
  color: rgba(0, 0, 0, 0.6);
  font-size: 14px;
}
.add-symbol-status {
  margin-top: 16px;
}
</style>
