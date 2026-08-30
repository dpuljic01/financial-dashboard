<template>
  <div class="fin-loader" :class="`fin-loader--${size}`">
    <div class="fin-loader-bars">
      <span
        v-for="n in 5"
        :key="n"
        class="fin-loader-bar"
        :style="{ animationDelay: `${(n - 1) * 0.12}s` }"
      ></span>
    </div>
    <p v-if="label" class="fin-loader-label">{{ label }}</p>
  </div>
</template>

<script>
export default {
  name: 'FinancialLoader',
  props: {
    size: {
      type: String,
      default: 'large',
      validator: (value) => ['small', 'large'].includes(value),
    },
    label: {
      type: String,
      default: '',
    },
  },
};
</script>

<style scoped>
.fin-loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}
.fin-loader-bars {
  display: flex;
  align-items: flex-end;
  gap: 4px;
}
.fin-loader--large .fin-loader-bars {
  height: 40px;
}
.fin-loader--small .fin-loader-bars {
  height: 22px;
}
.fin-loader-bar {
  width: 6px;
  height: 100%;
  border-radius: 2px;
  background: linear-gradient(180deg, #2fd8d4, #00aaad 60%, #116468);
  transform-origin: bottom;
  animation: fin-loader-bounce 1s ease-in-out infinite;
}
.fin-loader--small .fin-loader-bar {
  width: 4px;
  border-radius: 1px;
}
@keyframes fin-loader-bounce {
  0%, 100% {
    transform: scaleY(0.35);
    opacity: 0.7;
  }
  50% {
    transform: scaleY(1);
    opacity: 1;
  }
}
.fin-loader-label {
  margin: 0;
  font-size: 13px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.5);
}
@media (prefers-reduced-motion: reduce) {
  .fin-loader-bar {
    animation: none;
    transform: scaleY(0.75);
    opacity: 0.9;
  }
}
</style>
