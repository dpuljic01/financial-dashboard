<template>
  <div v-if="loaded" class="portfolio">
    <div>
      <router-link to="/portfolios">Portfolios</router-link><span> > {{ portfolio.name }}</span>
    </div>
    <md-tabs @md-changed="onTabChange" :md-active-tab="tabId">
      <md-tab id="tab-summary" md-label="Summary">
        <md-table v-model="stocks">
          <md-table-row slot="md-table-row" slot-scope="{ item }">
            <md-table-cell md-label="Symbol" md-sort-by="symbol">{{ item.ticker }}</md-table-cell>
            <md-table-cell md-label="Name" md-sort-by="name">{{ item.short_name }}</md-table-cell>
            <md-table-cell md-label="Price (USD)" md-sort-by="price">{{
              item.latest_market_data.price || 'NA'
            }}</md-table-cell>
            <md-table-cell md-label="Change (%)">{{
              +(
                item.latest_market_data.changepercent
              ).toFixed(2) || 'NA'
            }}</md-table-cell>
            <md-table-cell md-label="Volume">{{ item.latest_market_data.volume || 'NA' }}</md-table-cell>
          </md-table-row>
        </md-table>
        <!--<portfolio-summary :stocks="stocks"></portfolio-summary>-->
      </md-tab>

      <md-tab id="tab-holdings" md-label="Holdings">
        <!--<portfolio-holdings :holdings="holdings"></portfolio-holdings>-->
      </md-tab>

      <md-tab id="tab-news" md-label="News">
        <div v-if="!showIframe" class="wsj" style="overflow: hidden; margin: 15px auto; max-width: 736px;">
          <iframe
            class="wsj"
            :src="articleUrl"
          >
          </iframe>
        </div>
        <md-list>
          <md-list-item @click="loadArticle(url)">
            <span class="md-caption">08/31/20 Press Release</span><br />
            <p>
              Thinking about buying stock in Apple, Alexion Pharmaceuticals, Nio Inc, Advanced Micro Devices, or Whiting
              Petroleum Corp?
            </p>
          </md-list-item>
        </md-list>
        <!--<portfolio-news :portfolioId="portfolioId"></portfolio-news>-->
      </md-tab>
      <md-tab id="tab-add-symbol" md-label="Add symbol">
        <search @search="addSymbol($event)" v-bind:search-layout="'floating'"></search>
      </md-tab>
    </md-tabs>
    <md-card v-if="this.$route.name == 'Portfolios'">
      <md-table class="md-content table" v-model="stocks" md-sort="name" md-sort-order="asc">
        <md-empty-state
          v-if="portfolio.stocks.length == 0"
          md-description="Your list is empty. Add symbols to get relevant info."
        >
          <md-button class="md-primary md-raised" @click="open = true"><md-icon>add</md-icon> Add symbol</md-button>
        </md-empty-state>
        <md-table-toolbar>
          <div class="md-toolbar-section-start">
            <h3>Holdings</h3>
          </div>
        </md-table-toolbar>

        <md-table-row slot="md-table-row" slot-scope="{ item }">
          <md-table-cell md-label="Name" md-sort-by="name">{{ item.name }}</md-table-cell>
          <md-table-cell md-label="Holdings">{{ item.holdings.length }}</md-table-cell>
          <md-table-cell md-label="Worth (USD)">{{ calculatePortfolioValue(item.holdings) }}</md-table-cell>
        </md-table-row>
      </md-table>
    </md-card>
  </div>
</template>

<script>
import Search from './Search.vue';

export default {
  name: 'Portfolio',
  components: {
    Search,
  },
  created() {
    this.portfolioId = this.$route.params.portfolioId;
  },
  data() {
    return {
      tabId: 'tab-summary',
      stocks: [],
      open: false,
      valid: false,
      hasPortfolio: this.$store.getters.hasPortfolio,
      portfolio: [],
      newSymbol: null,
      loaded: false,
      articleUrl: '#',
      showIframe: true,
    };
  },
  async mounted() {
    this.$store.commit('setLoading', true);
    await this.$store.dispatch('getPortfolio', this.portfolioId);
    const tickers = this.$store.getters.currentPortfolio.stocks.map((stock) => stock.ticker);
    console.log(tickers.join());
    await this.$store.dispatch('getLatestStockPrices', { symbols: tickers.join() });
    await this.$store.dispatch('getPortfolio', this.portfolioId);
    this.portfolio = this.$store.getters.currentPortfolio;
    this.stocks = this.portfolio.stocks;
    this.$store.commit('setLoading', false);
    this.loaded = true;
  },
  methods: {
    async createPortfolio() {
      this.open = false;
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('submitNewPortfolio', { name: this.portfolioName, info: this.info });
      this.portfolioName = '';
      this.info = '';
      this.$store.commit('setLoading', false);
    },
    onTabChange(id) {
      this.tabId = id;
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
        portfolio: this.portfolio.name,
        payload: {
          symbol: payload.symbol,
          short_name: payload.short_name,
        },
      });
      this.$store.dispatch('successMessage');
      this.updateUserDetails();
      this.$store.commit('setLoading', false);
    },
    async updateUserDetails() {
      await this.$store.dispatch('getCurrentUser');
      await this.$store.dispatch('getPortfolio', this.portfolioId);
      this.portfolio = this.$store.getters.currentPortfolio;
      this.stocks = this.portfolio.stocks;
      this.tabId = 'tab-summary';
    },
    loadArticle(url) {
      this.articleUrl = url;
    },
  },
};
</script>
<style scoped>
iframe {
  border: 0px none; height: 500px; width: 100%; overflow: hidden ;margin-right: -40px; margin-top: -150px;
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

* {
  text-align: left;
}
</style>
