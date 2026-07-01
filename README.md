# EduAgent

基于大模型的个性化学习多智能体系统 — 一键 Docker 部署

---

## 快速开始（3 步，5 分钟）

### 第 1 步：配置 API Key

在项目目录下，复制环境变量模板：

```
cp .env.example .env
```

用记事本（或任意编辑器）打开 `.env` 文件，把 `LLM_API_KEY` 改成你自己的 OpenAI 兼容 API Key：

```env
LLM_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

> **哪里获取 API Key？** 如果你用的是 OpenCode 套餐，在 OpenCode 设置页面可以找到。如果你用 DeepSeek，去 platform.deepseek.com 注册获取。如果你用 OpenAI，去 platform.openai.com 获取。

### 第 2 步：启动服务

打开终端（PowerShell 或 WSL），进入项目目录，输入：

```
docker compose up -d
```

首次运行会自动下载镜像、安装依赖、初始化数据库。等待约 2-3 分钟。

### 第 3 步：打开浏览器

| 地址 | 功能 |
|------|------|
| http://localhost | 前端页面 |
| http://localhost:8000/docs | 后端 API 文档 |

**默认账号**: `admin` / `admin123`

---

## 前置要求

### Windows 用户（Docker Desktop）

1. 下载安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. 安装后启动 Docker Desktop，等待右下角图标变绿
3. 打开 PowerShell 或命令提示符，输入 `docker --version` 确认安装成功

### WSL 用户

1. 在 WSL 终端中安装 Docker：
   ```bash
   sudo apt update && sudo apt install docker.io docker-compose-v2 -y
   sudo usermod -aG docker $USER
   # 重新登录 WSL 使权限生效
   ```
2. 启动 Docker 服务：`sudo service docker start`
3. 验证：`docker --version`

---

## 组员使用指南

### 方式 A：从 GitHub 克隆（推荐）

```bash
git clone https://github.com/Hexingxing-26/EduAgent.git
cd EduAgent
cp .env.example .env          # 编辑 .env 填入 API Key
docker compose up -d           # 一键启动
```

### 方式 B：从压缩包部署

如果你收到了 `eduagent-dist.tar.gz` 文件：

**Windows (PowerShell):**
```powershell
tar -xzf eduagent-dist.tar.gz
cd eduagent-dist
notepad .env                   # 编辑填入 API Key
docker compose up -d
```

**WSL / Linux / Mac:**
```bash
tar -xzf eduagent-dist.tar.gz
cd eduagent-dist
nano .env                      # 编辑填入 API Key
docker compose up -d
```

---

## 停止和重启

```bash
docker compose down            # 停止服务
docker compose up -d           # 重新启动（数据不丢失）
docker compose down -v         # 完全清除（包括数据库数据）
```

---

## 默认账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| student1 | 123456 | 学生 |

---

## 环境变量说明

| 变量 | 说明 | 示例 |
|------|------|------|
| LLM_API_KEY | LLM API 密钥（必填） | sk-xxxx |
| LLM_BASE_URL | OpenAI 兼容接口地址 | https://api.openai.com/v1 |
| LLM_MODEL | 模型名称 | gpt-4o |
| DATABASE_URL | 数据库连接 | sqlite:///./edu_agent.db |
| JWT_SECRET_KEY | JWT 密钥（必填） | 随机字符串 32 位以上 |
| BACKEND_PORT | 后端端口 | 8000 |
| FRONTEND_PORT | 前端端口 | 80 |

---

## 常见问题

**Q: 启动后访问 localhost 显示"无法连接"？**
A: 等待 1-2 分钟，首次启动需要初始化数据库和下载模型。可以用 `docker compose logs backend` 查看后端日志。

**Q: AI 聊天无回复？**
A: 检查 `.env` 中的 `LLM_API_KEY` 是否正确。查看日志：`docker compose logs backend | grep ERROR`

**Q: Docker Desktop 提示"WSL integration not enabled"？**
A: 打开 Docker Desktop → Settings → Resources → WSL Integration → 启用你的 WSL 发行版

**Q: 端口被占用？**
A: 修改 `.env` 中的 `BACKEND_PORT` 和 `FRONTEND_PORT`，然后重新 `docker compose up -d`

---

## 技术栈

Python 3.11 / FastAPI / LangGraph / FAISS / Vue 3 / Element Plus / SQLite / Docker / nginx

## License

MIT
