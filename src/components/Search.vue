<template>
  <div>
    <md-autocomplete
      class="search-box"
      v-model="selectedLabel"
      :md-options="getSanitizedLabels"
      @input="getTickers"
      @md-selected="onSelect"
      :md-layout="searchLayout"
    >
      <label>{{ this.placeholder }}</label>
      <template slot="md-autocomplete-item" slot-scope="{ item, term }">
        <md-highlight-text :md-term="term">{{ item.Symbol }} - {{ item.Name }}</md-highlight-text>
      </template>
    </md-autocomplete>
  </div>
</template>

<script>
export default {
  name: 'Search',
  props: {
    searchLayout: {
      type: String,
      default: 'box',
    },
    placeholder: {
      type: String,
      default: 'Search symbols',
    },
  },
  data: () => ({
    selectedLabel: '',
    tickers: [],
    value: '',
  }),
  methods: {
    async getTickers(q) {
      this.$emit('input', this.selectedLabel);
      this.$store.dispatch('search', { q }).then((resp) => {
        const results = [];
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
      this.$emit('search', { symbol: ticker.Symbol, short_name: ticker.Name });
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
.search-box {
  width: 100%;
  max-width: 100%;
}
</style>
