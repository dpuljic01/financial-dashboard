<template>
  <div>
    <div class="futures noselect">
      <a
        class="charts"
        v-for="(value, index) in trendData"
        :key="index"
        :href="`/quote/${value.name}`"
        style="text-decoration: none;"
      >
        <div style="margin: 0;padding: 0; height: 0;text-align:left;">
          <span class="md-subheading">{{ value.label }}</span
          ><br />
          <strong>{{ value.price }}</strong>
          <span :style="`color:${value.color}`"> ({{ value.change }}%)</span>
        </div>
        <Area :series="[value.serie]" :options="value.options" />
      </a>
    </div>
  </div>
</template>

<script>
import { setQuoteSeries, setYAxis, percentChange } from '../../utils';
import Area from './Area.vue';
import { QUOTE_OPTIONS } from '../../consts';

export default {
  name: 'TrendChart',
  components: {
    Area,
  },
  data() {
    return {
      symbols: ['EURUSD=X', '^gspc', '^dji', '^ixic', '^rut', 'cl=f', 'gc=f', 'si=f', '^vix'], // most popular indexes
      trendData: [],
      interval: '1m',
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
        const serieLength = Object.keys(series[i].data).length;
        const symbol = this.nameFromSymbol(series[i].name);
        const latestPrice = series[i].data[serieLength - 1][1];
        const { openPrice } = series[i];
        const positiveTrend = openPrice < latestPrice;
        const changePercent = percentChange(openPrice, latestPrice);
        const { name } = series[i];
        /* eslint-disable-next-line no-param-reassign */
        series[i].name = symbol;
        const chartData = {
          name,
          label: symbol,
          price: `$${latestPrice.toString()}`, // last value is the newest
          color: positiveTrend ? 'green' : 'red',
          change: changePercent ? changePercent.toFixed(2) : 'NA',
          serie: series[i],
          options: this.setOptions(series[i]),
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
        'EURUSD=X': 'EUR/USD',
        '^vix': 'Vix',
      };
      return mapping[symbol];
    },
    setOptions(serie) {
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
              format: 'HH:MM',
            },
          },
          yaxis: yAxis,
          legend: {
            show: false,
          },
          tooltip: {
            x: {
              show: false,
              formatter: function f(val) {
                const formattedDate = new Date(val);
                return `${formattedDate.getHours()}:${formattedDate.getMinutes()}`;
              },
            },
            y: {
              show: false,
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
          colors: positiveTrend ? ['rgba(29, 191, 172)'] : ['rgba(191, 29, 99)'],
          chart: {
            zoom: {
              enabled: false,
            },
            selection: {
              enabled: false,
            },
            width: '100%',
            height: 300,
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
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}
a {
  text-decoration: none;
}
.charts {
  width: 200px;
  min-width: 200px;
  max-width: 200px;
  height: 160px;
  min-height: 150px;
  padding: 5px;
  display: inline-block;
  font-size: 10px;
  font-weight: 400;
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
