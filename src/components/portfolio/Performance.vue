<template>
  <div v-if="!loaded" class="performance-loading">
    <md-progress-spinner :md-diameter="50" :md-stroke="4" md-mode="indeterminate"></md-progress-spinner>
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
    <Area :series="series" :options="chartOptions" />
  </div>
</template>

<script>
import moment from 'moment';
import Area from '../charts/Area.vue';
import { QUOTE_OPTIONS } from '../../consts';
import { formatCompactNumber } from '../../utils';

const BENCHMARK_TICKER = '^gspc';
const BENCHMARK_LABEL = 'S&P 500';

export default {
  name: 'Performance',
  components: {
    Area,
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
      chartOptions: {},
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
      this.chartOptions = this.buildChartOptions();

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
    buildChartOptions() {
      return {
        ...QUOTE_OPTIONS,
        chart: {
          animations: { enabled: false },
          toolbar: { show: false },
          zoom: { enabled: false },
        },
        stroke: {
          curve: 'smooth',
          width: [2, 1.5, 1.5],
          dashArray: [0, 4, 2],
        },
        colors: ['#0f9d70', 'rgba(0, 0, 0, 0.35)', '#00aaad'],
        fill: {
          type: ['gradient', 'solid', 'solid'],
          gradient: {
            opacityFrom: 0.35,
            opacityTo: 0,
          },
          opacity: [1, 0, 0],
        },
        legend: {
          show: true,
          position: 'top',
          horizontalAlign: 'left',
        },
        yaxis: {
          labels: {
            formatter: (val) => `$${formatCompactNumber(val)}`,
          },
        },
        tooltip: {
          shared: true,
          x: {
            formatter: (val) => moment(val).format('LL'),
          },
          y: {
            formatter: (val) => `$${(+val).toFixed(2)}`,
          },
        },
        // Raw dollar labels ("$100,000") eat too much of a narrow mobile
        // chart's width for what they add - drop them there entirely
        // rather than just compacting the format further.
        responsive: [
          {
            breakpoint: 768,
            options: {
              yaxis: { labels: { show: false } },
              legend: { position: 'bottom', horizontalAlign: 'center' },
            },
          },
        ],
      };
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
</style>
