export function isMainlandPhone(value) {
  return !value || /^1[3-9]\d{9}$/.test(value)
}

export function isEmail(value) {
  return !value || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
}
