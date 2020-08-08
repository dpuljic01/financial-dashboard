<template>
  <div>
    <md-autocomplete
      class="search"
      v-model="selectedLabel"
      :md-options="getSanitizedLabels"
      @md-changed="getTickers"
      @md-selected="onSelect"
      md-layout="box"
      md-dense
    >
      <label>Search for symbols or companies</label>

      <template slot="md-autocomplete-item" slot-scope="{ item, term }">
        <md-highlight-text :md-term="term">{{ item.Symbol }}  -  {{ item.Name }}</md-highlight-text>
      </template>
    </md-autocomplete>
  </div>
</template>

<script>
export default {
  name: 'Search',
  data: () => ({
    selectedLabel: [],
    searchTerm: '',
    tickers: [],
    value: '',
  }),
  methods: {
    async getTickers(q) {
      this.$store.dispatch('search', { q }).then((resp) => {
        const results = [];
        if (!resp || !resp.data) {
          this.tickers = [{ id: 1, symbol: '---', name: '----' }];
        }
        for (let i = 1; i < resp.data.length + 1; i += 1) {
          results.push({
            id: i,
            symbol: resp.data[i - 1].symbol,
            name: resp.data[i - 1].name,
          });
        }
        this.tickers = results;
      });
    },
    onSelect(ticker) {
      this.symbol = ticker.Symbol;
      console.log(this.symbol);
    },
  },
  computed: {
    getSanitizedLabels() {
      return this.tickers.map((label) => ({
        Id: label.id,
        Name: label.name,
        Symbol: label.symbol,
        toLowerCase: () => label.name.toLowerCase() && label.symbol.toLowerCase(),
        toString: () => label.name && label.symbol,
      }));
    },
  },
};
</script>

<style scoped>
.search {
  max-width: 100%;
}
</style>
