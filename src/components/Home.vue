<template>
  <div>
    <h1>Welcome Home</h1>
  </div>
</template>

<script>
import Vue from 'vue';

export default {
  name: 'Home',
  mounted() {
    if (this.$store.state.portfolios.length === 0) {
      Vue.toasted.show("You don't have any portfolio", {
        position: 'bottom-center',
        duration: null, // forever
        icon: 'error',
        type: 'error',
        after: true,
        action: [
          {
            text: 'Close',
            onClick: (e, toast) => {
              toast.goAway(0);
            },
          },
          {
            text: 'Portfolios',
            push: {
              name: 'Portfolio',
            },
          },
        ],
      });
    }
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
