# 手动配置与启动（Windows）

本教程用于学习每个步骤、调试、排错和自定义配置。选择本流程后，不要运行 `start.bat` 或 `start.ps1`。

手动方式可以自由设置：

- MySQL 数据库名称、专用账号、密码、主机和端口
- Django 超级管理员的用户名、邮箱和密码
- Django 后端运行端口
- Vue 前端运行端口
- 前端开发代理连接的后端地址

下面先给出可直接照做的默认示例，再说明如何替换为自己的配置。

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

### 自定义数据库名称和账号

数据库名、账号和密码可以自行命名。例如希望使用数据库 `my_manager_db`、账号 `my_manager_user`，可执行：

```sql
CREATE DATABASE IF NOT EXISTS my_manager_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'my_manager_user'@'localhost' IDENTIFIED BY 'MyStrongPassword_123';
ALTER USER 'my_manager_user'@'localhost' IDENTIFIED BY 'MyStrongPassword_123';
GRANT ALL PRIVILEGES ON my_manager_db.* TO 'my_manager_user'@'localhost';
FLUSH PRIVILEGES;
```

然后把项目根目录 `.env` 中对应内容改成：

```dotenv
MYSQL_DATABASE=my_manager_db
MYSQL_USER=my_manager_user
MYSQL_PASSWORD=MyStrongPassword_123
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

SQL 中的数据库名、账号、密码必须与 `.env` 完全一致。如果 MySQL 使用的不是 `3306`，同时修改 `MYSQL_PORT`。

## 第 3 步：启动后端

终端一：

```powershell
cd backend
python manage.py migrate
python manage.py init_system
python manage.py createsuperuser
python manage.py runserver
```

后台地址：`http://127.0.0.1:8000/admin/`。

执行 `python manage.py createsuperuser` 时，Django 会提示输入用户名、邮箱和密码，这些内容都可以自行设置。创建完成后，该账号既可以登录 Django Admin，也可以登录前端系统。

希望后端使用其他端口时，把最后一条命令改为类似：

```powershell
python manage.py runserver 127.0.0.1:9000
```

此时 Django Admin 地址变为 `http://127.0.0.1:9000/admin/`。

## 第 4 步：启动前端

终端二：

```powershell
cd frontend
npm install
npm run serve
```

前端地址：`http://127.0.0.1:8080/`。

### 自定义前端和后端端口

假设后端改为 `9000`，前端希望使用 `9090`，请在前端终端执行：

```powershell
cd frontend
$env:VUE_APP_API_TARGET='http://127.0.0.1:9000'
npm run serve -- --host 127.0.0.1 --port 9090
```

登录地址相应变为：

```text
http://127.0.0.1:9090/#/login
```

同时把根目录 `.env` 的前端可信来源改为实际端口：

```dotenv
DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:9090,http://127.0.0.1:9090
```

`VUE_APP_API_TARGET` 必须指向真实的 Django 后端地址，否则前端页面可以打开，但登录会提示无法连接后端。

## 以后再次启动（只需这两步）

第一次已经完成虚拟环境、依赖、数据库迁移和管理员创建后，再次启动时不需要重复安装。

如果一直使用默认端口，先在项目根目录打开终端一，启动后端：

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

如果使用自定义端口，再次启动时也要使用相同端口。例如后端 `9000`、前端 `9090`：

终端一：

```powershell
.\.venv\Scripts\python.exe backend\manage.py runserver 127.0.0.1:9000
```

终端二：

```powershell
cd frontend
$env:VUE_APP_API_TARGET='http://127.0.0.1:9000'
npm run serve -- --host 127.0.0.1 --port 9090
```

只有在 `requirements.txt`、`package-lock.json` 或数据库模型发生变化时，才需要重新安装依赖或执行迁移。

## 怎样停止项目

在后端和前端两个终端中分别按 `Ctrl + C`。关闭浏览器不会停止服务。

如果再次启动时出现端口占用，先检查是否还有旧的 Django、Vue 或 IIS 服务正在使用 `8000`、`8080`。手动启动时请确认终端最终显示 `http://127.0.0.1:8080/`；如果 Vue 提示改用 `8081`，应停止它、释放 `8080` 后再运行。

## 手动测试账号

测试账号不是手动启动的必需步骤。需要自动化测试账号时，在后端终端执行：

```powershell
python manage.py seed_e2e
```

账号为 `e2e_admin / E2E_Admin!234` 和 `e2e_user / E2E_Temp!234`。
