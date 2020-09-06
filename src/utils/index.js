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

export function parseTuple(t) {
  const newT = t
    .replace(/'/g, '"')
    .replace('(', '[')
    .replace(')', ']');
  return JSON.parse(newT);
}

export function setQuoteSeries(data) {
  const series = [];
  const symbols = Object.keys(data);

  for (let i = 0; i < symbols.length; i += 1) {
    const key = symbols[i];
    const symbol = parseTuple(key)[0];
    const field = parseTuple(key)[1];

    if (field === 'Close') {
      const values = Object.values(data[key]);
      const keys = Object.keys(data[key]);
      const quoteSeries = {
        name: symbol,
        data: keys
          .filter((e, j) => {
            if (!values[j]) {
              return false; // skip
            }
            return true;
          })
          .map((e, j) => [e, values[j]]), // fix this to be filtered right
      };
      // for (let j = 0; j < values.length; j += 1) {
      //   if (values[j].Close) {
      //     quoteSeries.data.push({ x: new Date(keys[j]).getTime(), y: values[j].Close });
      //   }
      // }
      series.push(quoteSeries);
    }
  }
  return series;
}

export function setYAxis(series) {
  const yAxes = [];

  for (let i = 0; i < series.length; i += 1) {
    let minPrice = series[i].data[0][1];
    let maxPrice = minPrice;
    for (let j = 0; j < series[i].data.length; j += 1) {
      if (series[i].data[j][1] < minPrice) {
        [, minPrice] = series[i].data[j];
      }
      if (series[i].data[j][1] > maxPrice) {
        [, maxPrice] = series[i].data[j];
      }
    }
    yAxes.push({
      labels: {
        show: false,
        maxWidth: 0,
      },
      seriesName: series[i].name,
      min: minPrice - minPrice / 10,
      max: maxPrice + maxPrice / 10,
    });
  }
  return yAxes;
}
