<template>
  <div v-if="loaded">
    <md-table v-model="stocks">
      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="Symbol" md-sort-by="symbol">{{ item.ticker }}</md-table-cell>
        <md-table-cell md-label="Name" md-sort-by="name">{{ item.short_name }}</md-table-cell>
        <md-table-cell md-label="Price (USD)" md-sort-by="price">{{
          roundFloat(item.latest_market_data.price) || roundFloat(item.latest_market_data.delayedprice) || 'NA'
        }}</md-table-cell>
        <md-table-cell md-label="Change (%)">{{
          roundFloat(item.latest_market_data.changepercent) || 'NA'
        }}</md-table-cell>
        <md-table-cell md-label="Volume">{{ item.latest_market_data.volume || 'NA' }}</md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>

<script>
export default {
  name: 'Summary',
  props: {
    stocks: {
      type: Array,
    },
  },
  data() {
    return {
      loaded: false,
    };
  },
  async mounted() {
    this.loaded = true;
  },
  methods: {
    roundFloat(val) {
      if (val) return +val.toFixed(2);
      return val;
    },
  },
};
</script>

<style lang="scss" scoped>
.md-card {
  text-align: left;
}

.close-icon {
  position: absolute;
  right: 4%;
}
.md-table .md-table-head {
  text-align: left;
}
.md-table .md-table-cell {
  text-align: left;
}
</style>
