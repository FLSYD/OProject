import { coverScale, keyboardOffset, nextScale } from '@/utils/avatar'

describe('头像裁剪计算', () => {
  test('缩放限制在允许范围', () => {
    expect(nextScale(0.5, -1)).toBe(0.5)
    expect(nextScale(4, 1)).toBe(4)
    expect(nextScale(1, 0.2)).toBeCloseTo(1.2)
  })

  test('Shift 方向键使用加速步长', () => {
    expect(keyboardOffset('ArrowLeft', false)).toEqual([-2, 0])
    expect(keyboardOffset('ArrowDown', true)).toEqual([0, 10])
  })

  test('旋转后仍按画布覆盖比例计算', () => {
    expect(coverScale(640, 320, 0)).toBe(1)
    expect(coverScale(640, 320, 90)).toBe(1)
    expect(coverScale(800, 600, 0)).toBeCloseTo(320 / 600)
  })
})
