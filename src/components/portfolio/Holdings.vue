<template>
  <div v-if="loaded">
    <table>
      <thead>
        <td>Symbol</td>
        <td>Shares</td>
        <td>Worth (USD)</td>
      </thead>
      <tbody v-for="item in portfolio.stocks" :key="item.id">
        <tr>
          <td>{{ item.ticker }}</td>
          <td>{{ portfolio.holdings.length }}</td>
          <td>{{ calculatePortfolioValue(portfolio.holdings, item.id) }}</td>
        </tr>
      </tbody>
    </table>
    <!--<md-table v-if="this.portfolio.stocks.length > 0" class="md-content tbl" md-sort="name" md-sort-order="asc">
      <md-table-row>
        <md-table-head>Symbol</md-table-head>
        <md-table-head>Shares</md-table-head>
        <md-table-head>Worth (USD)</md-table-head>
      </md-table-row>
      <router-link v-for="item in portfolio.stocks" :key="item.id" tag="md-table-row">
        <md-table-cell>{{ item.ticker }}</md-table-cell>
        <md-table-cell>{{ portfolio.holdings.length }}</md-table-cell>
        <md-table-cell>{{ calculatePortfolioValue(portfolio.holdings, item.id) }}</md-table-cell>
      </router-link>
    </md-table>-->
  </div>
</template>

<script>
export default {
  name: 'Holdings',
  props: {
    portfolio: {
      type: Object,
    },
  },
  data() {
    return {
      open: false,
      portfolioName: '',
      info: '',
      valid: false,
      portfolios: [],
      loaded: false,
    };
  },
  async mounted() {
    this.loaded = true;
  },
  methods: {
    async createPortfolio() {
      this.open = false;
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('submitNewPortfolio', { name: this.portfolioName, info: this.info });
      await this.$store.dispatch('getPortfolios');
      this.portfolios = this.$store.getters.listPortfolios;
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
    calculatePortfolioValue(holdings, stockId) {
      let price = 0;
      for (let i = 0; i < holdings.length; i += 1) {
        if (holdings[i].stock_id === stockId) {
          price += parseFloat(holdings[i].price);
        }
      }
      return price;
    },
  },
  watch: {
    portfolioName: {
      handler: function portfolioName(value) {
        this.portfolioName = value;
        this.valid = this.validName(value);
      },
    },
  },
};
</script>

<style lang="scss" scoped>
.md-card {
  text-align: left;
}

.close-icon {
  position: absolute;
  right: 4%;
}
.md-table .md-table-head {
  text-align: left;
}
.md-table .md-table-cell {
  text-align: left;
}
</style>
