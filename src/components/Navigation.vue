<template>
  <div class="app-shell">
    <md-toolbar class="md-primary app-toolbar">
      <router-link to="/dashboard" class="toolbar-brand">
        <md-icon>insights</md-icon>
        <span class="toolbar-brand-name">Financial Dashboard</span>
      </router-link>

      <nav class="toolbar-nav">
        <router-link
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          class="toolbar-nav-link"
          :class="{ 'toolbar-nav-link--active': isActive(link.path) }"
        >{{ link.label }}</router-link>
      </nav>

      <md-menu :md-offset-x="-150" :md-offset-y="8">
        <md-button class="toolbar-user-trigger" md-menu-trigger>
          <img v-if="userAvatar" :src="userAvatar" alt="" class="toolbar-user-avatar toolbar-user-avatar-img" />
          <span v-else class="toolbar-user-avatar">{{ userInitials }}</span>
          <span v-if="currentUserName" class="toolbar-user-name">{{ currentUserName }}</span>
          <md-icon class="toolbar-user-caret">expand_more</md-icon>
        </md-button>
        <md-menu-content class="user-menu-content">
          <md-menu-item @click="goToProfile">
            <md-icon>person</md-icon>
            <span>Profile</span>
          </md-menu-item>
          <md-menu-item class="user-menu-item--danger" @click="logout">
            <md-icon>logout</md-icon>
            <span>Log out</span>
          </md-menu-item>
        </md-menu-content>
      </md-menu>
    </md-toolbar>

    <div class="app-content">
      <progress-bar></progress-bar>
      <router-view></router-view>
    </div>
    <ConfirmDialog />
  </div>
</template>

<script>
import ProgressBar from './ProgressBar.vue';
import ConfirmDialog from './ConfirmDialog.vue';

export default {
  name: 'Navigation',
  components: {
    ProgressBar,
    ConfirmDialog,
  },
  data() {
    return {
      navLinks: [
        { path: '/dashboard', label: 'Dashboard' },
        { path: '/portfolios', label: 'Portfolios' },
        { path: '/compare', label: 'Compare' },
      ],
    };
  },
  computed: {
    userAvatar() {
      const user = this.$store.getters.getCurrentUser;
      return user ? user.avatar : null;
    },
    currentUserName() {
      const user = this.$store.getters.getCurrentUser;
      if (!user) return '';
      return user.first_name || user.email || '';
    },
    userInitials() {
      const user = this.$store.getters.getCurrentUser;
      if (!user) return '?';
      const first = (user.first_name || '').charAt(0);
      const last = (user.last_name || '').charAt(0);
      const initials = `${first}${last}`.toUpperCase();
      if (initials) return initials;
      return user.email ? user.email.charAt(0).toUpperCase() : '?';
    },
  },
  methods: {
    isActive(prefix) {
      return this.$route.path === prefix || this.$route.path.startsWith(`${prefix}/`);
    },
    goToProfile() {
      this.$router.push('/profile');
    },
    async logout() {
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('logout');
      this.$store.dispatch('resetState');
      this.$router.replace('/login');
      this.$store.commit('setLoading', false);
    },
  },
};
</script>

<style scoped>
.app-toolbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 12px;
}

.app-content {
  padding: 80px 24px 40px;
  min-height: 100vh;
  box-sizing: border-box;
}

@media (max-width: 600px) {
  .app-content {
    padding: 76px 16px 32px;
  }
}

.toolbar-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  /* !important throughout this block: vue-material's own link/button
     theming otherwise wins over a plain `color` declaration here and the
     text renders as a tinted teal instead of solid white. */
  color: #fff !important;
  text-decoration: none !important;
  font-weight: 700;
  font-size: 15px;
  flex-shrink: 0;
  -webkit-tap-highlight-color: transparent;
}
.toolbar-brand:hover,
.toolbar-brand:focus,
.toolbar-brand:active,
.toolbar-brand:visited {
  text-decoration: none !important;
}
.toolbar-brand :deep(.md-icon) {
  display: inline-flex !important;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  margin: 0 !important;
  color: #fff !important;
  font-size: 22px !important;
  line-height: 1 !important;
}
.toolbar-brand-name {
  display: none;
  color: #fff !important;
}
@media (min-width: 560px) {
  .toolbar-brand-name {
    display: inline;
  }
}

.toolbar-nav {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
  min-width: 0;
  overflow-x: auto;
  scrollbar-width: none;
}
.toolbar-nav::-webkit-scrollbar {
  display: none;
}
.toolbar-nav-link {
  color: #fff !important;
  text-decoration: none !important;
  font-size: 13px;
  font-weight: 500;
  padding: 7px 10px;
  border-radius: 8px;
  white-space: nowrap;
  flex-shrink: 0;
  transition: background-color 0.15s ease;
  -webkit-tap-highlight-color: transparent;
}
/* Mobile browsers apply a default underline to a tapped/focused link that a
   bare `text-decoration: none` on the base selector doesn't reach - cover
   every interaction state explicitly. */
.toolbar-nav-link:hover,
.toolbar-nav-link:focus,
.toolbar-nav-link:active,
.toolbar-nav-link:visited {
  text-decoration: none !important;
}
.toolbar-nav-link:hover {
  background: rgba(255, 255, 255, 0.08);
}
.toolbar-nav-link--active {
  background: rgba(255, 255, 255, 0.18);
  font-weight: 700;
}
@media (min-width: 700px) {
  .toolbar-nav-link {
    font-size: 14px;
    padding: 8px 14px;
  }
}

.toolbar-user-trigger {
  display: flex !important;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  min-width: 0 !important;
  height: auto !important;
  margin: 0 !important;
  padding: 4px 6px !important;
  border-radius: 8px !important;
  background: transparent !important;
  box-shadow: none !important;
}
.toolbar-user-trigger:hover {
  background: rgba(255, 255, 255, 0.08) !important;
}
.toolbar-user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.18);
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.02em;
}
.toolbar-user-avatar-img {
  object-fit: cover;
}
.toolbar-user-name {
  display: none;
  color: #fff !important;
  font-size: 14px;
  font-weight: 600;
  text-transform: none;
  white-space: nowrap;
}
.toolbar-user-caret {
  display: none;
  margin: 0 !important;
  color: rgba(255, 255, 255, 0.7) !important;
  font-size: 18px !important;
}
@media (min-width: 700px) {
  .toolbar-user-trigger {
    padding: 6px 10px 6px 6px !important;
  }
  .toolbar-user-name {
    display: inline;
  }
  .toolbar-user-caret {
    display: inline-flex;
  }
}
</style>
