<template>
  <div v-if="loaded" class="holdings-list">
    <div class="holdings-header">
      <span></span>
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
      <button type="button" class="row-action" title="Remove" @click.stop="deleteSymbol(item.id)">
        <md-icon>close</md-icon>
      </button>
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

export default {
  name: 'Summary',
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
      if (!window.confirm('Delete?')) return;
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
$grid-columns: 32px minmax(0, 1fr) 90px 80px 80px;

.holdings-header {
  display: grid;
  grid-template-columns: $grid-columns;
  gap: 8px;
  padding: 0 0 10px;
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
  display: grid;
  grid-template-columns: $grid-columns;
  align-items: center;
  gap: 8px;
  padding: 12px 0;
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
    position: relative;
    padding: 14px 32px 14px 0;
  }
  .holdings-row > .row-action {
    position: absolute;
    top: 8px;
    right: 0;
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
