<template>
  <div class="compare card-surface" :class="{ 'compare--single': !multiple }">
    <h2 v-if="multiple" class="md-heading compare-heading">Compare multiple tickers and analyze their movement.</h2>

    <div v-if="multiple" class="compare-input">
      <p class="compare-input-label">Enter exact ticker symbols</p>
      <md-chips
        v-model="localSymbols"
        :md-auto-insert="true"
        :md-format="toUppercase"
        @md-insert="compare"
        @md-delete="delayedCompare"
      >
      </md-chips>
    </div>

    <div v-else-if="loaded" class="compare-price-header">
      <div class="compare-price-row">
        <span class="compare-price fin-figure">{{ formattedPrice }}</span>
        <span
          class="compare-change fin-figure"
          :class="displayTrend === 'up' ? 'fin-gain' : 'fin-loss'"
        >{{ formattedChange }}</span>
      </div>
      <span v-if="hoveredDateLabel" class="compare-hovered-date">{{ hoveredDateLabel }}</span>
      <span v-else-if="loadingEarlier" class="compare-hovered-date">Loading earlier history…</span>
    </div>

    <div v-if="multiple && loaded" class="compare-legend">
      <div v-for="item in legendItems" :key="item.name" class="compare-legend-item">
        <span class="compare-legend-swatch" :style="{ background: item.color }"></span>
        <span class="compare-legend-name">{{ item.name }}</span>
        <span
          v-if="item.value != null"
          class="compare-legend-value fin-figure"
          :class="item.value >= 0 ? 'fin-gain' : 'fin-loss'"
        >{{ item.value >= 0 ? '+' : '' }}{{ item.value.toFixed(2) }}%</span>
      </div>
    </div>

    <div class="compare-toolbar">
      <TabBar variant="pill" :tabs="periodTabs" v-model="activeTab" @change="onTabChange" />
    </div>

    <div class="chart">
      <LightweightChart
        v-if="loaded"
        ref="chart"
        :series="lwcSeries"
        :height="320"
        :hide-crosshair-labels="!multiple"
        :load-more-on-pan="!multiple && period !== 'max'"
        @crosshair-move="onCrosshairMove"
        @load-earlier="onLoadEarlier"
      />
      <FinancialLoader v-else style="margin-top: 50px;" />
    </div>
  </div>
</template>

<script>
import moment from 'moment';
import LightweightChart from './charts/LightweightChart.vue';
import TabBar from './TabBar.vue';
import FinancialLoader from './FinancialLoader.vue';
import { setQuoteSeries, percentChange } from '../utils';

const PALETTE = ['#116468', '#0f9d70', '#d1435c', '#00aaad', '#8c6dfd', '#e8873a', '#3a86ff'];

// How far back one "load earlier" fetch reaches, matched to the active
// period tab - panning on a 1D chart pages in another day at a time,
// panning on a 1Y chart pages in another year, and so on.
const PERIOD_SPAN_DAYS = {
  '1d': 1, '5d': 5, '1mo': 31, '6mo': 183, '1y': 366, '5y': 1827,
};
// Yahoo Finance doesn't have data before a company existed - stop paging
// back once a fetch comes back empty, or once this floor is hit either way.
const EARLIEST_FETCHABLE = '1970-01-01';

export default {
  name: 'Compare',
  props: {
    multiple: {
      type: Boolean,
      default: true,
    },
    symbols: {
      type: Array,
      default: () => ['GOOG', 'TSLA'],
    },
  },
  components: {
    LightweightChart,
    TabBar,
    FinancialLoader,
  },
  data() {
    return {
      localSymbols: [...this.symbols],
      // 1D defaults to a 5-minute intraday view, which on a quiet trading
      // day (or outside market hours) can render as a near-flat line that
      // reads as "no data" rather than "not much happened today". 1M gives
      // a chart that reliably shows real movement on first load.
      period: '1mo',
      interval: '1h',
      series: [],
      lwcSeries: [],
      legendItems: [],
      loaded: false,
      latestPrice: null,
      periodOpenPrice: null,
      hoveredPrice: null,
      hoveredTime: null,
      earliestLoadedDate: null,
      loadingEarlier: false,
      trend: 'flat',
      changePercent: null,
      activeTab: 'tab-1mo',
      periodTabs: [
        { id: 'tab-1d', label: '1D' },
        { id: 'tab-5d', label: '5D' },
        { id: 'tab-1mo', label: '1M' },
        { id: 'tab-6mo', label: '6M' },
        { id: 'tab-1y', label: '1Y' },
        { id: 'tab-5y', label: '5Y' },
        { id: 'tab-max', label: 'MAX' },
      ],
    };
  },
  computed: {
    // Falls back to the latest value when nothing's being hovered, so the
    // header reads live as you drag the crosshair (like a real trading
    // platform) without needing separate "hovering vs not" template logic.
    displayPrice() {
      return this.hoveredPrice != null ? this.hoveredPrice : this.latestPrice;
    },
    displayChangePercent() {
      if (this.hoveredPrice != null && this.periodOpenPrice) {
        return percentChange(this.periodOpenPrice, this.hoveredPrice);
      }
      return this.changePercent;
    },
    displayTrend() {
      if (this.displayChangePercent == null) return 'flat';
      return this.displayChangePercent >= 0 ? 'up' : 'down';
    },
    formattedPrice() {
      return this.displayPrice != null ? `$${(+this.displayPrice).toFixed(2)}` : '';
    },
    formattedChange() {
      if (this.displayChangePercent == null) return '';
      const sign = this.displayChangePercent > 0 ? '+' : '';
      return `${sign}${this.displayChangePercent.toFixed(2)}%`;
    },
    // Only relevant while actually hovering (blank the rest of the time,
    // rather than showing today's date) - and only for single-symbol mode,
    // since that's the only place with one unambiguous price to pair it with.
    hoveredDateLabel() {
      if (this.multiple || this.hoveredTime == null) return '';
      const intraday = /[mh]$/.test(this.interval);
      const format = intraday ? 'MMM D, YYYY HH:mm' : 'MMM D, YYYY';
      return moment.unix(this.hoveredTime).utc().format(format);
    },
  },
  mounted() {
    this.compare();
  },
  methods: {
    onTabChange(tabId) {
      [, this.period] = tabId.split('-');
      switch (this.period) {
        case '1d':
          this.interval = '5m';
          break;
        case '5d':
          this.interval = '30m';
          break;
        case '1mo':
          this.interval = '1h';
          break;
        case '6mo':
          this.interval = '1d';
          break;
        case '1y':
          this.interval = '1d';
          break;
        case '5y':
          this.interval = '1wk';
          break;
        case 'max':
          this.interval = '1mo';
          break;
        default:
          this.period = '1mo';
          this.interval = '1h';
          this.activeTab = 'tab-1mo';
      }
      this.compare();
    },
    toUppercase(str) {
      const newStr = str.toUpperCase();
      return newStr;
    },
    async compare() {
      if (this.localSymbols.length > 0) {
        this.loaded = false;
        await this.getQuoteHistory();
        if (!this.multiple) {
          this.updateSingleSymbolStats();
        }
        this.buildLwcSeries();
        this.loaded = true;
      }
    },
    updateSingleSymbolStats() {
      const [serie] = this.series;
      this.hoveredPrice = null;
      if (!serie || serie.data.length === 0) {
        this.latestPrice = null;
        this.periodOpenPrice = null;
        this.changePercent = null;
        this.trend = 'flat';
        this.earliestLoadedDate = null;
        return;
      }
      const [earliestDate, openPrice] = serie.data[0];
      const [, latestPrice] = serie.data[serie.data.length - 1];
      this.latestPrice = latestPrice;
      this.periodOpenPrice = openPrice;
      this.earliestLoadedDate = earliestDate;
      this.changePercent = percentChange(openPrice, latestPrice);
      if (this.changePercent > 0) {
        this.trend = 'up';
      } else if (this.changePercent < 0) {
        this.trend = 'down';
      } else {
        this.trend = 'flat';
      }
    },
    buildLwcSeries() {
      if (!this.multiple) {
        const [serie] = this.series;
        const data = serie ? this.toLwcData(serie.data) : [];
        const gain = this.trend !== 'down';
        this.lwcSeries = [
          {
            type: 'area',
            data,
            color: gain ? '#0f9d70' : '#d1435c',
            lineWidth: 2,
            topColor: gain ? 'rgba(15, 157, 112, 0.25)' : 'rgba(209, 67, 92, 0.25)',
            bottomColor: 'rgba(0, 0, 0, 0)',
          },
        ];
        this.legendItems = [];
        return;
      }

      // Different symbols trade at very different absolute prices, so a
      // shared raw-price scale makes the cheaper one unreadable. Normalize
      // every series to % change from the start of the visible period -
      // the same thing a real "compare" tool on a trading platform does -
      // so they're all directly comparable on one scale.
      this.lwcSeries = this.series.map((serie, index) => ({
        type: 'line',
        data: this.toPercentSeries(serie),
        color: PALETTE[index % PALETTE.length],
        lineWidth: 2,
        priceFormat: { type: 'percent', precision: 2 },
      }));
      this.legendItems = this.computeLegendItems();
    },
    toPercentSeries(serie) {
      const points = this.toLwcData(serie.data);
      const base = points.length > 0 ? points[0].value : null;
      if (!base) return [];
      return points.map((point) => ({ time: point.time, value: ((point.value / base) - 1) * 100 }));
    },
    computeLegendItems() {
      return this.series.map((serie, index) => {
        const percentPoints = this.toPercentSeries(serie);
        const last = percentPoints.length > 0 ? percentPoints[percentPoints.length - 1] : null;
        return { name: serie.name, color: PALETTE[index % PALETTE.length], value: last ? last.value : null };
      });
    },
    onCrosshairMove({ time, values }) {
      if (this.multiple) {
        if (time) {
          this.legendItems = this.legendItems.map((item, i) => (
            values[i] != null ? { ...item, value: values[i] } : item
          ));
        } else {
          this.legendItems = this.computeLegendItems();
        }
        return;
      }
      this.hoveredPrice = time && values[0] != null ? values[0] : null;
      this.hoveredTime = time || null;
    },
    // Fires when LightweightChart reports the user has panned within a
    // few bars of the earliest loaded point. Fetches one more chunk
    // further back (sized to the active period tab) and hands it to the
    // chart directly via prependSeriesData(), rather than going through
    // the `series` prop - that path always does a full rebuild + re-fit,
    // which would yank the view back to "fit everything" on every page of
    // history instead of leaving the user exactly where they were panning.
    async onLoadEarlier() {
      if (this.loadingEarlier || this.multiple || !this.earliestLoadedDate) return;
      if (this.earliestLoadedDate <= EARLIEST_FETCHABLE) return;

      this.loadingEarlier = true;
      try {
        const spanDays = PERIOD_SPAN_DAYS[this.period] || 31;
        const end = moment.utc(this.earliestLoadedDate);
        const start = moment.max(end.clone().subtract(spanDays, 'days'), moment.utc(EARLIEST_FETCHABLE));

        const resp = await this.$store.dispatch('getStockHistoryData', {
          symbols: this.localSymbols.join(),
          interval: this.interval,
          start: start.format('YYYY-MM-DD'),
          end: end.format('YYYY-MM-DD'),
          include_info: false,
        });
        const [earlierSerie] = setQuoteSeries(resp.data);
        const [serie] = this.series;

        if (!earlierSerie || earlierSerie.data.length === 0 || !serie) {
          // Nothing further back exists (e.g. reached the ticker's
          // earliest trading day) - stop trying past this point.
          this.earliestLoadedDate = null;
          return;
        }

        const existingDates = new Set(serie.data.map(([date]) => date));
        const newPoints = earlierSerie.data.filter(([date]) => !existingDates.has(date));
        if (newPoints.length === 0) {
          this.earliestLoadedDate = null;
          return;
        }

        serie.data = [...newPoints, ...serie.data];
        const [[earliestDate]] = serie.data;
        this.earliestLoadedDate = earliestDate;

        if (this.$refs.chart) {
          this.$refs.chart.prependSeriesData([this.toLwcData(serie.data)]);
        }
      } finally {
        this.loadingEarlier = false;
      }
    },
    // apexcharts-era data shape ([isoDateString, value] pairs) into
    // lightweight-charts' {time (unix seconds), value} points.
    toLwcData(pairs) {
      const bySecond = new Map();
      pairs.forEach(([isoDate, value]) => {
        if (value === null || value === undefined) return;
        const time = Math.floor(new Date(isoDate).getTime() / 1000);
        bySecond.set(time, value);
      });
      return [...bySecond.entries()]
        .sort((a, b) => a[0] - b[0])
        .map(([time, value]) => ({ time, value }));
    },
    async getQuoteHistory() {
      const resp = await this.$store.dispatch('getStockHistoryData', {
        symbols: this.localSymbols.join(),
        interval: this.interval,
        period: this.period,
        include_info: false,
      });
      this.series = setQuoteSeries(resp.data);
      this.$store.commit('setLoading', false);
    },
    async delayedCompare() {
      await this.compare();
    },
  },
  watch: {
    localSymbols() {
      this.onTabChange('1d');
    },
    symbols(val) {
      const unchanged = val.length === this.localSymbols.length
        && val.every((symbol, i) => symbol === this.localSymbols[i]);
      if (!unchanged) {
        this.localSymbols = [...val];
      }
    },
  },
};
</script>

<style scoped>
.compare {
  padding: 24px 28px 12px;
}
@media (max-width: 480px) {
  .compare {
    padding: 18px 14px 10px;
  }
}
.compare--single {
  max-width: 820px;
  margin: 0 auto;
}
.compare-heading {
  margin-top: 0;
}
.compare-input-label {
  margin: 0 0 8px;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.6);
}
.compare-input {
  margin-bottom: 8px;
}
.compare-price-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 16px;
}
.compare-price-row {
  display: flex;
  align-items: baseline;
  gap: 12px;
}
.compare-price {
  font-size: 28px;
  font-weight: 700;
  color: #0a2f31;
}
.compare-change {
  font-size: 15px;
  font-weight: 600;
}
.compare-hovered-date {
  font-size: 13px;
  color: rgba(0, 0, 0, 0.5);
}
.compare-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 20px;
  margin-bottom: 16px;
}
.compare-legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
}
.compare-legend-swatch {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.compare-legend-name {
  font-weight: 600;
  color: rgba(0, 0, 0, 0.75);
}
.compare-legend-value {
  font-size: 12px;
}
.compare-toolbar {
  margin-bottom: 16px;
}
.chart {
  margin: 0 auto;
  width: 100%;
  height: 100%;
  max-width: 800px;
}
</style>
