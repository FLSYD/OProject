<template>
  <div v-loading="loading" class="profile-page">
    <el-card v-if="mustChange" class="page-card initial-password-card">
      <h1>设置新密码</h1>
      <p>当前使用的是临时密码，完成修改后才能进入系统</p>
      <el-alert title="首次登录必须先修改初始密码，成功后请使用新密码重新登录。" type="warning" :closable="false" show-icon />
      <password-form-panel :form="passwordForm" :rules="passwordRules" :loading="savingPassword" :initial="true" @submit="changePassword" />
    </el-card>

    <template v-else-if="form.username">
      <el-card class="page-card profile-card">
        <div slot="header" class="profile-card-header"><span><i class="el-icon-user" />个人信息</span><small>管理个人资料与账号安全</small></div>

        <el-tabs v-model="activeTab" class="profile-tabs">
          <el-tab-pane name="basic">
            <span slot="label"><i class="el-icon-user" /> 基本资料</span>
            <div class="profile-hero">
              <div class="avatar-wrap">
                <el-avatar :size="112" :src="form.avatar"><span>{{ avatarText }}</span></el-avatar>
                <el-button data-testid="avatar-edit" class="avatar-edit" type="primary" circle icon="el-icon-camera" title="编辑头像" @click="avatarVisible = true" />
              </div>
              <div class="identity">
                <h2>{{ form.nickname || form.username }}</h2>
                <p>@{{ form.username }}</p>
                <el-tag v-for="role in form.roles" :key="role" :type="role === '超级管理员' ? 'warning' : ''" :effect="role === '超级管理员' ? 'dark' : 'plain'" :class="{ 'super-admin-tag': role === '超级管理员' }"><i v-if="role === '超级管理员'" class="el-icon-star-on" />{{ role }}</el-tag>
              </div>
              <div class="hero-actions">
                <el-button data-testid="profile-edit" type="primary" icon="el-icon-edit-outline" @click="openEdit">编辑资料</el-button>
                <el-button v-if="form.avatar" data-testid="avatar-delete" type="danger" plain icon="el-icon-delete" @click="deleteAvatar">恢复默认头像</el-button>
              </div>
            </div>

            <div class="section-title"><i class="el-icon-info" /><span><b>基本资料</b><small>当前账号的联系信息与个人介绍</small></span></div>
            <el-descriptions :column="2" border class="details">
              <el-descriptions-item label="用户名"><span class="detail-value">{{ form.username }}</span><el-tag size="mini" type="info" class="login-tag">登录账号</el-tag></el-descriptions-item>
              <el-descriptions-item label="昵称">{{ form.nickname || '未填写' }}</el-descriptions-item>
              <el-descriptions-item label="邮箱"><i class="detail-icon el-icon-message" />{{ form.email || '未填写' }}</el-descriptions-item>
              <el-descriptions-item label="手机号"><i class="detail-icon el-icon-phone" />{{ form.phone || '未填写' }}</el-descriptions-item>
              <el-descriptions-item label="性别">{{ genderText }}</el-descriptions-item>
              <el-descriptions-item label="生日"><i class="detail-icon el-icon-date" />{{ form.birthday || '未填写' }}</el-descriptions-item>
              <el-descriptions-item label="地址" :span="2"><i class="detail-icon el-icon-location-outline" />{{ form.address || '未填写' }}</el-descriptions-item>
              <el-descriptions-item label="个人简介" :span="2">{{ form.bio || '这个人很低调，还没有填写简介。' }}</el-descriptions-item>
              <el-descriptions-item label="注册时间">{{ formatDate(form.created_at) }}</el-descriptions-item>
              <el-descriptions-item label="更新时间">{{ formatDate(form.updated_at) }}</el-descriptions-item>
            </el-descriptions>
          </el-tab-pane>

          <el-tab-pane name="password">
            <span slot="label"><i class="el-icon-lock" /> 修改密码</span>
            <div class="password-pane">
              <div class="card-title"><span class="title-icon"><i class="el-icon-lock" /></span><div><strong>修改登录密码</strong><small>定期更新密码可以保护账号安全</small></div></div>
              <el-alert title="修改密码后，当前账号的登录状态会立即失效，请使用新密码重新登录。" type="warning" :closable="false" show-icon />
              <password-form-panel :form="passwordForm" :rules="passwordRules" :loading="savingPassword" @submit="changePassword" />
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>

      <el-dialog title="编辑个人资料" :visible.sync="editVisible" width="620px" custom-class="profile-dialog">
        <el-form ref="profileForm" :model="editForm" :rules="profileRules" label-width="82px">
          <el-form-item label="用户名"><el-input :value="form.username" disabled /></el-form-item>
          <el-form-item label="昵称" prop="nickname"><el-input v-model.trim="editForm.nickname" data-testid="profile-nickname" maxlength="50" show-word-limit /></el-form-item>
          <el-form-item label="邮箱" prop="email"><el-input v-model.trim="editForm.email" data-testid="profile-email" /></el-form-item>
          <el-form-item label="手机号" prop="phone"><el-input v-model.trim="editForm.phone" data-testid="profile-phone" maxlength="11" /></el-form-item>
          <el-form-item label="性别"><el-radio-group v-model="editForm.gender"><el-radio label="male">男</el-radio><el-radio label="female">女</el-radio><el-radio label="private">保密</el-radio></el-radio-group></el-form-item>
          <el-form-item label="生日"><el-date-picker v-model="editForm.birthday" type="date" value-format="yyyy-MM-dd" placeholder="选择日期" /></el-form-item>
          <el-form-item label="地址"><el-input v-model.trim="editForm.address" maxlength="200" /></el-form-item>
          <el-form-item label="个人简介"><el-input v-model="editForm.bio" type="textarea" :rows="4" maxlength="200" show-word-limit /></el-form-item>
        </el-form>
        <span slot="footer"><el-button @click="editVisible = false">取消</el-button><el-button data-testid="profile-save" type="primary" :loading="savingProfile" @click="saveProfile">保存修改</el-button></span>
      </el-dialog>

      <avatar-editor :visible.sync="avatarVisible" :saving="savingAvatar" @save="uploadAvatar" />
    </template>

    <el-empty v-else-if="!loading" description="个人信息加载失败"><el-button type="primary" @click="fetchProfile">重新加载</el-button></el-empty>
  </div>
</template>

<script>
import AvatarEditor from '@/components/AvatarEditor.vue'
import PasswordFormPanel from '@/components/PasswordForm.vue'
import { isEmail, isMainlandPhone } from '@/utils/profile'

const emptyForm = () => ({ username: '', nickname: '', email: '', phone: '', gender: '', birthday: null, address: '', bio: '', avatar: '', roles: [], must_change_password: false, created_at: '', updated_at: '' })
const editableFields = profile => ({ nickname: profile.nickname || '', email: profile.email || '', phone: profile.phone || '', gender: profile.gender || '', birthday: profile.birthday || null, address: profile.address || '', bio: profile.bio || '' })

export default {
  name: 'ProfileView',
  components: { AvatarEditor, PasswordFormPanel },
  data() {
    const confirmPassword = (rule, value, callback) => value !== this.passwordForm.new_password ? callback(new Error('两次输入的新密码不一致')) : callback()
    const emailValidator = (rule, value, callback) => isEmail(value) ? callback() : callback(new Error('请输入正确邮箱'))
    const phoneValidator = (rule, value, callback) => isMainlandPhone(value) ? callback() : callback(new Error('请输入正确的中国大陆手机号'))
    return {
      loading: false, savingProfile: false, savingPassword: false, savingAvatar: false, avatarVisible: false, editVisible: false, activeTab: 'basic',
      form: emptyForm(), editForm: editableFields(emptyForm()),
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
    genderText() { return ({ male: '男', female: '女', private: '保密', '': '未填写' })[this.form.gender] || '未填写' }
  },
  created() { this.fetchProfile() },
  methods: {
    applyProfile(profile) { this.form = Object.assign(emptyForm(), profile); this.$store.commit('setUser', this.form) },
    async fetchProfile() {
      this.loading = true
      try { const response = await this.$http.get('/api/profile/'); this.applyProfile(response.data.data) }
      catch (error) { this.$message.error((error.response && error.response.data && error.response.data.msg) || '个人信息加载失败') }
      finally { this.loading = false }
    },
    openEdit() { this.editForm = editableFields(this.form); this.editVisible = true },
    saveProfile() {
      this.$refs.profileForm.validate(async valid => {
        if (!valid) return
        this.savingProfile = true
        try { const response = await this.$http.put('/api/profile/', this.editForm); this.applyProfile(response.data.data); this.editVisible = false; this.$message.success('资料保存成功') }
        catch (error) { this.$message.error((error.response && error.response.data && error.response.data.msg) || '保存失败') }
        finally { this.savingProfile = false }
      })
    },
    async changePassword() {
      this.savingPassword = true
      try { await this.$http.post('/api/profile/password/', this.passwordForm); this.$message.success(this.mustChange ? '密码设置成功，请使用新密码登录' : '密码修改成功，请重新登录'); this.$store.dispatch('logout'); this.$router.replace('/login') }
      catch (error) { this.$message.error((error.response && error.response.data && error.response.data.msg) || '密码修改失败') }
      finally { this.savingPassword = false }
    },
    async uploadAvatar(blob) {
      this.savingAvatar = true
      const data = new FormData(); data.append('avatar', blob, 'avatar.webp')
      try { const response = await this.$http.post('/api/profile/avatar/', data); this.applyProfile(response.data.data); this.avatarVisible = false; this.$message.success('头像保存成功') }
      catch (error) { this.$message.error((error.response && error.response.data && error.response.data.msg) || '头像上传失败') }
      finally { this.savingAvatar = false }
    },
    deleteAvatar() {
      this.$confirm('确定删除当前头像并恢复默认头像吗？', '恢复默认头像', { type: 'warning' }).then(async () => { await this.$http.delete('/api/profile/avatar/'); this.form.avatar = ''; this.$store.commit('setUser', Object.assign({}, this.form)); this.$message.success('已恢复默认头像') }).catch(() => {})
    },
    formatDate(value) { return value ? new Date(value).toLocaleString('zh-CN') : '—' }
  }
}
</script>

<style scoped>
.profile-page { min-height: 300px; }
.initial-password-card { width: min(500px, 100%); margin: 28px auto; }
.initial-password-card h1 { margin: 4px 0 8px; text-align: center; }
.initial-password-card > p { margin: 0 0 22px; text-align: center; color: var(--app-muted); }
.initial-password-card .el-alert, .password-pane .el-alert { margin-bottom: 24px; }
.profile-card { width: min(1120px, 100%); margin: 0 auto; overflow: hidden; }
.profile-card >>> .el-card__header { padding: 20px 26px; border-bottom-color: #edf0f5; }
.profile-card >>> .el-card__body { padding: 0 26px 28px; }
.profile-card-header { display: flex; align-items: center; justify-content: space-between; }
.profile-card-header > span { color: #283147; font-size: 18px; font-weight: 700; }
.profile-card-header > span i { margin-right: 8px; color: var(--app-primary); }
.profile-card-header small { color: var(--app-muted); font-size: 12px; }
.profile-tabs >>> .el-tabs__header { margin: 0 0 24px; }
.profile-tabs >>> .el-tabs__item { height: 52px; padding: 0 24px; font-weight: 600; line-height: 52px; }
.profile-tabs >>> .el-tabs__item i { margin-right: 4px; }
.profile-tabs >>> .el-tabs__active-bar { height: 3px; border-radius: 3px; }
.profile-hero { display: flex; align-items: center; gap: 24px; margin-bottom: 27px; padding: 24px 26px; background: linear-gradient(135deg, rgba(102,126,234,.09), rgba(118,75,162,.07)); border: 1px solid rgba(101,113,221,.1); border-radius: 14px; }
.avatar-wrap { position: relative; flex: 0 0 auto; }
.avatar-wrap >>> .el-avatar { color: #fff; font-size: 38px; background: linear-gradient(135deg, var(--app-primary), #825bc0); border: 4px solid #fff; box-shadow: 0 8px 24px rgba(89,104,232,.24); }
.avatar-edit { position: absolute; right: -2px; bottom: 3px; }
.identity h2 { margin: 0 0 5px; font-size: 25px; }
.identity p { margin: 0 0 10px; color: var(--app-muted); }
.identity .el-tag { margin-right: 7px; }
.identity .el-tag i { margin-right: 5px; }
.identity .super-admin-tag { color: #fff; background: #f59e0b; border-color: #f59e0b; font-weight: 700; box-shadow: 0 4px 12px rgba(245,158,11,.25); }
.hero-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-left: auto; }
.hero-actions .el-button { margin: 0; }
.section-title { display: flex; align-items: center; gap: 10px; margin: 0 0 14px; }
.section-title > i { display: grid; place-items: center; width: 34px; height: 34px; color: var(--app-primary); background: #eef0ff; border-radius: 9px; }
.section-title > span { display: grid; gap: 2px; }
.section-title b { color: #31394c; font-size: 15px; }
.section-title small { color: var(--app-muted); font-size: 12px; }
.details { overflow: hidden; border-radius: 9px; }
.details >>> .el-descriptions__label { width: 100px; color: #667085; font-weight: 600; background: #fafbfc; }
.details >>> .el-descriptions__content { color: #30384c; }
.detail-icon { margin-right: 6px; color: #9aa2b4; }
.detail-value { margin-right: 9px; }
.login-tag { vertical-align: middle; }
.password-pane { width: min(620px, 100%); margin: 6px auto 12px; padding: 22px 0 6px; }
.card-title { display: flex; align-items: center; gap: 12px; }
.card-title div { display: grid; gap: 3px; }
.card-title strong { font-size: 17px; }
.card-title small { color: var(--app-muted); font-weight: 400; }
.title-icon { width: 38px; height: 38px; display: grid; place-items: center; flex: 0 0 auto; border-radius: 11px; color: #fff; background: linear-gradient(135deg, var(--app-primary), #825bc0); box-shadow: 0 7px 16px rgba(89,104,232,.24); }
.password-pane .card-title { margin-bottom: 22px; }
.password-pane >>> .password-form { max-width: none; }
.password-pane >>> .password-form .el-input__inner { height: 42px; border-radius: 8px; }
.password-pane >>> .password-form .el-button { min-width: 112px; height: 40px; border-radius: 8px; }
.profile-page >>> .profile-dialog { width: min(620px, 94vw) !important; }
@media (max-width: 700px) { .profile-card >>> .el-card__header { padding: 17px 18px; } .profile-card >>> .el-card__body { padding: 0 18px 20px; } .profile-card-header small { display: none; } .profile-tabs >>> .el-tabs__item { padding: 0 15px; } .profile-hero { flex-direction: column; gap: 15px; padding: 24px 18px; text-align: center; } .hero-actions { margin-left: 0; justify-content: center; } .details >>> .el-descriptions__body { overflow: auto; } .password-pane { padding-top: 8px; } }
</style>
