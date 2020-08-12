<template>
  <div>
    <md-empty-state
      v-if="!hasPortfolio"
      md-icon="post_add"
      md-label="Create your first portfolio"
      md-description="By creating a portfolio, you'll be able to add your holdings and get valuable information."
    >
      <!--<md-button class="md-primary md-raised" @click="open = true">Create portfolio</md-button>-->
      <md-button class="md-primary md-raised" @click="open = true">Create portfolio</md-button>
    </md-empty-state>
    <div v-else class="md-layout">
      <div>
        Portfolio
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Portfolio',
  data() {
    return {
      open: false,
      valid: false,
      hasPortfolio: this.$store.getters.hasPortfolio,
    };
  },
  methods: {
    async createPortfolio() {
      this.open = false;
      this.$store.state.loading = true;
      await this.$store.dispatch('submitNewPortfolio', { name: this.portfolioName, info: this.info });
      this.portfolioName = '';
      this.info = '';
    },
    submit() {
      if (this.valid) {
        this.createPortfolio();
      }
    },
    validName(value) {
      return value.length > 1;
    },
  },
};
</script>
<style scoped>
.md-icon {
  position: absolute;
  right: 4%;
}
</style>
