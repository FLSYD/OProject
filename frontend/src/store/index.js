import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

function readUser() {
  try {
    return JSON.parse(sessionStorage.getItem('user') || 'null')
  } catch (_) {
    return null
  }
}

export default new Vuex.Store({
  state: {
    token: sessionStorage.getItem('token') || '',
    user: readUser(),
    menus: []
  },
  getters: {
    loggedIn: state => Boolean(state.token),
    mustChangePassword: state => Boolean(state.user && state.user.must_change_password),
    menuCodes: state => state.menus.map(item => item.code)
  },
  mutations: {
    setSession(state, payload) {
      state.token = payload.token
      state.user = payload.user
      sessionStorage.setItem('token', payload.token)
      sessionStorage.setItem('user', JSON.stringify(payload.user))
    },
    setUser(state, user) {
      state.user = user
      sessionStorage.setItem('user', JSON.stringify(user))
    },
    setMenus(state, menus) {
      state.menus = menus
    },
    clearSession(state) {
      state.token = ''
      state.user = null
      state.menus = []
      sessionStorage.removeItem('token')
      sessionStorage.removeItem('user')
    }
  },
  actions: {
    async login({ commit }, form) {
      const response = await axios.post('/api/login/', form)
      commit('setSession', response.data.data)
      return response.data.data
    },
    async fetchMenus({ commit }) {
      const response = await axios.get('/api/menu/')
      commit('setMenus', response.data.data)
      return response.data.data
    },
    logout({ commit }) {
      commit('clearSession')
    }
  }
})

