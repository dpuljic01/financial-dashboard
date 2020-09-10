<template>
  <div>
    <h1 class="md-heading">{{ this.user.first_name }} {{ this.user.last_name }}</h1>
    <span class="md-subtitle">({{ this.user.email }})</span>
    <div class="md-layout md-gutter">
      <div class="md-layout-item md-size-45 md-xsmall-size-100 md-elevation-4 md-gutter">
        <h4>Update name:</h4>
        <form @submit.prevent="updateName">
          <md-field>
            <label>First name:</label>
            <md-input v-model="firstName" type="text"></md-input>
          </md-field>
          <p class="dp-error" v-if="!validName">Can't be empty</p>

          <md-field md-clearable>
            <label>Last name:</label>
            <md-input v-model="lastName" type="text"></md-input>
          </md-field>
          <p class="dp-error" v-if="!validName">Can't be empty</p>

          <md-button class="md-raised md-primary" type="submit">Save</md-button>
        </form>
      </div>
      <div class="md-layout-item md-gutter md-elevation-4 md-size-45 md-xsmall-size-100">
        <h4 class="md-subtitle">Update password:</h4>
        <form @submit.prevent="updatePassword">
          <md-field>
            <label>Old password:</label>
            <md-input v-model="oldPass" type="password"></md-input>
          </md-field>

          <md-field>
            <label>New password:</label>
            <md-input v-model="newPass" type="password" maxlength="255"></md-input>
          </md-field>
          <p class="dp-error" v-if="!validPass">Minimum 8 characters</p>
          <md-button class="md-primary md-raised" type="submit">Update</md-button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data() {
    return {
      user: this.$store.getters.getCurrentUser,
      initial: '',
      firstName: '',
      lastName: '',
      oldPass: '',
      newPass: '',
      validName: true,
      validPass: true,
    };
  },
  async mounted() {
    if (Object.keys(this.user).length === 0) {
      this.user = await this.$store.dispatch('getCurrentUser');
      this.firstName = this.user.first_name;
      this.lastName = this.user.last_name;
    }
  },
  methods: {
    async updateName() {
      this.validName = this.firstName.length > 0 && this.lastName.length > 0;
      if (this.validName) {
        this.$store.commit('setLoading', true);
        const resp = await this.$store.dispatch('updateUser', { first_name: this.firstName, last_name: this.lastName });
        this.user = resp;
        this.$store.commit('setLoading', false);
      }
    },
    async updatePassword() {
      this.validPass = this.newPass.length > 7;
      if (this.validPass) {
        this.$store.commit('setLoading', true);
        await this.$store.dispatch('changePassword', { old: this.oldPass, new: this.newPass });
        await this.$store.dispatch('logout');
        this.$store.commit('setLoading', false);
        this.$router.push('/login');
      }
    },
  },
  watch: {
    user(val) {
      this.user = val;
    },
    firstName(val) {
      this.firstName = val;
    },
    lastName(val) {
      this.lastName = val;
    },
    oldPass(val) {
      this.oldPass = val;
    },
    newPass(val) {
      this.newPass = val;
    },
  },
};
</script>

<style scoped>
.md-layout {
  display: flex;
  justify-content: space-evenly;
  flex-direction: row;
}
.md-layout-item {
  margin-top: 30px;
}
.md-button {
  left: 0;
}
</style>
