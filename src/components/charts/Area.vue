<template>
  <div class="chart">
    <apexchart type="area" :options="options" :series="series"></apexchart>
  </div>
</template>

<script>
export default {
  name: 'Area',
  props: ['options', 'series'],
};
</script>
