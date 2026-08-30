const toastedRef = { instance: null };

const TYPE_TITLES = {
  success: 'Success',
  error: 'Error',
  info: 'Info',
  warning: 'Warning',
};

const TYPE_ICONS = {
  success: 'check_circle',
  error: 'cancel',
  info: 'info',
  warning: 'warning',
};

export function setToastedInstance(instance) {
  toastedRef.instance = instance;
}

export function showToast(message, options = {}) {
  if (!toastedRef.instance) return;
  const type = options.type || 'success';
  const title = options.title || TYPE_TITLES[type] || '';

  toastedRef.instance.show(
    `<span class="toast-body">
      ${title ? `<strong class="toast-title">${title}</strong>` : ''}
      <span class="toast-desc">${message}</span>
    </span>`,
    {
      icon: TYPE_ICONS[type] || 'info',
      // Every toast gets a close button by default so it doesn't have to
      // sit and wait out its duration - callers can still override.
      action: {
        icon: 'close',
        onClick: (e, toastObject) => toastObject.goAway(0),
      },
      ...options,
    },
  );
}

export default toastedRef;
