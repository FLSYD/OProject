<template>
  <div class="login-page">
    <el-card class="login-card" shadow="always">
      <div class="login-title"><h1>XX管理系统</h1><p>欢迎登录新手教学模板</p></div>
      <el-alert v-if="errorMsg" :title="errorMsg" type="error" :closable="false" show-icon />
      <el-form ref="loginForm" :model="form" :rules="rules" @keyup.enter.native="submit">
        <el-form-item prop="username"><el-input v-model.trim="form.username" prefix-icon="el-icon-user" placeholder="用户名" /></el-form-item>
        <el-form-item prop="password"><el-input v-model="form.password" prefix-icon="el-icon-lock" type="password" show-password placeholder="密码" /></el-form-item>
        <el-button type="primary" class="login-button" :loading="loading" @click="submit">登录</el-button>
      </el-form>
      <div class="login-footer">© 2026 XX管理系统</div>
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
          this.$router.replace(data.must_change_password ? '/index/profile?forcePassword=1' : '/index/dashboard')
        } catch (error) {
          this.errorMsg = (error.response && error.response.data && error.response.data.msg) || '登录失败，请检查网络连接'
        } finally { this.loading = false }
      })
    }
  }
}
</script>

<style scoped>
.login-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; background: linear-gradient(135deg, #667eea, #764ba2); }
.login-card { width: 420px; border: 0; border-radius: 16px; padding: 18px; }
.login-title { text-align: center; margin-bottom: 25px; }
.login-title h1 { margin: 0 0 8px; font-size: 28px; }
.login-title p, .login-footer { color: #909399; }
.el-alert { margin-bottom: 18px; }
.login-button { width: 100%; height: 44px; background: linear-gradient(135deg, #667eea, #764ba2); border: 0; }
.login-footer { text-align: center; margin-top: 28px; font-size: 12px; }
</style>

