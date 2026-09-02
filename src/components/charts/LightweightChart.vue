<template>
  <div class="lightweight-chart-wrapper" :style="{ height: `${height}px` }">
    <!--
      lightweight-charts takes ownership of this div's children the moment
      createChart() runs - it injects and manages its own canvas/table DOM
      here directly, outside Vue's virtual DOM. Rendering anything of our
      own (like the combo tooltip) as a child of this same node means Vue
      and the chart library are both trying to own its child list, which is
      exactly the kind of conflict that silently drops updates. The tooltip
      lives as a sibling in the wrapper below instead, positioned over the
      chart with plain absolute positioning.
    -->
    <div ref="container" class="lightweight-chart"></div>
    <div v-if="comboTooltip && comboVisible" class="combo-tooltip" :style="{ left: `${comboX}px` }">
      {{ comboText }}
    </div>
  </div>
</template>

<script>
import moment from 'moment';
import { markRaw } from 'vue';
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
    // Hides the native price/date crosshair labels lightweight-charts draws
    // on the axes. Set this when the caller shows its own combined
    // price+date readout elsewhere (e.g. above the chart) - two disconnected
    // native labels sitting on opposite edges of the chart is a worse
    // reading experience than one clear spot, especially on mobile where
    // the right-edge price label is easy to miss entirely.
    hideCrosshairLabels: {
      type: Boolean,
      default: false,
    },
    // Renders a single floating pill at the bottom of the chart, following
    // the crosshair, combining price and date/time in one place - instead of
    // the price sitting on the right axis and the date on the bottom axis,
    // disconnected from each other.
    comboTooltip: {
      type: Boolean,
      default: false,
    },
    // Index into the `series` prop whose value is shown as the price in the
    // combo tooltip (defaults to the first/primary series).
    comboSeriesIndex: {
      type: Number,
      default: 0,
    },
    comboTimeFormat: {
      type: String,
      default: 'MMM D, YYYY',
    },
    comboFormatter: {
      type: Function,
      default: null,
    },
    // Emits 'load-earlier' when the user pans/zooms within a few bars of
    // the start of the currently-loaded data, so a caller can fetch and
    // prepend an earlier chunk (see prependSeriesData()) instead of the
    // pan just running out into empty space.
    loadMoreOnPan: {
      type: Boolean,
      default: false,
    },
    // Emits 'visible-range-change' ({ from, to }, unix seconds) whenever
    // the visible window shifts from panning or zooming - lets a caller
    // (e.g. keeping a 1D/1M/1Y timeframe picker in sync) react to where the
    // user has actually scrolled to, independent of loadMoreOnPan.
    emitVisibleRange: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['crosshair-move', 'load-earlier', 'visible-range-change'],
  data() {
    return {
      chart: null,
      seriesInstances: [],
      resizeObserver: null,
      comboVisible: false,
      comboX: 0,
      comboText: '',
    };
  },
  mounted() {
    // Plain instance properties, not reactive data - read-and-reset purely
    // inside the crosshair/pan callbacks below, no need to trigger a
    // re-render themselves.
    this.loadEarlierRequested = false;
    // fitContent() and resize() (called on every render/layout pass,
    // including the very first) each fire their own visible-range-change
    // events - sometimes more than one apiece (an intermediate range, then
    // the settled one) - and "fit everything" by definition starts right at
    // the first bar, which alone would satisfy the "near the edge" check
    // below. A timestamp window rather than a one-shot flag survives that
    // burst regardless of how many events one internal call happens to
    // produce, while still passing through genuine pans/zooms, which occur
    // well outside this window.
    this.suppressRangeEventsUntil = 0;
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
      // markRaw is essential here, not an optimization: lightweight-charts
      // keys its internal seriesData map (read in subscribeCrosshairMove
      // below) by the exact SeriesApi object identity it handed back from
      // addSeries(). Storing that object in Vue's reactive data wraps it in
      // a Proxy, so `this.seriesInstances[i]` is never === the object the
      // chart itself is using as a map key - every seriesData.get() lookup
      // silently misses and returns undefined, which is why hover
      // price/tooltip readouts driven by this map went blank. Same
      // reasoning applies to the chart instance itself.
      this.chart = markRaw(createChart(container, {
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
          horzLine: {
            visible: !this.sparkline,
            labelVisible: !this.sparkline && !this.hideCrosshairLabels && !this.comboTooltip,
          },
          vertLine: {
            visible: !this.sparkline,
            labelVisible: !this.sparkline && !this.hideCrosshairLabels && !this.comboTooltip,
          },
        },
        handleScroll: !this.sparkline,
        handleScale: !this.sparkline,
      }));

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

        if (this.comboTooltip) {
          const price = param.point ? values[this.comboSeriesIndex] : null;
          this.comboVisible = !!param.point && price !== null && price !== undefined;
          if (this.comboVisible) {
            const dateLabel = moment.unix(param.time).utc().format(this.comboTimeFormat);
            const priceLabel = this.comboFormatter ? this.comboFormatter(price) : `$${price.toFixed(2)}`;
            this.comboText = `${priceLabel}  ·  ${dateLabel}`;
            this.comboX = param.point.x;
          }
        }
      });

      if (this.loadMoreOnPan || this.emitVisibleRange) {
        this.chart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
          if (Date.now() < this.suppressRangeEventsUntil) return;
          if (!range) return;

          if (this.loadMoreOnPan && !this.loadEarlierRequested && this.seriesInstances.length > 0) {
            // range.from is the logical index of the visible window's left
            // edge - 0 is the first loaded bar, and it goes negative once
            // panning moves past all loaded data into empty space. Reading
            // it directly (rather than via barsInLogicalRange, which
            // returns null once the visible range no longer overlaps any
            // bars at all) means a fast/continuous pan that outruns one
            // fetch still keeps requesting the next chunk instead of
            // stalling on a permanently blank view once nothing is left to
            // measure from.
            if (range.from <= 5) {
              this.loadEarlierRequested = true;
              this.$emit('load-earlier');
            }
          }

          if (this.emitVisibleRange) {
            const visibleRange = this.chart.timeScale().getVisibleRange();
            if (visibleRange) this.$emit('visible-range-change', visibleRange);
          }
        });
      }
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

        const instance = markRaw(this.chart.addSeries(SeriesCtor, options));
        instance.setData(spec.data);
        return instance;
      });
      this.suppressRangeEventsUntil = Date.now() + 200;
      this.chart.timeScale().fitContent();
    },
    // Updates existing series in place with a fuller dataset (e.g. more
    // history prepended after a load-earlier fetch) without touching the
    // `series` prop. Deliberately bypasses renderSeries()'s remove/recreate
    // + fitContent() - the whole point of loading more while panning is
    // that new data quietly appears at the edge without the view jumping
    // or resetting back to a fit-everything zoom level.
    prependSeriesData(perSeriesData) {
      if (!this.chart) return;
      perSeriesData.forEach((data, index) => {
        const instance = this.seriesInstances[index];
        if (instance && data) instance.setData(data);
      });
      this.loadEarlierRequested = false;
    },
    handleResize() {
      if (!this.chart || !this.$refs.container) return;
      const width = this.$refs.container.clientWidth;
      // chart.resize() also fires a visible-range-change event (more bars
      // fit / don't fit at the new width) - suppress it the same way as
      // fitContent(), including the ResizeObserver's own initial callback
      // (which fires once as soon as observe() is called, before any real
      // resize has happened).
      this.suppressRangeEventsUntil = Date.now() + 200;
      this.chart.resize(width, this.height);
      if (this.hidePriceScaleBelow > 0) {
        this.chart.applyOptions({ rightPriceScale: { visible: width >= this.hidePriceScaleBelow } });
      }
    },
  },
};
</script>

<style scoped>
.lightweight-chart-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}
.lightweight-chart {
  width: 100%;
  height: 100%;
}
.combo-tooltip {
  position: absolute;
  bottom: 4px;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.9);
  color: #fff;
  font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 11px;
  line-height: 1;
  padding: 4px 8px;
  border-radius: 4px;
  white-space: nowrap;
  pointer-events: none;
  z-index: 3;
}
</style>
