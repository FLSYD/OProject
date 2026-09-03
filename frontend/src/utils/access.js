export function basicRouteRedirect(to, loggedIn, mustChangePassword) {
  if (to.path === '/login') return loggedIn ? '/index/dashboard' : ''
  if (to.meta.requireAuth && !loggedIn) return '/login'
  if (mustChangePassword && !to.meta.profile) return '/index/profile?forcePassword=1'
  return ''
}

export function menuRouteAllowed(menuCode, menuCodes) {
  return !menuCode || menuCodes.includes(menuCode)
}
