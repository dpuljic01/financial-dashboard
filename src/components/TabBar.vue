<template>
  <div class="tab-bar" :class="`tab-bar--${variant}`" role="tablist">
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
  compatConfig: { MODE: 3 },
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
    // 'underline': navigational section tabs. 'pill': a compact value picker
    // (e.g. chart timeframe) - visually distinct so it doesn't read as page
    // navigation.
    variant: {
      type: String,
      default: 'underline',
      validator: (value) => ['underline', 'pill'].includes(value),
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
}

.tab-bar--underline {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  margin-bottom: 16px;
}

.tab-bar--underline .tab-bar-item {
  padding: 12px 16px;
  text-transform: uppercase;
  border-bottom: 2px solid transparent;
}

.tab-bar--underline .tab-bar-item--active {
  color: #116468;
  border-bottom-color: #116468;
}

.tab-bar--pill {
  display: inline-flex;
  gap: 2px;
  padding: 3px;
  background: rgba(17, 100, 104, 0.06);
  border-radius: 10px;
}

.tab-bar--pill .tab-bar-item {
  padding: 6px 14px;
  border-radius: 8px;
}

.tab-bar--pill .tab-bar-item--active {
  color: #fff;
  background: #116468;
}

.tab-bar-item {
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.54);
  cursor: pointer;
  white-space: nowrap;
  transition: color 0.15s ease, background-color 0.15s ease, border-color 0.15s ease;
}

.tab-bar-item:hover {
  color: #116468;
}

.tab-bar--pill .tab-bar-item--active:hover {
  color: #fff;
}
</style>
