<template>
  <div class="centered-container dp-bg">
    <md-content class="md-elevation-3">
      <div>
        <div style="text-align: right;"><router-link to="/landing">Back to home</router-link></div>
        <div>
          <md-icon class="md-size-3x md-primary">enhanced_encryption</md-icon>
        </div>
        <h1 class="dp-primary">SET PASSWORD</h1>
      </div>

      <form novalidate @submit.prevent="onSubmit">
        <md-field md-has-password>
          <label for="password">Password</label>
          <md-input v-model="password" name="password" type="password" autofocus></md-input>
        </md-field>
        <p class="dp-error" v-if="msg">{{ msg }}</p>

        <md-button class="md-raised md-primary" @click="reset">Confirm</md-button>
      </form>

      <div class="loading-overlay" v-if="this.$store.getters.isLoading">
        <md-progress-spinner md-mode="indeterminate" :md-stroke="1"></md-progress-spinner>
      </div>
    </md-content>
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
      msg: 'Must be at least 8 characters long',
    };
  },
  watch: {
    password(value) {
      this.password = value;
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
