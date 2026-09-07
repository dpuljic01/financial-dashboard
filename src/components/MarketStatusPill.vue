<template>
  <span class="market-status" :class="`market-status--${status.key}`" :title="status.detail || status.label">
    <span class="market-status-dot"></span>
    {{ status.label }}
  </span>
</template>

<script>
import { getMarketStatus } from '../utils/marketHours';

export default {
  name: 'MarketStatusPill',
  data() {
    return {
      status: getMarketStatus(),
      timer: null,
    };
  },
  mounted() {
    // Cheap to recompute (pure date math, no request) - a minute is plenty
    // to catch the open/close transition without redoing this every tick.
    this.timer = setInterval(() => {
      this.status = getMarketStatus();
    }, 60000);
  },
  beforeUnmount() {
    if (this.timer) clearInterval(this.timer);
  },
};
</script>

<style scoped>
.market-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  cursor: default;
}
.market-status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}
.market-status--open {
  background: rgba(15, 157, 112, 0.1);
  color: var(--gain-color);
}
.market-status--open .market-status-dot {
  background: var(--gain-color);
  box-shadow: 0 0 0 3px rgba(15, 157, 112, 0.18);
}
.market-status--pre,
.market-status--post {
  background: rgba(217, 119, 6, 0.1);
  color: #b45309;
}
.market-status--pre .market-status-dot,
.market-status--post .market-status-dot {
  background: #d97706;
}
.market-status--closed {
  background: rgba(0, 0, 0, 0.06);
  color: rgba(0, 0, 0, 0.5);
}
.market-status--closed .market-status-dot {
  background: rgba(0, 0, 0, 0.3);
}
</style>
