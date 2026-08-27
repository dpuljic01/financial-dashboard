<template>
  <div class="tab-bar" role="tablist">
    <button
      v-for="tab in tabs"
      :key="tab.id"
      type="button"
      role="tab"
      class="tab-bar-item"
      :class="{ 'tab-bar-item--active': tab.id === modelValue }"
      @click="select(tab)"
    >
      {{ tab.label }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'TabBar',
  props: {
    tabs: {
      // [{ id, label }]
      type: Array,
      required: true,
    },
    modelValue: {
      type: String,
      required: true,
    },
  },
  emits: ['update:modelValue', 'change'],
  methods: {
    select(tab) {
      this.$emit('update:modelValue', tab.id);
      this.$emit('change', tab.id);
    },
  },
};
</script>

<style scoped>
.tab-bar {
  display: flex;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  margin-bottom: 16px;
}

.tab-bar-item {
  background: none;
  border: none;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 500;
  text-transform: uppercase;
  color: rgba(0, 0, 0, 0.54);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  white-space: nowrap;
}

.tab-bar-item--active {
  color: #116468;
  border-bottom-color: #116468;
}
</style>
