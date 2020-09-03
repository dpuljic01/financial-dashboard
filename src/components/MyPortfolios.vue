<template>
  <div v-if="loaded">
    <div v-if="this.portfolios.length > 0" class="md-layout md-size-100 md-alignment-center-space-between">
      <div class="md-layout-item md-size-40">
        <h3>PORTFOLIOS</h3>
      </div>
      <div class="md-layout-item md-size-30">
        <md-button class="md-fab md-mini md-primary" @click="open = true">
          <md-icon>add</md-icon>
        </md-button>
      </div>
    </div>
    <md-table v-if="this.portfolios.length > 0" class="md-content tbl" md-sort="name" md-sort-order="asc">
      <md-table-row>
        <md-table-head>Name</md-table-head>
        <md-table-head>Holdings</md-table-head>
        <md-table-head>Shares</md-table-head>
        <md-table-head>Worth (USD)</md-table-head>
      </md-table-row>
      <router-link v-for="item in portfolios" :key="item.id" :to="`/portfolios/${item.id}`" tag="md-table-row">
        <md-table-cell>{{ item.name }}</md-table-cell>
        <md-table-cell>{{ item.stocks.length }}</md-table-cell>
        <md-table-cell>{{ item.holdings.length }}</md-table-cell>
        <md-table-cell>{{ calculatePortfolioValue(item.holdings) }}</md-table-cell>
      </router-link>
    </md-table>
    <md-empty-state
      v-if="this.portfolios.length === 0"
      md-icon="post_add"
      md-label="No portfolios found"
      md-description="By creating a portfolio, you'll be able to add your holdings and get valuable information."
    >
      <md-button class="md-primary md-raised" @click="open = true">Create portfolio</md-button>
    </md-empty-state>

    <md-dialog :md-active.sync="open" :md-fullscreen="false">
      <md-dialog-title
        >Create portfolio
        <md-button class="md-icon close-icon" @click="open = false">close</md-button>
      </md-dialog-title>
      <md-dialog-content>
        <form @submit.prevent="submit">
          <md-field>
            <label for="portfolioName">Portfolio name</label>
            <md-input v-model="portfolioName" name="portfolioName" id="portfolioName" autofocus></md-input>
          </md-field>
          <p class="dp-error" v-if="!valid">Must have at least two characters</p>

          <md-field>
            <label>Additional info (Optional)</label>
            <md-textarea v-model="info"></md-textarea>
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
  name: 'MyPortfolios',
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
    this.$store.commit('setLoading', true);
    await this.$store.dispatch('getPortfolios');
    this.portfolios = this.$store.getters.listPortfolios;
    this.$store.commit('setLoading', false);
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
    calculatePortfolioValue(holdings) {
      let price = 0;
      for (let i = 0; i < holdings.length; i += 1) {
        price += parseFloat(holdings[i].price);
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