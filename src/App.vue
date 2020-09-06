<template>
  <div id="app">
    <navigation v-if="protectedRoutes.includes(this.$route.name)" />
    <router-view v-else></router-view>
  </div>
</template>

<script>
import { PROTECTED_ROUTES } from './consts';

export default {
  data() {
    return {
      protectedRoutes: PROTECTED_ROUTES,
    };
  },
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  min-height: 100vh;
}
#app .md-app {
  min-height: 100vh;
}
.apexcharts-canvas {
  width: 100%;
  min-height: 400px;
  height: 600px;
  margin: 0 auto;
  padding: 0 !important;
  margin-left: 0 !important;
}
</style>
