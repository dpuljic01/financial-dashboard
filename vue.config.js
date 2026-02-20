module.exports = {
  outputDir: 'dist',
  assetsDir: 'static',
  chainWebpack: (config) => {
    config.resolve.alias.set('vue', '@vue/compat');
    config.module
      .rule('vue')
      .use('vue-loader')
      .tap((options) => ({
        ...options,
        compilerOptions: {
          compatConfig: {
            MODE: 2,
          },
        },
      }));
  },
  devServer: {
    proxy: {
      '/api': {
        // Forward frontend dev server request for /api to flask dev server
        target: 'http://127.0.0.1:5000',
      },
    },
  },
};
