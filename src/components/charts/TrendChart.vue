<template>
  <div>
    <div class="futures noselect">
      <div class="md-content" v-for="(value, index) in trendData" :key="index">
        <Area :height="100" :series="[value.serie]" :options="value.options" />
      </div>
    </div>
  </div>
</template>

<script>
import { setQuoteSeries, setYAxis } from '../../utils';
import Area from './Area.vue';
import { QUOTE_OPTIONS } from '../../consts';

export default {
  name: 'TrendChart',
  components: {
    Area,
  },
  data() {
    return {
      symbols: ['^gspc', '^dji', '^ixic', '^rut', 'cl=f', 'gc=f', 'si=f'], // most popular market indexes
      trendData: [],
      interval: '5m',
      period: '1d',
      options: QUOTE_OPTIONS,
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
      const series = setQuoteSeries(resp.data);
      this.setTrendData(series);
      this.$store.commit('setLoading', false);
    },
    setTrendData(series) {
      for (let i = 0; i < series.length; i += 1) {
        const symbol = this.nameFromSymbol(series[i].name);
        const latestPrice = series[i].data[Object.keys(series[i].data).length - 1][1];
        /* eslint-disable-next-line no-param-reassign */
        series[i].name = symbol;
        const chartData = {
          label: symbol,
          price: `$${latestPrice.toString()}`, // last value is the newest
          serie: series[i],
          options: this.setOptions(series[i], symbol, latestPrice),
        };
        this.trendData.push(chartData);
      }
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
    setOptions(serie, symbol, price) {
      const positiveTrend = serie.data[0][1] < serie.data[Object.keys(serie.data).length - 1][1];
      const yAxis = setYAxis(serie);
      return {
        ...this.options,
        ...{
          stroke: {
            curve: 'straight',
            width: 1,
          },
          xaxis: {
            type: 'datetime',
            floating: true,
            axisTicks: {
              show: false,
            },
            axisBorder: {
              show: false,
            },
            labels: {
              show: false,
            },
          },
          yaxis: yAxis,
          legend: {
            show: false,
          },
          tooltip: {
            x: {
              show: false,
            },
            y: {
              formatter: function f(val) {
                return +val.toFixed(2);
              },
            },
          },
          grid: {
            show: false,
            padding: {
              left: 0,
              right: 0,
              top: 0,
              bottom: 0,
            },
          },
          colors: positiveTrend ? ['rgba(29, 191, 172, 0.4)'] : ['rgba(191, 29, 99, 0.5)'],
          subtitle: {
            text: `${symbol} - $${price}`,
          },
          chart: {
            height: '100%',
            animations: {
              enabled: false,
            },
            toolbar: {
              maxHeight: 0,
              show: false,
            },
          },
        },
      };
    },
  },
};
</script>

<style scoped>
.futures {
  display: flex;
  overflow-x: auto;
  overflow-y: hidden;
  justify-content: flex-start;
  align-items: center;
}

.md-content {
  width: 200px;
  height: 100px;
  max-height: 150px;
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

</style>
