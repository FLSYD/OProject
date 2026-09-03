import { isEmail, isMainlandPhone } from '@/utils/profile'

describe('个人资料表单校验', () => {
  test('手机号允许留空或填写中国大陆 11 位号码', () => {
    expect(isMainlandPhone('')).toBe(true)
    expect(isMainlandPhone('13800138000')).toBe(true)
    expect(isMainlandPhone('123')).toBe(false)
  })

  test('邮箱允许留空并拒绝明显错误格式', () => {
    expect(isEmail('')).toBe(true)
    expect(isEmail('user@example.com')).toBe(true)
    expect(isEmail('invalid-email')).toBe(false)
  })
})
