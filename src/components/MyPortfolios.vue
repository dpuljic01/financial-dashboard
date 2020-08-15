<template>
  <div>
    <md-table class="md-content" v-model="searched" md-sort="name" md-sort-order="asc">
      <md-table-toolbar>
        <md-field md-clearable class="md-toolbar-section-end">
          <md-input placeholder="Search by name..." v-model="search" @input="searchOnTable" />
        </md-field>
      </md-table-toolbar>

      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="Name" md-sort-by="name">{{ item.name }}</md-table-cell>
        <md-table-cell md-label="Holdings">{{ item.stocks.length }}</md-table-cell>
        <md-table-cell md-label="Shares">{{ item.holdings.length }}</md-table-cell>
        <md-table-cell md-label="Worth (USD)">{{ calculatePortfolioValue(item.holdings) }}</md-table-cell>
      </md-table-row>
    </md-table>
    <md-empty-state
      v-if="searched.length == 0"
      md-icon="post_add"
      md-label="No portfolios found"
      md-description="By creating a portfolio, you'll be able to add your holdings and get valuable information."
    >
      <md-button class="md-primary md-raised" @click="open = true">Create portfolio</md-button>
    </md-empty-state>

    <md-dialog :md-active.sync="open" :md-fullscreen="false">
      <md-dialog-title
        >Create portfolio
        <md-button class="md-icon" @click="open = false">close</md-button>
      </md-dialog-title>
      <md-dialog-content>
        <form novalidate @submit.prevent="submit">
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
const toLower = (text) => text.toString().toLowerCase();

const searchByName = (items, term) => {
  if (term) {
    return items.filter((item) => toLower(item.name).includes(toLower(term)));
  }
  return items;
};

export default {
  name: 'MyPortfolios',
  data() {
    return {
      search: null,
      searched: [],
      open: false,
      portfolioName: '',
      info: '',
      valid: false,
      icon: this.$route.name === 'MyPortfolios' ? 'post_add' : '',
      hasPortfolio: this.$store.getters.hasPortfolio,
      portfolios: this.$store.getters.getPortfolios,
    };
  },
  methods: {
    async createPortfolio() {
      this.open = false;
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('submitNewPortfolio', { name: this.portfolioName, info: this.info });
      await this.$store.dispatch('getCurrentUser');
      this.portfolios = this.$store.getters.getPortfolios;
      this.searched = this.portfolios;
      this.portfolioName = '';
      this.info = '';
    },
    submit() {
      if (this.valid) {
        this.createPortfolio();
      }
    },
    validName(value) {
      return value.length > 1;
    },
    searchOnTable() {
      this.searched = searchByName(this.portfolios, this.search);
    },
    calculatePortfolioValue(holdings) {
      let price = 0;
      for (let i = 0; i < holdings.length; i += 1) {
        price += parseFloat(holdings[i].price);
      }
      return price;
    },
  },
  created() {
    this.searched = this.portfolios;
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

.md-icon {
  position: absolute;
  right: 4%;
}
</style>
