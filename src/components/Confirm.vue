<template>
  <div id="confirm" :style="{ 'background-image': 'url(' + require('../assets/bg1.jpg') + ')' }">
    <md-empty-state
      class="md-accent"
      md-icon="attach_money"
      md-label="Please check your email to finish setting up your account"
      md-description="We evaluate and analyze your investment portfolio,
      and provide advice on future investments based on a risk you can take"
    >
      <router-link to="register">
        <md-button class="md-primary md-raised">Create account</md-button>
      </router-link>
      <br><span flex>Once you confirm your account</span>
      <router-link to="login">
        <md-button class="md-secondary md-raised">Log in</md-button>
      </router-link>
    </md-empty-state>
  </div>
</template>

<script>
export default {
  name: 'Landing',
};
</script>

<style scoped>
#landing {
  background-size: cover;
  min-height: 100vh;
}
</style>
