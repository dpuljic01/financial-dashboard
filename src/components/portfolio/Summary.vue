<template>
  <div v-if="loaded">
    <table class="plain-table">
      <thead>
        <tr>
          <th class="col-del">Del</th>
          <th>Symbol</th>
          <th>Name</th>
          <th>Price (USD)</th>
          <th>Change (%)</th>
          <th>Volume</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in stonks" :key="item.id">
          <td class="col-del">
            <md-button
              class="md-icon md-primary md-raised"
              style="background-color: #d00000;"
              @click="deleteSymbol(item.id)"
              >remove</md-button
            >
          </td>
          <td @click="goToQuote(item.ticker)"><strong>{{ item.ticker }}</strong></td>
          <td @click="goToQuote(item.ticker)">{{ item.short_name }}</td>
          <td @click="goToQuote(item.ticker)">
            {{ roundFloat(item.latest_market_data.price) || roundFloat(item.latest_market_data.delayedprice) || 'NA' }}
          </td>
          <td @click="goToQuote(item.ticker)">
            {{ roundFloat(item.latest_market_data.changepercent) || 'NA' }}
          </td>
          <td @click="goToQuote(item.ticker)">{{ item.latest_market_data.volume || 'NA' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
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
      this.$router.push(`/quote/${ticker}`);
    },
    roundFloat(val) {
      if (val) return +val.toFixed(2);
      return val;
    },
    deleteSymbol(stockId) {
      this.$confirm('Delete?').then(async () => {
        this.$store.commit('setLoading', true);
        await this.$store.dispatch('deleteSymbol', { portfolioId: this.portfolioId, stockId });
        const resp = await this.$store.dispatch('getPortfolio', this.portfolioId);
        this.stonks = resp.stocks;
        this.$emit('deletedSymbol');
        this.$store.commit('setLoading', false);
      });
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
  text-align: center;
  padding: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
.plain-table td:not(.col-del) {
  cursor: pointer;
}
.col-del {
  max-width: 50px;
}
</style>
