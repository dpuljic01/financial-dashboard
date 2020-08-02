<template>
  <div class="centered-container dp-bg">
    <md-content class="md-elevation-3">
      <div>
        <router-link to="/landing" style="text-decoration: none">
          <md-icon class="md-size-3x md-primary">enhanced_encryption</md-icon>
        </router-link>
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

      <div class="loading-overlay" v-if="loading">
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
      loading: false,
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
    reset() {
      // callout to login user
      this.loading = true;
      this.$store
        .dispatch('changePassword', { token: this.passwordToken, password: this.password })
        .then(() => {
          this.loading = false;
          this.$router.push('/login');
        })
        .catch(() => {
          this.loading = false;
        });
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
