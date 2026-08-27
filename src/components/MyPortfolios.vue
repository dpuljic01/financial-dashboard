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
    <table v-if="portfolios.length > 0" class="md-content tbl plain-table">
      <thead>
        <tr>
          <th class="col-del">Del</th>
          <th>Name</th>
          <th>Symbols</th>
          <th>Shares</th>
          <th>Worth (USD)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in portfolios" :key="item.id">
          <td class="col-del">
            <md-button
              class="md-icon md-raised md-primary"
              style="background-color: #d00000;"
              @click="deletePortfolio(item.id)"
              >delete_outline</md-button
            >
          </td>
          <td @click="goToSummary(item.id)">{{ item.name }}</td>
          <td @click="goToSummary(item.id)">{{ item.stocks.length }}</td>
          <td @click="goToSummary(item.id)">{{ item.holdings.length }}</td>
          <td @click="goToSummary(item.id)">{{ calculatePortfolioValue(item.holdings) }}</td>
        </tr>
      </tbody>
    </table>
    <md-empty-state v-if="portfolios.length === 0" md-label="Create your first portfolio">
      <md-button class="md-primary md-raised" @click="open = true"><md-icon>add</md-icon> Create portfolio</md-button>
    </md-empty-state>

    <md-dialog v-model:md-active="open" :md-fullscreen="false">
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
    goToSummary(id) {
      this.$router.push(`/portfolios/${id}/summary`);
    },
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
  max-width: 40px;
  padding: 0;
  margin: 0;
}
</style>
