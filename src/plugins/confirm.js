import { reactive } from 'vue';

// A single shared confirm-dialog instance (mounted once in Navigation.vue)
// instead of a native window.confirm() - keeps the app's own styling and
// still lets call sites just `await confirmDialog(...)` for a boolean.
const state = reactive({
  open: false,
  title: 'Are you sure?',
  message: '',
  confirmLabel: 'Delete',
  cancelLabel: 'Cancel',
  danger: true,
  resolve: null,
});

export function confirmDialog(message, options = {}) {
  return new Promise((resolve) => {
    state.open = true;
    state.message = message;
    state.title = options.title || 'Are you sure?';
    state.confirmLabel = options.confirmLabel || 'Delete';
    state.cancelLabel = options.cancelLabel || 'Cancel';
    state.danger = options.danger !== false;
    state.resolve = resolve;
  });
}

export function resolveConfirm(value) {
  state.open = false;
  if (state.resolve) {
    state.resolve(value);
    state.resolve = null;
  }
}

export default state;
