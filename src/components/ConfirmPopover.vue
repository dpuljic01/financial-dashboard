<template>
  <VDropdown :triggers="['click']" placement="top" :distance="8" :overflow-padding="12" theme="dropdown">
    <slot></slot>
    <template #popper="{ hide }">
      <div class="confirm-popover">
        <p class="confirm-popover-message">{{ message }}</p>
        <div class="confirm-popover-actions">
          <button type="button" class="popover-btn" @click="hide">{{ cancelLabel }}</button>
          <button type="button" class="popover-btn popover-btn--danger" @click="onConfirm(hide)">
            {{ confirmLabel }}
          </button>
        </div>
      </div>
    </template>
  </VDropdown>
</template>

<script>
export default {
  name: 'ConfirmPopover',
  props: {
    message: {
      type: String,
      required: true,
    },
    confirmLabel: {
      type: String,
      default: 'Delete',
    },
    cancelLabel: {
      type: String,
      default: 'Cancel',
    },
  },
  emits: ['confirm'],
  methods: {
    onConfirm(hide) {
      hide();
      this.$emit('confirm');
    },
  },
};
</script>

<style scoped>
.confirm-popover {
  padding: 14px;
  max-width: 240px;
}
.confirm-popover-message {
  margin: 0 0 12px;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.75);
}
.confirm-popover-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
.popover-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  background: rgba(0, 0, 0, 0.06);
  color: rgba(0, 0, 0, 0.75);
}
.popover-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}
.popover-btn--danger {
  /* Hardcoded, not var(--loss-color): floating-vue teleports this popover
     to <body>, outside #app where that custom property is defined, so the
     variable would resolve to nothing and only the hover state (a literal
     hex value) would ever show a background. */
  background: #d1435c;
  color: #fff;
}
.popover-btn--danger:hover {
  background: #b5384c;
}
</style>
