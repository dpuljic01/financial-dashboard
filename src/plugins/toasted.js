const toastedRef = { instance: null };

export function setToastedInstance(instance) {
  toastedRef.instance = instance;
}

export function showToast(message, options = {}) {
  if (toastedRef.instance) {
    toastedRef.instance.show(message, {
      // Every toast gets a close button by default so it doesn't have to
      // sit and wait out its duration - callers can still override.
      action: {
        icon: 'close',
        onClick: (e, toastObject) => toastObject.goAway(0),
      },
      ...options,
    });
  }
}

export default toastedRef;
