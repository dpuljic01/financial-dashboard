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
      v-else-if="news.length === 0 && loaded"
      md-icon="announcement"
      md-label="No news related to your portfolio holdings"
    >
    </md-empty-state>
    <div v-else>
      <md-field style="max-width: 400px;">
        <label for="symbols">Filter by symbols:</label>
        <md-select v-model="selected" name="Symbols" id="symbols" md-dense>
          <md-option value="ALL">All</md-option>
          <md-option v-for="(ticker, id) in symbols" :key="id" :value="ticker">{{ ticker }}</md-option>
        </md-select>
      </md-field>
      <md-card
        v-for="(article, id) in filteredNews"
        :key="id"
        :href="article.link"
        class="md-elevation-1 articles"
        style="margin: auto auto 10px auto"
      >
        <md-card-header>
          <div class="md-caption">
            <strong>{{ article.symbol }}</strong> - {{ article.date_posted }} | {{ article.provider }}
          </div>
        </md-card-header>

        <md-card-content>
          <strong>{{ article.headline }}</strong>
        </md-card-content>

        <md-card-actions>
          <md-button :href="article.link" target="_blank" class="md-dense md-mini md-accent">Read more</md-button>
        </md-card-actions>
      </md-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'News',
  props: {
    tickers: {
      type: Array,
    },
  },
  data() {
    return {
      loaded: false,
      symbols: this.tickers,
      news: [],
      filteredNews: [],
      url: '#',
      selected: 'ALL',
    };
  },
  async mounted() {
    this.symbols = this.tickers;
    if (this.tickers.length > 0) {
      await this.getNews();
    }
    this.loaded = true;
  },
  watch: {
    selected(ticker) {
      if (ticker !== 'ALL') {
        this.filteredNews = this.news.filter((n) => n.symbol === ticker);
      } else {
        this.filteredNews = this.news;
      }
    },
    tickers(val) {
      this.getNews();
      this.symbols = val;
    },
  },
  methods: {
    async getNews() {
      const resp = await this.$store.dispatch('getNews', { symbols: this.tickers.join() });
      this.news = resp.data;
      this.filteredNews = this.news;
    },
  },
};
</script>

<style lang="scss" scoped>
.articles {
  text-align: left;
}
</style>
