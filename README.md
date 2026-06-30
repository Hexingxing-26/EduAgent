# AI智能体模块 - AI_Agent_System

基于 FastAPI + LangGraph 构建的智能学习助手，包含5个协作Agent，为用户提供个性化学习资料生成和路径规划服务。

## 📋 项目简介

本模块采用多Agent协作架构，通过LangGraph编排5个专业Agent，实现从用户画像分析到学习路径规划的完整流程。

### 核心功能

- **用户画像分析**：基于教育心理学模型分析学习特征
- **知识检索(RAG)**：从知识库检索相关知识点
- **学习资料生成**：生成讲解文档、随堂测验、思维导图
- **内容审核**：确保生成内容的质量和准确性
- **学习路径规划**：制定个性化学习步骤

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI 接口层                           │
│                 POST /chat/stream (SSE)                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    LangGraph 工作流                         │
│  profile → rag → generator → guardrail → planner → END     │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Agent 核心层                             │
│  画像机器人 | RAG检索 | 资源生成 | 审核机器人 | 路径规划     │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    外部服务                                  │
│              讯飞星火大模型 API                              │
└─────────────────────────────────────────────────────────────┘
```

## 📁 项目结构

```
AI_Agent_System/
├── .env                    # 环境变量配置（不提交Git）
├── .env.example            # 环境变量模板
├── requirements.txt        # Python依赖清单
├── README.md               # 项目说明文档
├── API文档.md              # API接口文档（Markdown）
├── API文档.html            # API接口文档（HTML）
├── 启动服务器.bat          # Windows一键启动脚本
├── start.sh                # Linux/Mac一键启动脚本
├── test.py                 # 测试脚本
├── app/
│   ├── __init__.py         # 模块初始化
│   ├── main.py             # FastAPI入口 + API定义
│   ├── agents.py           # 5个Agent核心逻辑
│   ├── workflow.py         # LangGraph工作流编排
│   └── models.py           # 状态数据模型
└── data/
    └── demo.txt            # 知识库示例数据
```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- pip 包管理器

### 安装步骤

#### 方式一：一键启动（推荐）

**Windows 用户**：
```
双击运行：启动服务器.bat
```

**Linux / Mac 用户**：
```bash
chmod +x start.sh
./start.sh
```

一键脚本会自动完成：检查环境 → 安装依赖 → 检查配置 → 启动服务

---

#### 方式二：手动启动

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd AI_Agent_System
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   
   Windows:
   ```cmd
   copy .env.example .env
   ```
   
   Linux/Mac:
   ```bash
   cp .env.example .env
   ```
   
   编辑 `.env` 文件，填入讯飞API密钥：
   ```env
   SPARK_APP_ID=""
   SPARK_API_KEY="your_api_key"
   SPARK_API_SECRET="your_api_secret"
   SPARK_BASE_URL="https://spark-api-open.xf-yun.com/x2/chat/completions"
   SPARK_MODEL="spark-x2"
   ```

4. **启动服务**
   ```bash
   # 开发模式（支持热重载）
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   
   # 生产模式
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

5. **访问服务**
   - 健康检查：http://localhost:8000/
   - API文档：http://localhost:8000/docs
   - 测试接口：运行 `python test.py`

## 🔌 API接口

### 核心接口

| 路径 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 健康检查 |
| `/chat/stream` | POST | 流式对话（核心功能） |
| `/docs` | GET | Swagger API文档 |

### 调用示例

**请求**：
```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test001", "message": "我想学习机器学习中的决策树算法"}'
```

**响应**（流式返回）：
```json
{"type": "画像", "content": {"knowledge_base": "初学者", "cognitive_style": "视觉型", ...}}
{"type": "学习资料", "content": {"type": "multi_resource", "content": "..."}}
{"type": "状态", "content": "审核通过"}
{"type": "学习路线", "content": [{"step_name": "...", "action": "...", "time_minutes": 20}]}
{"type": "完成", "content": "全部生成完毕"}
```

## 🤖 Agent工作流

```
用户输入 
    ↓
[画像机器人] → 分析学习特征（知识基础、认知风格、易错点等6个维度）
    ↓
[RAG检索] → 从知识库检索相关知识点
    ↓
[资源生成] → 生成学习资料（讲解文档、测验、思维导图）
    ↓
[审核机器人] → 内容质量检查（关键词检测 + 长度验证）
    ↓
    ├─ 通过 → [路径规划] → 输出学习路线
    └─ 失败 → 重新生成（最多3次重试）
```

## 📝 各模块说明

### app/main.py
FastAPI应用入口，定义API路由和请求处理逻辑。

### app/agents.py
包含5个Agent的核心实现：
- `profile_agent`: 用户画像分析
- `rag_agent`: RAG知识检索
- `generator_agent`: 学习资源生成
- `guardrail_agent`: 内容审核
- `planner_agent`: 学习路径规划

### app/workflow.py
LangGraph工作流定义，编排Agent执行顺序和条件分支。

### app/models.py
AgentState数据模型，定义工作流中传递的状态结构。

### data/demo.txt
知识库示例文件，RAG检索的数据源。

## 🧪 测试

运行测试脚本验证功能：
```bash
python test.py
```

## 📦 团队协作

### 给前端同学
- API文档：打开 `API文档.html` 或访问 http://localhost:8000/docs
- 核心接口：`POST /chat/stream`（SSE流式响应）
- 响应类型：`画像`、`学习资料`、`状态`、`学习路线`、`完成`

### 给后端同学
- 集成方式：独立服务部署或模块导入
- 调用示例：参考 `API文档.md` 中的后端代码示例

### 给数据库同学
- 用户画像表：存储用户学习特征
- 学习记录表：记录生成的学习资料和路线
- 知识数据表：支持RAG检索的向量数据库

### 给部署同学
- Dockerfile：可参考 `requirements.txt` 构建镜像
- 环境变量：需要配置讯飞API密钥

## ⚠️ 注意事项

1. **密钥安全**：`.env` 文件包含敏感信息，不要提交到Git仓库
2. **API配额**：讯飞API有调用次数限制，注意合理使用
3. **重试机制**：内容审核失败会自动重试（最多3次）
4. **网络环境**：需要联网才能调用讯飞API

## 📄 许可证

MIT License

## 📧 联系方式

如有问题，请联系项目负责人。