<template>
  <div v-if="!this.$store.state.loading">
    <h3>Market summary</h3>
    <div class="futures">
      <div class="md-content md-elevation-2" v-for="(value, index) in trendData" :key="index">
        <div class="md-layout-item md-size-30">
          {{ value.datasets[0].label.toUpperCase() }}<br />
          {{ value.datasets[0].price }}
        </div>
        <trend-line class="md-layout-item md-size-70" :chart-data="value" :options="options"></trend-line>
      </div>
    </div>
  </div>
</template>

<script>
import TrendLine from './TrendLine';

export default {
  name: 'TrendChart',
  components: {
    TrendLine,
  },
  data() {
    return {
      symbols: ['es=f', '^dji', '^ixic', '^rut', 'cl=f', 'gc=f', 'si=f'], // most popular market indexes
      trendData: [],
      interval: '5m',
      options: {
        legend: { display: false },
        tooltips: {
          callbacks: {
            title() {
              return '';
            },
            label(tooltipItem, data) {
              return data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
            },
          },
          displayColors: false,
          mode: 'index',
          intersect: false,
        },
        hover: {
          mode: 'index',
          intersect: false,
        },
        scales: {
          xAxes: [
            {
              gridLines: { display: false },
              ticks: { display: false },
            },
          ],
          yAxes: [
            {
              gridLines: { display: false },
              ticks: { display: false },
            },
          ],
        },
      },
    };
  },
  mounted() {
    this.fetchStockHistory();
  },
  methods: {
    async fetchStockHistory() {
      this.$store.state.loading = true;
      this.trendData = [];
      const resp = await this.$store.dispatch('getStockHistoryData', {
        symbols: this.symbols.join(),
        interval: this.interval,
      });
      this.$store.state.loading = false;
      const keys = Object.keys(resp.data);
      const values = Object.values(resp.data);
      for (let i = 0; i < keys.length; i += 1) {
        this.setTrendData(keys[i], values[i]);
      }
    },
    setTrendData(symbol, symbolData) {
      const keys = Object.keys(symbolData);
      const values = Object.values(symbolData);

      if (values.length < 5) {
        // TODO: find better solution to handle graphs with small dataset
        return;
      }
      const data = [];
      for (let i = 0; i < keys.length; i += 1) {
        data.push(values[i].Open);
      }
      const positiveTrend = data[0] < data[data.length - 1];
      this.trendData.push({
        labels: new Array(keys.length),
        datasets: [
          {
            label: this.nameFromSymbol(symbol),
            price: `$${data[data.length - 1].toString()}`, // last value is the newest
            borderColor: 'rgba(0, 0, 0, 0.5)',
            borderWidth: 1,
            backgroundColor: positiveTrend ? 'rgb(0,154,128)' : 'rgb(200, 60, 90)',
            pointRadius: 0,
            data,
          },
        ],
      });
    },
    nameFromSymbol(symbol) {
      const mapping = {
        'es=f': 'S&P 500',
        '^dji': 'DOW 30',
        '^ixic': 'NASDAQ',
        '^rut': 'Russell 2000',
        'cl=f': 'Crude Oil',
        'gc=f': 'Gold',
        'si=f': 'Silver',
      };
      return mapping[symbol];
    },
  },
};
</script>

<style scoped>
.futures {
  display: flex;
  overflow-x: auto;
  justify-content: flex-start;
  align-items: center;
}

.md-content {
  width: 150px;
  height: 100px;
  max-height: 100px;
  min-width: 150px;
  margin: 15px;
  padding: 5px;
  display: flex;
  font-size: 10px;
  font-weight: 600;
}

::-webkit-scrollbar {
  height: 5px;
}

/* Track */
::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  -webkit-border-radius: 10px;
  border-radius: 10px;
}

/* Handle */
::-webkit-scrollbar-thumb {
  -webkit-border-radius: 10px;
  border-radius: 10px;
  background: rgba(85, 85, 85, 0.8);
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5);
}
::-webkit-scrollbar-thumb:window-inactive {
  background: rgba(144, 144, 144, 0.4);
}
</style>
