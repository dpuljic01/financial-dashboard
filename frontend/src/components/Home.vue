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
          <md-list-item>
            <md-icon>dashboard</md-icon>
            <span class="md-list-item-text">Dashboard</span>
          </md-list-item>

          <md-list-item>
            <md-icon>pie_chart</md-icon>
            <span class="md-list-item-text">Portfolio</span>
          </md-list-item>

          <md-list-item>
            <md-icon>notifications_none</md-icon>
            <span class="md-list-item-text">Notifications</span>
          </md-list-item>

          <md-menu md-size="small" :md-offset-x="200" :md-offset-y="-120">
            <md-list-item md-menu-trigger>
              <md-icon>person_outline</md-icon>
              <span class="md-list-item-text">Profile</span>
              <md-icon>keyboard_arrow_right</md-icon>
            </md-list-item>
            <md-menu-content>
              <md-menu-item>
                <md-icon>settings</md-icon>
                <span flex>Settings</span>
              </md-menu-item>
              <md-menu-item>
                <md-icon>lock</md-icon>
                <span flex>Logout</span>
              </md-menu-item>
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
import noPortfolio from './NoPortfolio.vue';

export default {
  name: 'home',
  components: {
    noPortfolio,
  },
  data: () => ({
    menuVisible: false,
  }),
  methods: {
    toggleMenu() {
      this.menuVisible = !this.menuVisible;
    },
  },
};
</script>

<style scoped>
.md-drawer {
  max-width: 250px;
}
</style>
