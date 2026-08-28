<template>
  <div class="app-shell">
    <md-toolbar class="md-primary app-toolbar">
      <md-button class="md-icon-button md-dense menu-trigger" @click="toggleMenu" v-if="!menuVisible">
        <md-icon>menu</md-icon>
      </md-button>
      <span class="mobile-title">{{ title }}</span>

      <div class="toolbar-desktop">
        <router-link to="/dashboard" class="toolbar-brand">
          <md-icon>insights</md-icon>
          <span>Financial Dashboard</span>
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
          <md-button class="md-icon-button md-dense toolbar-user-trigger" md-menu-trigger>
            <md-icon>account_circle</md-icon>
          </md-button>
          <md-menu-content>
            <md-menu-item @click="goToProfile">Profile</md-menu-item>
            <md-menu-item @click="logout">Log out</md-menu-item>
          </md-menu-content>
        </md-menu>
      </div>
    </md-toolbar>

    <md-drawer v-model:md-active="menuVisible" md-swipeable>
      <md-toolbar class="md-transparent" md-elevation="0">
        <span flex>Financial Dashboard</span>
        <div class="md-toolbar-section-end">
          <md-button class="md-icon-button md-dense" @click="toggleMenu">
            <md-icon>menu_open</md-icon>
          </md-button>
        </div>
      </md-toolbar>

      <md-list>
        <md-list-item @click="goTo('/dashboard')">
          <md-icon>dashboard</md-icon>
          <span class="md-list-item-text">Dashboard</span>
        </md-list-item>

        <md-list-item @click="goTo('/portfolios')">
          <md-icon>pie_chart</md-icon>
          <span class="md-list-item-text">Portfolios</span>
        </md-list-item>

        <md-list-item @click="goTo('/compare')">
          <md-icon>multiline_chart</md-icon>
          <span class="md-list-item-text">Compare</span>
        </md-list-item>

        <md-menu :md-offset-x="200" :md-offset-y="-110">
          <md-list-item @click="toggleSubmenu" md-menu-trigger>
            <md-icon>person_outline</md-icon>
            <span class="md-list-item-text">{{ this.$store.getters.getCurrentUser.email || 'Profile' }}</span>
            <md-icon>keyboard_arrow_right</md-icon>
          </md-list-item>
          <md-menu-content>
            <md-menu-item @click="goTo('/profile')">
              Profile
            </md-menu-item>
            <md-menu-item @click="logout">
              Logout
            </md-menu-item>
          </md-menu-content>
        </md-menu>
      </md-list>
    </md-drawer>
    <div class="app-content">
      <progress-bar class="progress-bar" v-if="this.$store.getters.isLoading"></progress-bar>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import ProgressBar from './ProgressBar.vue';

export default {
  name: 'Navigation',
  components: {
    ProgressBar,
  },
  data() {
    return {
      menuVisible: false,
      submenuVisible: false,
      title: this.$route.name,
      navLinks: [
        { path: '/dashboard', label: 'Dashboard' },
        { path: '/portfolios', label: 'Portfolios' },
        { path: '/compare', label: 'Compare' },
      ],
    };
  },
  watch: {
    $route(to) {
      this.title = to.name;
    },
  },
  methods: {
    isActive(prefix) {
      return this.$route.path === prefix || this.$route.path.startsWith(`${prefix}/`);
    },
    goTo(path) {
      this.toggleMenu();
      if (this.$route.path !== path) {
        this.$router.push(path);
      }
    },
    goToProfile() {
      this.$router.push('/profile');
    },
    toggleMenu() {
      this.menuVisible = !this.menuVisible;

      if (this.title !== this.$route.name) {
        this.title = this.$route.name;
      }
    },
    toggleSubmenu() {
      this.submenuVisible = !this.submenuVisible;
    },
    async logout() {
      this.$store.commit('setLoading', true);
      this.menuVisible = false;
      await this.$store.dispatch('logout');
      this.$store.dispatch('resetState');
      this.$router.replace('/login');
      this.$store.commit('setLoading', false);
    },
  },
};
</script>

<style scoped>
.md-drawer {
  max-width: 250px;
}

.app-toolbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  display: flex;
  align-items: center;
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

.mobile-title {
  flex: 1;
}
.toolbar-desktop {
  display: none;
}

@media (min-width: 960px) {
  .menu-trigger,
  .mobile-title {
    display: none;
  }
  .toolbar-desktop {
    display: flex;
    align-items: center;
    width: 100%;
    gap: 32px;
  }
}

.toolbar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #fff;
  text-decoration: none;
  font-weight: 700;
  font-size: 15px;
  flex-shrink: 0;
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

.toolbar-nav {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
}
.toolbar-nav-link {
  /* Solid white, not alpha-blended - see .sidebar-link's old note: any
     alpha white over this teal background picks up a visible cyan cast. */
  color: #fff;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 14px;
  border-radius: 8px;
  transition: background-color 0.15s ease;
}
.toolbar-nav-link:hover {
  background: rgba(255, 255, 255, 0.08);
}
.toolbar-nav-link--active {
  background: rgba(255, 255, 255, 0.18);
  font-weight: 700;
}

.toolbar-user-trigger {
  flex-shrink: 0;
}
.toolbar-user-trigger :deep(.md-icon) {
  color: #fff !important;
  font-size: 26px !important;
}
</style>
