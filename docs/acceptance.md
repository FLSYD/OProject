# 验收清单

## 自动化命令

Windows 可先在项目根目录运行 `start.bat` 完成环境配置和服务启动；脚本会自动创建 `.venv`、安装依赖、迁移数据库，并在没有管理员时引导创建管理员，因此不需要手动输入虚拟环境命令。

真实 MySQL 验收使用 README 中已写明的本机专用连接：数据库 `oproject_db`，用户 `oproject_user`，密码 `OProject_Test_9vK4_r2L`，主机 `127.0.0.1:3306`。这是本地教学密码，部署到其他环境前必须更换。

运行下面命令前，请先在项目根目录创建并激活虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
```

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

执行 `backend\manage.py seed_e2e` 后，管理员测试账号为 `e2e_admin / E2E_Admin!234`，普通用户测试账号为 `e2e_user / E2E_Temp!234`。普通用户首次登录需修改为新密码（示例：`E2E_New!2345`）。

后台 Admin 登录必须使用 `e2e_admin`，不能使用普通用户；前端登录入口是 `http://127.0.0.1:8080/#/login`，后台入口是 `http://127.0.0.1:8000/admin/`。

注意：`seed_e2e` 仅用于自动化测试。如果只是运行后台管理，不要执行此命令；请使用 `python manage.py migrate`、`python manage.py init_system` 和 `python manage.py createsuperuser`。

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
