<template>
  <header class="app-header">
    <div class="header-left">
      <el-button class="desktop-toggle" type="text" circle :title="collapsed ? '展开侧栏' : '收起侧栏'" @click="$emit('toggle')"><i :class="collapsed ? 'el-icon-s-unfold' : 'el-icon-s-fold'" /></el-button>
      <el-button class="mobile-toggle" type="text" circle title="打开菜单" @click="$emit('open-mobile')"><i class="el-icon-menu" /></el-button>
      <strong>XX管理系统</strong>
    </div>

    <el-dropdown trigger="click" placement="bottom-end" popper-class="oproject-user-dropdown" @visible-change="dropdownVisible = $event" @command="handleCommand">
      <div class="user-info" :class="{ 'is-open': dropdownVisible }" data-testid="user-menu">
        <el-avatar :size="40" :src="user && user.avatar" class="user-avatar"><span>{{ avatarText }}</span></el-avatar>
        <div class="user-details">
          <div class="user-name">{{ displayName }}</div>
          <el-tag v-if="isSuperAdmin" size="mini" type="warning" effect="dark" class="user-role-tag super-admin-role"><i class="el-icon-star-on" />超级管理员</el-tag>
          <el-tag v-else size="mini" type="info" effect="plain" class="user-role-tag"><i class="el-icon-user" />{{ roleText }}</el-tag>
        </div>
        <i class="dropdown-icon el-icon-arrow-down" />
      </div>

      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item command="profile" class="dropdown-item"><i class="el-icon-user" /><span>个人信息</span></el-dropdown-item>
        <el-dropdown-item command="logout" divided class="dropdown-item logout-item"><i class="el-icon-switch-button" /><span>退出登录</span></el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  props: { collapsed: Boolean },
  data() { return { dropdownVisible: false } },
  computed: {
    user() { return this.$store.state.user },
    displayName() { return (this.user && (this.user.nickname || this.user.username)) || '用户' },
    avatarText() { return this.displayName.slice(0, 1).toUpperCase() },
    roleText() {
      if (this.user && this.user.is_superuser) return '超级管理员'
      return this.user && this.user.roles && this.user.roles.length ? this.user.roles[0] : '普通用户'
    },
    isSuperAdmin() { return this.roleText === '超级管理员' }
  },
  methods: {
    handleCommand(command) {
      if (command === 'profile') {
        if (this.$route.path !== '/index/profile') this.$router.push('/index/profile').catch(error => { if (error.name !== 'NavigationDuplicated') throw error })
        return
      }
      if (command === 'logout') {
        this.$confirm('确定退出当前账号吗？', '退出登录', { type: 'warning' }).then(() => {
          this.$store.dispatch('logout')
          this.$router.replace('/login')
        }).catch(() => {})
      }
    }
  }
}
</script>

<style scoped>
.app-header { height: 68px; flex: 0 0 auto; display: flex; align-items: center; justify-content: space-between; padding: 0 22px; color: #fff; background: linear-gradient(135deg, var(--app-primary), #7658c5); box-shadow: 0 4px 18px rgba(69,80,178,.22); }
.header-left { display: flex; align-items: center; gap: 10px; font-size: 20px; }
.header-left .el-button { color: #fff; font-size: 20px; }
.mobile-toggle { display: none; }
.user-info { display: flex; align-items: center; gap: 11px; max-width: 260px; height: 52px; padding: 6px 15px 6px 7px; overflow: hidden; border-radius: 28px; background: rgba(255,255,255,.14); cursor: pointer; box-sizing: border-box; transition: background .25s, box-shadow .25s, transform .25s; }
.user-info:hover, .user-info.is-open { background: rgba(255,255,255,.23); box-shadow: 0 5px 16px rgba(43,35,103,.17); transform: translateY(-1px); }
.user-avatar { flex: 0 0 auto; color: #fff; background: linear-gradient(135deg, #6576ee, #8553bd); border: 2px solid rgba(255,255,255,.86); box-shadow: 0 2px 8px rgba(35,30,85,.18); }
.user-details { display: flex; min-width: 0; flex: 1; flex-direction: column; align-items: flex-start; gap: 4px; }
.user-name { max-width: 150px; overflow: hidden; color: #fff; font-size: 14px; font-weight: 700; line-height: 16px; text-overflow: ellipsis; text-shadow: 0 1px 2px rgba(0,0,0,.1); white-space: nowrap; }
.user-role-tag { display: inline-flex; align-items: center; max-width: 130px; height: 18px; padding: 0 7px; overflow: hidden; border: 0; border-radius: 9px; font-size: 11px; line-height: 18px; text-overflow: ellipsis; white-space: nowrap; }
.user-role-tag i { margin-right: 3px; font-size: 10px; }
.super-admin-role { color: #fff; background: linear-gradient(135deg, #ffad22, #ee8a00); box-shadow: 0 2px 6px rgba(157,85,0,.2); }
.dropdown-icon { flex: 0 0 auto; margin-left: 2px; color: rgba(255,255,255,.9); font-size: 12px; transition: transform .25s; }
.user-info.is-open .dropdown-icon { transform: rotate(180deg); }
@media (max-width: 700px) { .app-header { padding: 0 14px; } .desktop-toggle { display: none; } .mobile-toggle { display: inline-flex; } .header-left strong { font-size: 17px; } .user-info { width: 46px; height: 46px; padding: 3px; justify-content: center; } .user-details, .dropdown-icon { display: none; } }
</style>

<style>
.oproject-user-dropdown.el-dropdown-menu { min-width: 172px; margin-top: 10px !important; padding: 7px; border: 0; border-radius: 12px; box-shadow: 0 10px 32px rgba(31,40,88,.18); }
.oproject-user-dropdown .popper__arrow { display: none; }
.oproject-user-dropdown .dropdown-item { display: flex !important; align-items: center !important; gap: 11px; height: 44px !important; margin: 2px 0; padding: 0 13px !important; color: #374056; line-height: 44px !important; border-radius: 8px; transition: color .2s, background .2s; }
.oproject-user-dropdown .dropdown-item i { width: 18px; margin: 0 !important; color: #8b93a7; font-size: 17px; text-align: center; }
.oproject-user-dropdown .dropdown-item:hover { color: #5965df; background: linear-gradient(135deg, rgba(102,126,234,.1), rgba(118,75,162,.1)); }
.oproject-user-dropdown .dropdown-item:hover i { color: #5965df; }
.oproject-user-dropdown .logout-item { margin-top: 7px; color: #e35d5d; border-top-color: #edf0f5; }
.oproject-user-dropdown .logout-item::before { height: 7px; margin: -8px -13px 0; background: #fff; }
.oproject-user-dropdown .logout-item i, .oproject-user-dropdown .logout-item:hover i { color: #e35d5d; }
.oproject-user-dropdown .logout-item:hover { color: #e35d5d; background: #fff1f1; }
</style>
