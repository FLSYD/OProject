<template>
  <section class="page-card profile-page" v-loading="loading">
    <div class="profile-head">
      <el-avatar :size="88" :src="form.avatar"><span>{{ avatarText }}</span></el-avatar>
      <div><h2>{{ form.nickname || form.username || '个人信息' }}</h2><p>{{ roleText }}</p></div>
      <div class="avatar-actions"><el-button data-testid="avatar-edit" size="small" @click="avatarVisible = true">编辑头像</el-button><el-button v-if="form.avatar" data-testid="avatar-delete" size="small" type="danger" plain @click="deleteAvatar">删除头像</el-button></div>
    </div>

    <el-alert v-if="mustChange" title="首次登录必须先修改初始密码，成功后请使用新密码重新登录。" type="warning" :closable="false" show-icon />
    <el-tabs v-model="activeTab">
      <el-tab-pane label="基本资料" name="profile" :disabled="mustChange">
        <el-form ref="profileForm" :model="form" :rules="profileRules" label-width="90px" class="form-grid">
          <el-form-item label="用户名"><el-input v-model="form.username" disabled /></el-form-item>
          <el-form-item label="昵称" prop="nickname"><el-input v-model.trim="form.nickname" data-testid="profile-nickname" maxlength="50" show-word-limit /></el-form-item>
          <el-form-item label="邮箱" prop="email"><el-input v-model.trim="form.email" data-testid="profile-email" /></el-form-item>
          <el-form-item label="手机号" prop="phone"><el-input v-model.trim="form.phone" data-testid="profile-phone" maxlength="11" /></el-form-item>
          <el-form-item label="性别"><el-select v-model="form.gender" clearable><el-option label="男" value="male" /><el-option label="女" value="female" /><el-option label="保密" value="private" /></el-select></el-form-item>
          <el-form-item label="生日"><el-date-picker v-model="form.birthday" type="date" value-format="yyyy-MM-dd" placeholder="选择日期" /></el-form-item>
          <el-form-item label="地址" class="wide"><el-input v-model.trim="form.address" maxlength="200" /></el-form-item>
          <el-form-item label="个人简介" class="wide"><el-input v-model="form.bio" type="textarea" :rows="4" maxlength="200" show-word-limit /></el-form-item>
          <el-form-item class="wide"><el-button data-testid="profile-save" type="primary" :loading="savingProfile" @click="saveProfile">保存资料</el-button></el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="修改密码" name="password">
        <el-form ref="passwordForm" :model="passwordForm" :rules="passwordRules" label-width="100px" class="password-form">
          <el-form-item label="原密码" prop="old_password"><el-input v-model="passwordForm.old_password" type="password" show-password /></el-form-item>
          <el-form-item label="新密码" prop="new_password"><el-input v-model="passwordForm.new_password" type="password" show-password /></el-form-item>
          <el-form-item label="确认密码" prop="confirm_password"><el-input v-model="passwordForm.confirm_password" type="password" show-password /></el-form-item>
          <el-form-item><el-button type="primary" :loading="savingPassword" @click="changePassword">修改密码</el-button></el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
    <avatar-editor :visible.sync="avatarVisible" :saving="savingAvatar" @save="uploadAvatar" />
  </section>
</template>

<script>
import AvatarEditor from '@/components/AvatarEditor.vue'
import { isEmail, isMainlandPhone } from '@/utils/profile'

const emptyForm = () => ({ username: '', nickname: '', email: '', phone: '', gender: '', birthday: null, address: '', bio: '', avatar: '', roles: [], must_change_password: false })

export default {
  name: 'ProfileView', components: { AvatarEditor },
  data() {
    const confirmPassword = (rule, value, callback) => value !== this.passwordForm.new_password ? callback(new Error('两次输入的新密码不一致')) : callback()
    const emailValidator = (rule, value, callback) => isEmail(value) ? callback() : callback(new Error('请输入正确邮箱'))
    const phoneValidator = (rule, value, callback) => isMainlandPhone(value) ? callback() : callback(new Error('请输入正确的中国大陆手机号'))
    return {
      loading: false, savingProfile: false, savingPassword: false, savingAvatar: false, avatarVisible: false,
      activeTab: this.$route.query.forcePassword ? 'password' : 'profile', form: emptyForm(),
      passwordForm: { old_password: '', new_password: '', confirm_password: '' },
      profileRules: {
        nickname: [{ max: 50, message: '昵称最多 50 个字符', trigger: 'blur' }],
        email: [{ validator: emailValidator, trigger: 'blur' }],
        phone: [{ validator: phoneValidator, trigger: 'blur' }]
      },
      passwordRules: {
        old_password: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
        new_password: [{ required: true, message: '请输入新密码', trigger: 'blur' }, { min: 8, message: '密码至少 8 位', trigger: 'blur' }],
        confirm_password: [{ required: true, message: '请再次输入新密码', trigger: 'blur' }, { validator: confirmPassword, trigger: 'blur' }]
      }
    }
  },
  computed: {
    mustChange() { return Boolean(this.form.must_change_password) },
    avatarText() { return (this.form.nickname || this.form.username || 'U').slice(0, 1).toUpperCase() },
    roleText() { return this.form.roles && this.form.roles.length ? this.form.roles.join('、') : '未分配角色' }
  },
  created() { this.fetchProfile() },
  methods: {
    async fetchProfile() {
      this.loading = true
      try { const response = await this.$http.get('/api/profile/'); this.form = Object.assign(emptyForm(), response.data.data); this.$store.commit('setUser', this.form); if (this.mustChange) this.activeTab = 'password' }
      finally { this.loading = false }
    },
    saveProfile() {
      this.$refs.profileForm.validate(async valid => {
        if (!valid) return
        this.savingProfile = true
        try { const response = await this.$http.put('/api/profile/', this.form); this.form = Object.assign(emptyForm(), response.data.data); this.$store.commit('setUser', this.form); this.$message.success('资料保存成功') }
        catch (error) { this.$message.error((error.response && error.response.data && error.response.data.msg) || '保存失败') }
        finally { this.savingProfile = false }
      })
    },
    changePassword() {
      this.$refs.passwordForm.validate(async valid => {
        if (!valid) return
        this.savingPassword = true
        try { await this.$http.post('/api/profile/password/', this.passwordForm); this.$message.success('密码修改成功，请重新登录'); this.$store.dispatch('logout'); this.$router.replace('/login') }
        catch (error) { this.$message.error((error.response && error.response.data && error.response.data.msg) || '密码修改失败') }
        finally { this.savingPassword = false }
      })
    },
    async uploadAvatar(blob) {
      this.savingAvatar = true
      const data = new FormData(); data.append('avatar', blob, 'avatar.webp')
      try { const response = await this.$http.post('/api/profile/avatar/', data); this.form = Object.assign(emptyForm(), response.data.data); this.$store.commit('setUser', this.form); this.avatarVisible = false; this.$message.success('头像保存成功') }
      finally { this.savingAvatar = false }
    },
    deleteAvatar() {
      this.$confirm('确定恢复默认头像吗？', '提示', { type: 'warning' }).then(async () => { await this.$http.delete('/api/profile/avatar/'); this.form.avatar = ''; this.$store.commit('setUser', Object.assign({}, this.form)); this.$message.success('已恢复默认头像') }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.profile-page { max-width: 1050px; margin: auto; }.profile-head { display: flex; align-items: center; gap: 18px; padding-bottom: 22px; border-bottom: 1px solid #ebeef5; }.profile-head h2 { margin: 0 0 8px; }.profile-head p { margin: 0; color: #909399; }.avatar-actions { margin-left: auto; }.el-alert { margin: 20px 0; }.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 22px; max-width: 850px; margin-top: 20px; }.wide { grid-column: 1 / -1; }.password-form { max-width: 520px; margin-top: 24px; }
@media (max-width: 700px) { .profile-head { flex-wrap: wrap; }.avatar-actions { width: 100%; margin-left: 0; }.form-grid { display: block; } }
</style>
