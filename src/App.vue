<template>
  <div id="app">
    <navigation v-if="this.$route.name !== 'Login' && this.$route.name !== 'Register'" />
    <router-view v-else></router-view>
  </div>
</template>

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
</style>
