<template>
  <div class="centered-container">
    <div class="auth-card">
      <router-link to="/landing" class="auth-brand">
        <md-icon>insights</md-icon>
        <span>Financial Dashboard</span>
      </router-link>

      <h1 class="auth-title">Set a new password</h1>
      <p class="auth-subtitle">Choose a password with at least 8 characters.</p>

      <form novalidate @submit.prevent="onSubmit">
        <label class="field-label" for="password">New password</label>
        <div class="field-with-action">
          <input
            id="password"
            class="field-input"
            :type="showPassword ? 'text' : 'password'"
            v-model="password"
            autofocus
            autocomplete="new-password"
          />
          <button type="button" class="field-toggle" @click="showPassword = !showPassword">
            <md-icon>{{ showPassword ? 'visibility_off' : 'visibility' }}</md-icon>
          </button>
        </div>
        <p class="dp-error" v-if="touched && msg">{{ msg }}</p>

        <md-button class="md-raised md-primary auth-submit" type="submit">Confirm</md-button>
      </form>

      <div class="loading-overlay" v-if="this.$store.getters.isLoading">
        <md-progress-spinner md-mode="indeterminate" :md-stroke="1"></md-progress-spinner>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResetPassword',
  created() {
    this.passwordToken = this.$route.params.passwordToken;
  },
  data() {
    return {
      password: '',
      touched: false,
      showPassword: false,
      msg: 'Must be at least 8 characters long',
    };
  },
  watch: {
    password(value) {
      this.password = value;
      this.touched = true;
      this.validPassword(value);
    },
  },
  methods: {
    validPassword(value) {
      if (value.length < 8) {
        this.msg = 'Must be at least 8 characters long';
      } else {
        this.msg = '';
      }
    },
    async reset() {
      // callout to login user
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('setPassword', { token: this.passwordToken, password: this.password });
      this.$router.push('/login');
      this.$store.commit('setLoading', false);
    },
    onSubmit() {
      if (this.msg === '') {
        this.reset();
      }
    },
  },
};
</script>

<style lang="scss" src="../assets/auth.scss" scoped></style>
