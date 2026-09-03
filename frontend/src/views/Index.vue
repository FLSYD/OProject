<template>
  <div><app-header /><div class="body"><left-tree /><main><el-breadcrumb separator="/" class="breadcrumb"><el-breadcrumb-item>系统</el-breadcrumb-item><el-breadcrumb-item>{{ $route.meta.title || '页面' }}</el-breadcrumb-item></el-breadcrumb><router-view /></main></div></div>
</template>

<script>
import AppHeader from '@/components/Header.vue'
import LeftTree from '@/components/LeftTree.vue'
export default { name: 'IndexView', components: { AppHeader, LeftTree } }
</script>

<style scoped>
.body { display: flex; min-height: calc(100vh - 64px); }
main { flex: 1; min-width: 0; padding: 22px; }
.breadcrumb { margin-bottom: 18px; }
@media (max-width: 700px) { .body { display: block; } .body >>> .sidebar { width: 100%; min-height: auto; } }
</style>

