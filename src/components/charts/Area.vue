<template>
  <div class="chart">
    <apexchart type="area" ref="chart" id="main-chart" :options="options" :series="series"></apexchart>
  </div>
</template>

<script>
export default {
  name: 'Area',
  props: {
    options: {
      type: Object,
    },
    series: {
      type: Array,
    },
  },
};
</script>

<style scoped>
.chart, .apexcharts-canvas {
  width: 100%;
  max-width: 800px;
  min-height: 40px;
  height: 600px;
  margin: 0 auto;
  padding: 0 !important;
  margin-left: 0 !important;
}
</style>
