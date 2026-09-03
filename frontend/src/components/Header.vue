<template>
  <header class="app-header">
    <div class="system-name">XX管理系统</div>
    <el-dropdown trigger="click" @command="handleCommand">
      <div class="user-entry" data-testid="user-menu">
        <el-avatar :size="34" :src="user && user.avatar"><span>{{ avatarText }}</span></el-avatar>
        <span>{{ displayName }}</span><i class="el-icon-arrow-down" />
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
  computed: {
    user() { return this.$store.state.user },
    displayName() { return (this.user && (this.user.nickname || this.user.username)) || '用户' },
    avatarText() { return this.displayName.slice(0, 1).toUpperCase() }
  },
  methods: {
    handleCommand(command) {
      if (command === 'profile') this.$router.push('/index/profile')
      if (command === 'logout') {
        this.$store.dispatch('logout')
        this.$router.replace('/login')
      }
    }
  }
}
</script>

<style scoped>
.app-header { height: 64px; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; color: white; background: linear-gradient(135deg, #667eea, #764ba2); box-shadow: 0 2px 10px rgba(56, 67, 129, .25); }
.system-name { font-size: 21px; font-weight: 600; }
.user-entry { display: flex; align-items: center; gap: 9px; color: #fff; cursor: pointer; }
</style>
