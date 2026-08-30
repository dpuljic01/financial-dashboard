<template>
  <div ref="container" class="lightweight-chart" :style="{ height: `${height}px` }"></div>
</template>

<script>
import {
  createChart, AreaSeries, LineSeries, CrosshairMode,
} from 'lightweight-charts';

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
    // Auto-hides the right price scale when the chart's own rendered width
    // drops below this (0 = never). Raw dollar labels ("$100,000") eat too
    // much of a narrow chart's width for what they add.
    hidePriceScaleBelow: {
      type: Number,
      default: 0,
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
          // Magnet sticks the horizontal line/label to the series' actual
          // value at the hovered point - without it explicit, the label can
          // end up showing whatever price the raw cursor Y position maps
          // to, which doesn't match the point the vertical line/marker is
          // actually sitting on.
          mode: CrosshairMode.Magnet,
          horzLine: { visible: !this.sparkline, labelVisible: !this.sparkline },
          vertLine: { visible: !this.sparkline, labelVisible: !this.sparkline },
        },
        handleScroll: !this.sparkline,
        handleScale: !this.sparkline,
      });

      this.chart.subscribeCrosshairMove((param) => {
        // Translate lightweight-charts' own param (keyed by internal series
        // instances the parent has no handle on) into a plain array aligned
        // with the `series` prop order, so callers don't need to know
        // anything about how this wrapper built its series.
        const values = this.seriesInstances.map((instance) => {
          const point = param.seriesData && param.seriesData.get(instance);
          return point && point.value !== undefined ? point.value : null;
        });
        this.$emit('crosshair-move', { time: param.time || null, values });
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
          // The pinned "latest value" axis tag doesn't track the crosshair
          // at all - every caller already shows the current price/value of
          // its own elsewhere (a header, stat card, or legend), so leaving
          // this on just sits there looking like a hover readout that
          // doesn't match wherever you're actually pointing.
          lastValueVisible: false,
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
      const width = this.$refs.container.clientWidth;
      this.chart.resize(width, this.height);
      if (this.hidePriceScaleBelow > 0) {
        this.chart.applyOptions({ rightPriceScale: { visible: width >= this.hidePriceScaleBelow } });
      }
    },
  },
};
</script>

<style scoped>
.lightweight-chart {
  width: 100%;
}
</style>
