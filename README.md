# OProject：经典 Django + Vue 2 管理系统模板

这是为新手准备的前后端分离教学模板。它保留旧项目容易理解的目录和 Options API 写法，仅包含登录、基础框架、个人信息和简单 RBAC 示例。

> 注意：Django 5.0.7 和 Vue 2 已停止维护。本项目用于理解旧架构，不建议直接作为长期生产项目。

## 目录结构

```text
OProject/
├─ backend/                 Django 后端
│  ├─ djangoproject/        settings.py、urls.py
│  ├─ permission/           用户资料、角色、菜单和 API
│  ├─ tests/                后端测试
│  └─ manage.py
├─ frontend/                Vue 2 前端
│  ├─ src/components/       顶栏、侧栏、头像编辑器
│  ├─ src/views/            登录、首页、示例、个人信息
│  ├─ src/router/           页面路由与登录守卫
│  ├─ src/store/            用户与菜单状态
│  └─ tests/                单元测试和浏览器测试
├─ docs/                    架构、接口与验收说明
└─ .env.example             环境变量示例
```

## 1. 创建 MySQL 数据库

为了让新手可以直接验证，本项目提供一组本机专用测试账号（仅适用于本地教学环境）：

| 配置项 | 值 |
|---|---|
| 数据库 | `oproject_db` |
| 用户 | `oproject_user` |
| 密码 | `OProject_Test_9vK4_r2L` |
| 主机/端口 | `127.0.0.1:3306` |

按下面 3 步操作即可：

### 第 1 步：创建数据库和专用账号

用 MySQL 管理员执行以下完整 SQL（账号和密码已经写好，不需要自行修改）：

```sql
CREATE DATABASE IF NOT EXISTS oproject_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'oproject_user'@'localhost' IDENTIFIED BY 'OProject_Test_9vK4_r2L';
ALTER USER 'oproject_user'@'localhost' IDENTIFIED BY 'OProject_Test_9vK4_r2L';
GRANT ALL PRIVILEGES ON oproject_db.* TO 'oproject_user'@'localhost';
FLUSH PRIVILEGES;
```

### 第 2 步：准备 `.env`

复制 `.env.example` 为 `.env`。示例文件已经填写好上表中的专用账号和密码，直接复制即可。`.env` 已被 Git 忽略，不会提交到仓库。

> 这组密码只用于本地教学。部署到其他电脑或生产环境时，请修改 `.env` 和 SQL 中的密码。

### 第 3 步：验证数据库连接

```powershell
cd OProject
.\.venv\Scripts\python.exe backend\manage.py check --database default
.\.venv\Scripts\python.exe backend\manage.py migrate --noinput
.\.venv\Scripts\python.exe backend\manage.py init_system
```

如果最后一条命令显示“角色和菜单初始化完成”，说明数据库配置正确。

## 2. 启动后端

```powershell
cd OProject
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\backend\requirements.txt
cd backend
python manage.py migrate
python manage.py init_system
python manage.py createsuperuser
python manage.py runserver
```

后台管理地址：`http://127.0.0.1:8000/admin/`。先创建普通账号并分配角色，普通账号首次登录必须修改临时密码。

管理员新建账号的顺序：进入“认证和授权 → 用户 → 增加用户”，填写用户名、唯一邮箱、临时密码并选择角色。系统会自动标记“首次需改密”，临时密码不会被明文保存。

## 3. 启动前端

另开一个终端：

```powershell
cd OProject\frontend
npm install
npm run serve
```

浏览器访问 `http://127.0.0.1:8080/`。

## 4. API

| 方法 | 地址 | 用途 |
|---|---|---|
| POST | `/api/login/` | 登录并获取 8 小时 access token |
| GET | `/api/menu/` | 获取当前用户菜单 |
| GET/PUT | `/api/profile/` | 获取、修改个人资料 |
| POST | `/api/profile/password/` | 修改密码并注销旧 Token |
| POST/DELETE | `/api/profile/avatar/` | 上传或删除头像 |
| GET | `/api/example/` | RBAC 示例接口 |
| GET | `/api/health/` | Django 和 MySQL 健康检查 |

所有响应采用 `{ code, msg, data }`。前端将 Token 放在 `sessionStorage`，关闭浏览器标签页后会话自动清除。

## 5. 测试

后端测试默认使用独立 SQLite，不会修改 MySQL：

```powershell
$env:DJANGO_USE_SQLITE='true'
python -m pytest backend
```

前端测试和构建：

```powershell
cd frontend
npm run test:unit
npm run build
npx playwright install chromium
$env:E2E_PYTHON='..\.venv\Scripts\python.exe'
npm run test:e2e
```

E2E 使用专用 SQLite 和测试账号，不会写入 MySQL。测试服务固定使用 `18000` 与 `18080` 端口，避免与日常开发端口冲突。

进一步说明见 [架构导读](docs/architecture.md)、[API 说明](docs/api.md) 和 [验收清单](docs/acceptance.md)。

## 常见问题

- `Access denied for user`：检查 `.env` 用户、密码、数据库名和 `GRANT` 是否一致。
- 前端请求 404：确认 Django 位于 8000 端口，Vue 开发服务器位于 8080 端口。
- 登录后立即回到登录页：Token 已过期或修改密码后版本失效，请重新登录。
- 看不到“权限示例”：在 Django Admin 中给账号角色分配 `example` 菜单。
- 图片上传失败：仅支持 JPEG、PNG、WebP，原文件不能超过 2MB。
