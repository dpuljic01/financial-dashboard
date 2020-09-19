<template>
  <div v-if="loaded">
    <md-table>
      <md-table-row>
        <md-table-head style="max-width:40px;padding:0;margin:0;">Del</md-table-head>
        <md-table-head>Symbol</md-table-head>
        <md-table-head>Name</md-table-head>
        <md-table-head>Price (USD)</md-table-head>
        <md-table-head>Change (%)</md-table-head>
        <md-table-head>Volume</md-table-head>
      </md-table-row>
      <md-table-row v-for="item in stonks" :key="item.id">
        <md-table-cell style="max-width:50px;"
          ><md-button
            class="md-icon md-primary md-raised"
            style="background-color: #d00000;"
            @click="deleteSymbol(item.id)"
            >remove</md-button
          ></md-table-cell
        >
        <router-link tag="td" class="md-table-cell" :to="`/quote/${item.ticker}`"
          ><strong>{{ item.ticker }}</strong></router-link
        >
        <router-link tag="td" class="md-table-cell" :to="`/quote/${item.ticker}`">{{ item.short_name }}</router-link>
        <router-link tag="td" class="md-table-cell" :to="`/quote/${item.ticker}`">{{
          roundFloat(item.latest_market_data.price) || roundFloat(item.latest_market_data.delayedprice) || 'NA'
        }}</router-link>
        <router-link tag="td" class="md-table-cell" :to="`/quote/${item.ticker}`">{{
          roundFloat(item.latest_market_data.changepercent) || 'NA'
        }}</router-link>
        <router-link tag="td" class="md-table-cell" :to="`/quote/${item.ticker}`">{{
          item.latest_market_data.volume || 'NA'
        }}</router-link>
      </md-table-row>
    </md-table>
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
.md-table-head {
  text-align: center;
}
.md-table-cell {
  text-align: center;
}
</style>
