<template>
  <div v-if="loaded" class="portfolio">
    <div>
      <Search @search="addSymbol($event)" v-bind:placeholder="'Add symbol'"></Search>
    </div>
    <div class="md-layout md-size-100">
      <h3 class="md-title md-layout-item">
        Portfolio: <strong>{{ portfolio.name }}</strong>
      </h3>
    </div>
    <TabBar :tabs="portfolioTabs" :modelValue="'tab-' + path" @change="onPortfolioTabChange" />

    <div v-if="path === 'summary'">
      <md-empty-state
        v-if="portfolio.stocks.length == 0"
        md-description="Your list is empty. Add symbols to get relevant info."
      >
      </md-empty-state>
      <Summary v-else :stocks="portfolio.stocks"></Summary>
    </div>

    <div v-if="path === 'holdings'">
      <md-empty-state
        v-if="portfolio.stocks.length === 0"
        md-description="Your list is empty. Add symbols to get relevant info."
      >
      </md-empty-state>
      <Holdings @deletedSymbol="onDelete" v-else :portfolio="portfolio"></Holdings>
    </div>

    <div v-if="path === 'news'">
      <md-empty-state
        v-if="portfolio.stocks.length === 0"
        md-description="Your list is empty. Add symbols to get relevant info."
      >
      </md-empty-state>
      <News v-else :tickers="tickers"></News>
    </div>

    <div v-if="path === 'performance'">
      <md-empty-state
        v-if="portfolio.stocks.length === 0"
        md-description="Your list is empty. Add symbols to get relevant info."
      >
      </md-empty-state>
      <Performance v-else :portfolio="portfolio"></Performance>
    </div>
  </div>
</template>

<script>
import Search from './Search.vue';
import Holdings from './portfolio/Holdings.vue';
import Summary from './portfolio/Summary.vue';
import News from './portfolio/News.vue';
import Performance from './portfolio/Performance.vue';
import TabBar from './TabBar.vue';

export default {
  name: 'Portfolio',
  components: {
    Holdings,
    Summary,
    Search,
    News,
    Performance,
    TabBar,
  },
  data() {
    return {
      open: false,
      valid: false,
      portfolio: {},
      newSymbol: null,
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
    if (this.tickers.length > 0) {
      await this.$store.dispatch('getLatestStockPrices', { symbols: this.tickers.join() });
    }
    this.$store.commit('setLoading', false);
    this.loaded = true;
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
    async createPortfolio() {
      this.open = false;
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('submitNewPortfolio', { name: this.portfolioName, info: this.info });
      this.portfolioName = '';
      this.info = '';
      this.$store.commit('setLoading', false);
    },
    submit() {
      if (this.valid) {
        this.createPortfolio();
      }
    },
    validName(value) {
      return value.length > 1;
    },
    async addSymbol(payload) {
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('addSymbol', {
        portfolio: this.portfolio.id,
        payload: {
          symbol: payload.symbol,
          short_name: payload.short_name,
        },
      });
      this.portfolio = await this.$store.dispatch('getPortfolio', this.portfolioId);
      this.$store.dispatch('successMessage');
      this.$store.commit('setLoading', false);
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
iframe {
  border: 0px none;
  height: 500px;
  width: 100%;
  overflow: hidden;
  margin-right: -40px;
  margin-top: -150px;
}
iframe html {
  overflow: hidden;
}

.md-content {
  width: 100%;
  display: flex;
  padding: 10px;
  justify-content: left;
  align-items: left;
}

.md-tab {
  padding: 0;
}
</style>
