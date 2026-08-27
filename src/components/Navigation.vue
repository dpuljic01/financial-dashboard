<template>
  <div class="app-shell">
    <md-toolbar class="md-primary app-toolbar">
      <md-button class="md-icon-button md-dense" @click="toggleMenu" v-if="!menuVisible">
        <md-icon>menu</md-icon>
      </md-button>
      <span class="md-title">{{ title }}</span>
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
    };
  },
  watch: {
    $route(to) {
      this.title = to.name;
    },
  },
  methods: {
    goTo(path) {
      this.toggleMenu();
      if (this.$route.path !== path) {
        this.$router.push(path);
      }
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
</style>
