// const IS_PRODUCTION = process.env.NODE_ENV === 'production';

module.exports = {
  outputDir: 'dist',
  assetsDir: 'static',
  configureWebpack: {
    resolve: {
      alias: {
        vue: '@vue/compat',
      },
    },
  },
  // publicPath: IS_PRODUCTION ? 'https://test-vuejsflask.herokuapp.com/static' : '/',
  // For Production, replace set baseUrl to CDN
  // And set the CDN origin to `yourdomain.com/static`
  // Whitenoise will serve once to CDN which will then cache
  // and distribute
  devServer: {
    proxy: {
      '/api': {
        // Forward frontend dev server request for /api to flask dev server
        target: 'http://127.0.0.1:5000',
      },
    },
  },
};
