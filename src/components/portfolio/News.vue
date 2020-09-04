<template>
  <div v-if="loaded">
    <div v-if="news.length > 0">
      <md-field style="max-width: 400px;">
        <label for="symbols">Filter by symbols:</label>
        <md-select v-model="selected" name="Symbols" id="symbols" md-dense>
          <md-option value="ALL">All</md-option>
          <md-option v-for="(ticker, id) in tickers" :key="id" :value="ticker">{{ ticker }}</md-option>
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
    <md-empty-state v-else md-icon="announcement" md-label="No news related to your portfolio holdings">
    </md-empty-state>
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
      news: [],
      filteredNews: [],
      url: '#',
      selected: 'ALL',
    };
  },
  async mounted() {
    this.$store.commit('setLoading', true);
    if (this.tickers.length > 0) {
      const resp = await this.$store.dispatch('getNews', { symbols: this.tickers.join() });
      this.news = resp.data;
      this.filteredNews = this.news;
    }
    this.$store.commit('setLoading', false);
    this.loaded = true;
  },
  watch: {
    selected: {
      handler(ticker) {
        if (ticker !== 'ALL') {
          this.filteredNews = this.news.filter((n) => n.symbol === ticker);
        } else {
          this.filteredNews = this.news;
        }
      },
    },
  },
  updated() {
    this.$store.commit('setLoading', false);
    this.loaded = true;
  },
};
</script>

<style lang="scss" scoped>
.articles {
  text-align: left;
}
</style>
