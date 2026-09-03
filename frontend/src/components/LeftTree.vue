<template>
  <aside class="sidebar">
    <el-menu :default-active="$route.path" router background-color="#263445" text-color="#c7d0dc" active-text-color="#67c23a">
      <el-menu-item v-for="menu in menus" :key="menu.code" :index="menu.path">
        <i :class="menu.icon || 'el-icon-menu'" /><span slot="title">{{ menu.name }}</span>
      </el-menu-item>
    </el-menu>
  </aside>
</template>

<script>
export default {
  name: 'LeftTree',
  computed: { menus() { return this.$store.state.menus } },
  created() {
    if (!this.$store.getters.mustChangePassword) this.$store.dispatch('fetchMenus').catch(() => {})
  }
}
</script>

<style scoped>
.sidebar { width: 220px; min-height: calc(100vh - 64px); background: #263445; }
.el-menu { border-right: none; }
</style>

