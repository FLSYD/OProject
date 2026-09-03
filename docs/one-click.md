# 一键配置与启动（Windows）

这是按项目默认约定执行的自动启动流程，适合希望尽快运行项目的新手。它的自定义能力有限，请严格按照本页的数据库名称、数据库账号、端口和操作顺序执行，不要把手动教程中的自定义命令混入此流程。

一键方式固定使用以下约定：

```text
数据库：oproject_db
数据库账号：oproject_user
数据库密码：OProject_Test_9vK4_r2L
前端端口：8080
管理员账号：admin
管理员密码：Admin@123456
```

如果需要修改数据库名称、数据库账号、运行端口或管理员信息，请不要使用一键脚本，改用[手动配置与启动](manual.md)。

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
6. 固定使用前端 `8080`，并为后端选择可用端口
7. 验证“前端 → 后端 → MySQL”的登录链路
8. 打开正确的前端登录页

## 第 3 步：登录

前端登录地址固定为 `http://127.0.0.1:8080/#/login`，不会自动变成 `8081`。后端优先使用 `8000`；如果后端端口被占用，脚本会自动选择可用端口并正确配置前端代理。

如果前端 `8080` 已被旧 Vue 进程、IIS 或其他程序占用，脚本会停止并提示释放端口。关闭占用程序后重新双击 `start.bat` 即可。

网页登录信息：

```text
登录入口：http://127.0.0.1:8080/#/login
用户名：admin
密码：Admin@123456
```

Django Admin 使用同一账号，入口为脚本单独显示的 `DJANGO ADMIN` 地址。

脚本重复运行时会自动确保 `admin` 账号可以使用上述密码登录。生产环境请修改脚本和密码。

## 以后再次启动

第一次运行成功后，虚拟环境、依赖、数据库配置和管理员账号都已经准备好了。以后启动项目仍然只需：

1. 确认上一次打开的后端和前端终端已经关闭。
2. 回到项目根目录，双击 `start.bat`。
3. 等待脚本显示 `All services are ready and login was verified.`，浏览器会自动打开登录页。

脚本会复用现有 `.venv`、`.env` 和 `node_modules`，依赖没有变化时不会重新安装。现有版本的迁移和初始化步骤可以重复执行，不会重建数据库或重复创建基础数据。

仍可直接使用：

```text
前端账号：admin
前端密码：Admin@123456
Django Admin 账号：admin
Django Admin 密码：Admin@123456
```

## 怎样停止项目

一键脚本会打开两个服务窗口：

- Django 后端窗口
- Vue 前端窗口

需要停止项目时，在这两个窗口中分别按 `Ctrl + C`，看到程序停止后即可关闭窗口。只关闭浏览器页面不会停止项目，也不会释放 `8000` 和 `8080` 端口。

如果直接关闭了两个服务窗口，也可以停止项目；下次仍然双击 `start.bat` 即可重新启动。

不要在项目已经运行时重复双击 `start.bat`。脚本检测到 `8080` 已被占用后会停止，避免误启动到 `8081`。

## 出错时

脚本失败时窗口会保留错误信息。重点检查：

- `python` 或 `py -3.10` 是否可用
- `npm` 是否可用
- MySQL 是否启动
- 根目录 `.env` 中的数据库配置是否正确
- 是否保留了以前启动的 Django/Vue 窗口（脚本会自动避开其端口）
- 浏览器打开的是 IIS 页面：说明 `8080` 被 IIS 占用，请停止绑定 `8080` 的 IIS 站点，再重新运行脚本

修正后重新双击 `start.bat` 即可，不需要手动清理虚拟环境。
