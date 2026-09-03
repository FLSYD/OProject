# 验收清单

## 自动化命令

```powershell
$env:DJANGO_USE_SQLITE='true'
.\.venv\Scripts\python.exe backend\manage.py check
.\.venv\Scripts\python.exe backend\manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe -m pytest backend -q

cd frontend
npm run test:unit
npm run build
npm run test:e2e
```

## 手工浏览器检查

1. 在 Django Admin 创建普通用户，填写唯一邮箱、临时密码并选择普通用户角色。
2. 验证临时密码登录后只能进入个人信息和修改密码，不能打开权限示例。
3. 修改密码后验证旧 Token 失效，并使用新密码重新登录。
4. 编辑昵称、邮箱、手机号等资料，确认顶部用户名立即同步。
5. 分别通过点击和拖放选择头像，检查拖动、滚轮/按钮缩放、旋转、重置、方向键和触摸操作。
6. 上传头像后删除，确认页面和顶部恢复首字符默认头像。
7. 禁用账号后验证登录返回 403；移除 `example` 菜单后验证页面隐藏且接口返回 403。
8. 访问 `/api/health/`，确认 MySQL 状态为 `ok`。

## 独立性检查

- `.env`、数据库、媒体文件、`node_modules`、`dist` 和测试产物均不提交。
- 源码不包含旧项目绝对路径、旧数据库密码、学生管理或文件管理依赖。
- 依赖只从本目录的 `requirements.txt` 与 `package-lock.json` 安装。
