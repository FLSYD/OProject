# API 说明

统一前缀为 `/api/`，成功与失败都使用 `{ "code", "msg", "data" }`。除登录和健康检查外，请求头需包含 `Authorization: Bearer <token>`。

| 方法 | 地址 | 权限 | 主要参数 |
|---|---|---|---|
| POST | `/api/login/` | 公开 | `username`、`password` |
| GET | `/api/menu/` | 已登录且已完成首次改密 | 无 |
| GET | `/api/profile/` | 已登录 | 无 |
| PUT | `/api/profile/` | 已登录 | `nickname`、`email`、`phone`、`gender`、`birthday`、`address`、`bio` |
| POST | `/api/profile/password/` | 已登录 | `old_password`、`new_password`、`confirm_password` |
| POST | `/api/profile/avatar/` | 已登录 | `multipart/form-data` 的 `avatar` 文件 |
| DELETE | `/api/profile/avatar/` | 已登录 | 无 |
| GET | `/api/example/` | 拥有 `example` 菜单 | 无 |
| GET | `/api/health/` | 公开 | 无 |

常见状态码：登录凭据错误或 Token 失效为 `401`；账号禁用、首次改密限制或角色权限不足为 `403`；表单和文件校验失败为 `400`。

头像原文件只能是经 Pillow 验证的 JPEG、PNG 或 WebP，最大 2MB；服务端最终保存为 320×320 WebP。
