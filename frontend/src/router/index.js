import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'
import Login from '@/views/Login.vue'
import Index from '@/views/Index.vue'
import { basicRouteRedirect, menuRouteAllowed } from '@/utils/access'

Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'login', component: Login },
  {
    path: '/index',
    component: Index,
    redirect: '/index/dashboard',
    meta: { requireAuth: true },
    children: [
      { path: 'dashboard', name: 'dashboard', component: () => import('@/views/Dashboard.vue'), meta: { requireAuth: true, title: '首页', menuCode: 'dashboard' } },
      { path: 'example', name: 'example', component: () => import('@/views/Example.vue'), meta: { requireAuth: true, title: '权限示例', menuCode: 'example' } },
      { path: 'profile', name: 'profile', component: () => import('@/views/Profile.vue'), meta: { requireAuth: true, title: '个人信息', profile: true } }
    ]
  },
  { path: '*', redirect: '/login' }
]

const router = new VueRouter({ mode: 'hash', routes })

router.beforeEach(async (to, from, next) => {
  const redirect = basicRouteRedirect(to, store.getters.loggedIn, store.getters.mustChangePassword)
  if (redirect) return next(redirect)
  if (to.meta.menuCode) {
    try {
      if (!store.state.menus.length) await store.dispatch('fetchMenus')
      if (!menuRouteAllowed(to.meta.menuCode, store.getters.menuCodes)) return next('/index/dashboard')
    } catch (_) {
      return next('/login')
    }
  }
  next()
})

router.afterEach(to => {
  document.title = to.meta.title ? `${to.meta.title} - XX管理系统` : 'XX管理系统'
})

export default router
