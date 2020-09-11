<template>
  <div v-if="loaded">
    <md-table>
      <md-table-row>
        <md-table-head style="max-width:50px;padding:0;margin:0;">Add</md-table-head>
        <md-table-head>Symbol</md-table-head>
        <md-table-head>Shares</md-table-head>
        <md-table-head>Worth (USD)</md-table-head>
      </md-table-row>
      <md-table-row v-for="stock in currentPortfolio.stocks" :key="stock.id">
        <md-table-cell style="max-width:40px;padding:0;margin:0;"
          ><md-button class="md-icon md-primary md-raised" @click="add(stock.ticker)">add</md-button></md-table-cell
        >
        <md-table-cell>{{ stock.ticker }}</md-table-cell>
        <md-table-cell>{{ getNumberOfShares(stock.id) }}</md-table-cell>
        <md-table-cell>{{ calculatePortfolioValue(currentPortfolio.holdings, stock.id) }}</md-table-cell>
      </md-table-row>
    </md-table>
    <md-dialog :md-active.sync="open" :md-fullscreen="false">
      <md-dialog-title
        >Add holding
        <md-button class="md-icon close-icon" @click="open = false">close</md-button>
      </md-dialog-title>
      <md-dialog-content>
        <form @submit.prevent="submit">
          <md-field>
            <label for="shares">Number of shares</label>
            <md-input type="number" step="any" v-model="newShares" name="shares" id="shares" autofocus></md-input>
          </md-field>
          <p class="dp-error" v-if="!valid">Must be greater than zero</p>

          <md-field>
            <label for="average">Average price (USD)</label>
            <md-input type="number" step="any" v-model="average" name="average" id="average"></md-input>
          </md-field>
          <p class="dp-error" v-if="!valid">Must be greater than zero</p>

          <md-field>
            <label for="purchased">Purchased on</label>
            <md-datepicker name="purchased" v-model="purchasedOn" />
          </md-field>
          <md-dialog-actions>
            <md-button class="md-raised" @click="open = false">Cancel</md-button>
            <md-button class="md-raised md-primary" type="submit">Save</md-button>
          </md-dialog-actions>
        </form>
      </md-dialog-content>
    </md-dialog>
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
      valid: true,
      portfolios: [],
      loaded: false,
      newShares: 1,
      average: 1,
      purchasedOn: new Date(),
      currentPortfolio: this.portfolio,
      portfolioId: this.portfolio.id,
      symbol: '',
    };
  },
  async mounted() {
    this.currentPortfolio = this.portfolio;
    this.loaded = true;
  },
  methods: {
    add(ticker) {
      this.open = true;
      this.symbol = ticker;
    },
    async createHolding() {
      this.open = false;
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('createNewHolding', {
        portfolio: this.portfolioId,
        payload: {
          symbol: this.symbol,
          shares: parseFloat(this.newShares),
          price: parseFloat(this.average),
          purchased_at: this.purchasedOn,
        },
      });
      this.currentPortfolio = await this.$store.dispatch('getPortfolio', this.portfolioId);
      this.$store.commit('setLoading', false);
    },
    submit() {
      this.valid = this.validNumber(this.newShares) && this.validNumber(this.average);
      if (this.valid) {
        this.createHolding();
      }
    },
    validNumber(value) {
      return value > 0;
    },
    calculatePortfolioValue(holdings, stockId) {
      let price = 0;
      for (let i = 0; i < holdings.length; i += 1) {
        if (holdings[i].stock_id === stockId) {
          price += holdings[i].price * holdings[i].shares;
        }
      }
      return price;
    },
    getNumberOfShares(stockId) {
      const { holdings } = this.currentPortfolio;
      let shares = 0;
      for (let i = 0; i < holdings.length; i += 1) {
        if (holdings[i].stock_id === stockId) {
          shares += holdings[i].shares;
        }
      }
      return shares;
    },
  },
  watch: {
    portfolio(val) {
      this.currentPortfolio = val;
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
