# 架构导读

## 请求流向

```text
浏览器（Vue 2）
  └─ Axios 携带 sessionStorage 中的 Bearer Token
      └─ Django /api/
          ├─ VersionedJWTAuthentication：校验签名、有效期、账号状态和 token_version
          ├─ PasswordReadyPermission：首次改密前阻止普通功能
          └─ RequiredMenuPermission：按角色拥有的菜单编码校验接口
```

开发时，Vue CLI 把 `/api/` 与 `/media/` 代理到 `http://127.0.0.1:8000`。前后端代码互不导入，移动整个 `OProject` 目录后仍可独立安装。

## 后端文件定位

- `backend/djangoproject/settings.py`：单一配置入口，读取根目录 `.env`。
- `backend/djangoproject/urls.py`：Django Admin、API 和开发媒体路由。
- `backend/permission/models.py`：资料、角色与菜单三张业务模型。
- `backend/permission/views.py`：登录、菜单、资料、头像和示例接口。
- `backend/permission/authentication.py`：JWT 与 `token_version` 校验。
- `backend/permission/admin.py`：管理员创建账号并分配角色。
- `backend/permission/management/commands/init_system.py`：可重复执行的初始化命令。

## 前端文件定位

- `frontend/src/main.js`：Axios 请求头及 401/403 统一处理。
- `frontend/src/router/index.js`：固定路由、登录守卫、首次改密和菜单校验。
- `frontend/src/store/index.js`：当前用户、Token 和菜单状态。
- `frontend/src/views/Profile.vue`：资料表单与密码操作。
- `frontend/src/components/AvatarEditor.vue`：头像选择、拖动、触摸、缩放、旋转和导出。

## 首次改密流程

1. 管理员在 Django Admin 创建账号并选择角色。
2. 用户使用临时密码登录，Token 带有当前 `token_version`。
3. 前端强制进入个人信息的修改密码标签；后端同时拒绝菜单和示例接口。
4. 修改成功后 `must_change_password` 变为 `false`，`token_version` 加一。
5. 旧 Token 立即失效，用户必须使用新密码重新登录。
