# OProject：经典 Django + Vue 2 管理系统模板

这是一个面向新手的前后端分离教学模板，包含登录、主界面、个人信息、头像编辑和基础角色权限。

> Django 5.0.7 和 Vue 2 已停止维护，本项目用于学习旧架构，不建议直接用于长期生产环境。

## 启动教程（两种方式完全分开）

请选择一种方式，不要同时执行：

- [一键配置与启动](docs/one-click.md)：推荐新手使用，只需运行一个脚本。
- [手动配置与启动](docs/manual.md)：用于学习每一步、调试和排错。

## 数据库参数

本地教学验证使用以下专用 MySQL 账号：

```text
数据库：oproject_db
用户：oproject_user
密码：OProject_Test_9vK4_r2L
主机：127.0.0.1
端口：3306
```

创建数据库后，将 `.env.example` 复制为 `.env`。完整 SQL 和操作顺序请查看上面的启动教程。

一键脚本会自动检测端口占用，等待前后端服务就绪，验证登录链路，再打开正确的前端登录地址；不要根据固定端口猜测访问地址。

## 测试账号（仅自动化验收使用）

运行测试流程后可使用：

```text
管理员：e2e_admin / E2E_Admin!234
普通用户：e2e_user / E2E_Temp!234
普通用户首次登录新密码示例：E2E_New!2345
```

## 其他文档

- [架构导读](docs/architecture.md)
- [API 说明](docs/api.md)
- [验收清单](docs/acceptance.md)

## GitHub

[FLSYD/OProject](https://github.com/FLSYD/OProject)
