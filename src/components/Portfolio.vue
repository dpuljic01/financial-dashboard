<template>
  <div>
    <div class="portfolio">
      <md-content><router-link to="portfolios">My Portfolios</router-link> / {{ portfolio.name }}</md-content>
      <md-tabs @md-changed="onTabChange" :md-active-tab="tabId">
        <md-tab id="tab-summary" md-label="Summary">
          <md-table v-model="stocks">
            <md-table-row slot="md-table-row" slot-scope="{ item }">
              <md-table-cell md-label="Symbol" md-sort-by="symbol">{{ item.ticker }}</md-table-cell>
              <md-table-cell md-label="Name" md-sort-by="name">{{ item.short_name }}</md-table-cell>
              <md-table-cell md-label="Price (USD)" md-sort-by="price">{{
                item.latest_market_data.Close || 'NA'
              }}</md-table-cell>
              <md-table-cell md-label="Change (%)" md-sort-by="change">{{
                +(
                  ((item.latest_market_data.Close - item.latest_market_data.Open) / item.latest_market_data.Open) *
                  100
                ).toFixed(2) || 'NA'
              }}</md-table-cell>
              <md-table-cell md-label="Volume" md-sort-by="change">{{
                item.latest_market_data.Volume || 'NA'
              }}</md-table-cell>
            </md-table-row>
          </md-table>
          <!--<portfolio-summary :stocks="stocks"></portfolio-summary>-->
        </md-tab>

        <md-tab id="tab-holdings" md-label="Holdings">
          <!--<portfolio-holdings :holdings="holdings"></portfolio-holdings>-->
        </md-tab>

        <md-tab id="tab-news" md-label="News">
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
  </div>
</template>

<script>
import Search from './Search.vue';

export default {
  name: 'Portfolio',
  props: ['portfolioId', 'portfolio'],
  components: {
    Search,
  },
  data() {
    return {
      tabId: 'tab-summary',
      stocks: this.portfolio.stocks,
      open: false,
      valid: false,
      hasPortfolio: this.$store.getters.hasPortfolio,
      newSymbol: null,
    };
  },
  mounted() {
    this.$store.dispatch('getCurrentUser');
  },
  methods: {
    async createPortfolio() {
      this.open = false;
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('submitNewPortfolio', { name: this.portfolioName, info: this.info });
      this.portfolioName = '';
      this.info = '';
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
    },
    async updateUserDetails() {
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('getCurrentUser');
      const [p] = this.$store.getters.getPortfolios;
      this.stocks = p.stocks;
      this.tabId = 'tab-summary';
    },
  },
};
</script>
<style scoped>
.md-content {
  width: 100%;
  display: flex;
  padding: 10px;
}
.md-tab {
  padding: 0;
}
* {
  text-align: left;
}
</style>
