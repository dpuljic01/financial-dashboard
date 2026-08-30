<template>
  <Modal :model-value="state.open" @update:model-value="onDismiss">
    <h3 class="confirm-title">{{ state.title }}</h3>
    <p class="confirm-message">{{ state.message }}</p>
    <div class="confirm-actions">
      <md-button class="md-raised" @click="respond(false)">{{ state.cancelLabel }}</md-button>
      <md-button
        class="md-raised"
        :class="state.danger ? 'confirm-btn--danger' : 'md-primary'"
        @click="respond(true)"
      >{{ state.confirmLabel }}</md-button>
    </div>
  </Modal>
</template>

<script>
import Modal from './Modal.vue';
import confirmState, { resolveConfirm } from '../plugins/confirm';

export default {
  name: 'ConfirmDialog',
  components: {
    Modal,
  },
  data() {
    return {
      state: confirmState,
    };
  },
  methods: {
    respond(value) {
      resolveConfirm(value);
    },
    onDismiss(value) {
      // Modal only ever emits `false` (backdrop click / close button) -
      // treat that the same as clicking Cancel.
      if (!value) resolveConfirm(false);
    },
  },
};
</script>

<style scoped>
.confirm-title {
  margin: 0 0 8px;
}
.confirm-message {
  margin: 0 0 20px;
  color: rgba(0, 0, 0, 0.65);
}
.confirm-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
.confirm-btn--danger {
  background-color: var(--loss-color) !important;
  color: #fff !important;
}
</style>
