# 🤖 Agent 框架实战指南

> 从入门到大师：LangChain、LlamaIndex、向量数据库、AutoGen、AgentScope、DeerFlow

---

## 📚 目录

- [框架总览](#-框架总览)
- [1. LangChain / LangGraph](#-1-langchain--langgraph)
- [2. LlamaIndex](#-2-llamaindex)
- [3. 向量数据库](#-3-向量数据库)
- [4. OpenAI SDK](#-4-openai-sdk)
- [5. AutoGen](#-5-autogen)
- [6. AgentScope](#-6-agentscope)
- [7. DeerFlow](#-7-deerflow)
- [选型建议](#-选型建议)

---

## 📊 框架总览

| 框架 | ⭐ 星数 | 定位 | 最适合 |
| --- | --- | --- | --- |
| **LangChain** | 100k+ | 通用 LLM 应用框架 | 快速搭建 LLM 应用 |
| **LangGraph** | 15k+ | 有状态多角色 Agent | 复杂工作流、人在回路 |
| **LlamaIndex** | 35k+ | RAG 数据框架 | 知识库、文档问答 |
| **Chroma** | 18k+ | 轻量向量数据库 | 本地开发、快速原型 |
| **Pinecone** | 7k+ | 托管向量数据库 | 生产环境、免运维 |
| **Milvus** | 30k+ | 开源向量数据库 | 大规模、私有化部署 |
| **AutoGen** | 45k+ | 微软多智能体框架 | 多 Agent 对话协作 |
| **AgentScope** | 5k+ | 阿里多智能体框架 | 企业级分布式 Agent |
| **DeerFlow** | 20k+ | 字节跳动研究型 Agent | 深度研究、长时程任务 |

---

## 🦜️🔗 1. LangChain / LangGraph

### 入门级：第一个 LLM 应用

**安装**：
```bash
pip install langchain langchain-openai
```

**代码**：
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 初始化模型
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# 2. 创建提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个翻译助手，把英语翻译成中文。"),
    ("user", "{text}")
])

# 3. 组装链
chain = prompt | llm | StrOutputParser()

# 4. 运行
result = chain.invoke({"text": "Hello, world!"})
print(result)
# 输出：你好，世界！
```

---

### 精通级：带记忆的聊天机器人

**代码**：
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatOpenAI(model="gpt-4o")

# 提示词带历史消息占位符
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手。"),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

chain = prompt | llm

# 会话历史存储
store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 带记忆的链
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 对话
chain_with_history.invoke(
    {"input": "我叫小明"},
    config={"configurable": {"session_id": "user_123"}}
)

chain_with_history.invoke(
    {"input": "我叫什么名字？"},
    config={"configurable": {"session_id": "user_123"}}
)
# 输出：你叫小明！
```

---

### 大师级：LangGraph 多角色工作流

**安装**：
```bash
pip install langgraph
```

**代码**：
```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
import operator

# 1. 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next: str

llm = ChatOpenAI(model="gpt-4o")

# 2. 定义节点
def researcher_node(state: AgentState):
    """研究员节点：收集信息"""
    response = llm.invoke(f"研究这个问题：{state['messages'][-1]}")
    return {"messages": [response]}

def writer_node(state: AgentState):
    """写手节点：写报告"""
    response = llm.invoke(f"根据这些信息写报告：{state['messages']}")
    return {"messages": [response]}

def reviewer_node(state: AgentState):
    """审核员节点：审核报告"""
    response = llm.invoke(f"审核这个报告：{state['messages'][-1]}")
    return {"messages": [response]}

# 3. 定义路由
def router(state: AgentState):
    last_message = state["messages"][-1].content
    if "需要修改" in last_message:
        return "writer"
    else:
        return END

# 4. 构建图
workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")
workflow.add_conditional_edges("reviewer", router)

# 5. 编译运行
app = workflow.compile()

result = app.invoke({
    "messages": ["写一份关于 AI Agent 的报告"]
})
print(result["messages"][-1].content)
```

---

## 📚 2. LlamaIndex

### 入门级：第一个 RAG 应用

**安装**：
```bash
pip install llama-index llama-index-llms-openai
```

**代码**：
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# 1. 加载文档
documents = SimpleDirectoryReader("./data").load_data()

# 2. 创建索引
index = VectorStoreIndex.from_documents(documents)

# 3. 创建查询引擎
query_engine = index.as_query_engine()

# 4. 提问
response = query_engine.query("这份文档讲了什么？")
print(response)
```

---

### 精通级：高级 RAG（混合检索 + 重排）

**代码**：
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SentenceTransformerRerank

# 1. 加载文档
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)

# 2. 配置检索器
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,  # 先召回 10 个
)

# 3. 加重排器
reranker = SentenceTransformerRerank(
    model="BAAI/bge-reranker-base",
    top_n=3,  # 重排后只保留 3 个
)

# 4. 组装查询引擎
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    node_postprocessors=[reranker],
)

# 5. 提问
response = query_engine.query("详细解释一下 RAG 的工作原理")
print(response)
```

---

### 大师级：Agentic RAG（路由 + 工具调用）

**代码**：
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI

# 1. 加载两个不同的知识库
docs1 = SimpleDirectoryReader("./docs/python").load_data()
docs2 = SimpleDirectoryReader("./docs/java").load_data()

index1 = VectorStoreIndex.from_documents(docs1)
index2 = VectorStoreIndex.from_documents(docs2)

# 2. 创建查询工具
python_tool = QueryEngineTool(
    query_engine=index1.as_query_engine(),
    metadata=ToolMetadata(
        name="python_docs",
        description="Python 语言相关的文档查询"
    )
)

java_tool = QueryEngineTool(
    query_engine=index2.as_query_engine(),
    metadata=ToolMetadata(
        name="java_docs",
        description="Java 语言相关的文档查询"
    )
)

# 3. 创建 ReAct Agent
llm = OpenAI(model="gpt-4o")
agent = ReActAgent.from_tools(
    [python_tool, java_tool],
    llm=llm,
    verbose=True,
)

# 4. Agent 自动选择工具回答
response = agent.chat("Python 和 Java 哪个更适合写后端？")
print(response)
```

---

## 🗄️ 3. 向量数据库

### 选型对比

| 数据库 | ⭐ 星数 | 类型 | 适合场景 | 优点 | 缺点 |
| --- | --- | --- | --- | --- | --- |
| **Chroma** | 18k+ | 开源 | 本地开发、原型 | 最简单，pip install 就用 | 不适合大规模 |
| **FAISS** | 30k+ | 开源库 | 研究、离线计算 | 最快，Meta 出品 | 不是完整数据库 |
| **Qdrant** | 25k+ | 开源 | 生产环境 | Rust 写的，性能好 | 学习成本略高 |
| **Weaviate** | 15k+ | 开源 | 混合搜索 | 向量+关键词混合搜索强 | 部署略复杂 |
| **Milvus** | 30k+ | 开源 | 大规模生产 | 十亿级向量，功能最全 | 资源占用大 |
| **Pinecone** | 7k+ | 托管 | 快速上线 | 免运维，最省心 | 贵，厂商锁定 |

---

### 入门级：Chroma 5 分钟上手

**安装**：
```bash
pip install chromadb
```

**代码**：
```python
import chromadb

# 1. 连接客户端
client = chromadb.Client()

# 2. 创建集合
collection = client.create_collection("my_docs")

# 3. 添加数据
collection.add(
    documents=["Python 是一种编程语言", "Java 也是一种编程语言"],
    metadatas=[{"lang": "python"}, {"lang": "java"}],
    ids=["doc1", "doc2"]
)

# 4. 查询
results = collection.query(
    query_texts=["Python 是什么？"],
    n_results=1
)

print(results["documents"][0][0])
# 输出：Python 是一种编程语言
```

---

### 精通级：Qdrant 生产级部署

**Docker 部署**：
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**代码**：
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 1. 连接
client = QdrantClient(url="http://localhost:6333")

# 2. 创建集合
client.create_collection(
    collection_name="my_collection",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# 3. 插入向量
client.upsert(
    collection_name="my_collection",
    points=[
        PointStruct(id=1, vector=[0.1] * 1536, payload={"text": "Hello"}),
        PointStruct(id=2, vector=[0.2] * 1536, payload={"text": "World"}),
    ]
)

# 4. 搜索
hits = client.search(
    collection_name="my_collection",
    query_vector=[0.15] * 1536,
    limit=2,
)

for hit in hits:
    print(hit.payload, hit.score)
```

---

### 大师级：Milvus 大规模分布式

**Docker Compose 部署**：
```yaml
version: '3.5'
services:
  etcd:
    image: milvusdb/etcd:3.5.5-r2
  minio:
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
  milvus:
    image: milvusdb/milvus:v2.4.0
    ports:
      - "19530:19530"
    depends_on:
      - etcd
      - minio
```

**代码**：
```python
from pymilvus import Collection, connections, utility

# 1. 连接
connections.connect(host="localhost", port="19530")

# 2. 创建集合
utility.drop_collection("large_docs") if utility.has_collection("large_docs") else None

from pymilvus import CollectionSchema, FieldSchema, DataType

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1536),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=500),
]

schema = CollectionSchema(fields=fields)
collection = Collection("large_docs", schema=schema)

# 3. 创建索引（IVF_FLAT 适合大规模）
index_params = {
    "metric_type": "COSINE",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 1024}
}
collection.create_index("vector", index_params)

# 4. 批量插入（百万级数据）
collection.insert([
    [1, 2, 3],  # id
    [[0.1]*1536, [0.2]*1536, [0.3]*1536],  # vector
    ["doc1", "doc2", "doc3"],  # text
])

# 5. 加载到内存并搜索
collection.load()

results = collection.search(
    data=[[0.15]*1536],
    anns_field="vector",
    param={"metric_type": "COSINE", "params": {"nprobe": 10}},
    limit=5,
    output_fields=["text"],
)

for hits in results:
    for hit in hits:
        print(hit.entity.get("text"), hit.score)
```

---

## 📡 4. OpenAI SDK

### 入门级：第一个 API 调用

**安装**：
```bash
pip install openai
```

**代码**：
```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# 1. 聊天补全
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是一个助手"},
        {"role": "user", "content": "你好！"}
    ]
)

print(response.choices[0].message.content)
```

---

### 精通级：Function Calling（工具调用）

**代码**：
```python
from openai import OpenAI
import json

client = OpenAI()

# 1. 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名，比如：北京、上海"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# 2. 模拟工具实现
def get_weather(city: str):
    return {"city": city, "temp": "25°C", "weather": "晴"}

# 3. 第一次调用，模型决定是否调用工具
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "北京今天天气怎么样？"}],
    tools=tools,
)

message = response.choices[0].message

if message.tool_calls:
    # 4. 执行工具
    for tool_call in message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        result = get_weather(**args)

        # 5. 把结果返回给模型
        client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "北京今天天气怎么样？"},
                message,
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            ],
        )
```

---

### 大师级：流式输出 + Assistant API

**代码**：
```python
from openai import OpenAI

client = OpenAI()

# 1. 创建 Assistant（可以理解为一个配置好的 AI 助手）
assistant = client.beta.assistants.create(
    name="代码助手",
    instructions="你是一个 Python 编程助手，帮助用户写代码和 debug。",
    model="gpt-4o",
    tools=[{"type": "code_interpreter"}],  # 可以执行代码
)

# 2. 创建会话
thread = client.beta.threads.create()

# 3. 添加用户消息
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="帮我写一个快速排序的 Python 函数"
)

# 4. 运行并流式输出
with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
) as stream:
    for event in stream:
        if event.event == "thread.message.delta":
            print(event.data.delta.content[0].text.value, end="", flush=True)
```

---

## 🤝 5. AutoGen

### 入门级：两个 Agent 对话

**安装**：
```bash
pip install pyautogen
```

**代码**：
```python
from autogen import AssistantAgent, UserProxyAgent

# 1. 配置 LLM
config_list = [
    {"model": "gpt-4o", "api_key": "your-api-key"}
]

# 2. 创建两个 Agent
assistant = AssistantAgent(
    name="Assistant",
    llm_config={"config_list": config_list},
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  # 不需要人工输入
    max_consecutive_auto_reply=3,
)

# 3. 开始对话
user_proxy.initiate_chat(
    assistant,
    message="写一个 Python 函数，计算斐波那契数列"
)
```

---

### 精通级：多 Agent 协作（编程团队）

**代码**：
```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

config_list = [{"model": "gpt-4o", "api_key": "your-key"}]

# 1. 创建不同角色的 Agent
product_manager = AssistantAgent(
    name="产品经理",
    system_message="你是产品经理，负责定义需求和验收标准。",
    llm_config={"config_list": config_list},
)

developer = AssistantAgent(
    name="开发工程师",
    system_message="你是开发工程师，负责写代码。",
    llm_config={"config_list": config_list},
)

tester = AssistantAgent(
    name="测试工程师",
    system_message="你是测试工程师，负责写测试用例。",
    llm_config={"config_list": config_list},
)

user = UserProxyAgent(
    name="用户",
    human_input_mode="NEVER",
)

# 2. 创建群聊
groupchat = GroupChat(
    agents=[product_manager, developer, tester, user],
    messages=[],
    max_round=10,
)

manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

# 3. 启动工作流
user.initiate_chat(
    manager,
    message="开发一个待办事项管理的 CLI 工具"
)
```

---

### 大师级：代码执行 + 人工审核

**代码**：
```python
from autogen import AssistantAgent, UserProxyAgent

config_list = [{"model": "gpt-4o", "api_key": "your-key"}]

# 1. 代码执行 Agent
coder = AssistantAgent(
    name="程序员",
    llm_config={"config_list": config_list},
    system_message="你是一个 Python 程序员，写代码并解释。",
)

# 2. 带代码执行能力的用户代理
executor = UserProxyAgent(
    name="执行器",
    human_input_mode="TERMINATE",  # 完成后需要人工确认
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # 生产环境建议用 Docker
    },
)

# 3. 对话：写代码 → 自动执行 → 检查结果 → 人工确认
executor.initiate_chat(
    coder,
    message="写一个 Python 脚本，计算 1 到 100 的和，并打印结果"
)
```

---

## 🏢 6. AgentScope

### 入门级：第一个 Agent

**安装**：
```bash
pip install agentscope
```

**代码**：
```python
import agentscope
from agentscope.agents import ReActAgent, UserAgent
from agentscope.message import Msg

# 1. 初始化（配置模型）
agentscope.init(
    model_configs={
        "config_name": "my_config",
        "model_type": "openai",
        "model_name": "gpt-4o",
        "api_key": "your-key",
    }
)

# 2. 创建 Agent
assistant = ReActAgent(
    name="Assistant",
    sys_prompt="你是一个有帮助的助手。",
    model_config="my_config",
)

user = UserAgent(name="User")

# 3. 对话
x = user()
while x is not None:
    x = assistant(x)
    x = user(x)
```

---

### 精通级：多 Agent 消息总线

**代码**：
```python
import agentscope
from agentscope.agents import ReActAgent, UserAgent
from agentscope.message import Msg

agentscope.init(model_configs={...})

# 1. 创建多个 Agent
researcher = ReActAgent(name="研究员", sys_prompt="你负责研究问题。", ...)
writer = ReActAgent(name="写手", sys_prompt="你负责写文章。", ...)
reviewer = ReActAgent(name="审核员", sys_prompt="你负责审核文章。", ...)

# 2. 创建消息总线（分布式通信）
from agentscope.rpc import RpcAgentServer

# 每个 Agent 可以跑在不同的节点上
researcher = researcher.to_distributed("node_1")
writer = writer.to_distributed("node_2")
reviewer = reviewer.to_distributed("node_3")

# 3. 消息总线通信
msg = Msg("user", "写一篇关于 AI 的文章", role="user")
msg = researcher(msg)  # 研究员研究
msg = writer(msg)      # 写手写文章
msg = reviewer(msg)    # 审核员审核

print(msg.content)
```

---

### 大师级：企业级分布式多 Agent

**代码**：
```python
import agentscope
from agentscope.agents import ReActAgent
from agentscope.formatter import SlackFormatter
from agentscope.memory import LlamaIndexMemory

# 1. 企业级配置
agentscope.init(
    model_configs=[...],
    runtime_config={
        "timeout": 300,  # 超时时间
        "retry": 3,      # 重试次数
    }
)

# 2. 带记忆的 Agent
agent = ReActAgent(
    name="客服",
    sys_prompt="你是客服，记住用户的所有问题。",
    model_config="my_config",
    memory=LlamaIndexMemory(),  # 向量记忆
    formatter=SlackFormatter(),  # 格式化输出
)

# 3. 加中间件（权限控制、日志、监控）
from agentscope.middleware import (
    LoggingMiddleware,
    PermissionMiddleware,
    MetricsMiddleware,
)

agent.add_middleware(LoggingMiddleware())
agent.add_middleware(PermissionMiddleware(allowed_tools=["query_order"]))
agent.add_middleware(MetricsMiddleware())

# 4. 分布式部署（每个 Agent 跑在不同服务器）
agent = agent.to_distributed("server_1", port=8000)

# 5. 运行
while True:
    msg = input("User: ")
    response = agent(msg)
    print(f"Assistant: {response.content}")
```

---

## 🌊 7. DeerFlow

### 入门级：第一个研究任务

**安装**：
```bash
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow
pip install -e .
```

**代码**：
```python
from deerflow import DeerFlowAgent

# 1. 初始化 Agent
agent = DeerFlowAgent(
    model="gpt-4o",
    tools=["search", "scrape", "crawl"],
)

# 2. 深度研究
result = agent.research(
    query="2025 年 AI Agent 行业发展趋势"
)

print(result.summary)
print(result.references)
```

---

### 精通级：多步研究工作流

**代码**：
```python
from deerflow import DeerFlowAgent, ResearchStep

agent = DeerFlowAgent(model="gpt-4o")

# 1. 定义研究步骤
steps = [
    ResearchStep("收集行业报告"),
    ResearchStep("分析头部公司动态"),
    ResearchStep("整理技术趋势"),
    ResearchStep("撰写总结报告"),
]

# 2. 执行研究
result = agent.run_research(
    topic="大模型 RAG 技术最新进展",
    steps=steps,
    max_iterations=10,
)

# 3. 生成报告
report = agent.generate_report(result, format="markdown")
print(report)
```

---

### 大师级：Lead Agent + 子 Agent 动态调用

**代码**：
```python
from deerflow import DeerFlowAgent

agent = DeerFlowAgent(model="gpt-4o")

# 1. 注册子 Agent
agent.register_subagent(
    name="web_researcher",
    prompt="你是一个网页研究专家，擅长搜索和总结网页内容。",
    tools=["search", "scrape", "summarize"],
)

agent.register_subagent(
    name="code_analyzer",
    prompt="你是一个代码分析专家，擅长分析 GitHub 项目。",
    tools=["github_search", "repo_analysis"],
)

agent.register_subagent(
    name="writer",
    prompt="你是一个技术写作专家，擅长写技术报告。",
    tools=["write", "format"],
)

# 2. Lead Agent 自动编排
result = agent.orchestrate(
    task="调研最流行的 5 个开源 RAG 框架，写一份对比报告",
    max_depth=3,
)

# 3. 输出
print(result.final_report)
print(f"用了多少个子 Agent: {len(result.used_subagents)}")
```

---

## 🎯 选型建议

### 如果你是新手

1. **先学 OpenAI SDK** — 最基础，理解 API 调用
2. **再学 LangChain** — 快速搭建 LLM 应用
3. **然后学 LlamaIndex** — 做 RAG 知识库
4. **最后学 LangGraph / AutoGen** — 做多 Agent 协作

### 如果你是开发者

| 场景 | 推荐框架 |
| --- | --- |
| **做聊天机器人** | LangChain + 向量数据库 |
| **做知识库问答** | LlamaIndex + Chroma/Pinecone |
| **做多 Agent 协作** | AutoGen / AgentScope |
| **做深度研究** | DeerFlow |
| **企业级生产** | AgentScope（分布式 + 可观测） |

### 如果你是架构师

- **快速原型** → LangChain + Chroma
- **生产上线** → LangGraph + Qdrant/Milvus
- **复杂多 Agent** → AutoGen + 自定义编排
- **企业级分布式** → AgentScope
- **深度研究场景** → DeerFlow

---

<div align="center">

**先跑起来第一个 Hello World，再慢慢深入。** 🚀

</div>
