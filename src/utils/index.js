import Vue from 'vue';

export const EventBus = new Vue();

export function isValidJwt(jwt) {
  if (!jwt || jwt.split('.').length < 3) {
    return false;
  }
  const data = JSON.parse(atob(jwt.split('.')[1])); // atob decodes base64 encoded string
  const exp = new Date(data.exp * 1000); // JS deals with dates in milliseconds and in flask we had seconds
  const now = new Date();
  return now < exp;
}

export function isValidEmail(email) {
  /* eslint max-len: ["error", { "code": 200 }] */
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

export function getLastItem(path) {
  return path.substring(path.lastIndexOf('/') + 1);
}

export function formatDate(date) {
  return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
}

export function formatTime(date) {
  return `${date.getHours()}:${date.getMinutes()}`;
}

export function formatDateTime(date) {
  return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}  ${date.getHours()}:${date.getMinutes()}`;
}

export function isValidDate(d) {
  /* eslint-disable-next-line no-restricted-globals */
  return d instanceof Date && !isNaN(d);
}

// export function parseTuple(t) {
//   const newT = t
//     .replace(/'/g, '"')
//     .replace('(', '[')
//     .replace(')', ']');
//   return JSON.parse(newT);
// }

export function setQuoteSeries(data) {
  const series = [];
  const symbols = Object.keys(data);

  for (let i = 0; i < symbols.length; i += 1) {
    const symbol = symbols[i];
    const closeKeys = Object.keys(data[symbol].Close);
    const closeValues = Object.values(data[symbol].Close);

    if (closeValues.length > 0) {
      const quoteSeries = {
        name: symbol,
        data: [],
      };

      // this below fixes the problem where one line chart ends too soon
      for (let j = 0; j < closeValues.length; j += 1) {
        if (closeValues[j]) {
          quoteSeries.data.push([closeKeys[j], closeValues[j]]);
        }
      }
      series.push(quoteSeries);
    }
  }
  return series;
}

function seriesMinMax(series) {
  let minPrice = series.data[0][1];
  let maxPrice = minPrice;
  for (let j = 0; j < series.data.length; j += 1) {
    if (series.data[j][1] < minPrice) {
      [, minPrice] = series.data[j];
    }
    if (series.data[j][1] > maxPrice) {
      [, maxPrice] = series.data[j];
    }
  }
  return [minPrice, maxPrice];
}

export function setYAxis(series) {
  if (!Array.isArray(series)) {
    const [smin, smax] = seriesMinMax(series);
    const yAxis = {
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
      seriesName: series.name,
      min: smin - smax / 100,
      max: smax + smax / 100,
    };
    return yAxis;
  }
  const yAxes = [];

  for (let i = 0; i < series.length; i += 1) {
    const [smin, smax] = seriesMinMax(series[i]);
    yAxes.push({
      floating: true,
      labels: {
        show: false,
        maxWidth: 0,
      },
      tooltip: {
        shared: true,
      },
      seriesName: series[i].name,
      min: smin - smax / 10,
      max: smax + smax / 10,
    });
  }
  return yAxes;
}
