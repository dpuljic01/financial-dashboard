<template>
  <div class="app-shell">
    <md-toolbar class="md-primary app-toolbar">
      <div class="app-toolbar-inner">
        <router-link
          to="/dashboard"
          class="toolbar-brand"
          :class="{ 'toolbar-brand--active': isActive('/dashboard') }"
        >
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

        <!-- >=700px: search sits inline in the toolbar, no extra tap needed. -->
        <Search
          compact
          class="toolbar-search"
          placeholder="Search symbols"
          @search="onGlobalSearch"
        ></Search>

        <!-- <700px: there's no room for an inline box next to nav links and
             the user menu, so it collapses to an icon that drops down a
             full-width search panel instead of competing for space. -->
        <button
          type="button"
          class="toolbar-search-toggle"
          :title="mobileSearchOpen ? 'Close search' : 'Search symbols'"
          @click="toggleMobileSearch"
        >
          <md-icon>{{ mobileSearchOpen ? 'close' : 'search' }}</md-icon>
        </button>

        <md-menu class="toolbar-user-menu" :md-offset-x="0" :md-offset-y="8">
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
      </div>

      <div v-if="mobileSearchOpen" class="toolbar-search-mobile" @keydown.esc="mobileSearchOpen = false">
        <Search ref="mobileSearch" placeholder="Search symbols" @search="onGlobalSearch"></Search>
      </div>
    </md-toolbar>

    <div class="app-content">
      <progress-bar></progress-bar>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import ProgressBar from './ProgressBar.vue';
import Search from './Search.vue';

export default {
  name: 'Navigation',
  components: {
    ProgressBar,
    Search,
  },
  data() {
    return {
      // Dashboard isn't listed here - the brand/logo already links there
      // (a standard "click the logo to go home" pattern), and dropping the
      // duplicate pill is what actually buys back the room nav needs on
      // narrow screens instead of clipping.
      navLinks: [
        { path: '/portfolios', label: 'Portfolios' },
        { path: '/compare', label: 'Compare' },
      ],
      mobileSearchOpen: false,
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
    onGlobalSearch(event) {
      this.mobileSearchOpen = false;
      this.$router.push(`/quote/${event.symbol}/profile`);
    },
    toggleMobileSearch() {
      this.mobileSearchOpen = !this.mobileSearchOpen;
      if (this.mobileSearchOpen) {
        this.$nextTick(() => {
          if (this.$refs.mobileSearch) this.$refs.mobileSearch.focus();
        });
      }
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
/* Mirrors .app-content's own padding (below) at each breakpoint, applied
   outside the centered column exactly like .app-content does for
   .page-container - so the brand/nav align with the page cards underneath
   instead of the toolbar hugging the viewport edge while the content
   column floats centered further in. */
.app-toolbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  padding: 0 16px;
}
@media (min-width: 600px) {
  .app-toolbar {
    padding: 0 24px;
  }
}

/* Mirrors .page-container's max-width + centering (see App.vue). */
.app-toolbar-inner {
  position: relative;
  width: 100%;
  max-width: 1180px;
  margin: 0 auto;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 56px;
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
  padding: 6px 8px;
  margin: 0 -8px;
  border-radius: 8px;
  transition: background-color 0.15s ease;
  -webkit-tap-highlight-color: transparent;
}
/* Dashboard has no separate nav pill (see navLinks) - the brand carries its
   own active state instead, so "where am I" doesn't disappear along with
   the pill. */
.toolbar-brand--active {
  background: rgba(255, 255, 255, 0.18);
}
.toolbar-brand:hover,
.toolbar-brand:focus,
.toolbar-brand:active,
.toolbar-brand:visited {
  text-decoration: none !important;
}
.toolbar-brand:hover {
  background: rgba(255, 255, 255, 0.08);
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
  /* Only needed once the brand text itself is visible at this width - below
     it, the brand is just the icon and the 12px flex gap already reads as
     clear separation from the first nav link. With "Financial Dashboard"
     spelled out, that same 12px put it right up against "Dashboard" (the
     nav link), reading as one run-on phrase instead of two separate
     things. */
  .toolbar-nav {
    margin-left: 20px;
  }
}

.toolbar-nav {
  display: flex;
  align-items: center;
  gap: 2px;
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

.toolbar-search {
  display: none;
  flex-shrink: 0;
  /* Extra separation from the last nav link - the container's own 12px
     flex gap read as part of the nav group rather than a distinct search
     affordance next to it. */
  margin-left: 28px;
}
@media (min-width: 700px) {
  .toolbar-search {
    display: block;
  }
}

.toolbar-search-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: transparent;
  cursor: pointer;
  flex-shrink: 0;
  -webkit-tap-highlight-color: transparent;
}
.toolbar-search-toggle:hover {
  background: rgba(255, 255, 255, 0.08);
}
.toolbar-search-toggle .md-icon {
  color: #fff !important;
  font-size: 20px !important;
  margin: 0 !important;
}
@media (min-width: 700px) {
  .toolbar-search-toggle {
    display: none;
  }
}

.toolbar-search-mobile {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--surface-color, #fff);
  border-bottom: 1px solid var(--surface-border, rgba(0, 0, 0, 0.08));
  box-shadow: 0 10px 24px rgba(15, 34, 36, 0.18);
  padding: 12px 16px;
  z-index: 9;
}
@media (min-width: 700px) {
  .toolbar-search-mobile {
    display: none;
  }
}

.toolbar-user-menu {
  margin-left: auto;
  flex-shrink: 0;
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
