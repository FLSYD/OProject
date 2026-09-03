describe('认证 Store', () => {
  beforeEach(() => {
    sessionStorage.clear()
    jest.resetModules()
  })

  test('保存和清理登录会话', () => {
    const store = require('@/store').default
    store.commit('setSession', { token: 'demo-token', user: { username: 'demo', must_change_password: true } })
    expect(store.getters.loggedIn).toBe(true)
    expect(store.getters.mustChangePassword).toBe(true)
    expect(sessionStorage.getItem('token')).toBe('demo-token')
    store.commit('clearSession')
    expect(store.getters.loggedIn).toBe(false)
    expect(sessionStorage.getItem('token')).toBeNull()
  })

  test('菜单编码用于路由判断', () => {
    const store = require('@/store').default
    store.commit('setMenus', [{ code: 'dashboard' }, { code: 'example' }])
    expect(store.getters.menuCodes).toEqual(['dashboard', 'example'])
  })
})

