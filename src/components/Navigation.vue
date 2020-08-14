<template>
  <div>
    <md-app>
      <md-app-toolbar class="md-primary">
        <md-button class="md-icon-button" @click="toggleMenu" v-if="!menuVisible">
          <md-icon>menu</md-icon>
        </md-button>
        <span class="md-title">{{ title }}</span>
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
          <md-list-item to="dashboard" @click="toggleMenu">
            <md-icon>dashboard</md-icon>
            <span class="md-list-item-text">Dashboard</span>
          </md-list-item>

          <md-list-item to="portfolios" @click="toggleMenu">
            <md-icon>pie_chart</md-icon>
            <span class="md-list-item-text">Portfolios</span>
          </md-list-item>

          <md-list-item to="notifications" @click="toggleMenu">
            <md-icon>notifications_none</md-icon>
            <span class="md-list-item-text">Notifications</span>
          </md-list-item>

          <md-menu :md-offset-x="200" :md-offset-y="-110">
            <md-list-item @click="toggleSubmenu" md-menu-trigger>
              <md-icon>person_outline</md-icon>
              <span class="md-list-item-text">Profile</span>
              <md-icon>keyboard_arrow_right</md-icon>
            </md-list-item>
            <md-menu-content>
              <md-menu-item to="settings" @click="toggleMenu">
                Settings
              </md-menu-item>
              <md-menu-item @click="logout">
                Logout
              </md-menu-item>
            </md-menu-content>
          </md-menu>
        </md-list>
      </md-app-drawer>
      <md-app-content>
        <progress-bar class="progress-bar" v-if="this.$store.getters.isLoading"></progress-bar>
        <router-view></router-view>
      </md-app-content>
    </md-app>
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
  methods: {
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
    },
  },
};
</script>

<style scoped>
.md-drawer {
  max-width: 250px;
}
</style>
