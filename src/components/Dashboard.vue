<template>
  <div>
    <search />
    <trend-chart></trend-chart>
    <portfolio v-if="!hasPortfolio"></portfolio>
  </div>
</template>

<script>
// import Vue from 'vue';
import TrendChart from './charts/TrendChart.vue';
import Portfolio from './Portfolio.vue';
import Search from './Search.vue';

export default {
  name: 'Dashboard',
  components: {
    TrendChart,
    Portfolio,
    Search,
  },
  data() {
    return {
      hasPortfolio: this.$store.getters.hasPortfolio,
    };
  },
  // created() {
  //   if (this.$store.state.portfolios.length === 0) {
  //     Vue.toasted.show('Set up your first portfolio. ', {
  //       position: 'bottom-center',
  //       duration: null, // forever
  //       icon: 'error',
  //       type: 'error',
  //       after: true,
  //       action: [
  //         {
  //           text: 'Close',
  //           onClick: (e, toast) => {
  //             toast.goAway(0);
  //           },
  //         },
  //         {
  //           text: 'Setup',
  //           className: 'dp-accent',
  //           push: {
  //             name: 'Portfolio',
  //           },
  //         },
  //       ],
  //     });
  //   }
  // },
};
</script>

<style scoped>
.md-drawer {
  max-width: 250px;
}
.md-menu.md-button {
  height: 100%;
}
</style>
