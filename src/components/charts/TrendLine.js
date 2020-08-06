import { Line, mixins } from 'vue-chartjs';

const { reactiveProp } = mixins;

export default {
  extends: Line,
  mixins: [reactiveProp],
  props: ['options'],
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
