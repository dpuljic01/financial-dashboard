<template>
  <div class="page-container">
    <div class="page-section card-surface profile-header">
      <div class="profile-avatar-wrap">
        <img v-if="user.avatar" :src="user.avatar" alt="" class="profile-avatar profile-avatar-img" />
        <div v-else class="profile-avatar">{{ initials }}</div>
        <button
          type="button"
          class="avatar-edit-btn"
          title="Change photo"
          :disabled="uploadingAvatar"
          @click="$refs.avatarInput.click()"
        >
          <md-icon>{{ uploadingAvatar ? 'hourglass_empty' : 'photo_camera' }}</md-icon>
        </button>
        <input
          ref="avatarInput"
          type="file"
          accept="image/*"
          class="avatar-file-input"
          @change="onAvatarSelected"
        />
      </div>
      <div class="profile-info">
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
import { resizeImageToDataUrl } from '../utils';

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
      uploadingAvatar: false,
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
    async onAvatarSelected(event) {
      const { target } = event;
      const [file] = target.files;
      target.value = ''; // allow re-selecting the same file later
      if (!file) return;
      if (!file.type.startsWith('image/')) {
        this.$store.dispatch('errorMessage', 'Please choose an image file');
        return;
      }
      this.uploadingAvatar = true;
      try {
        const dataUrl = await resizeImageToDataUrl(file);
        this.user = await this.$store.dispatch('updateUser', { avatar: dataUrl });
      } catch (e) {
        this.$store.dispatch('errorMessage', "Couldn't process that image");
      } finally {
        this.uploadingAvatar = false;
      }
    },
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
  gap: 24px;
  padding: 28px;
}
.profile-avatar-wrap {
  position: relative;
  flex-shrink: 0;
}
.profile-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #116468;
  color: #fff;
  font-size: 26px;
  font-weight: 700;
  letter-spacing: 0.02em;
}
.profile-avatar-img {
  object-fit: cover;
}
.avatar-edit-btn {
  position: absolute;
  right: -2px;
  bottom: -2px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid #fff;
  background: #116468;
  color: #fff;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}
.avatar-edit-btn:hover {
  background: #0a4547;
}
.avatar-edit-btn:disabled {
  cursor: default;
  opacity: 0.7;
}
.avatar-edit-btn :deep(.md-icon) {
  font-size: 16px !important;
  color: #fff !important;
}
.avatar-file-input {
  display: none;
}
.profile-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}
.profile-name {
  margin: 0;
  line-height: 1.3;
  overflow-wrap: break-word;
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
.dp-error {
  /* Global .dp-error (theme.scss) has margin-top: -15px, tuned for
     vue-material's md-field layout - wrong here since these are plain
     inputs with no floating label eating vertical space. */
  margin: 4px 0 0;
}
</style>
