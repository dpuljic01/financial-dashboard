<template>
  <div>
    <md-progress-spinner
      v-if="!loaded"
      :md-diameter="50"
      :md-stroke="4"
      style="margin-top: 50px;"
      md-mode="indeterminate"
    ></md-progress-spinner>
    <md-empty-state
      v-else-if="Object.values(companyProfile).length === 0 && loaded"
      md-icon="error"
      md-label="Couldn't retrieve info about this company"
    >
    </md-empty-state>
    <div v-else class="profile">
      <div class="profile-header">
        <div class="profile-badge">{{ companyProfile.symbol ? companyProfile.symbol.slice(0, 2) : '' }}</div>
        <div>
          <h2 class="md-title profile-title">{{ companyProfile.longname }}</h2>
          <div class="profile-subtitle">
            <span v-if="companyProfile.sector">{{ companyProfile.sector }}</span>
            <span v-if="companyProfile.sector && companyProfile.industry"> &middot; </span>
            <span v-if="companyProfile.industry">{{ companyProfile.industry }}</span>
          </div>
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat" v-for="stat in stats" :key="stat.label">
          <span class="stat-label">{{ stat.label }}</span>
          <a v-if="stat.link" class="stat-value stat-link" :href="stat.link" target="_blank" rel="noopener">{{
            stat.value
          }}</a>
          <span v-else class="stat-value">{{ stat.value }}</span>
        </div>
      </div>

      <p v-if="companyProfile.longbusinesssummary" class="summary">
        {{ companyProfile.longbusinesssummary }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CompanyProfile',
  props: {
    companyInfo: {
      type: Object,
    },
  },
  data() {
    return {
      loaded: false,
      companyProfile: this.companyInfo,
    };
  },
  async mounted() {
    this.companyProfile = this.companyInfo;
    this.loaded = true;
  },
  computed: {
    stats() {
      const c = this.companyProfile;
      const items = [
        { label: 'Market cap', value: this.formatMarketCap(c.marketcap) },
        { label: 'Employees', value: this.formatNumber(c.fulltimeemployees) },
        { label: 'Headquarters', value: this.formatHeadquarters(c) },
        { label: 'Website', value: this.formatWebsite(c.website), link: c.website },
        { label: 'P/E (TTM)', value: this.formatDecimal(c.trailingpe) },
        { label: 'Forward P/E', value: this.formatDecimal(c.forwardpe) },
        { label: 'Dividend yield', value: c.dividendyield != null ? `${c.dividendyield}%` : null },
        { label: 'Beta', value: this.formatDecimal(c.beta) },
        { label: 'Day range', value: c.dayrange },
        { label: '52-week range', value: c.fiftytwoweekrange },
        { label: 'Analyst rating', value: c.averageanalystrating },
      ];
      return items.filter((item) => item.value !== null && item.value !== undefined && item.value !== '');
    },
  },
  methods: {
    formatMarketCap(value) {
      if (!value) return null;
      const units = [
        { threshold: 1e12, suffix: 'T' },
        { threshold: 1e9, suffix: 'B' },
        { threshold: 1e6, suffix: 'M' },
      ];
      const unit = units.find((u) => value >= u.threshold);
      if (!unit) return `$${value}`;
      return `$${(value / unit.threshold).toFixed(2)}${unit.suffix}`;
    },
    formatNumber(value) {
      if (value == null) return null;
      return value.toLocaleString('en-US');
    },
    formatDecimal(value) {
      if (value == null) return null;
      return value.toFixed(2);
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
    companyInfo(val) {
      this.companyProfile = val;
    },
  },
};
</script>

<style lang="scss" scoped>
.profile {
  text-align: left;
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
  width: 56px;
  height: 56px;
  border-radius: 8px;
  background: #116468;
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.02em;
}
.profile-title {
  margin: 0;
}
.profile-subtitle {
  color: rgba(0, 0, 0, 0.6);
  font-size: 14px;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
  padding: 16px;
  margin-bottom: 20px;
  background: rgba(17, 100, 104, 0.05);
  border-radius: 8px;
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
