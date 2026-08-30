<template>
  <div v-if="loaded" class="page-container quote-page">
    <div class="page-section">
      <Search @search="searchQuote($event)"></Search>
    </div>

    <div class="page-section">
      <h3 class="md-title">
        {{ quote.toUpperCase() }}<span v-if="companyInfo.shortname"> &middot; {{ companyInfo.shortname }}</span>
      </h3>
      <Compare :multiple="false" :symbols="quoteSymbols"></Compare>
    </div>

    <div v-if="quote[0] !== '^'" class="page-section">
      <TabBar :tabs="quoteTabs" :modelValue="'tab-' + path" @change="onQuoteTabChange" />

      <div v-if="path === 'profile'">
        <md-empty-state
          v-if="stats.length === 0 && !companyInfo.longbusinesssummary"
          md-icon="error"
          md-label="Detailed company data isn't available right now"
          md-description="The data provider may be temporarily rate-limited - try again in a few minutes."
        >
        </md-empty-state>
        <div v-else class="profile card-surface">
          <div class="profile-header">
            <div class="profile-badge">
              <img
                v-if="logoUrl && !logoFailed"
                :src="logoUrl"
                :alt="`${quote} logo`"
                class="profile-logo"
                @error="logoFailed = true"
              />
              <span v-else>{{ quote.slice(0, 2) }}</span>
            </div>
            <div>
              <h2 class="md-title profile-title">{{ companyInfo.longname || companyInfo.shortname || quote }}</h2>
              <div class="profile-subtitle">
                <span class="profile-symbol">{{ quote.toUpperCase() }}</span>
                <span v-if="companyInfo.sector"> &middot; {{ companyInfo.sector }}</span>
                <span v-if="companyInfo.industry"> &middot; {{ companyInfo.industry }}</span>
              </div>
            </div>
          </div>

          <div class="stats-grid">
            <div class="stat" v-for="stat in stats" :key="stat.label">
              <span class="stat-label">{{ stat.label }}</span>
              <a v-if="stat.link" class="stat-value stat-link" :href="stat.link" target="_blank" rel="noopener">{{
                stat.value
              }}</a>
              <span v-else class="stat-value" :class="{ 'fin-figure': stat.numeric }">{{ stat.value }}</span>
            </div>
          </div>

          <p v-if="companyInfo.longbusinesssummary" class="summary">
            {{ companyInfo.longbusinesssummary }}
          </p>
        </div>
      </div>

      <div v-if="path === 'news'">
        <News :tickers="[quote]"></News>
      </div>
    </div>
  </div>
</template>

<script>
import Search from './Search.vue';
import Compare from './Compare.vue';
import News from './portfolio/News.vue';
import TabBar from './TabBar.vue';
import { formatCompactNumber } from '../utils';

const VALID_QUOTE_PATHS = ['profile', 'news'];

export default {
  name: 'Quote',
  components: {
    Search,
    News,
    Compare,
    TabBar,
  },
  data() {
    return {
      quote: this.$route.params.quote,
      loaded: false,
      logoFailed: false,
      companyInfo: {},
      path: 'profile',
      quoteTabs: [
        { id: 'tab-profile', label: 'Profile' },
        { id: 'tab-news', label: 'News' },
      ],
    };
  },
  async mounted() {
    const requestedPath = this.$route.path.split('/').pop();
    this.path = VALID_QUOTE_PATHS.includes(requestedPath) ? requestedPath : 'profile';
    this.companyInfo = await this.$store.dispatch('getCompanyInfo', this.quote);
    this.$store.commit('setLoading', false);
    this.loaded = true;
  },
  computed: {
    quoteSymbols() {
      return [this.quote];
    },
    logoUrl() {
      // Keyed off the ticker directly rather than companyInfo.website - the
      // full Yahoo info scrape this data comes from is unreliable (falls
      // back to a sparse dict under rate-limiting) and website is one of
      // the fields that goes missing first, which left the logo blank even
      // when the rest of the profile loaded fine.
      if (!this.quote || this.quote[0] === '^') return null;
      return `https://financialmodelingprep.com/image-stock/${this.quote.toUpperCase()}.png`;
    },
    stats() {
      const c = this.companyInfo;
      const items = [
        { label: 'Market cap', value: this.formatMarketCap(c.marketcap), numeric: true },
        { label: 'Volume', value: formatCompactNumber(c.volume), numeric: true },
        { label: 'Avg volume', value: formatCompactNumber(c.averagevolume), numeric: true },
        { label: 'Employees', value: formatCompactNumber(c.fulltimeemployees), numeric: true },
        { label: 'Headquarters', value: this.formatHeadquarters(c) },
        { label: 'Website', value: this.formatWebsite(c.website), link: c.website },
        { label: 'P/E (TTM)', value: this.formatDecimal(c.trailingpe), numeric: true },
        { label: 'Forward P/E', value: this.formatDecimal(c.forwardpe), numeric: true },
        { label: 'Dividend yield', value: c.dividendyield != null ? `${c.dividendyield}%` : null, numeric: true },
        { label: 'Beta', value: this.formatDecimal(c.beta), numeric: true },
        { label: 'Day range', value: this.formatRange(c.dayrange), numeric: true },
        { label: '52-week range', value: this.formatRange(c.fiftytwoweekrange), numeric: true },
        { label: 'Analyst rating', value: c.averageanalystrating },
      ];
      return items.filter((item) => item.value !== null && item.value !== undefined && item.value !== '');
    },
  },
  methods: {
    onQuoteTabChange(tabId) {
      this.path = tabId.replace('tab-', '');
      this.$router.push(`/quote/${this.quote}/${this.path}`);
    },
    async searchQuote(event) {
      await this.$router.push(`/quote/${event.symbol}/profile`);
      this.path = 'profile';
      this.quote = event.symbol;
    },
    formatMarketCap(value) {
      const compact = formatCompactNumber(value);
      return compact ? `$${compact}` : null;
    },
    formatDecimal(value) {
      if (value == null) return null;
      return value.toFixed(2);
    },
    formatRange(range) {
      if (!range) return null;
      const parts = range.split('-').map((part) => parseFloat(part));
      if (parts.length !== 2 || parts.some(Number.isNaN)) return range;
      return `${parts[0].toFixed(2)} - ${parts[1].toFixed(2)}`;
    },
    formatHeadquarters(c) {
      const parts = [c.city, c.state, c.country].filter(Boolean);
      return parts.length ? parts.join(', ') : null;
    },
    formatWebsite(website) {
      if (!website) return null;
      try {
        return new URL(website).hostname.replace(/^www\./, '');
      } catch (e) {
        return website;
      }
    },
  },
  watch: {
    async quote(val) {
      this.loaded = false;
      this.logoFailed = false;
      this.quote = val;
      if (this.quote.toLowerCase() !== (this.companyInfo.symbol || '').toLowerCase()) {
        this.companyInfo = await this.$store.dispatch('getCompanyInfo', this.quote);
      }
      this.loaded = true;
    },
  },
};
</script>

<style lang="scss" scoped>
.chart {
  width: 100%;
  height: 100%;
}
.chart-tabs > div {
  min-width: 20px;
  padding: 10px 0;
}
.active {
  background-color: #01a2a8;
}
.profile {
  text-align: left;
  padding: 24px 28px 28px;
}
.profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}
.profile-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
  width: 56px;
  height: 56px;
  border-radius: 8px;
  background: #116468;
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.02em;
}
.profile-logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #fff;
}
.profile-title {
  margin: 0;
}
.profile-subtitle {
  color: rgba(0, 0, 0, 0.6);
  font-size: 14px;
}
.profile-symbol {
  font-weight: 600;
  color: rgba(0, 0, 0, 0.75);
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 20px;
  padding: 20px 0;
  margin-bottom: 12px;
  border-top: 1px solid var(--surface-border);
  border-bottom: 1px solid var(--surface-border);
}
.stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow: hidden;
}
.stat-label {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: rgba(0, 0, 0, 0.54);
}
.stat-value {
  font-size: 15px;
  font-weight: 600;
  color: #0a383a;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.stat-link {
  text-decoration: none;
}
.stat-link:hover {
  text-decoration: underline;
}
.summary {
  line-height: 1.6;
  color: rgba(0, 0, 0, 0.8);
}
</style>
