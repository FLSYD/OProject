<template>
  <aside class="sidebar">
    <div class="brand"><span class="logo">X</span><b v-if="!collapsed || mobile">XX管理系统</b></div>
    <el-menu :default-active="$route.path" :collapse="collapsed && !mobile" router background-color="#182235" text-color="#aeb9cd" active-text-color="#fff" @select="$emit('navigate')">
      <el-menu-item v-for="menu in menus" :key="menu.code" :index="menu.path">
        <i :class="menu.icon || 'el-icon-menu'" /><span slot="title">{{ menu.name }}</span>
      </el-menu-item>
    </el-menu>
  </aside>
</template>

<script>
export default {
  name: 'LeftTree',
  props: { collapsed: Boolean, mobile: Boolean },
  computed: { menus() { return this.$store.state.menus } },
  created() {
    if (!this.$store.getters.mustChangePassword) this.$store.dispatch('fetchMenus').catch(() => {})
  }
}
</script>

<style scoped>
.sidebar { width: 100%; min-height: 100vh; background: var(--app-sidebar); }
.brand { height: 68px; display: flex; align-items: center; gap: 12px; padding: 0 17px; color: #fff; white-space: nowrap; }
.logo { width: 38px; height: 38px; flex: 0 0 auto; display: grid; place-items: center; border-radius: 12px; font-weight: 800; background: linear-gradient(135deg, #7182ff, #9b6de1); }
.brand b { overflow: hidden; text-overflow: ellipsis; }
.el-menu { border-right: 0; }
.sidebar >>> .el-menu-item { margin: 4px 9px; border-radius: 9px; }
.sidebar >>> .el-menu-item.is-active { background: var(--app-primary) !important; }
.sidebar >>> .el-menu--collapse { width: 72px; }
</style>
