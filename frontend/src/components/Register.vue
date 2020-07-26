<template>
  <div class="centered-container">
    <md-content class="md-elevation-3">
      <div class="title">
        <div class="md-display-1">
          <md-icon class="md-size-2x md-primary">business_center</md-icon>
          <p class="dp-primary">Register</p>
        </div>
      </div>

      <form @submit="auth" action="/register" method="post">
        <md-field>
          <label>First name</label>
          <md-input v-model="register.firstName" autofocus name="firstName"></md-input>
        </md-field>

        <md-field>
          <label>Last name</label>
          <md-input v-model="register.lastName" autofocus></md-input>
        </md-field>

        <md-field>
          <label>Email</label>
          <md-input v-model="register.email" autofocus></md-input>
        </md-field>

        <md-field md-has-password>
          <label>Password</label>
          <md-input v-model="register.password" type="password"></md-input>
        </md-field>

        <md-button class="md-raised md-primary" type="submit">Register</md-button>
        <p>
          Already have an account?
          <router-link to="login">Login</router-link>
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
  name: 'register',
  data() {
    return {
      loading: false,
      register: {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
      },
    };
  },
  methods: {
    auth() {
      // your code to register user
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
