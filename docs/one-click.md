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
6. 打开后端和前端服务窗口

## 第 3 步：登录

```text
前端：http://127.0.0.1:8080/
后台：http://127.0.0.1:8000/admin/
管理员用户名：admin
管理员密码：Admin@123456
```

脚本重复运行时会自动确保 `admin` 账号可以使用上述密码登录。生产环境请修改脚本和密码。

## 出错时

脚本失败时窗口会保留错误信息。重点检查：

- `python` 或 `py -3.10` 是否可用
- `npm` 是否可用
- MySQL 是否启动
- 根目录 `.env` 中的数据库配置是否正确

修正后重新双击 `start.bat` 即可，不需要手动清理虚拟环境。
