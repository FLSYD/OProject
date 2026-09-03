<template>
  <div class="auth-page">
    <el-card class="auth-card" shadow="always">
      <h1 class="auth-title">XX管理系统</h1>
      <p class="auth-subtitle">欢迎回来，请登录您的账号</p>
      <el-alert v-if="errorMsg" :title="errorMsg" type="error" :closable="false" show-icon />
      <el-form ref="loginForm" :model="form" :rules="rules" label-position="top" @keyup.enter.native="submit">
        <el-form-item label="用户名" prop="username"><el-input v-model.trim="form.username" prefix-icon="el-icon-user" placeholder="请输入用户名" /></el-form-item>
        <el-form-item label="密码" prop="password"><el-input v-model="form.password" prefix-icon="el-icon-lock" type="password" show-password placeholder="请输入密码" /></el-form-item>
        <el-button type="primary" class="full-button" :loading="loading" @click="submit">登录</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      form: { username: '', password: '' }, loading: false, errorMsg: '',
      rules: { username: [{ required: true, message: '请输入用户名', trigger: 'blur' }], password: [{ required: true, message: '请输入密码', trigger: 'blur' }] }
    }
  },
  methods: {
    submit() {
      this.$refs.loginForm.validate(async valid => {
        if (!valid) return
        this.loading = true
        this.errorMsg = ''
        try {
          const data = await this.$store.dispatch('login', this.form)
          this.$message.success('登录成功')
          this.$router.replace(data.must_change_password ? '/index/profile?forcePassword=1' : (this.$route.query.redirect || '/index/dashboard'))
        } catch (error) {
          const response = error.response
          if (response && response.data && response.data.msg) {
            this.errorMsg = response.data.msg
          } else if (response) {
            this.errorMsg = `登录接口返回 HTTP ${response.status}，请确认当前前端连接的是本项目后端`
          } else {
            this.errorMsg = '无法连接后端服务，请使用一键脚本显示的实际登录地址'
          }
        } finally { this.loading = false }
      })
    }
  }
}
</script>

<style scoped>
.auth-page { min-height: 100vh; display: grid; place-items: center; padding: 24px; background: radial-gradient(circle at 12% 18%, rgba(255,255,255,.22), transparent 28%), linear-gradient(135deg, var(--app-primary), #7658c5); }
.auth-card { width: min(430px, 100%); padding: 16px 14px; border: 0; border-radius: 20px; box-shadow: 0 24px 70px rgba(20, 27, 58, .3); }
.auth-title { margin: 8px 0 4px; text-align: center; font-size: 28px; }
.auth-subtitle { margin: 0 0 28px; text-align: center; color: var(--app-muted); }
.el-alert { margin-bottom: 18px; }
.full-button { background: var(--app-primary); border-color: var(--app-primary); }
</style>
