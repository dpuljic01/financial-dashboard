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
h4 {
  text-align: left;
}
.md-heading {
  margin: 30px auto;
}
</style>
