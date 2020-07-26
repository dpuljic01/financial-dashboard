<template>
  <div class="centered-container">
    <md-content class="md-elevation-3">
      <div class="title">
        <div class="md-display-1">
          <md-icon class="md-size-2x md-primary">login</md-icon>
          <p class="dp-primary">Login</p>
        </div>
      </div>

      <form @submit="auth" action="/login" method="post">
        <md-field>
          <label>Email</label>
          <md-input v-model="login.email" autofocus></md-input>
        </md-field>

        <md-field md-has-password>
          <label>Password</label>
          <md-input v-model="login.password" type="password"></md-input>
        </md-field>

        <div class="actions md-layout md-alignment-center-space-between">
          <md-checkbox v-model="login.remember" class="md-primary">Remember me</md-checkbox>
          <router-link to="reset-password">Reset password</router-link>
        </div>
        <md-button class="md-raised md-primary" type="submit">Log in</md-button>
        <p>
            Don't have an account?
            <router-link to="register">Register</router-link>
        </p>
      </form>

      <div class="loading-overlay" v-if="loading">
        <md-progress-spinner md-mode="indeterminate" :md-stroke="1"></md-progress-spinner>
      </div>
    </md-content>
    <div class="background" />
  </div>
</template>

<script>
export default {
  name: 'login',
  data() {
    return {
      loading: false,
      login: {
        email: '',
        password: '',
        remember: false,
      },
    };
  },
  methods: {
    auth() {
      // your code to login user
      // this is only for example of loading
      this.loading = true;
      setTimeout(() => {
        this.loading = false;
      }, 2000);
    },
  },
};
</script>

<style lang="scss" src="../assets/auth.scss" scoped></style>
