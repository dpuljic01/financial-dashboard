<template>
  <div v-if="loaded" class="table-scroll">
    <table class="fin-table">
      <thead>
        <tr>
          <th class="col-del"></th>
          <th>Symbol</th>
          <th>Name</th>
          <th class="num">Price (USD)</th>
          <th class="num">Change (%)</th>
          <th class="num">Volume</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in stonks" :key="item.id">
          <td class="col-del">
            <button type="button" class="row-action" title="Remove" @click="deleteSymbol(item.id)">
              <md-icon>close</md-icon>
            </button>
          </td>
          <td @click="goToQuote(item.ticker)"><strong>{{ item.ticker }}</strong></td>
          <td @click="goToQuote(item.ticker)">{{ item.short_name }}</td>
          <td @click="goToQuote(item.ticker)" class="num fin-figure">
            {{ roundFloat(item.latest_market_data.price) || roundFloat(item.latest_market_data.delayedprice) || 'NA' }}
          </td>
          <td
            @click="goToQuote(item.ticker)"
            class="num fin-figure"
            :class="changeClass(item.latest_market_data.changepercent)"
          >
            {{ roundFloat(item.latest_market_data.changepercent) || 'NA' }}
          </td>
          <td @click="goToQuote(item.ticker)" class="num fin-figure">
            {{ formatVolume(item.latest_market_data.volume) || 'NA' }}
          </td>
        </tr>
      </tbody>
    </table>
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
.table-scroll {
  overflow-x: auto;
}
.fin-table {
  width: 100%;
  min-width: 560px;
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
.fin-table td:not(.col-del) {
  cursor: pointer;
}
.fin-table td.num {
  text-align: right;
}
.fin-table tbody tr:hover td {
  background: rgba(17, 100, 104, 0.04);
}
.col-del {
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
.row-action:hover {
  background: var(--loss-tint);
  color: var(--loss-color);
}
.row-action .md-icon {
  margin: 0;
  font-size: 18px !important;
}
</style>
