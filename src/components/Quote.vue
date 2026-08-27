<template>
  <div
    v-if="loaded"
    style="max-width: 800px; display: flex; flex-direction: column; justify-content: space-around; margin: 0 auto;"
  >
    <div>
      <Search @search="searchQuote($event)"></Search>
    </div>

    <h3 class="md-title">{{ this.companyInfo.shortname || this.quote }}</h3>
    <Compare :multiple="false" :symbols="[this.quote]"></Compare>

    <div v-if="this.quote[0] !== '^'">
      <TabBar :tabs="quoteTabs" :modelValue="'tab-' + path" @change="onQuoteTabChange" />

      <div v-if="path === 'profile'">
        <md-empty-state
          v-if="Object.values(companyInfo).length == 0"
          md-description="We couldn't retrieve company info"
        >
        </md-empty-state>
        <CompanyProfile v-else :company-info="companyInfo"></CompanyProfile>
      </div>

      <div v-if="path === 'news'">
        <News :tickers="[this.quote]"></News>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';
import Search from './Search.vue';
import CompanyProfile from './portfolio/CompanyProfile.vue';
import Compare from './Compare.vue';
import News from './portfolio/News.vue';
import TabBar from './TabBar.vue';
import { QUOTE_OPTIONS } from '../consts';
import { setQuoteSeries, setYAxis } from '../utils';

export default {
  name: 'Quote',
  components: {
    Search,
    CompanyProfile,
    News,
    Compare,
    TabBar,
  },
  data() {
    return {
      quote: this.$route.params.quote,
      period: '1d',
      fullPeriod: '1 day',
      interval: '5m',
      options: QUOTE_OPTIONS,
      series: [],
      loaded: false,
      activeTab: 'tab-1d',
      companyInfo: {},
      path: 'profile',
      quoteTabs: [
        { id: 'tab-profile', label: 'Profile' },
        { id: 'tab-news', label: 'News' },
      ],
    };
  },
  async mounted() {
    this.path = this.$route.path.split('/').pop();
    this.companyInfo = await this.$store.dispatch('getCompanyInfo', this.quote);
    await this.loadQuote();
    this.$store.commit('setLoading', false);
    this.loaded = true;
  },
  methods: {
    onQuoteTabChange(tabId) {
      this.path = tabId.replace('tab-', '');
      this.$router.push(`/quote/${this.quote}/${this.path}`);
    },
    switchPeriod(period) {
      this.period = period;
      switch (this.period) {
        case '1d':
          this.fullPeriod = '1 day';
          this.interval = '5m';
          break;
        case '5d':
          this.fullPeriod = '5 days';
          this.interval = '30m';
          break;
        case '1mo':
          this.fullPeriod = '1 month';
          this.interval = '1d';
          break;
        case '6mo':
          this.fullPeriod = '6 months';
          this.interval = '1d';
          break;
        case '1y':
          this.fullPeriod = '1 year';
          this.interval = '1d';
          break;
        case '5y':
          this.fullPeriod = '5 years';
          this.interval = '1wk';
          break;
        case 'max':
          this.fullPeriod = 'Since going public';
          this.interval = '1mo';
          break;
        default:
          this.period = '1d';
          this.interval = '5m';
      }
      this.loadQuote();
    },
    async loadQuote() {
      if (this.quote) {
        this.$store.commit('setLoading', true);
        await this.getQuoteHistory();
        this.options = {
          ...this.options,
          ...{
            xaxis: {
              type: 'datetime',
            },
            yaxis: setYAxis(this.series),
            legend: {
              position: 'top',
              horizontalAlign: 'left',
            },
            tooltip: {
              x: {
                formatter: function f(val) {
                  return moment(val).format('LLL');
                },
              },
              y: {
                formatter: function f(val) {
                  return +val.toFixed(4);
                },
              },
            },
            title: {
              text: this.companyInfo.shortname,
            },
            subtitle: {
              text: this.fullPeriod,
            },
            chart: {
              animations: {
                enabled: false,
              },
              height: 'auto',
            },
          },
        };
        this.$store.commit('setLoading', false);
      }
    },
    async searchQuote(event) {
      await this.$router.push(`/quote/${event.symbol}/profile`);
      this.path = 'profile';
      this.quote = event.symbol;
      await this.loadQuote();
    },
    async getQuoteHistory() {
      const resp = await this.$store.dispatch('getStockHistoryData', {
        symbols: this.quote,
        interval: this.interval,
        period: this.period,
        include_info: false,
      });
      this.series = setQuoteSeries(resp.data);
      this.$store.commit('setLoading', false);
    },
    async delayedCompare() {
      await this.compare();
    },
  },
  watch: {
    async quote(val) {
      this.loaded = false;
      this.quote = val;
      if (this.quote.toLowerCase() !== this.companyInfo.symbol.toLowerCase()) {
        this.companyInfo = await this.$store.dispatch('getCompanyInfo', this.quote);
      }
      this.loaded = true;
    },
  },
};
</script>

<style scoped>
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
</style>
