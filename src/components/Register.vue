<template>
  <div class="centered-container dp-bg">
    <md-content class="md-elevation-3">
      <div>
        <router-link to="/landing" style="text-decoration: none">
          <md-icon class="md-size-3x md-primary">person</md-icon>
        </router-link>
        <h1 class="dp-primary">REGISTER</h1>
      </div>

      <form novalidate @submit.prevent="onSubmit">
        <md-field>
          <label for="firstName">First name</label>
          <md-input v-model="firstName" name="firstName" id="firstName" autofocus></md-input>
        </md-field>
        <p class="dp-error" v-if="msg.firstName">Must have at least two characters</p>

        <md-field>
          <label for="lastName">Last name</label>
          <md-input v-model="lastName" name="lastName" id="lastName"></md-input>
        </md-field>
        <p class="dp-error" v-if="msg.lastName">Must have at least two characters</p>

        <md-field>
          <label for="email">Email</label>
          <md-input v-model="email" name="email" id="email" autocomplete="off"></md-input>
        </md-field>
        <p class="dp-error" v-if="msg.email">Invalid email address</p>

        <md-button class="md-raised md-primary" type="submit" :disabled="loading">Submit</md-button>
        <p>
          Already have an account?
          <router-link to="login">Login</router-link>
        </p>
      </form>

      <div class="loading-overlay" v-if="this.$store.getters.isLoading">
        <md-progress-spinner md-mode="indeterminate" :md-stroke="1"></md-progress-spinner>
      </div>
    </md-content>
  </div>
</template>

<script>
import { isValidEmail } from '../utils';

export default {
  name: 'Register',
  data() {
    return {
      firstClick: true,
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
