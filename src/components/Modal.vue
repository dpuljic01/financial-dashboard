<template>
  <div v-if="modelValue" class="modal-overlay" @click.self="close">
    <div class="modal-box">
      <button type="button" class="modal-close" @click="close">close</button>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Modal',
  compatConfig: { MODE: 3 },
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
  },
  emits: ['update:modelValue'],
  methods: {
    close() {
      this.$emit('update:modelValue', false);
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 40px 16px;
  overflow-y: auto;
  box-sizing: border-box;
  z-index: 1000;
}

.modal-box {
  position: relative;
  background: #fff;
  border-radius: 4px;
  padding: 24px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  text-align: left;
  flex-shrink: 0;
  box-sizing: border-box;
}

.modal-close {
  position: absolute;
  top: 12px;
  right: 12px;
  background: none;
  border: none;
  font-size: 0;
  width: 24px;
  height: 24px;
  cursor: pointer;
  color: rgba(0, 0, 0, 0.54);
}

.modal-close::before {
  content: '\2715';
  font-size: 16px;
}
</style>
