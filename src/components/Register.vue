<template>
  <div class="centered-container">
    <div class="auth-card">
      <router-link to="/landing" class="auth-brand">
        <md-icon>insights</md-icon>
        <span>Financial Dashboard</span>
      </router-link>

      <h1 class="auth-title">Create your account</h1>
      <p class="auth-subtitle">Takes less than a minute — no credit card required.</p>

      <form novalidate @submit.prevent="onSubmit">
        <label class="field-label" for="firstName">First name</label>
        <input id="firstName" class="field-input" type="text" v-model="firstName" autofocus />
        <p class="dp-error" v-if="msg.firstName">Must have at least two characters</p>

        <label class="field-label" for="lastName">Last name</label>
        <input id="lastName" class="field-input" type="text" v-model="lastName" />
        <p class="dp-error" v-if="msg.lastName">Must have at least two characters</p>

        <label class="field-label" for="email">Email</label>
        <input id="email" class="field-input" type="email" v-model="email" autocomplete="off" />
        <p class="dp-error" v-if="msg.email">Invalid email address</p>

        <md-button
          class="md-raised md-primary auth-submit"
          type="submit"
          :disabled="this.$store.getters.isLoading"
        >
          Create account
        </md-button>

        <p class="auth-footer">
          Already have an account?
          <router-link to="/login">Log in</router-link>
        </p>
      </form>

      <div class="loading-overlay" v-if="this.$store.getters.isLoading">
        <FinancialLoader />
      </div>
    </div>
  </div>
</template>

<script>
import { isValidEmail } from '../utils';
import FinancialLoader from './FinancialLoader.vue';

export default {
  name: 'Register',
  components: {
    FinancialLoader,
  },
  data() {
    return {
      email: '',
      firstName: '',
      lastName: '',
      msg: {
        firstName: false,
        lastName: false,
        email: false,
      },
    };
  },
  watch: {
    email: {
      handler: function email(value) {
        // binding this to the data value in the email input
        this.email = value;
        this.msg.email = !isValidEmail(value);
      },
    },
    firstName: {
      handler: function firstName(value) {
        this.firstName = value;
        this.msg.firstName = !this.validName(value);
      },
    },
    lastName: {
      handler: function lastName(value) {
        this.lastName = value;
        this.msg.lastName = !this.validName(value);
      },
    },
  },
  methods: {
    validName(value) {
      return value.length > 1;
    },
    async save() {
      // callout to login user
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('register', {
        first_name: this.firstName,
        last_name: this.lastName,
        email: this.email,
      });
      this.$store.commit('setLoading', false);
    },
    onSubmit() {
      const valid = !this.msg.email && !this.msg.firstName && !this.msg.lastName;

      if (valid) {
        if (this.firstName === '' && this.lastName === '' && this.email === '') {
          this.msg.firstName = true;
          this.msg.lastName = true;
          this.msg.email = true;
        } else {
          this.save();
        }
      }
    },
  },
};
</script>

<style lang="scss" src="../assets/auth.scss" scoped></style>
