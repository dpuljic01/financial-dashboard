<template>
  <div v-if="!loaded" class="performance-loading">
    <FinancialLoader label="Loading performance…" />
  </div>
  <md-empty-state
    v-else-if="!hasHistory"
    md-description="Add holdings with a purchase date to see performance over time."
  ></md-empty-state>
  <div v-else>
    <div class="performance-stats">
      <div class="stat">
        <span class="stat-label">Current Value</span>
        <span class="stat-value fin-figure">${{ formatNumber(currentValue) }}</span>
      </div>
      <div class="stat">
        <span class="stat-label">Cost Basis</span>
        <span class="stat-value fin-figure">${{ formatNumber(currentCostBasis) }}</span>
      </div>
      <div class="stat">
        <span class="stat-label">Total Return</span>
        <span class="stat-value fin-figure" :class="totalReturn >= 0 ? 'fin-gain' : 'fin-loss'">
          {{ totalReturn >= 0 ? '+' : '' }}${{ formatNumber(totalReturn) }} ({{ totalReturnPercent.toFixed(2) }}%)
        </span>
      </div>
      <div class="stat" v-if="showBenchmark">
        <span class="stat-label">vs S&amp;P 500</span>
        <span class="stat-value fin-figure" :class="vsBenchmark >= 0 ? 'fin-gain' : 'fin-loss'">
          {{ vsBenchmark >= 0 ? '+' : '' }}{{ vsBenchmark.toFixed(2) }} pts
        </span>
      </div>
    </div>

    <div class="performance-legend">
      <div class="performance-legend-item">
        <span class="performance-legend-swatch performance-legend-swatch--solid"></span>
        <span>Portfolio Value</span>
      </div>
      <div class="performance-legend-item">
        <span class="performance-legend-swatch performance-legend-swatch--dashed"></span>
        <span>Cost Basis</span>
      </div>
      <div v-if="showBenchmark" class="performance-legend-item">
        <span class="performance-legend-swatch performance-legend-swatch--dotted"></span>
        <span>S&amp;P 500 (same contributions)</span>
      </div>
    </div>

    <LightweightChart :series="lwcSeries" :height="320" :hide-price-scale-below="500" />
  </div>
</template>

<script>
import moment from 'moment';
import LightweightChart from '../charts/LightweightChart.vue';
import FinancialLoader from '../FinancialLoader.vue';
import { formatCompactNumber } from '../../utils';

const BENCHMARK_TICKER = '^gspc';
const BENCHMARK_LABEL = 'S&P 500';

export default {
  name: 'Performance',
  components: {
    LightweightChart,
    FinancialLoader,
  },
  props: {
    portfolio: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loaded: false,
      hasHistory: false,
      series: [],
      currentValue: 0,
      currentCostBasis: 0,
      totalReturn: 0,
      totalReturnPercent: 0,
      showBenchmark: false,
      benchmarkReturnPercent: 0,
    };
  },
  computed: {
    vsBenchmark() {
      return this.totalReturnPercent - this.benchmarkReturnPercent;
    },
    lwcSeries() {
      if (this.series.length === 0) return [];
      const priceFormat = { type: 'custom', formatter: (price) => `$${formatCompactNumber(price)}` };
      const specs = [
        {
          type: 'area',
          data: this.toLwcPoints(this.series[0].data),
          color: '#0f9d70',
          lineWidth: 2,
          topColor: 'rgba(15, 157, 112, 0.3)',
          bottomColor: 'rgba(15, 157, 112, 0)',
          priceFormat,
        },
        {
          type: 'line',
          data: this.toLwcPoints(this.series[1].data),
          color: 'rgba(0, 0, 0, 0.35)',
          lineWidth: 1.5,
          lineStyle: 2, // dashed
          priceFormat,
        },
      ];
      if (this.series[2]) {
        specs.push({
          type: 'line',
          data: this.toLwcPoints(this.series[2].data),
          color: '#00aaad',
          lineWidth: 1.5,
          lineStyle: 1, // dotted
          priceFormat,
        });
      }
      return specs;
    },
  },
  async mounted() {
    await this.loadPerformance();
  },
  methods: {
    async loadPerformance() {
      this.loaded = false;
      const { holdings, stocks } = this.portfolio;

      const normalizedHoldings = this.normalizeHoldings(holdings, stocks);
      if (normalizedHoldings.length === 0) {
        this.hasHistory = false;
        this.loaded = true;
        return;
      }

      const tickers = [...new Set(normalizedHoldings.map((h) => h.ticker))];
      const startDate = normalizedHoldings[0].purchasedAt;
      const endDate = moment().format('YYYY-MM-DD');

      const resp = await this.$store.dispatch('getStockHistoryData', {
        symbols: [...tickers, BENCHMARK_TICKER].join(),
        interval: '1d',
        period: 'max',
        start: startDate,
        end: endDate,
        include_info: false,
      });

      const closesByTicker = this.extractCloses(resp.data, tickers);
      const benchmarkCloses = this.extractCloses(resp.data, [BENCHMARK_TICKER])[BENCHMARK_TICKER];
      const timeline = this.buildTimeline({ ...closesByTicker, [BENCHMARK_TICKER]: benchmarkCloses });

      if (timeline.length === 0) {
        this.hasHistory = false;
        this.loaded = true;
        return;
      }

      const {
        valueSeries, costSeries, benchmarkSeries,
      } = this.calcSeries(timeline, closesByTicker, normalizedHoldings, benchmarkCloses);

      this.series = [
        { name: 'Portfolio Value', data: valueSeries },
        { name: 'Cost Basis', data: costSeries },
      ];
      if (benchmarkSeries) {
        this.series.push({ name: `${BENCHMARK_LABEL} (same contributions)`, data: benchmarkSeries });
      }

      const lastValue = valueSeries[valueSeries.length - 1];
      const lastCost = costSeries[costSeries.length - 1];
      this.currentValue = lastValue ? lastValue[1] : 0;
      this.currentCostBasis = lastCost ? lastCost[1] : 0;
      this.totalReturn = this.currentValue - this.currentCostBasis;
      this.totalReturnPercent = this.currentCostBasis
        ? (this.totalReturn / this.currentCostBasis) * 100
        : 0;

      this.showBenchmark = !!benchmarkSeries;
      if (benchmarkSeries) {
        const lastBenchmark = benchmarkSeries[benchmarkSeries.length - 1];
        const currentBenchmarkValue = lastBenchmark ? lastBenchmark[1] : 0;
        this.benchmarkReturnPercent = this.currentCostBasis
          ? ((currentBenchmarkValue - this.currentCostBasis) / this.currentCostBasis) * 100
          : 0;
      }

      this.hasHistory = true;
      this.loaded = true;
    },
    normalizeHoldings(holdings, stocks) {
      if (!holdings || holdings.length === 0 || !stocks) return [];
      const tickerByStockId = {};
      stocks.forEach((stock) => {
        tickerByStockId[stock.id] = stock.ticker;
      });
      return holdings
        .filter((h) => tickerByStockId[h.stock_id])
        .map((h) => ({
          ...h,
          ticker: tickerByStockId[h.stock_id],
          purchasedAt: moment(h.purchased_at).format('YYYY-MM-DD'),
        }))
        .sort((a, b) => (a.purchasedAt < b.purchasedAt ? -1 : 1));
    },
    extractCloses(data, tickers) {
      const closesByTicker = {};
      tickers.forEach((ticker) => {
        const tickerData = data[ticker];
        closesByTicker[ticker] = {};
        if (tickerData && tickerData.Close) {
          Object.entries(tickerData.Close).forEach(([isoDate, close]) => {
            if (close !== null && close !== undefined) {
              closesByTicker[ticker][isoDate.slice(0, 10)] = close;
            }
          });
        }
      });
      return closesByTicker;
    },
    buildTimeline(closesByTicker) {
      const dateSet = new Set();
      Object.values(closesByTicker).forEach((closes) => {
        Object.keys(closes).forEach((date) => dateSet.add(date));
      });
      return [...dateSet].sort();
    },
    calcSeries(timeline, closesByTicker, normalizedHoldings, benchmarkCloses) {
      const tickers = Object.keys(closesByTicker);
      const lastKnownPrice = {};
      const valueSeries = [];
      const costSeries = [];
      const benchmarkSeries = [];

      const hasBenchmark = !!benchmarkCloses && Object.keys(benchmarkCloses).length > 0;
      const benchmarkPriceByDate = hasBenchmark ? this.forwardFill(timeline, benchmarkCloses) : {};

      // Each holding's cost basis converted into "shares" of the benchmark
      // bought on that holding's own purchase date - so a holding added
      // later isn't unfairly compared against the benchmark's price from
      // the portfolio's very first day.
      const holdings = hasBenchmark
        ? normalizedHoldings.map((holding) => ({
          ...holding,
          benchmarkShares: (holding.shares * holding.price)
            / this.priceOnOrBefore(timeline, benchmarkPriceByDate, holding.purchasedAt),
        }))
        : normalizedHoldings;

      timeline.forEach((date) => {
        tickers.forEach((ticker) => {
          if (closesByTicker[ticker][date] !== undefined) {
            lastKnownPrice[ticker] = closesByTicker[ticker][date];
          }
        });

        let value = 0;
        let cost = 0;
        let benchmarkValue = 0;
        holdings.forEach((holding) => {
          if (holding.purchasedAt > date) return;
          const price = lastKnownPrice[holding.ticker];
          if (price !== undefined) {
            value += holding.shares * price;
          }
          cost += holding.shares * holding.price;
          if (hasBenchmark && benchmarkPriceByDate[date] !== undefined) {
            benchmarkValue += holding.benchmarkShares * benchmarkPriceByDate[date];
          }
        });

        const timestamp = moment(date).valueOf();
        valueSeries.push([timestamp, +value.toFixed(2)]);
        costSeries.push([timestamp, +cost.toFixed(2)]);
        if (hasBenchmark) {
          benchmarkSeries.push([timestamp, +benchmarkValue.toFixed(2)]);
        }
      });

      return { valueSeries, costSeries, benchmarkSeries: hasBenchmark ? benchmarkSeries : null };
    },
    forwardFill(timeline, closes) {
      const filled = {};
      let last;
      timeline.forEach((date) => {
        if (closes[date] !== undefined) last = closes[date];
        if (last !== undefined) filled[date] = last;
      });
      return filled;
    },
    priceOnOrBefore(timeline, filledPrices, targetDate) {
      let result;
      for (let i = 0; i < timeline.length; i += 1) {
        if (timeline[i] > targetDate) break;
        if (filledPrices[timeline[i]] !== undefined) {
          result = filledPrices[timeline[i]];
        }
      }
      return result !== undefined ? result : filledPrices[timeline[0]];
    },
    // calcSeries already produces sorted, one-point-per-day [timestampMs,
    // value] pairs, so unlike TrendChart/Compare (which parse raw ISO
    // strings that could collide or arrive unsorted) this just needs the
    // ms-to-seconds unit conversion lightweight-charts expects.
    toLwcPoints(pairs) {
      return pairs.map(([timestampMs, value]) => ({ time: Math.floor(timestampMs / 1000), value }));
    },
    formatNumber(val) {
      return (+val).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
  },
  watch: {
    portfolio() {
      this.loadPerformance();
    },
  },
};
</script>

<style scoped>
.performance-loading {
  display: flex;
  justify-content: center;
  margin-top: 50px;
}
.performance-stats {
  display: flex;
  gap: 32px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.stat {
  display: flex;
  flex-direction: column;
}
.stat-label {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.6);
}
.stat-value {
  font-size: 20px;
  font-weight: 600;
}
@media (max-width: 600px) {
  .performance-stats {
    gap: 16px 20px;
  }
  .stat-label {
    font-size: 10px;
  }
  .stat-value {
    font-size: 15px;
  }
}
.performance-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 20px;
  margin-bottom: 8px;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.7);
}
.performance-legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}
.performance-legend-swatch {
  display: inline-block;
  width: 20px;
  border-top-width: 2px;
  border-top-style: solid;
}
.performance-legend-swatch--solid {
  border-top-color: #0f9d70;
}
.performance-legend-swatch--dashed {
  border-top-color: rgba(0, 0, 0, 0.35);
  border-top-style: dashed;
}
.performance-legend-swatch--dotted {
  border-top-color: #00aaad;
  border-top-style: dotted;
  border-top-width: 3px;
}
</style>
