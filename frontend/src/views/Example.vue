<template><section class="page-card example-page"><div class="example-icon"><i class="el-icon-lock" /></div><h2 class="page-title">权限示例</h2><p>此页面用于演示角色菜单与后端接口权限。</p><el-alert type="success" :closable="false" show-icon :title="text || '正在读取受保护接口…'" /></section></template>
<script>
export default { name: 'ExampleView', data: () => ({ text: '' }), async created() { const response = await this.$http.get('/api/example/'); this.text = response.data.data.text } }
</script>
<style scoped>.example-page { max-width: 900px; }.example-icon { width: 52px; height: 52px; display: grid; place-items: center; margin-bottom: 18px; border-radius: 14px; color: #fff; font-size: 24px; background: linear-gradient(135deg, var(--app-primary), #825bc0); }.example-page p { margin-top: -8px; color: var(--app-muted); }</style>
