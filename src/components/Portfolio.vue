<template>
  <div class="page-container">
    <div v-if="!loaded" class="portfolio-loading">
      <FinancialLoader label="Loading portfolio…" />
    </div>
    <template v-else>
      <div class="page-section card-surface portfolio-card">
        <div class="portfolio-card-header">
          <div class="portfolio-head">
            <span class="portfolio-label">Portfolio</span>
            <div class="portfolio-name-row" v-if="!editingName">
              <h3 class="portfolio-name" @click="startEditName">{{ portfolio.name }}</h3>
              <button
                type="button"
                class="portfolio-name-edit"
                title="Rename portfolio"
                @click="startEditName"
              >
                <md-icon>edit</md-icon>
              </button>
            </div>
            <div class="portfolio-name-row" v-else>
              <input
                ref="nameInput"
                v-model="nameDraft"
                class="portfolio-name-input"
                maxlength="50"
                @keydown.enter.prevent="confirmName"
                @keydown.esc.prevent="cancelEditName"
                @blur="confirmName"
              />
            </div>
            <p v-if="portfolio.info" class="portfolio-meta">{{ portfolio.info }}</p>
          </div>
          <md-button v-if="path === 'holdings'" class="md-raised md-primary" @click="addSymbolOpen = true">
            <md-icon>add</md-icon> Add symbol
          </md-button>
        </div>
        <TabBar :tabs="portfolioTabs" :modelValue="'tab-' + path" @change="onPortfolioTabChange" />

        <md-empty-state
          v-if="portfolio.stocks.length === 0"
          md-icon="playlist_add"
          md-label="No symbols yet"
          md-description="Add a symbol to start tracking it in this portfolio."
        >
          <md-button class="md-primary md-raised" @click="addSymbolOpen = true">
            <md-icon>add</md-icon> Add symbol
          </md-button>
        </md-empty-state>

        <template v-else>
          <div v-if="path === 'summary'">
            <Summary :stocks="portfolio.stocks" :last-updated="lastUpdated"></Summary>
          </div>
          <div v-if="path === 'holdings'">
            <Holdings ref="holdings" @deletedSymbol="onDelete" :portfolio="portfolio"></Holdings>
          </div>
          <div v-if="path === 'news'">
            <News :tickers="tickers"></News>
          </div>
          <div v-if="path === 'performance'">
            <Performance :portfolio="portfolio"></Performance>
          </div>
        </template>
      </div>

      <Modal
        :model-value="addSymbolOpen"
        @update:model-value="addSymbolOpen = $event"
      >
        <h3 class="modal-title">Add a symbol</h3>
        <p class="modal-subtitle">
          Search a ticker - symbols you already hold jump straight to logging shares, new ones
          get added first.
        </p>
        <Search
          @search="onAddSymbol($event)"
          :disabled="addingSymbol"
          placeholder="e.g. AAPL, MSFT..."
        ></Search>
        <div v-if="addingSymbol" class="add-symbol-status">
          <FinancialLoader size="small" :label="`Adding ${pendingSymbol}…`" />
        </div>
      </Modal>
    </template>
  </div>
</template>

<script>
import Search from './Search.vue';
import Holdings from './portfolio/Holdings.vue';
import Summary from './portfolio/Summary.vue';
import News from './portfolio/News.vue';
import Performance from './portfolio/Performance.vue';
import TabBar from './TabBar.vue';
import Modal from './Modal.vue';
import FinancialLoader from './FinancialLoader.vue';

export default {
  name: 'Portfolio',
  components: {
    Holdings,
    Summary,
    Search,
    News,
    Performance,
    TabBar,
    Modal,
    FinancialLoader,
  },
  data() {
    return {
      addSymbolOpen: false,
      addingSymbol: false,
      pendingSymbol: '',
      editingName: false,
      nameDraft: '',
      portfolio: {},
      loaded: false,
      tickers: [],
      path: 'summary',
      lastUpdated: null,
      pollTimer: null,
      polling: false,
      portfolioTabs: [
        { id: 'tab-summary', label: 'Summary' },
        { id: 'tab-holdings', label: 'Holdings' },
        { id: 'tab-performance', label: 'Performance' },
        { id: 'tab-news', label: 'News' },
      ],
    };
  },
  created() {
    this.portfolioId = this.$route.params.portfolioId;
    this.path = this.$route.path.split('/').pop();
  },
  async mounted() {
    this.$store.commit('setLoading', true);
    this.portfolio = await this.$store.dispatch('getPortfolio', this.portfolioId);
    this.getTickers();
    this.$store.commit('setLoading', false);
    this.loaded = true;
    this.lastUpdated = new Date();
    if (this.tickers.length > 0) {
      this.startPolling();
    }
  },
  beforeUnmount() {
    this.stopPolling();
  },
  methods: {
    startPolling() {
      // 20s matches the backend's cache TTL on /yfinance/latest (see
      // tickers.py) - polling faster than that would just re-request the
      // same cached response instead of getting fresher prices.
      this.pollTimer = setInterval(() => this.refreshPrices(), 20000);
    },
    stopPolling() {
      if (this.pollTimer) {
        clearInterval(this.pollTimer);
        this.pollTimer = null;
      }
    },
    async refreshPrices() {
      // Skip a backgrounded tab and skip overlapping ticks if a previous
      // refresh is still in flight (e.g. a slow upstream provider).
      if (document.hidden || this.polling || this.tickers.length === 0) {
        return;
      }
      this.polling = true;
      try {
        const resp = await this.$store.dispatch('getLatestStockPrices', { symbols: this.tickers.join() });
        const quoteByTicker = {};
        (resp.data || []).forEach((quote) => {
          if (quote.ticker) quoteByTicker[quote.ticker] = quote;
        });
        // Patch latest_market_data on the existing stock objects in place
        // rather than reassigning this.portfolio wholesale (which used to
        // re-fetch the entire portfolio - holdings, lots, company info,
        // everything - every 20s). Mutating just this one field still
        // updates the price/change/volume cells reactively, without the
        // full-portfolio prop change cascading into Holdings/Performance/
        // TabBar and making the whole page visibly redraw.
        for (let i = 0; i < this.portfolio.stocks.length; i += 1) {
          const quote = quoteByTicker[this.portfolio.stocks[i].ticker];
          if (quote) this.portfolio.stocks[i].latest_market_data = quote;
        }
        this.lastUpdated = new Date();
      } catch (err) {
        // A single missed refresh isn't worth surfacing to the user - the
        // next tick retries on its own.
      } finally {
        this.polling = false;
      }
    },
    onPortfolioTabChange(tabId) {
      this.path = tabId.replace('tab-', '');
      this.$router.push(`/portfolios/${this.portfolio.id}/${this.path}`);
    },
    getTickers() {
      const tickers = this.portfolio.stocks.map((stock) => stock.ticker);
      this.tickers = tickers;
    },
    async onAddSymbol(payload) {
      const symbol = payload.symbol.toUpperCase();

      // Already tracked in this portfolio - nothing to add, jump straight
      // to logging shares against it instead of erroring on a duplicate.
      const alreadyHeld = this.portfolio.stocks.some((stock) => stock.ticker === symbol);
      if (alreadyHeld) {
        this.addSymbolOpen = false;
        this.openAddHolding(symbol);
        return;
      }

      this.addingSymbol = true;
      this.pendingSymbol = symbol;
      this.$store.commit('setLoading', true);
      try {
        await this.$store.dispatch('addSymbol', {
          portfolio: this.portfolio.id,
          payload: {
            symbol,
            short_name: payload.short_name,
          },
        });
        this.portfolio = await this.$store.dispatch('getPortfolio', this.portfolioId);
        this.getTickers();
        this.addSymbolOpen = false;
        this.$store.dispatch('successMessage');
        // A freshly-added symbol has no shares yet - continue straight into
        // logging the first buy instead of leaving it at 0/$0.00 for the
        // user to notice and come back to separately.
        this.openAddHolding(symbol);
      } finally {
        this.addingSymbol = false;
        this.$store.commit('setLoading', false);
      }
    },
    openAddHolding(symbol) {
      // Only reachable when path === 'holdings' (the only tab the "Add
      // symbol" button renders on), so the Holdings child - and its own
      // "add holding" modal/form - is guaranteed to be mounted here.
      this.$nextTick(() => {
        if (this.$refs.holdings) {
          this.$refs.holdings.add(symbol);
        }
      });
    },
    onDelete() {
      this.getTickers();
    },
    startEditName() {
      this.nameDraft = this.portfolio.name;
      this.editingName = true;
      this.$nextTick(() => this.$refs.nameInput && this.$refs.nameInput.focus());
    },
    cancelEditName() {
      this.editingName = false;
    },
    confirmName() {
      // Guards against the blur that firing cancelEditName/Enter's own save
      // triggers as the input unmounts - without it, the blur handler would
      // re-run this and either re-save or overwrite the just-cancelled edit.
      if (!this.editingName) return;
      this.editingName = false;
      const trimmed = this.nameDraft.trim();
      if (!trimmed || trimmed === this.portfolio.name) return;
      this.saveName(trimmed);
    },
    async saveName(name) {
      const previous = this.portfolio.name;
      this.portfolio.name = name;
      try {
        await this.$store.dispatch('updatePortfolio', {
          portfolioId: this.portfolio.id,
          payload: { name },
        });
      } catch (err) {
        this.portfolio.name = previous;
        this.$store.dispatch('errorMessage', 'Could not rename portfolio');
      }
    },
  },
  watch: {
    portfolio: function portfolio(val) {
      this.portfolio = val;
    },
    tickers: function tickers(val) {
      this.tickers = val;
    },
  },
};
</script>
<style scoped>
.portfolio-loading {
  display: flex;
  justify-content: center;
  margin-top: 80px;
}
.portfolio-card {
  padding: 28px;
}
.portfolio-heading {
  margin-top: 0;
}
.portfolio-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 8px;
}
.portfolio-card-header .portfolio-heading {
  margin-bottom: 0;
}
.portfolio-head {
  min-width: 0;
}
.portfolio-label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: rgba(0, 0, 0, 0.4);
  margin-bottom: 2px;
}
.portfolio-name-row {
  display: flex;
  align-items: center;
  gap: 6px;
}
.portfolio-name {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  cursor: text;
  border-bottom: 1px dashed transparent;
  padding: 1px 2px;
  margin-left: -2px;
}
.portfolio-name-row:hover .portfolio-name {
  border-bottom-color: rgba(0, 0, 0, 0.25);
}
.portfolio-name-edit {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: none;
  color: rgba(0, 0, 0, 0.35);
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.1s ease;
}
.portfolio-name-row:hover .portfolio-name-edit,
.portfolio-name-edit:focus-visible {
  opacity: 1;
}
.portfolio-name-edit .md-icon {
  margin: 0;
  font-size: 15px !important;
}
.portfolio-name-input {
  font-size: 20px;
  font-weight: 600;
  font-family: inherit;
  padding: 1px 2px;
  margin-left: -2px;
  border: none;
  border-bottom: 1px dashed var(--gain-color, #116468);
  background: transparent;
  outline: none;
  min-width: 0;
  width: 100%;
  max-width: 360px;
}
.portfolio-meta {
  margin: 4px 0 0;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.55);
  max-width: 60ch;
}
.modal-title {
  margin: 0 0 4px;
}
.modal-subtitle {
  margin: 0 0 16px;
  color: rgba(0, 0, 0, 0.6);
  font-size: 14px;
}
.add-symbol-status {
  margin-top: 16px;
}
</style>
