<template>
  <div class="centered-container">
    <div class="auth-card">
      <router-link to="/landing" class="auth-brand">
        <md-icon>insights</md-icon>
        <span>Financial Dashboard</span>
      </router-link>

      <h1 class="auth-title">Welcome back</h1>
      <p class="auth-subtitle">Log in to see what your portfolio's doing.</p>

      <form novalidate @submit.prevent="onSubmit">
        <label class="field-label" for="email">Email</label>
        <input id="email" class="field-input" type="email" v-model="email" autofocus autocomplete="email" />
        <p class="dp-error" v-if="msg.email">Invalid email address.</p>

        <label class="field-label" for="password">Password</label>
        <div class="field-with-action">
          <input
            id="password"
            class="field-input"
            :type="showPassword ? 'text' : 'password'"
            v-model="password"
            autocomplete="current-password"
          />
          <button type="button" class="field-toggle" @click="showPassword = !showPassword">
            <md-icon>{{ showPassword ? 'visibility_off' : 'visibility' }}</md-icon>
          </button>
        </div>
        <p class="dp-error" v-if="msg.password">Must be at least 8 characters long</p>

        <div class="auth-row">
          <label class="auth-checkbox">
            <input type="checkbox" v-model="remember" />
            <span>Remember me</span>
          </label>
          <a class="auth-link" @click="showDialog = true">Forgot password?</a>
        </div>

        <md-button class="md-raised md-primary auth-submit" type="submit">Log in</md-button>

        <p class="auth-footer">
          Don't have an account?
          <router-link to="/register">Create one</router-link>
        </p>
      </form>

      <Modal v-model="showDialog">
        <h3 class="modal-title dp-primary">What's your email address?</h3>
        <p>
          We will email you a link to reset your password.
        </p>
        <form @submit.prevent="onModalSubmit">
          <label class="field-label" for="resetEmail">Email</label>
          <input id="resetEmail" class="field-input" type="email" v-model="resetEmail" autofocus />
          <p class="dp-error" v-if="msg.resetEmail">Invalid email address</p>
          <div class="modal-actions">
            <md-button class="md-raised" @click="showDialog = false">Cancel</md-button>
            <md-button class="md-raised md-primary" type="submit">Send</md-button>
          </div>
        </form>
      </Modal>
      <div class="loading-overlay" v-if="this.$store.getters.isLoading">
        <FinancialLoader />
      </div>
    </div>
  </div>
</template>

<script>
import { isValidEmail } from '../utils';
import Modal from './Modal.vue';
import FinancialLoader from './FinancialLoader.vue';

export default {
  name: 'Login',
  components: {
    Modal,
    FinancialLoader,
  },
  data() {
    return {
      showDialog: false,
      showPassword: false,
      resetEmail: '',
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
    remember(value) {
      this.remember = value;
    },
  },
  methods: {
    validPassword(value) {
      return value.length >= 8;
    },
    async auth() {
      // callout to login user
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('login', {
        remember: this.remember,
        payload: { email: this.email, password: this.password },
      });
      if (this.$store.state.loggedIn) {
        this.$router.push('/dashboard');
      }
      this.$store.commit('setLoading', false);
    },
    async sendResetEmail() {
      this.$store.commit('setLoading', true);
      this.showDialog = false;
      await this.$store.dispatch('resetPassword', { email: this.resetEmail });
      this.$store.commit('setLoading', false);
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
