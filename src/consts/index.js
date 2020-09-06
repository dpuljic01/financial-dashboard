const AUTH_COOKIE_NAME = 'ath_dash';
const PUBLIC_ROUTES = ['Login', 'Register', 'Landing', 'ResetPassword'];
const PROTECTED_ROUTES = [
  'Dashboard',
  'Portfolios',
  'Settings',
  'Compare',
  'Portfolio',
  'Holdings',
  'Summary',
  'News',
  'Quote',
];
const QUOTE_OPTIONS = {
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth',
    width: 1.5,
  },
  xaxis: {
    tickPlacement: 'on',
    type: 'datetime',
    labels: {
      show: true,
    },
  },
  tooltip: {
    shared: true,
  },
  markers: {
    size: 0,
  },
  chart: {
    animations: {
      enabled: false,
    },
    height: 'auto',
  },
};

export {
  AUTH_COOKIE_NAME,
  PUBLIC_ROUTES,
  PROTECTED_ROUTES,
  QUOTE_OPTIONS,
};
