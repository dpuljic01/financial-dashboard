<template>
  <div v-if="loaded">
    <div v-if="portfolios.length > 0" class="md-layout md-subheader md-size-100 md-alignment-center-space-between">
      <div class="md-size-40">
        <h3>PORTFOLIOS</h3>
      </div>
      <md-button class="md-size-40 md-fab md-mini md-primary" @click="open = true">
        <md-icon>add</md-icon>
      </md-button>
    </div>
    <md-table v-if="portfolios.length > 0" class="md-content tbl" md-sort="name" md-sort-order="asc">
      <md-table-row style="max-width:40px;padding:0;margin:0;">
        <md-table-head style="max-width:40px;padding:0;margin:0;">Del</md-table-head>
        <md-table-head>Name</md-table-head>
        <md-table-head>Symbols</md-table-head>
        <md-table-head>Shares</md-table-head>
        <md-table-head>Worth (USD)</md-table-head>
      </md-table-row>
      <md-table-row v-for="item in portfolios" :key="item.id">
        <md-table-cell style="max-width:40px;padding:0;margin:0;"
          ><md-button
            class="md-icon md-raised md-primary"
            style="background-color: #d00000;"
            @click="deletePortfolio(item.id)"
            >delete_outline</md-button
          ></md-table-cell
        >
        <router-link tag="td" class="md-table-cell" :to="`/portfolios/${item.id}/summary`">{{ item.name }}</router-link>
        <router-link tag="td" class="md-table-cell" :to="`/portfolios/${item.id}/summary`">{{
          item.stocks.length
        }}</router-link>
        <router-link tag="td" class="md-table-cell" :to="`/portfolios/${item.id}/summary`">{{
          item.holdings.length
        }}</router-link>
        <router-link tag="td" class="md-table-cell" :to="`/portfolios/${item.id}/summary`">{{
          calculatePortfolioValue(item.holdings)
        }}</router-link>
      </md-table-row>
    </md-table>
    <md-empty-state v-if="portfolios.length === 0" md-label="Create your first portfolio">
      <md-button class="md-primary md-raised" @click="open = true"><md-icon>add</md-icon> Create portfolio</md-button>
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
    this.portfolios = this.$store.getters.listPortfolios;
    if (this.portfolios.length === 0) {
      this.portfolios = await this.$store.dispatch('getPortfolios');
    }
    this.$store.commit('setLoading', false);
    this.loaded = true;
  },
  methods: {
    async createPortfolio() {
      this.open = false;
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('submitNewPortfolio', { name: this.portfolioName, info: this.info });
      this.portfolios = await this.$store.dispatch('getPortfolios');
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
        price += holdings[i].price;
      }
      return price;
    },
    deletePortfolio(pId) {
      this.$confirm('Are you sure about that?').then(async () => {
        this.$store.commit('setLoading', true);
        await this.$store.dispatch('deletePortfolio', { portfolioId: pId });
        this.portfolios = await this.$store.dispatch('getPortfolios');
        this.$store.commit('setLoading', false);
      });
    },
  },
  watch: {
    portfolioName(value) {
      this.portfolioName = value;
      this.valid = this.validName(value);
    },
    portfolios(val) {
      this.portfolios = val;
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
.md-table-head {
  text-align: center;
}
.md-table-cell {
  text-align: center;
}
</style>
