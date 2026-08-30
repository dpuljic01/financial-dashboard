<template>
  <div v-if="loaded" class="holdings-list">
    <div class="holdings-header">
      <span>Symbol</span>
      <span>Price</span>
      <span>Change</span>
      <span>Volume</span>
    </div>
    <div
      v-for="item in stonks"
      :key="item.id"
      class="holdings-row"
      @click="goToQuote(item.ticker)"
    >
      <ConfirmPopover
        message="Remove this symbol from the portfolio?"
        @confirm="deleteSymbol(item.id)"
      >
        <button type="button" class="row-action" title="Remove" @click.stop>
          <md-icon>close</md-icon>
        </button>
      </ConfirmPopover>
      <div class="holdings-identity">
        <span class="holdings-symbol">{{ item.ticker }}</span>
        <span v-if="showName(item)" class="holdings-name">{{ item.short_name }}</span>
      </div>
      <span class="holdings-price fin-figure">
        {{ roundFloat(item.latest_market_data.price) || roundFloat(item.latest_market_data.delayedprice) || 'NA' }}
      </span>
      <span class="holdings-change fin-figure" :class="changeClass(item.latest_market_data.changepercent)">
        {{ roundFloat(item.latest_market_data.changepercent) || 'NA' }}%
      </span>
      <span class="holdings-volume fin-figure">
        {{ formatVolume(item.latest_market_data.volume) || 'NA' }}
      </span>
    </div>
  </div>
</template>

<script>
import { formatCompactNumber } from '../../utils';
import ConfirmPopover from '../ConfirmPopover.vue';

export default {
  name: 'Summary',
  components: {
    ConfirmPopover,
  },
  props: {
    stocks: {
      type: Array,
    },
  },
  data() {
    return {
      loaded: false,
      portfolioId: this.$route.params.portfolioId,
      stonks: this.stocks,
    };
  },
  async mounted() {
    this.stonks = this.stocks;
    this.portfolioId = this.$route.params.portfolioId;
    this.loaded = true;
  },
  methods: {
    goToQuote(ticker) {
      this.$router.push(`/quote/${ticker}/profile`);
    },
    // Placeholder/fallback company data (e.g. a stalled provider fetch that
    // defaulted short_name to the ticker itself) reads as a duplicate
    // column, not useful information - just hide it rather than show
    // "AAPL / AAPL" twice.
    showName(item) {
      return item.short_name && item.short_name.toUpperCase() !== item.ticker.toUpperCase();
    },
    roundFloat(val) {
      if (val) return +val.toFixed(2);
      return val;
    },
    formatVolume(val) {
      return formatCompactNumber(val);
    },
    changeClass(val) {
      if (val > 0) return 'fin-gain';
      if (val < 0) return 'fin-loss';
      return '';
    },
    async deleteSymbol(stockId) {
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('deleteSymbol', { portfolioId: this.portfolioId, stockId });
      const resp = await this.$store.dispatch('getPortfolio', this.portfolioId);
      this.stonks = resp.stocks;
      this.$emit('deletedSymbol');
      this.$store.commit('setLoading', false);
    },
  },
  watch: {
    stocks(val) {
      this.stonks = val;
    },
  },
};
</script>

<style lang="scss" scoped>
$grid-columns: minmax(0, 1fr) 90px 80px 80px;

// ConfirmPopover wraps the delete button in floating-vue's own trigger
// element (a plain, unstyled <div class="v-popper">). display: contents
// makes that wrapper transparent to the grid below, so it doesn't eat one
// of the 4 grid-template-columns tracks meant for the real row content.
.holdings-row :deep(.v-popper) {
  display: contents;
}

.holdings-header {
  display: grid;
  grid-template-columns: $grid-columns;
  gap: 8px;
  padding: 0 0 10px 32px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: rgba(0, 0, 0, 0.5);
}
.holdings-header span:not(:first-child) {
  text-align: right;
}

.holdings-row {
  position: relative;
  display: grid;
  grid-template-columns: $grid-columns;
  align-items: center;
  gap: 8px;
  padding: 12px 0 12px 32px;
  border-top: 1px solid var(--surface-border);
  cursor: pointer;
}
.holdings-row:hover {
  background: rgba(17, 100, 104, 0.04);
}
.holdings-row > * {
  text-align: right;
}
.holdings-identity {
  display: flex;
  flex-direction: column;
  min-width: 0;
  text-align: left;
}
.holdings-symbol {
  font-weight: 700;
}
.holdings-name {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.5);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.holdings-volume {
  color: rgba(0, 0, 0, 0.55);
}
.row-action {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
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
.row-action:hover {
  background: var(--loss-tint);
  color: var(--loss-color);
}
.row-action .md-icon {
  margin: 0;
  font-size: 18px !important;
}

@media (max-width: 600px) {
  .holdings-header {
    display: none;
  }
  .holdings-row {
    grid-template-columns: 1fr auto;
    grid-template-areas:
      "identity price"
      "change volume";
    row-gap: 4px;
    padding: 14px 32px 14px 0;
  }
  .row-action {
    left: auto;
    right: 0;
    top: 8px;
    transform: none;
  }
  .holdings-identity {
    grid-area: identity;
  }
  .holdings-price {
    grid-area: price;
    font-size: 15px;
    font-weight: 700;
  }
  .holdings-change {
    grid-area: change;
    text-align: left;
    font-size: 12px;
  }
  .holdings-volume {
    grid-area: volume;
    font-size: 12px;
  }
}
</style>
