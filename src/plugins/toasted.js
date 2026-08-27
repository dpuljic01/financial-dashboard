const toastedRef = { instance: null };

export function setToastedInstance(instance) {
  toastedRef.instance = instance;
}

export function showToast(message, options) {
  if (toastedRef.instance) {
    toastedRef.instance.show(message, options);
  }
}

export default toastedRef;
