<template>
  <div class="loading-bar" :class="{ 'loading-bar--active': active, 'loading-bar--done': completing }"></div>
</template>

<script>
export default {
  name: 'ProgressBar',
  data() {
    return {
      active: false,
      completing: false,
      startTimer: null,
      hideTimer: null,
    };
  },
  computed: {
    isLoading() {
      return this.$store.getters.isLoading;
    },
  },
  watch: {
    isLoading: {
      immediate: true,
      handler(value) {
        clearTimeout(this.startTimer);
        clearTimeout(this.hideTimer);
        if (value) {
          // Starting from width:0 (not mid-transition) so the fill always
          // animates the same way, even if a previous load just finished.
          this.completing = false;
          this.active = false;
          this.startTimer = setTimeout(() => {
            this.active = true;
          }, 20);
        } else if (this.active) {
          // Snap to 100% and hold briefly before fading, rather than just
          // vanishing at 85% - reads as "finished", not "gave up".
          this.completing = true;
          this.hideTimer = setTimeout(() => {
            this.active = false;
            this.completing = false;
          }, 400);
        }
      },
    },
  },
  beforeUnmount() {
    clearTimeout(this.startTimer);
    clearTimeout(this.hideTimer);
  },
};
</script>

<style scoped>
.loading-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  width: 0;
  background: linear-gradient(90deg, #00aaad, #2fd8d4);
  box-shadow: 0 0 8px rgba(0, 170, 173, 0.55);
  opacity: 0;
  pointer-events: none;
  z-index: 2000;
  transition: width 6s cubic-bezier(0.1, 0.6, 0.2, 1), opacity 0.3s ease;
}
.loading-bar--active {
  width: 85%;
  opacity: 1;
}
.loading-bar--done {
  width: 100% !important;
  opacity: 0;
  transition: width 0.25s ease, opacity 0.3s ease 0.25s;
}
@media (prefers-reduced-motion: reduce) {
  .loading-bar {
    transition: opacity 0.2s ease;
  }
  .loading-bar--active {
    width: 100%;
  }
}
</style>
