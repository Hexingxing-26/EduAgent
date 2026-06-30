# AI智能体模块 - API接口文档

## 服务信息

| 项目 | 说明 |
|------|------|
| 服务名称 | AI_Agent_System |
| 技术框架 | FastAPI + LangGraph |
| 默认端口 | 8000 |
| 交互式文档 | http://localhost:8000/docs |

---

## 接口列表

### 1. 健康检查

| 项目 | 说明 |
|------|------|
| 路径 | `/` |
| 方法 | `GET` |

**响应示例**：
```json
{
  "message": "AI系统已启动！"
}
```

---

### 2. 流式对话（核心接口）

| 项目 | 说明 |
|------|------|
| 路径 | `/chat/stream` |
| 方法 | `POST` |
| 响应类型 | Server-Sent Events (SSE) |

**请求体**：
```json
{
  "user_id": "string (必填，用户唯一标识)",
  "message": "string (必填，用户提问内容)"
}
```

**请求示例**：
```json
{
  "user_id": "test001",
  "message": "我想学习机器学习中的决策树算法"
}
```

**响应格式**（流式返回，按顺序接收）：

| 类型 | 说明 | 示例 |
|------|------|------|
| `画像` | 用户画像分析结果 | `{"type": "画像", "content": {...}}` |
| `学习资料` | 生成的学习资源 | `{"type": "学习资料", "content": {...}}` |
| `状态` | 审核状态 | `{"type": "状态", "content": "审核通过"}` |
| `学习路线` | 规划的学习步骤 | `{"type": "学习路线", "content": [...]}` |
| `完成` | 全部流程结束 | `{"type": "完成", "content": "全部生成完毕"}` |

**详细响应示例**：

```json
// 1. 画像分析完成
{
  "type": "画像",
  "content": {
    "knowledge_base": "初学者",
    "cognitive_style": "视觉型",
    "weak_points": "数学推导",
    "interest": "AI",
    "learning_pace": "中等",
    "emotional_state": "积极"
  }
}

// 2. 学习资料生成完成
{
  "type": "学习资料",
  "content": {
    "type": "multi_resource",
    "content": "1. **知识讲解文档**：决策树是一种常用的机器学习算法..."
  }
}

// 3. 审核状态
{
  "type": "状态",
  "content": "审核通过"
}

// 4. 学习路线生成完成
{
  "type": "学习路线",
  "content": [
    {"step_name": "理论学习", "action": "阅读讲解文档", "time_minutes": 20},
    {"step_name": "巩固练习", "action": "完成随堂测验", "time_minutes": 15},
    {"step_name": "知识总结", "action": "绘制思维导图", "time_minutes": 10}
  ]
}

// 5. 全部完成
{
  "type": "完成",
  "content": "全部生成完毕"
}
```

---

## 前端接入示例

### JavaScript (SSE)

```javascript
async function chatWithAgent(userId, message) {
  const response = await fetch('/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, message: message }),
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder('utf-8');

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const text = decoder.decode(value);
    const lines = text.split('\n\n');
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.substring(6));
        handleResponse(data);
      }
    }
  }
}

function handleResponse(data) {
  switch (data.type) {
    case '画像':
      console.log('用户画像:', data.content);
      break;
    case '学习资料':
      console.log('学习资料:', data.content);
      break;
    case '状态':
      console.log('审核状态:', data.content);
      break;
    case '学习路线':
      console.log('学习路线:', data.content);
      break;
    case '完成':
      console.log('对话结束');
      break;
  }
}
```

---

## 后端调用示例

### Python (requests)

```python
import requests

def call_agent(user_id, message):
    url = "http://localhost:8000/chat/stream"
    payload = {"user_id": user_id, "message": message}
    
    response = requests.post(url, json=payload, stream=True)
    
    for line in response.iter_lines():
        if line and line.decode('utf-8').startswith("data: "):
            data = json.loads(line.decode('utf-8')[6:])
            print(f"收到: {data['type']} - {data['content']}")
```

---

## 工作流流程

```
用户输入 
    ↓
[画像机器人] → 分析学习特征（知识基础、认知风格、易错点等）
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

---

## 错误处理

| 错误类型 | HTTP状态码 | 说明 |
|----------|-----------|------|
| 请求参数缺失 | 422 | user_id 或 message 为空 |
| 服务内部错误 | 500 | LLM调用失败或其他异常 |

---

## 环境变量配置

参考 `.env.example` 文件：

```env
# 讯飞星火API配置
SPARK_APP_ID=""
SPARK_API_KEY="your_api_key_here"
SPARK_API_SECRET="your_api_secret_here"
SPARK_BASE_URL="https://spark-api-open.xf-yun.com/x2/chat/completions"
SPARK_MODEL="spark-x2"
```

---

## 依赖清单

```txt
fastapi>=0.100.0
uvicorn>=0.23.0
pydantic>=2.0.0
python-dotenv>=1.0.0
requests>=2.31.0
langgraph>=1.0.0
langchain-core>=1.0.0
```

---

## 启动方式

```bash
# 开发模式
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000
```