<template>
  <header class="app-header">
    <div class="header-left">
      <el-button class="desktop-toggle" type="text" circle :title="collapsed ? '展开侧栏' : '收起侧栏'" @click="$emit('toggle')"><i :class="collapsed ? 'el-icon-s-unfold' : 'el-icon-s-fold'" /></el-button>
      <el-button class="mobile-toggle" type="text" circle title="打开菜单" @click="$emit('open-mobile')"><i class="el-icon-menu" /></el-button>
      <strong>XX管理系统</strong>
    </div>
    <el-dropdown trigger="click" @command="handleCommand">
      <div class="user-entry" data-testid="user-menu">
        <el-avatar :size="34" :src="user && user.avatar"><span>{{ avatarText }}</span></el-avatar>
        <span class="user-copy"><b>{{ displayName }}</b><small>{{ roleText }}</small></span><i class="el-icon-arrow-down" />
      </div>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item command="profile" icon="el-icon-user">个人信息</el-dropdown-item>
        <el-dropdown-item command="logout" icon="el-icon-switch-button" divided>退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  props: { collapsed: Boolean },
  computed: {
    user() { return this.$store.state.user },
    displayName() { return (this.user && (this.user.nickname || this.user.username)) || '用户' },
    avatarText() { return this.displayName.slice(0, 1).toUpperCase() },
    roleText() {
      if (this.user && this.user.is_superuser) return '超级管理员'
      return this.user && this.user.roles && this.user.roles.length ? this.user.roles[0] : '普通用户'
    }
  },
  methods: {
    handleCommand(command) {
      if (command === 'profile') this.$router.push('/index/profile')
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
.app-header { height: 68px; flex: 0 0 auto; display: flex; align-items: center; justify-content: space-between; padding: 0 22px; color: #fff; background: linear-gradient(135deg, var(--app-primary), #7658c5); box-shadow: 0 4px 18px rgba(69, 80, 178, .22); }
.header-left { display: flex; align-items: center; gap: 10px; font-size: 20px; }
.header-left .el-button { color: #fff; font-size: 20px; }
.mobile-toggle { display: none; }
.user-entry { display: flex; align-items: center; gap: 10px; padding: 6px 12px 6px 7px; border-radius: 30px; color: #fff; background: rgba(255,255,255,.15); cursor: pointer; }
.user-copy { display: grid; min-width: 90px; text-align: left; }
.user-copy b { max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.user-copy small { margin-top: 2px; opacity: .8; }
@media (max-width: 800px) { .desktop-toggle { display: none; } .mobile-toggle { display: inline-flex; } .header-left strong { font-size: 17px; } .user-copy { display: none; } }
</style>
