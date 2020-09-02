import { Doughnut } from 'vue-chartjs';

export default {
  extends: Doughnut,
  props: ['chartData', 'options'],
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
  watch: {
    data() {
      /* eslint no-underscore-dangle: ["error", { "allow": ["_chart"] }] */
      this._chart.destroy();
      this.renderChart(this.chartData);
    },
  },
};
