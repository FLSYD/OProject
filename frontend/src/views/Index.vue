<template>
  <div v-if="mustChange" class="force-shell"><router-view /></div>
  <div v-else class="shell">
    <aside class="sidebar-shell" :class="{ collapsed }"><left-tree :collapsed="collapsed" /></aside>
    <el-drawer :visible.sync="mobileOpen" direction="ltr" size="260px" :with-header="false" custom-class="mobile-drawer">
      <left-tree :mobile="true" @navigate="mobileOpen = false" />
    </el-drawer>
    <section class="shell-main">
      <app-header :collapsed="collapsed" @toggle="collapsed = !collapsed" @open-mobile="mobileOpen = true" />
      <div class="breadcrumb-bar"><el-breadcrumb separator="/"><el-breadcrumb-item :to="{ path: '/index/dashboard' }">首页</el-breadcrumb-item><el-breadcrumb-item v-if="$route.path !== '/index/dashboard'">{{ $route.meta.title || '页面' }}</el-breadcrumb-item></el-breadcrumb></div>
      <main><router-view /></main>
      <footer>© {{ year }} XX管理系统</footer>
    </section>
  </div>
</template>

<script>
import AppHeader from '@/components/Header.vue'
import LeftTree from '@/components/LeftTree.vue'
export default {
  name: 'IndexView',
  components: { AppHeader, LeftTree },
  data: () => ({ collapsed: false, mobileOpen: false }),
  computed: {
    year() { return new Date().getFullYear() },
    mustChange() { return this.$store.getters.mustChangePassword }
  }
}
</script>

<style scoped>
.shell { min-height: 100vh; display: flex; background: var(--app-bg); }
.force-shell { min-height: 100vh; display: grid; place-items: center; padding: 24px; background: radial-gradient(circle at 12% 18%, rgba(255,255,255,.22), transparent 28%), linear-gradient(135deg, var(--app-primary), #7658c5); }
.force-shell >>> .profile-page { width: 100%; }
.sidebar-shell { width: 244px; flex: 0 0 auto; overflow: hidden; background: var(--app-sidebar); transition: width .25s; }
.sidebar-shell.collapsed { width: 72px; }
.shell-main { min-width: 0; flex: 1; display: flex; flex-direction: column; min-height: 100vh; }
.breadcrumb-bar { height: 46px; flex: 0 0 auto; display: flex; align-items: center; padding: 0 24px; background: #fff; border-bottom: 1px solid #edf0f5; }
main { flex: 1; min-width: 0; padding: 24px; overflow: auto; }
footer { height: 48px; display: grid; place-items: center; color: var(--app-muted); font-size: 13px; }
.shell >>> .mobile-drawer .el-drawer__body { padding: 0; background: var(--app-sidebar); }
@media (max-width: 800px) { .sidebar-shell { display: none; } main { padding: 14px; } .breadcrumb-bar { padding: 0 16px; } }
</style>
