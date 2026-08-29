<template>
  <div ref="container" class="lightweight-chart" :style="{ height: `${height}px` }"></div>
</template>

<script>
import { createChart, AreaSeries, LineSeries } from 'lightweight-charts';

const SERIES_CTORS = { area: AreaSeries, line: LineSeries };

export default {
  name: 'LightweightChart',
  props: {
    // [{ type: 'area'|'line', data: [{time, value}], color, lineWidth, lineStyle,
    //    topColor, bottomColor, priceScaleId, priceFormat }]
    series: {
      type: Array,
      required: true,
    },
    height: {
      type: Number,
      default: 300,
    },
    // Minimal mode for small decorative charts (market overview cards): no
    // axes, grid, crosshair, or scroll/zoom interaction - just the line.
    sparkline: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['crosshair-move'],
  data() {
    return {
      chart: null,
      seriesInstances: [],
      resizeObserver: null,
    };
  },
  mounted() {
    this.createChartInstance();
    this.renderSeries();
    this.resizeObserver = new ResizeObserver(() => this.handleResize());
    this.resizeObserver.observe(this.$refs.container);
  },
  beforeUnmount() {
    if (this.resizeObserver) this.resizeObserver.disconnect();
    if (this.chart) this.chart.remove();
  },
  watch: {
    series: {
      deep: true,
      handler() {
        this.renderSeries();
      },
    },
  },
  methods: {
    createChartInstance() {
      const { container } = this.$refs;
      this.chart = createChart(container, {
        width: container.clientWidth,
        height: this.height,
        autoSize: false,
        layout: {
          background: { color: 'transparent' },
          textColor: 'rgba(15, 34, 36, 0.55)',
          fontFamily: "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace",
          fontSize: 11,
          attributionLogo: false,
        },
        grid: {
          vertLines: { visible: false },
          horzLines: { visible: !this.sparkline, color: 'rgba(0, 0, 0, 0.06)' },
        },
        rightPriceScale: {
          visible: !this.sparkline,
          borderVisible: false,
        },
        timeScale: {
          visible: !this.sparkline,
          borderVisible: false,
          timeVisible: true,
          secondsVisible: false,
        },
        crosshair: {
          horzLine: { visible: !this.sparkline, labelVisible: !this.sparkline },
          vertLine: { visible: !this.sparkline, labelVisible: !this.sparkline },
        },
        handleScroll: !this.sparkline,
        handleScale: !this.sparkline,
      });

      this.chart.subscribeCrosshairMove((param) => {
        this.$emit('crosshair-move', param);
      });
    },
    renderSeries() {
      if (!this.chart) return;
      this.seriesInstances.forEach((instance) => this.chart.removeSeries(instance));
      this.seriesInstances = this.series.map((spec) => {
        const SeriesCtor = SERIES_CTORS[spec.type] || LineSeries;
        const options = {
          color: spec.color,
          lineWidth: spec.lineWidth || 2,
          lineStyle: spec.lineStyle || 0,
          priceLineVisible: false,
          lastValueVisible: !this.sparkline,
          crosshairMarkerVisible: !this.sparkline,
        };
        if (spec.type === 'area') {
          options.lineColor = spec.color;
          options.topColor = spec.topColor || 'rgba(15, 157, 112, 0.3)';
          options.bottomColor = spec.bottomColor || 'rgba(15, 157, 112, 0)';
        }
        if (spec.priceScaleId) options.priceScaleId = spec.priceScaleId;
        if (spec.priceFormat) options.priceFormat = spec.priceFormat;

        const instance = this.chart.addSeries(SeriesCtor, options);
        instance.setData(spec.data);
        return instance;
      });
      this.chart.timeScale().fitContent();
    },
    handleResize() {
      if (!this.chart || !this.$refs.container) return;
      this.chart.resize(this.$refs.container.clientWidth, this.height);
    },
  },
};
</script>

<style scoped>
.lightweight-chart {
  width: 100%;
}
</style>
