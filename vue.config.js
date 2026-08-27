// const IS_PRODUCTION = process.env.NODE_ENV === 'production';
const webpack = require('webpack');

module.exports = {
  outputDir: 'dist',
  assetsDir: 'static',
  // publicPath: IS_PRODUCTION ? 'https://test-vuejsflask.herokuapp.com/static' : '/',
  // For Production, replace set baseUrl to CDN
  // And set the CDN origin to `yourdomain.com/static`
  // Whitenoise will serve once to CDN which will then cache
  // and distribute
  configureWebpack: {
    resolve: {
      alias: {
        // vue-material is a Vue 2-only library (its precompiled components
        // call the Vue 2 constructor API directly). @vue/compat is Vue 3's
        // official migration build, which shims that API surface at
        // runtime. `vue$` (exact match) keeps subpath imports like
        // 'vue/dist/...' untouched, so our own Vue 3-native app code is
        // unaffected.
        vue$: require.resolve('@vue/compat'),
      },
    },
    plugins: [
      // vue-material's published dist/vue-material.esm.js also contains a
      // raw `module.exports = vue;` (a leftover externals stub from its own
      // build), expecting a global `vue` rather than requiring it.
      // ProvidePlugin injects the (now aliased, Vue 2-compatible) 'vue'
      // wherever that bare identifier is referenced. Resolved via an
      // absolute path so this doesn't accidentally pick up vue-material's
      // own nested Vue 2 copy.
      new webpack.ProvidePlugin({ vue: require.resolve('@vue/compat') }),
    ],
  },
  chainWebpack: (config) => {
    // vue-loader auto-detects the @vue/compat alias above and defaults our
    // own SFCs to Vue 2-compatible template compilation (e.g. v-model on a
    // component expands to value/input instead of Vue 3's
    // modelValue/update:modelValue). @vue/compat is only needed for
    // vue-material's precompiled runtime code, which isn't processed by
    // vue-loader at all, so force full Vue 3 semantics for everything
    // vue-loader actually compiles.
    config.module
      .rule('vue')
      .use('vue-loader')
      .tap((options) => ({
        ...options,
        compilerOptions: {
          ...(options && options.compilerOptions),
          compatConfig: { MODE: 3 },
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
