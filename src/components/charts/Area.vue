<template>
  <div class="example">
    <apexchart type="area" height="300" :options="options" :series="series"></apexchart>
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
