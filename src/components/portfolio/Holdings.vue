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
      <tbody v-for="stock in currentPortfolio.stocks" :key="stock.id">
        <tr
          class="stock-row"
          :class="{ 'stock-row--expanded': expandedStockId === stock.id }"
          @click="toggleExpand(stock.id)"
        >
          <td class="col-add">
            <button
              type="button"
              class="row-action row-action--add"
              title="Add holding"
              @click.stop="add(stock.ticker)"
            >
              <md-icon>add</md-icon>
            </button>
          </td>
          <td>
            <span class="stock-caret">{{ expandedStockId === stock.id ? '▾' : '▸' }}</span>
            <strong>{{ stock.ticker }}</strong>
          </td>
          <template v-if="getNumberOfShares(stock.id) > 0">
            <td class="num fin-figure">{{ roundFloat(getNumberOfShares(stock.id)) }}</td>
            <td class="num fin-figure">
              {{ formatCurrency(calculatePortfolioValue(currentPortfolio.holdings, stock.id)) }}
            </td>
          </template>
          <td v-else colspan="2" class="empty-holding-cell">
            <span class="empty-holding-msg">No shares logged yet</span>
            <button type="button" class="empty-holding-cta" @click.stop="add(stock.ticker)">
              Log first buy →
            </button>
          </td>
        </tr>
        <tr v-if="expandedStockId === stock.id" class="lots-row">
          <td></td>
          <td colspan="3" class="lots-cell">
            <div class="lots-list">
              <div v-for="lot in lotsFor(stock.id)" :key="lot.id" class="lot-row">
                <span class="lot-date">{{ formatDate(lot.purchased_at) }}</span>
                <span class="lot-detail fin-figure">
                  {{ roundFloat(lot.shares) }} sh @ ${{ roundFloat(lot.price) }}
                </span>
                <span class="lot-actions">
                  <button
                    type="button"
                    class="row-action"
                    title="Edit"
                    @click.stop="editLot(stock.ticker, lot)"
                  >
                    <md-icon>edit</md-icon>
                  </button>
                  <ConfirmPopover message="Delete this holding?" @confirm="deleteLot(lot.id)">
                    <button type="button" class="row-action row-action--delete" title="Delete" @click.stop>
                      <md-icon>close</md-icon>
                    </button>
                  </ConfirmPopover>
                </span>
              </div>
              <p v-if="lotsFor(stock.id).length === 0" class="lots-empty">No purchase lots.</p>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <Modal v-model="open">
      <h3 class="modal-title">{{ editingHoldingId ? 'Edit holding' : 'Add holding' }}</h3>
      <form @submit.prevent="submit">
        <md-field>
          <label for="shares">Number of shares</label>
          <md-input
            type="text"
            inputmode="decimal"
            v-model="newShares"
            name="shares"
            id="shares"
            autofocus
          ></md-input>
        </md-field>
        <p class="dp-error" v-if="!valid">Must be greater than zero</p>

        <md-field>
          <label for="average">Average price (USD)</label>
          <md-input
            type="text"
            inputmode="decimal"
            v-model="average"
            name="average"
            id="average"
          ></md-input>
        </md-field>
        <p class="dp-error" v-if="!valid">Must be greater than zero</p>

        <md-field>
          <label for="purchased">Purchased on</label>
          <md-datepicker name="purchased" v-model="purchasedOn" />
        </md-field>
        <div class="modal-actions">
          <md-button class="md-raised" :disabled="submitting" @click="cancel">Cancel</md-button>
          <md-button class="md-raised md-primary" type="submit" :disabled="submitting">
            {{ submitting ? 'Saving…' : 'Save' }}
          </md-button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script>
import moment from 'moment';
import Modal from '../Modal.vue';
import ConfirmPopover from '../ConfirmPopover.vue';

export default {
  name: 'Holdings',
  components: {
    Modal,
    ConfirmPopover,
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
      expandedStockId: null,
      editingHoldingId: null,
    };
  },
  async mounted() {
    this.currentPortfolio = this.portfolio;
    this.loaded = true;
  },
  methods: {
    toggleExpand(stockId) {
      this.expandedStockId = this.expandedStockId === stockId ? null : stockId;
    },
    lotsFor(stockId) {
      return this.currentPortfolio.holdings.filter((holding) => holding.stock_id === stockId);
    },
    add(ticker) {
      this.editingHoldingId = null;
      this.newShares = 1;
      this.average = 1;
      this.purchasedOn = new Date();
      this.open = true;
      this.symbol = ticker;
    },
    editLot(ticker, lot) {
      this.editingHoldingId = lot.id;
      this.symbol = ticker;
      this.newShares = lot.shares;
      this.average = lot.price;
      this.purchasedOn = new Date(lot.purchased_at);
      this.open = true;
    },
    cancel() {
      this.open = false;
      this.editingHoldingId = null;
    },
    async deleteLot(holdingId) {
      this.$store.commit('setLoading', true);
      try {
        await this.$store.dispatch('deleteHolding', holdingId);
        this.currentPortfolio = await this.$store.dispatch('getPortfolio', this.portfolioId);
      } finally {
        this.$store.commit('setLoading', false);
      }
    },
    async createHolding() {
      this.submitting = true;
      this.$store.commit('setLoading', true);
      try {
        if (this.editingHoldingId) {
          await this.$store.dispatch('deleteHolding', this.editingHoldingId);
        }
        await this.$store.dispatch('createNewHolding', {
          portfolio: this.portfolioId,
          payload: {
            symbol: this.symbol,
            shares: this.toFloat(this.newShares),
            price: this.toFloat(this.average),
            purchased_at: this.purchasedOn,
          },
        });
        this.currentPortfolio = await this.$store.dispatch('getPortfolio', this.portfolioId);
        this.open = false;
        this.editingHoldingId = null;
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
      return this.toFloat(value) > 0;
    },
    // Accepts a comma as decimal separator too - a plain type="number" input
    // silently rejects "5.12" on a browser/OS set to a comma-decimal locale,
    // which is what made fractional entry look broken.
    toFloat(value) {
      return parseFloat(String(value).replace(',', '.'));
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
    formatDate(val) {
      return moment(val).format('MMM D, YYYY');
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
.fin-table tbody tr.stock-row:hover td {
  background: rgba(17, 100, 104, 0.04);
}
.stock-row {
  cursor: pointer;
}
.stock-caret {
  display: inline-block;
  width: 14px;
  color: rgba(0, 0, 0, 0.35);
  font-size: 10px;
}
.col-add {
  width: 32px;
  padding-right: 0;
}
.row-action {
  position: relative;
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
  flex-shrink: 0;
}
/* Styled label replacing the browser's native (slow, unstyled) title
   tooltip - reads the same title attribute via attr(), so no markup or
   script changes needed to keep it in sync with the button's purpose. */
.row-action::after {
  content: attr(title);
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  background: rgba(15, 34, 36, 0.92);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  line-height: 1;
  white-space: nowrap;
  padding: 5px 8px;
  border-radius: 4px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.12s ease;
  z-index: 5;
}
.row-action:hover::after,
.row-action:focus-visible::after {
  opacity: 1;
}
.row-action--add:hover {
  background: var(--gain-tint);
  color: var(--gain-color);
}
/* Unlike edit/add, delete reads as destructive at rest too, not just on
   hover - a neutral-gray icon that only turns red once you're already
   hovering it isn't a strong enough "this deletes something" signal. */
.row-action--delete {
  color: var(--loss-color);
  opacity: 0.75;
}
.row-action--delete:hover {
  background: var(--loss-tint);
  opacity: 1;
}
.row-action .md-icon {
  margin: 0;
  font-size: 18px !important;
}
.empty-holding-cell {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  flex-wrap: wrap;
}
.empty-holding-msg {
  font-size: 12px;
  font-style: italic;
  color: rgba(0, 0, 0, 0.45);
}
.empty-holding-cta {
  background: none;
  border: none;
  padding: 0;
  font-size: 12px;
  font-weight: 600;
  color: var(--gain-color, #116468);
  cursor: pointer;
  white-space: nowrap;
}
.empty-holding-cta:hover {
  text-decoration: underline;
}
.lots-row td {
  padding: 0 12px 10px 0;
  border-top: none;
}
.lots-cell {
  background: rgba(17, 100, 104, 0.03);
  border-radius: 8px;
}
.lots-list {
  padding: 4px 12px;
}
.lot-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 0;
}
.lot-row + .lot-row {
  border-top: 1px solid var(--surface-border);
}
.lot-date {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.55);
  flex-shrink: 0;
}
.lot-detail {
  flex: 1;
  text-align: right;
  font-size: 13px;
}
.lot-actions {
  display: flex;
  gap: 2px;
  flex-shrink: 0;
}
.lots-empty {
  margin: 0;
  padding: 8px 0;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.5);
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
