import { toast } from 'vue-sonner';

const TOAST_METHODS = {
  success: toast.success,
  error: toast.error,
  warning: toast.warning,
  info: toast.info,
};

export function showToast(message, options = {}) {
  const type = options.type || 'success';
  const method = TOAST_METHODS[type] || toast.message;
  method(message, { duration: options.duration });
}

export default toast;
