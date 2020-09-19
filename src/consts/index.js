const AUTH_COOKIE_NAME = 'ath_dash';
const PUBLIC_ROUTES = ['Login', 'Register', 'Landing', 'ResetPassword'];
const PROTECTED_ROUTES = [
  'Dashboard',
  'Portfolios',
  'Profile',
  'Compare',
  'Portfolio',
  'Holdings',
  'Summary',
  'News',
  'Quote',
  'CompanyProfile',
  'CompanyNews',
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
      format: 'dd/MM',
    },
  },
  tooltip: {
    shared: true,
  },
  chart: {
    animations: {
      enabled: false,
    },
  },
  markers: {
    size: 0,
  },
};

export {
  AUTH_COOKIE_NAME,
  PUBLIC_ROUTES,
  PROTECTED_ROUTES,
  QUOTE_OPTIONS,
};
