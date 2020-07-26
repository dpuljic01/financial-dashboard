<template>
  <div id="showcase" :style="{ 'background-image': 'url(' + require('../assets/bg1.jpg') + ')' }">
    <md-empty-state
      class="md-accent"
      md-icon="attach_money"
      md-label="Financial Dashboard"
      md-description="We evaluate and analyze your investment portfolio,
      and provide advice on future investments based on a risk you can take"
    >
      <router-link to="hello_world">
        <md-button class="md-primary md-raised">Create account</md-button>
      </router-link>
      <br><span flex>Already a member?</span>
      <router-link to="login">
        <md-button class="md-secondary md-raised">Log in</md-button>
      </router-link>
    </md-empty-state>
  </div>
</template>

<script>
export default {
  name: 'showcase',
};
</script>

<style scoped>
#showcase {
  background-size: cover;
  min-height: 100vh;
}
</style>
