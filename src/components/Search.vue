<template>
  <div class="simple-search">
    <label v-if="placeholder">{{ placeholder }}</label>
    <div class="simple-search-input-row">
      <input
        type="text"
        class="simple-search-input"
        v-model="query"
        @input="onInput"
        @keyup.enter="submitTyped"
        @focus="showDropdown = true"
        @blur="onBlur"
      />
      <md-button class="md-icon-button md-dense" v-if="query" @click="submitTyped">
        <md-icon>add</md-icon>
      </md-button>
    </div>
    <ul v-if="showDropdown && tickers.length > 0" class="simple-search-dropdown">
      <li v-for="ticker in tickers" :key="ticker.symbol" @mousedown.prevent="select(ticker)">
        {{ ticker.symbol }} - {{ ticker.name }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Search',
  props: {
    placeholder: {
      type: String,
      default: 'Search symbols',
    },
  },
  data: () => ({
    query: '',
    tickers: [],
    showDropdown: false,
  }),
  methods: {
    async onInput() {
      if (!this.query) {
        this.tickers = [];
        return;
      }
      const resp = await this.$store.dispatch('search', { q: this.query });
      this.tickers = resp.data.map((ticker) => ({ symbol: ticker.symbol, name: ticker.name }));
    },
    select(ticker) {
      this.reset();
      this.$emit('search', { symbol: ticker.symbol, short_name: ticker.name });
    },
    submitTyped() {
      if (!this.query) return;
      const symbol = this.query.toUpperCase();
      this.reset();
      this.$emit('search', { symbol, short_name: symbol });
    },
    onBlur() {
      // delay so a mousedown on a dropdown item registers before it disappears
      setTimeout(() => {
        this.showDropdown = false;
      }, 150);
    },
    reset() {
      this.query = '';
      this.tickers = [];
      this.showDropdown = false;
    },
  },
};
</script>

<style scoped>
.simple-search {
  position: relative;
  width: 100%;
  max-width: 100%;
  text-align: left;
}
.simple-search label {
  display: block;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.54);
  margin-bottom: 4px;
}
.simple-search-input-row {
  display: flex;
  align-items: center;
}
.simple-search-input {
  flex: 1;
  border: none;
  border-bottom: 1px solid rgba(0, 0, 0, 0.42);
  padding: 8px 4px;
  font-size: 16px;
  outline: none;
}
.simple-search-input:focus {
  border-bottom: 2px solid #116468;
}
.simple-search-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 20;
  background: #fff;
  list-style: none;
  margin: 0;
  padding: 4px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  max-height: 240px;
  overflow-y: auto;
}
.simple-search-dropdown li {
  padding: 8px 12px;
  cursor: pointer;
}
.simple-search-dropdown li:hover {
  background: rgba(0, 0, 0, 0.06);
}
</style>
