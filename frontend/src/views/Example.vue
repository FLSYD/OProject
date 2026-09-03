<template><section class="page-card"><h2 class="page-title">权限示例</h2><el-alert type="success" :closable="false" show-icon :title="text || '正在读取受保护接口…'" /></section></template>
<script>
export default { name: 'ExampleView', data: () => ({ text: '' }), async created() { const response = await this.$http.get('/api/example/'); this.text = response.data.data.text } }
</script>

