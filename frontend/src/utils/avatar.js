export function nextScale(current, delta) {
  return Math.min(4, Math.max(0.5, current + delta))
}

export function keyboardOffset(key, shiftKey) {
  const step = shiftKey ? 10 : 2
  return {
    ArrowLeft: [-step, 0],
    ArrowRight: [step, 0],
    ArrowUp: [0, -step],
    ArrowDown: [0, step]
  }[key] || [0, 0]
}

export function coverScale(width, height, rotation = 0, size = 320) {
  const quarterTurn = Math.abs(rotation) % 180 !== 0
  const displayWidth = quarterTurn ? height : width
  const displayHeight = quarterTurn ? width : height
  return Math.max(size / displayWidth, size / displayHeight)
}
