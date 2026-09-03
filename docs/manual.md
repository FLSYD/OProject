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

## 手动测试账号

测试账号不是手动启动的必需步骤。需要自动化测试账号时，在后端终端执行：

```powershell
python manage.py seed_e2e
```

账号为 `e2e_admin / E2E_Admin!234` 和 `e2e_user / E2E_Temp!234`。
