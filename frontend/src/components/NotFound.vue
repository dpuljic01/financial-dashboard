<template>
  <div>
    <md-empty-state
      md-icon="error"
      md-label="404 - Not Found"
      md-description="Requested page could not be found."
    >
      <router-link to="home">Click here to find your way back</router-link>
    </md-empty-state>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
};
</script>
