<template>
  <div class="page-container">
    <md-app>
      <md-app-toolbar md-elevation="1" md-align="center" class="md-primary">
        <md-button class="md-icon-button" @click="toggleMenu" v-if="!menuVisible">
          <md-icon>menu</md-icon>
        </md-button>
        <span class="md-title">Dashboard</span>
      </md-app-toolbar>

      <md-app-drawer :md-active.sync="menuVisible" :width="200">
        <md-toolbar class="md-transparent" md-elevation="0">
          <span flex>Financial Dashboard</span>
          <div class="md-toolbar-section-end">
            <md-button class="md-icon-button md-dense" @click="toggleMenu">
              <md-icon>menu_open</md-icon>
            </md-button>
          </div>
        </md-toolbar>

        <md-list>
          <md-list-item to="home">
            <md-icon>dashboard</md-icon>
            <span class="md-list-item-text">Dashboard</span>
          </md-list-item>

          <md-list-item to="portfolio">
            <md-icon>pie_chart</md-icon>
            <span class="md-list-item-text">Portfolio</span>
          </md-list-item>

          <md-list-item to="notifications">
            <md-icon>notifications_none</md-icon>
            <span class="md-list-item-text">Notifications</span>
          </md-list-item>
          <md-menu md-size="small" :md-offset-x="200" :md-offset-y="-120" class="md-button">
            <md-list-item md-menu-trigger>
              <md-icon>person_outline</md-icon>
              <span class="md-list-item-text">Profile</span>
              <md-icon>keyboard_arrow_right</md-icon>
            </md-list-item>
            <md-menu-content>
              <md-list-item to="settings" class="md-alignment-center-center">
                Settings
              </md-list-item>
              <md-list-item @click="logout">
                Logout
              </md-list-item>
            </md-menu-content>
          </md-menu>
        </md-list>
      </md-app-drawer>

      <md-app-content>
        <no-portfolio></no-portfolio>
      </md-app-content>
    </md-app>
  </div>
</template>

<script>
import NoPortfolio from './NoPortfolio.vue';
import AUTH_COOKIE_NAME from '../consts';
import { removeCookie } from '../utils/cookie';

export default {
  name: 'Home',
  components: {
    NoPortfolio,
  },
  data: () => ({
    menuVisible: false,
  }),
  methods: {
    toggleMenu() {
      this.menuVisible = !this.menuVisible;
    },
    logout() {
      this.$store.dispatch('logout').then(() => {
        removeCookie(AUTH_COOKIE_NAME);
        this.$router.replace('/login');
      });
    },
  },
};
</script>

<style scoped>
.md-drawer {
  max-width: 250px;
}
.md-menu.md-button {
  height: 100%;
}
</style>
