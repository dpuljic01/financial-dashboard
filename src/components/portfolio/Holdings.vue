<template>
  <div v-if="loaded" class="table-scroll">
    <table class="fin-table">
      <thead>
        <tr>
          <th class="col-add"></th>
          <th>Symbol</th>
          <th class="num">Shares</th>
          <th class="num">Worth (USD)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stock in currentPortfolio.stocks" :key="stock.id">
          <td class="col-add">
            <button type="button" class="row-action row-action--add" title="Add holding" @click="add(stock.ticker)">
              <md-icon>add</md-icon>
            </button>
          </td>
          <td><strong>{{ stock.ticker }}</strong></td>
          <td class="num fin-figure">{{ roundFloat(getNumberOfShares(stock.id)) }}</td>
          <td class="num fin-figure">
            {{ formatCurrency(calculatePortfolioValue(currentPortfolio.holdings, stock.id)) }}
          </td>
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
          <md-button class="md-raised" :disabled="submitting" @click="open = false">Cancel</md-button>
          <md-button class="md-raised md-primary" type="submit" :disabled="submitting">
            {{ submitting ? 'Saving…' : 'Save' }}
          </md-button>
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
      submitting: false,
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
      this.submitting = true;
      this.$store.commit('setLoading', true);
      try {
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
        this.open = false;
      } finally {
        this.submitting = false;
        this.$store.commit('setLoading', false);
      }
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
    roundFloat(val) {
      return +val.toFixed(2);
    },
    formatCurrency(val) {
      return `$${val.toFixed(2)}`;
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
.table-scroll {
  overflow-x: auto;
}
.fin-table {
  width: 100%;
  min-width: 420px;
  border-collapse: collapse;
}
.fin-table th {
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: rgba(0, 0, 0, 0.5);
  padding: 0 12px 10px 0;
}
.fin-table th.num {
  text-align: right;
}
.fin-table td {
  padding: 12px 12px 12px 0;
  border-top: 1px solid var(--surface-border);
}
.fin-table td.num {
  text-align: right;
}
.fin-table tbody tr:hover td {
  background: rgba(17, 100, 104, 0.04);
}
.col-add {
  width: 32px;
  padding-right: 0;
}
.row-action {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: none;
  color: rgba(0, 0, 0, 0.35);
  cursor: pointer;
}
.row-action--add:hover {
  background: var(--gain-tint);
  color: var(--gain-color);
}
.row-action .md-icon {
  margin: 0;
  font-size: 18px !important;
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
