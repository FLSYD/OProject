import { basicRouteRedirect, menuRouteAllowed } from '@/utils/access'

describe('路由守卫', () => {
  test('未登录访问受保护页面时进入登录页', () => {
    const to = { path: '/index/dashboard', meta: { requireAuth: true } }
    expect(basicRouteRedirect(to, false, false)).toBe('/login')
  })

  test('首次改密用户只能进入个人信息页', () => {
    const dashboard = { path: '/index/dashboard', meta: { requireAuth: true } }
    const profile = { path: '/index/profile', meta: { requireAuth: true, profile: true } }
    expect(basicRouteRedirect(dashboard, true, true)).toBe('/index/profile?forcePassword=1')
    expect(basicRouteRedirect(profile, true, true)).toBe('')
  })

  test('菜单编码决定路由是否可见', () => {
    expect(menuRouteAllowed('dashboard', ['dashboard'])).toBe(true)
    expect(menuRouteAllowed('example', ['dashboard'])).toBe(false)
  })
})
