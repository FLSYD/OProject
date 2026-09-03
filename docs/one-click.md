# 一键配置与启动（Windows）

这是完全自动的启动流程。不要提前创建或激活虚拟环境，也不要再执行手动教程中的命令。

## 第 1 步：准备 MySQL

使用 MySQL 管理员执行：

```sql
CREATE DATABASE IF NOT EXISTS oproject_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'oproject_user'@'localhost' IDENTIFIED BY 'OProject_Test_9vK4_r2L';
ALTER USER 'oproject_user'@'localhost' IDENTIFIED BY 'OProject_Test_9vK4_r2L';
GRANT ALL PRIVILEGES ON oproject_db.* TO 'oproject_user'@'localhost';
FLUSH PRIVILEGES;
```

## 第 2 步：运行脚本

在项目根目录双击 `start.bat`，或执行：

```powershell
.\start.ps1
```

脚本会自动完成：

1. 创建 `.venv`（优先使用 Python 3.10）
2. 创建 `.env`
3. 按需安装后端和前端依赖
4. 执行数据库迁移和系统初始化
5. 创建管理员账号
6. 自动选择未被占用的后端和前端端口
7. 验证“前端 → 后端 → MySQL”的登录链路
8. 打开正确的前端登录页

## 第 3 步：登录

脚本优先使用后端 `8000`、前端 `8080`。如果端口已被其他项目占用，会自动选择可用端口，并在服务真正启动后打开浏览器。请以脚本最后显示的实际地址为准。

网页登录信息：

```text
登录入口：脚本显示并自动打开的 WEB APPLICATION LOGIN 地址
用户名：admin
密码：Admin@123456
```

Django Admin 使用同一账号，入口为脚本单独显示的 `DJANGO ADMIN` 地址。

脚本重复运行时会自动确保 `admin` 账号可以使用上述密码登录。生产环境请修改脚本和密码。

## 出错时

脚本失败时窗口会保留错误信息。重点检查：

- `python` 或 `py -3.10` 是否可用
- `npm` 是否可用
- MySQL 是否启动
- 根目录 `.env` 中的数据库配置是否正确
- 是否保留了以前启动的 Django/Vue 窗口（脚本会自动避开其端口）

修正后重新双击 `start.bat` 即可，不需要手动清理虚拟环境。
