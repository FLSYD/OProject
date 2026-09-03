# 手动配置与启动（Windows）

本教程用于学习每个步骤、调试和排错。选择本流程后，不要运行 `start.bat` 或 `start.ps1`。

## 第 1 步：创建并激活虚拟环境

在项目根目录执行：

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

如果没有 `py` 启动器，可使用 `python -m venv .venv`，但请确认 `python --version` 为 3.10 或更高版本。看到命令行前出现 `(.venv)` 即表示激活成功。

## 第 2 步：配置 MySQL

使用 MySQL 管理员执行：

```sql
CREATE DATABASE IF NOT EXISTS oproject_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'oproject_user'@'localhost' IDENTIFIED BY 'OProject_Test_9vK4_r2L';
ALTER USER 'oproject_user'@'localhost' IDENTIFIED BY 'OProject_Test_9vK4_r2L';
GRANT ALL PRIVILEGES ON oproject_db.* TO 'oproject_user'@'localhost';
FLUSH PRIVILEGES;
```

复制 `.env.example` 为 `.env`，填写对应连接参数。

## 第 3 步：启动后端

终端一：

```powershell
cd OProject\backend
python manage.py migrate
python manage.py init_system
python manage.py createsuperuser
python manage.py runserver
```

后台地址：`http://127.0.0.1:8000/admin/`。

## 第 4 步：启动前端

终端二：

```powershell
cd OProject\frontend
npm install
npm run serve
```

前端地址：`http://127.0.0.1:8080/`。

## 以后再次启动（只需这两步）

第一次已经完成虚拟环境、依赖、数据库迁移和管理员创建后，再次启动时不需要重复安装。

先在项目根目录打开终端一，启动后端：

```powershell
.\.venv\Scripts\python.exe backend\manage.py runserver 127.0.0.1:8000
```

再在项目根目录打开终端二，启动前端：

```powershell
cd frontend
npm run serve
```

然后访问：

```text
前端登录：http://127.0.0.1:8080/#/login
Django Admin：http://127.0.0.1:8000/admin/
```

只有在 `requirements.txt`、`package-lock.json` 或数据库模型发生变化时，才需要重新安装依赖或执行迁移。

## 怎样停止项目

在后端和前端两个终端中分别按 `Ctrl + C`。关闭浏览器不会停止服务。

如果再次启动时出现端口占用，先检查是否还有旧的 Django、Vue 或 IIS 服务正在使用 `8000`、`8080`。不要直接连续启动多份项目，否则 Vue 可能自动改用 `8081`。

## 手动测试账号

测试账号不是手动启动的必需步骤。需要自动化测试账号时，在后端终端执行：

```powershell
python manage.py seed_e2e
```

账号为 `e2e_admin / E2E_Admin!234` 和 `e2e_user / E2E_Temp!234`。
