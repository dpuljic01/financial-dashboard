<template>
  <div class="page-container">
    <div class="page-section profile-header">
      <div class="profile-avatar">{{ initials }}</div>
      <div>
        <h1 class="md-heading profile-name">{{ user.first_name }} {{ user.last_name }}</h1>
        <span class="profile-email">{{ user.email }}</span>
      </div>
    </div>

    <div class="page-section settings-grid">
      <div class="card-surface settings-card">
        <h3 class="settings-title">Name</h3>
        <form @submit.prevent="updateName">
          <label class="field-label" for="firstName">First name</label>
          <input id="firstName" class="field-input" type="text" v-model="firstName" />

          <label class="field-label" for="lastName">Last name</label>
          <input id="lastName" class="field-input" type="text" v-model="lastName" />

          <p class="dp-error" v-if="!validName">Can't be empty</p>
          <md-button class="md-raised md-primary" type="submit">Save</md-button>
        </form>
      </div>

      <div class="card-surface settings-card">
        <h3 class="settings-title">Password</h3>
        <form @submit.prevent="updatePassword">
          <label class="field-label" for="oldPass">Current password</label>
          <div class="field-with-action">
            <input
              id="oldPass"
              class="field-input"
              :type="showOld ? 'text' : 'password'"
              v-model="oldPass"
            />
            <button type="button" class="field-toggle" @click="showOld = !showOld">
              <md-icon>{{ showOld ? 'visibility_off' : 'visibility' }}</md-icon>
            </button>
          </div>

          <label class="field-label" for="newPass">New password</label>
          <div class="field-with-action">
            <input
              id="newPass"
              class="field-input"
              :type="showNew ? 'text' : 'password'"
              v-model="newPass"
              maxlength="255"
            />
            <button type="button" class="field-toggle" @click="showNew = !showNew">
              <md-icon>{{ showNew ? 'visibility_off' : 'visibility' }}</md-icon>
            </button>
          </div>
          <p class="dp-error" v-if="!validPass">Minimum 8 characters</p>
          <md-button class="md-raised md-primary" type="submit">Update password</md-button>
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
      firstName: '',
      lastName: '',
      oldPass: '',
      newPass: '',
      showOld: false,
      showNew: false,
      validName: true,
      validPass: true,
    };
  },
  computed: {
    initials() {
      const first = (this.user.first_name || '').charAt(0);
      const last = (this.user.last_name || '').charAt(0);
      return `${first}${last}`.toUpperCase() || '?';
    },
  },
  async mounted() {
    if (Object.keys(this.user).length === 0) {
      this.user = await this.$store.dispatch('getCurrentUser');
    }
    this.firstName = this.user.first_name;
    this.lastName = this.user.last_name;
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
  },
};
</script>

<style scoped>
.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
}
.profile-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #116468;
  color: #fff;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 0.02em;
}
.profile-name {
  margin: 0;
}
.profile-email {
  color: rgba(0, 0, 0, 0.55);
  font-size: 14px;
}
.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  align-items: start;
}
.settings-card {
  padding: 24px;
}
.settings-title {
  margin: 0 0 18px;
  font-size: 16px;
  font-weight: 600;
}
.field-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: rgba(0, 0, 0, 0.5);
  margin: 16px 0 6px;
}
.field-label:first-of-type {
  margin-top: 0;
}
.field-input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 14px;
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
  color: inherit;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.field-input:focus {
  outline: none;
  border-color: #116468;
  box-shadow: 0 0 0 3px rgba(17, 100, 104, 0.12);
}
.field-with-action {
  position: relative;
}
.field-with-action .field-input {
  padding-right: 40px;
}
.field-toggle {
  position: absolute;
  right: 4px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  background: none;
  border: none;
  padding: 6px;
  cursor: pointer;
  color: rgba(0, 0, 0, 0.4);
}
.field-toggle:hover {
  color: #116468;
}
.field-toggle :deep(.md-icon) {
  font-size: 20px !important;
}
form .md-button {
  margin-top: 20px;
}
</style>
