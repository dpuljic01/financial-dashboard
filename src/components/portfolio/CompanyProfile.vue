<template>
  <div>
    <md-progress-spinner
      v-if="!loaded"
      :md-diameter="50"
      :md-stroke="4"
      style="margin-top: 50px;"
      md-mode="indeterminate"
    ></md-progress-spinner>
    <md-empty-state
      v-else-if="Object.values(companyProfile).length === 0 && loaded"
      md-icon="error"
      md-label="Couldn't retrieve info about this company"
    >
    </md-empty-state>
    <div v-else>
      <h2 class="md-title">{{ companyProfile.longname }}</h2>
      <img style="margin: 20px auto;" :src="companyProfile.logo_url" />
      <div class="md-layout">
        <div class="md-layout-item">
          {{ companyProfile.longbusinesssummary }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CompanyProfile',
  props: {
    companyInfo: {
      type: Object,
    },
  },
  data() {
    return {
      loaded: false,
      companyProfile: this.companyInfo,
    };
  },
  async mounted() {
    this.companyProfile = this.companyInfo;
    this.loaded = true;
  },
  watch: {
    companyInfo(val) {
      this.companyProfile = val;
    },
  },
};
</script>

<style lang="scss" scoped>
.close-icon {
  position: absolute;
  right: 4%;
}
.md-table-head {
  text-align: center;
}
.md-table-cell {
  text-align: center;
}
</style>
