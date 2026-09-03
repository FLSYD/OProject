<template>
  <el-form ref="passwordForm" :model="form" :rules="rules" label-width="100px" class="password-form">
    <el-form-item label="原密码" prop="old_password"><el-input v-model="form.old_password" type="password" show-password autocomplete="current-password" /></el-form-item>
    <el-form-item label="新密码" prop="new_password"><el-input v-model="form.new_password" type="password" show-password autocomplete="new-password" /></el-form-item>
    <el-form-item label="确认密码" prop="confirm_password"><el-input v-model="form.confirm_password" type="password" show-password autocomplete="new-password" @keyup.enter.native="submit" /></el-form-item>
    <el-form-item><el-button type="primary" :loading="loading" @click="submit">{{ initial ? '设置新密码' : '修改密码' }}</el-button></el-form-item>
  </el-form>
</template>

<script>
export default {
  name: 'PasswordForm',
  props: {
    form: { type: Object, required: true },
    rules: { type: Object, required: true },
    loading: Boolean,
    initial: Boolean
  },
  methods: {
    submit() { this.$refs.passwordForm.validate(valid => { if (valid) this.$emit('submit') }) }
  }
}
</script>

<style scoped>
.password-form { max-width: 540px; }
@media (max-width: 700px) { .password-form { max-width: 100%; } }
</style>
