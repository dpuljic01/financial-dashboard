<template>
  <div class="simple-search" :class="{ 'simple-search--compact': compact }">
    <div
      class="simple-search-input-row"
      :class="{ 'simple-search-input-row--focused': focused, 'simple-search-input-row--disabled': disabled }"
    >
      <i class="md-icon md-icon-font simple-search-icon">search</i>
      <input
        type="text"
        class="simple-search-input"
        :placeholder="placeholder"
        :disabled="disabled"
        v-model="query"
        @input="onInput"
        @keyup.enter="submitTyped"
        @focus="onFocus"
        @blur="onBlur"
      />
      <div v-if="loading" class="simple-search-spinner"></div>
      <button
        v-else-if="query"
        type="button"
        class="simple-search-add"
        title="Add symbol as typed"
        @mousedown.prevent="submitTyped"
      >
        <i class="md-icon md-icon-font">add</i>
      </button>
    </div>
    <ul v-if="showDropdown && tickers.length > 0" class="simple-search-dropdown">
      <li v-for="ticker in tickers" :key="ticker.symbol" @mousedown.prevent="select(ticker)">
        <span class="simple-search-symbol">{{ ticker.symbol }}</span>
        <span class="simple-search-name">{{ ticker.name }}</span>
      </li>
    </ul>
    <ul v-else-if="showDropdown && query && !loading" class="simple-search-dropdown">
      <li class="simple-search-empty">
        No matches - press <strong>Enter</strong> or tap + to add "{{ query.toUpperCase() }}" anyway
      </li>
    </ul>
  </div>
</template>

<script>
const DEBOUNCE_MS = 250;

export default {
  name: 'Search',
  props: {
    placeholder: {
      type: String,
      default: 'Search symbols',
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    // Smaller footprint for tight spaces like the nav bar - same behavior,
    // just sized to sit next to nav links instead of anchoring a page.
    compact: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    query: '',
    tickers: [],
    showDropdown: false,
    focused: false,
    loading: false,
    debounceTimer: null,
  }),
  methods: {
    onFocus() {
      this.focused = true;
      this.showDropdown = true;
    },
    onInput() {
      clearTimeout(this.debounceTimer);
      if (!this.query) {
        this.tickers = [];
        this.loading = false;
        return;
      }
      this.loading = true;
      this.debounceTimer = setTimeout(async () => {
        const resp = await this.$store.dispatch('search', { q: this.query });
        this.tickers = resp.data.map((ticker) => ({ symbol: ticker.symbol, name: ticker.name }));
        this.loading = false;
      }, DEBOUNCE_MS);
    },
    select(ticker) {
      if (this.disabled) return;
      this.reset();
      this.$emit('search', { symbol: ticker.symbol, short_name: ticker.name });
    },
    submitTyped() {
      if (this.disabled || !this.query) return;
      const symbol = this.query.toUpperCase();
      this.reset();
      this.$emit('search', { symbol, short_name: symbol });
    },
    onBlur() {
      this.focused = false;
      // delay so a mousedown on a dropdown item registers before it disappears
      setTimeout(() => {
        this.showDropdown = false;
      }, 150);
    },
    reset() {
      clearTimeout(this.debounceTimer);
      this.query = '';
      this.tickers = [];
      this.loading = false;
      this.showDropdown = false;
    },
  },
};
</script>

<style scoped>
.simple-search {
  position: relative;
  width: 100%;
  max-width: 420px;
  text-align: left;
}
.simple-search-input-row {
  display: flex;
  align-items: center;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 24px;
  padding: 0 8px 0 16px;
  height: 44px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.simple-search-input-row--focused {
  border-color: #116468;
  box-shadow: 0 2px 8px rgba(17, 100, 104, 0.2);
}
.simple-search-input-row--disabled {
  opacity: 0.6;
  pointer-events: none;
}
.simple-search-icon {
  color: rgba(0, 0, 0, 0.4);
  font-size: 20px !important;
  margin-right: 8px;
}
.simple-search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
  background: transparent;
  height: 100%;
}
.simple-search-add {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: #116468;
  color: #fff;
  cursor: pointer;
  flex-shrink: 0;
}
.simple-search-add .md-icon {
  color: #fff;
  font-size: 18px !important;
}
.simple-search-add:hover {
  background: #0a4547;
}
.simple-search-spinner {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  border: 2px solid rgba(17, 100, 104, 0.2);
  border-top-color: #116468;
  border-radius: 50%;
  animation: simple-search-spin 0.7s linear infinite;
}
@keyframes simple-search-spin {
  to {
    transform: rotate(360deg);
  }
}
.simple-search--compact {
  max-width: 240px;
}
.simple-search--compact .simple-search-input-row {
  height: 34px;
  padding: 0 6px 0 12px;
  border-radius: 17px;
}
.simple-search--compact .simple-search-icon {
  font-size: 16px !important;
  margin-right: 6px;
}
.simple-search--compact .simple-search-input {
  font-size: 13px;
}
.simple-search--compact .simple-search-add {
  width: 24px;
  height: 24px;
}
.simple-search--compact .simple-search-add .md-icon {
  font-size: 14px !important;
}
.simple-search--compact .simple-search-spinner {
  width: 14px;
  height: 14px;
}
.simple-search-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  right: 0;
  z-index: 20;
  background: #fff;
  list-style: none;
  margin: 0;
  padding: 6px 0;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18);
  max-height: 280px;
  overflow-y: auto;
}
.simple-search-dropdown li {
  padding: 10px 16px;
  cursor: pointer;
  display: flex;
  align-items: baseline;
  gap: 10px;
}
.simple-search-dropdown li:hover {
  background: rgba(17, 100, 104, 0.08);
}
.simple-search-symbol {
  font-weight: 600;
  color: #116468;
  min-width: 56px;
}
.simple-search-name {
  color: rgba(0, 0, 0, 0.6);
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.simple-search-empty {
  color: rgba(0, 0, 0, 0.5);
  font-size: 13px;
  cursor: default !important;
}
.simple-search-empty:hover {
  background: transparent !important;
}
</style>
