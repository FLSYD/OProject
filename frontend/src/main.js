import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import store from './store'
import './styles/main.css'

Vue.use(ElementUI)
Vue.config.productionTip = false
axios.defaults.baseURL = process.env.NODE_ENV === 'production' ? '/' : '/'

axios.interceptors.request.use(config => {
  const token = sessionStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

axios.interceptors.response.use(
  response => response,
  error => {
    const status = error.response && error.response.status
    if (status === 401) {
      store.commit('clearSession')
      if (router.currentRoute.path !== '/login') router.replace('/login')
    } else if (status === 403) {
      Vue.prototype.$message.warning((error.response.data && error.response.data.msg) || '没有访问权限')
    }
    return Promise.reject(error)
  }
)

Vue.prototype.$http = axios

new Vue({ router, store, render: h => h(App) }).$mount('#app')

