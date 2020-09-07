<template>
  <div class="chart">
    <apexchart type="area" :height="height" :options="options" :series="series"></apexchart>
  </div>
</template>

<script>
export default {
  name: 'Area',
  props: ['height', 'options', 'series'],
};
</script>
