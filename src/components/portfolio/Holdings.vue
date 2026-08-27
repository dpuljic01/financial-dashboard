<template>
  <div v-if="loaded">
    <table class="plain-table">
      <thead>
        <tr>
          <th class="col-add">Add</th>
          <th>Symbol</th>
          <th>Shares</th>
          <th>Worth (USD)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stock in currentPortfolio.stocks" :key="stock.id">
          <td class="col-add">
            <md-button class="md-icon md-primary md-raised" @click="add(stock.ticker)"
              ><md-icon>add</md-icon></md-button
            >
          </td>
          <td>{{ stock.ticker }}</td>
          <td>{{ getNumberOfShares(stock.id) }}</td>
          <td>{{ calculatePortfolioValue(currentPortfolio.holdings, stock.id) }}</td>
        </tr>
      </tbody>
    </table>
    <Modal v-model="open">
      <h3 class="modal-title">Add holding</h3>
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
        <div class="modal-actions">
          <md-button class="md-raised" @click="open = false">Cancel</md-button>
          <md-button class="md-raised md-primary" type="submit">Save</md-button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script>
import Modal from '../Modal.vue';

export default {
  name: 'Holdings',
  components: {
    Modal,
  },
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
.plain-table {
  width: 100%;
  border-collapse: collapse;
}
.plain-table th,
.plain-table td {
  text-align: left;
  padding: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
.col-add {
  max-width: 50px;
}
.modal-title {
  margin: 0 0 16px;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 16px;
}
</style>
