<template>
  <div v-if="!this.$store.getters.isLoading">
    <div class="futures noselect">
      <div class="md-content" v-for="(value, index) in trendData" :key="index">
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
      symbols: ['^gspc', '^dji', '^ixic', '^rut', 'cl=f', 'gc=f', 'si=f'], // most popular market indexes
      trendData: [],
      interval: '5m',
      period: '1d',
      options: {
        animation: {
          duration: 0, // general animation time
        },
        responsiveAnimationDuration: 0, // animation duration after a resize
        legend: { display: false },
        tooltips: {
          callbacks: {
            title() {
              return '';
            },
            label(tooltipItem, data) {
              return data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].y;
            },
          },
          displayColors: false,
          mode: 'index',
          intersect: false,
        },
        hover: {
          animationDuration: 0, // duration of animations when hovering an item
          mode: 'index',
          intersect: false,
        },
        events: ['mousemove', 'mouseout', 'click', 'touchstart', 'touchmove', 'touchend'],
        scales: {
          xAxes: [
            {
              gridLines: { display: false },
              ticks: { display: false },
              type: 'time',
              time: {
                unit: 'minute',
                stepSize: 15,
              },
              distribution: 'series',
            },
          ],
          yAxes: [
            {
              gridLines: { display: false },
              ticks: { display: false },
            },
          ],
        },
        plugins: {
          zoom: {
            pan: {
              enabled: true,
              mode: 'x',
            },
            zoom: {
              enabled: true,
              mode: 'x',
            },
          },
        },
      },
    };
  },
  mounted() {
    this.fetchStockHistory();
  },
  methods: {
    async fetchStockHistory() {
      this.$store.commit('setLoading', true);
      this.trendData = [];
      const resp = await this.$store.dispatch('getStockHistoryData', {
        symbols: this.symbols.join(),
        interval: this.interval,
        period: this.period,
        include_info: false,
      });
      const keys = Object.keys(resp.data);
      const values = Object.values(resp.data);
      for (let i = 0; i < keys.length; i += 1) {
        this.setTrendData(keys[i], values[i]);
      }
      this.$store.commit('setLoading', false);
    },
    setTrendData(symbol, symbolData) {
      const keys = Object.keys(symbolData);
      const values = Object.values(symbolData);

      if (values.length < 4) {
        // TODO: find better solution to handle graphs with small dataset
        return;
      }
      const data = [];
      for (let i = 0; i < keys.length; i += 1) {
        const item = {
          x: new Date(keys[i]).getTime(),
          y: values[i].Open,
        };
        data.push(item);
      }
      const positiveTrend = data[0].y < data[data.length - 1].y;
      this.trendData.push({
        datasets: [
          {
            label: this.nameFromSymbol(symbol),
            price: `$${data[data.length - 1].y.toString()}`, // last value is the newest
            borderColor: positiveTrend ? 'rgb(29, 191, 172)' : 'rgb(191, 29, 99)',
            borderWidth: 1,
            backgroundColor: positiveTrend ? 'rgba(29, 191, 172, 0.4)' : 'rgba(191, 29, 99, 0.5)',
            pointRadius: 0,
            data,
          },
        ],
      });
    },
    nameFromSymbol(symbol) {
      const mapping = {
        '^gspc': 'S&P 500',
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

.refresh {
  position: absolute;
  right: 20px;
}

::-webkit-scrollbar {
  height: 5px;
}

/* Track */
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  -webkit-border-radius: 10px;
  border-radius: 10px;
}

/* Handle */
::-webkit-scrollbar-thumb {
  -webkit-border-radius: 10px;
  border-radius: 10px;
  background: rgba(85, 85, 85, 0.8);
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5);
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5);
}
::-webkit-scrollbar-thumb:window-inactive {
  background: rgba(144, 144, 144, 0.4);
}

.vertical-line {
  height: 100px;
  width: 1px;
  border: 1px solid gray;
}
</style>
