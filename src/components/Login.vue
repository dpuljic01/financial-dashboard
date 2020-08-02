<template>
  <div class="centered-container dp-bg">
    <md-content class="md-elevation-3">
      <div>
        <router-link to="/landing" style="text-decoration: none">
          <md-icon class="md-size-3x md-primary">person</md-icon>
        </router-link>
        <h1 class="dp-primary">LOGIN</h1>
      </div>

      <form novalidate @submit.prevent="onSubmit">
        <md-field>
          <label for="email">Email</label>
          <md-input v-model="email" autofocus name="email" id="email" type="text"></md-input>
        </md-field>
        <p class="dp-error" v-if="msg.email">Invalid email address.</p>

        <md-field md-has-password>
          <label name="password">Password</label>
          <md-input v-model="password" type="password" name="password"></md-input>
        </md-field>
        <p class="dp-error" v-if="msg.password">Must be at least 8 characters long</p>

        <div class="actions md-layout md-alignment-center-space-between">
          <md-checkbox v-model="remember" class="md-primary">Remember me</md-checkbox>
          <a class=" md-primary" @click="showDialog = true">Reset password</a>
        </div>
        <md-button class="md-raised md-primary" type="submit">Log in</md-button>
        <p>
          Don't have an account?
          <router-link to="register">Register</router-link>
        </p>
      </form>
      <md-dialog :md-active.sync="showDialog" :md-fullscreen="false">
        <md-dialog-title class="dp-primary">What's your email address?</md-dialog-title>
        <md-dialog-content>
          <p>
            We will email you a link to reset your password.
          </p>
          <form @submit.prevent="onModalSubmit">
            <md-field>
              <label for="email">Email</label>
              <md-input v-model="resetEmail" autofocus type="email" name="email"></md-input>
            </md-field>
            <p class="dp-error" v-if="msg.resetEmail">Invalid email address</p>
            <md-dialog-actions>
              <md-button class="md-raised" @click="showDialog = false">Cancel</md-button>
              <md-button class="md-raised md-primary" type="submit">Send</md-button>
            </md-dialog-actions>
          </form>
        </md-dialog-content>
      </md-dialog>
      <div class="loading-overlay" v-if="loading">
        <md-progress-spinner md-mode="indeterminate" :md-stroke="1"></md-progress-spinner>
      </div>
    </md-content>
    <div class="background" />
  </div>
</template>

<script>
import { isValidEmail } from '../utils';

export default {
  name: 'Login',
  data() {
    return {
      showDialog: false,
      resetEmail: '',
      loading: false,
      error: '',
      remember: false,
      email: '',
      password: '',
      msg: {},
    };
  },
  watch: {
    email(value) {
      // binding this to the data value in the email input
      this.email = value;
      this.msg.email = !isValidEmail(value);
    },
    password(value) {
      this.password = value;
      this.msg.password = !this.validPassword(value);
    },
    resetEmail(value) {
      this.resetEmail = value;
      this.msg.resetEmail = !isValidEmail(value);
    },
  },
  methods: {
    validPassword(value) {
      return value.length >= 8;
    },
    auth() {
      // callout to login user
      this.loading = true;
      this.$store.state.remember = true;
      this.$store
        .dispatch('login', { email: this.email, password: this.password })
        .then(() => {
          this.loading = false;
          if (this.$store.state.loggedIn) this.$router.push('/home');
        })
        .catch(() => {
          this.loading = false;
        });
    },
    sendResetEmail() {
      this.$store.dispatch('resetPassword', { email: this.resetEmail }).then(() => {
        this.showDialog = false;
      });
    },
    onModalSubmit() {
      if (!this.msg.resetEmail) {
        this.sendResetEmail();
      }
    },
    onSubmit() {
      const valid = !this.msg.email && !this.msg.password;
      if (valid) {
        this.auth();
      }
    },
  },
};
</script>

<style lang="scss" src="../assets/auth.scss" scoped></style>
