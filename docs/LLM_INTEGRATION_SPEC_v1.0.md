# 大模型对接规范 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\LLM_INTEGRATION_SPEC_v1.0.md
```


# 大模型对接规范 v1.0

## 一、架构设计

```yaml
# 大模型对接架构
architecture:
  pattern: "Adapter Pattern"
  description: "统一的模型调用接口，支持插拔式接入新模型"
  
  components:
    - name: "ModelRouter"
      description: "模型路由器，根据任务类型选择最优模型"
    - name: "ModelAdapter"
      description: "模型适配器，统一不同模型的调用接口"
    - name: "ModelFactory"
      description: "模型工厂，动态创建模型实例"
    - name: "ModelRegistry"
      description: "模型注册表，管理所有可用模型"
    - name: "ModelCache"
      description: "模型缓存，缓存相同请求的结果"
    - name: "ModelMonitor"
      description: "模型监控，记录调用耗时、成功率、成本"
```


## 二、统一模型接口定义

### 2.1 核心接口

```python
# models/llm/base.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncIterator
from pydantic import BaseModel

class Message(BaseModel):
    """对话消息"""
    role: str           # system, user, assistant
    content: str        # 消息内容
    name: Optional[str] = None  # 函数名（可选）

class Tool(BaseModel):
    """函数工具定义"""
    type: str = "function"
    function: Dict[str, Any]

class ModelRequest(BaseModel):
    """模型请求"""
    messages: List[Message]           # 对话历史
    model: str                        # 模型名称
    temperature: float = 0.7          # 温度 0-2
    max_tokens: int = 4096            # 最大输出token
    top_p: float = 0.95               # 核采样
    frequency_penalty: float = 0.0    # 频率惩罚
    presence_penalty: float = 0.0     # 存在惩罚
    tools: Optional[List[Tool]] = None  # 可用工具
    stream: bool = False              # 是否流式输出
    images: Optional[List[str]] = None # 图像URL列表（多模态）

class ModelResponse(BaseModel):
    """模型响应"""
    id: str                           # 响应ID
    content: str                      # 响应内容
    role: str                         # assistant
    finish_reason: str                # stop, length, tool_calls
    tool_calls: Optional[List[Dict]] = None  # 工具调用
    usage: Dict[str, int]             # token使用量 {prompt_tokens, completion_tokens, total_tokens}
    latency_ms: float                 # 响应延迟（毫秒）
    model: str                        # 实际使用的模型

class BaseModelAdapter(ABC):
    """模型适配器基类"""
    
    @abstractmethod
    async def chat_completion(
        self, 
        request: ModelRequest
    ) -> ModelResponse:
        """同步对话补全"""
        pass
    
    @abstractmethod
    async def stream_chat_completion(
        self, 
        request: ModelRequest
    ) -> AsyncIterator[str]:
        """流式对话补全"""
        pass
    
    @abstractmethod
    async def get_quota(self) -> Dict[str, int]:
        """获取当前配额（并发数、剩余请求数）"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息（能力、价格、速率限制）"""
        pass
```


## 三、模型配置数据模型

```yaml
# 模型配置
model_config:
  # 模型注册表
  registry:
    - id: "M-01"
      name: "GPT-4"
      provider: "OpenAI"
      status: "pending"  # pending, active, deprecated
      capabilities: ["text", "function_calling", "vision"]
      rate_limit:
        requests_per_minute: 500
        requests_per_day: 10000
        concurrent: 10
      pricing:
        input: 0.03      # $/1K tokens
        output: 0.06     # $/1K tokens
      adapter: "OpenAIAdapter"
      
    - id: "M-02"
      name: "Claude-3"
      provider: "Anthropic"
      status: "pending"
      capabilities: ["text", "function_calling", "vision"]
      rate_limit:
        requests_per_minute: 50
        requests_per_day: 5000
        concurrent: 5
      pricing:
        input: 0.025
        output: 0.075
      adapter: "AnthropicAdapter"
      
    - id: "M-03"
      name: "DeepSeek-V3"
      provider: "DeepSeek"
      status: "active"
      capabilities: ["text", "function_calling"]
      rate_limit:
        requests_per_minute: 100
        requests_per_day: 100000
        concurrent: 10
      pricing:
        input: 0.001
        output: 0.002
      adapter: "DeepSeekAdapter"
      
    - id: "M-04"
      name: "通义千问"
      provider: "Alibaba"
      status: "pending"
      capabilities: ["text", "function_calling", "vision"]
      rate_limit:
        requests_per_minute: 100
        requests_per_day: 10000
        concurrent: 5
      pricing:
        input: 0.008
        output: 0.016
      adapter: "TongyiAdapter"
      
    - id: "M-05"
      name: "文心一言"
      provider: "Baidu"
      status: "pending"
      capabilities: ["text", "function_calling"]
      rate_limit:
        requests_per_minute: 60
        requests_per_day: 5000
        concurrent: 3
      pricing:
        input: 0.012
        output: 0.024
      adapter: "WenxinAdapter"
      
    - id: "M-06"
      name: "Gemini"
      provider: "Google"
      status: "pending"
      capabilities: ["text", "vision"]
      rate_limit:
        requests_per_minute: 60
        requests_per_day: 5000
        concurrent: 5
      pricing:
        input: 0.002
        output: 0.004
      adapter: "GeminiAdapter"
      
    - id: "M-07"
      name: "Qwen-Max"
      provider: "Alibaba"
      status: "pending"
      capabilities: ["text", "function_calling", "vision"]
      rate_limit:
        requests_per_minute: 120
        requests_per_day: 20000
        concurrent: 10
      pricing:
        input: 0.02
        output: 0.04
      adapter: "QwenAdapter"
      
    - id: "M-08"
      name: "SparkDesk"
      provider: "iFlytek"
      status: "pending"
      capabilities: ["text"]
      rate_limit:
        requests_per_minute: 30
        requests_per_day: 3000
        concurrent: 2
      pricing:
        input: 0.005
        output: 0.01
      adapter: "SparkAdapter"

  # 路由策略
  routing:
    default_model: "DeepSeek-V3"
    fallback_model: "GPT-4"
    strategies:
      - name: "cost_based"
        description: "基于成本选择最便宜的模型"
      - name: "quality_based"
        description: "基于质量选择最优模型"
      - name: "latency_based"
        description: "基于延迟选择最快模型"
      - name: "load_balanced"
        description: "负载均衡，平均分配请求"
```


## 四、适配器实现模板

### 4.1 OpenAI适配器

```python
# models/llm/adapters/openai_adapter.py

import openai
from ..base import BaseModelAdapter, ModelRequest, ModelResponse

class OpenAIAdapter(BaseModelAdapter):
    """OpenAI GPT-4适配器"""
    
    def __init__(self, api_key: str, base_url: str = None):
        self.client = openai.AsyncOpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model_name = "gpt-4"
    
    async def chat_completion(self, request: ModelRequest) -> ModelResponse:
        start_time = time.time()
        
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=[msg.dict() for msg in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p,
            frequency_penalty=request.frequency_penalty,
            presence_penalty=request.presence_penalty,
            tools=[tool.dict() for tool in request.tools] if request.tools else None
        )
        
        latency_ms = (time.time() - start_time) * 1000
        
        return ModelResponse(
            id=response.id,
            content=response.choices[0].message.content or "",
            role="assistant",
            finish_reason=response.choices[0].finish_reason,
            tool_calls=response.choices[0].message.tool_calls,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            latency_ms=latency_ms,
            model=self.model_name
        )
    
    async def stream_chat_completion(self, request: ModelRequest) -> AsyncIterator[str]:
        stream = await self.client.chat.completions.create(
            model=self.model_name,
            messages=[msg.dict() for msg in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    async def get_quota(self) -> Dict[str, int]:
        # OpenAI配额查询
        return {
            "remaining": 10000,  # 剩余请求数
            "concurrent": 10,    # 最大并发
            "current": 5         # 当前并发
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        return {
            "id": "M-01",
            "name": "GPT-4",
            "provider": "OpenAI",
            "capabilities": ["text", "function_calling", "vision"],
            "rate_limit": {"rpm": 500, "rpd": 10000, "concurrent": 10},
            "pricing": {"input": 0.03, "output": 0.06}
        }
```

### 4.2 DeepSeek适配器

```python
# models/llm/adapters/deepseek_adapter.py

import aiohttp
from ..base import BaseModelAdapter, ModelRequest, ModelResponse

class DeepSeekAdapter(BaseModelAdapter):
    """DeepSeek-V3适配器"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = "deepseek-chat"
    
    async def chat_completion(self, request: ModelRequest) -> ModelResponse:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model_name,
                    "messages": [msg.dict() for msg in request.messages],
                    "temperature": request.temperature,
                    "max_tokens": request.max_tokens,
                    "stream": False
                }
            ) as resp:
                data = await resp.json()
                # 解析响应...
    
    # 其他方法实现...
```


## 五、模型路由器实现

```python
# models/llm/router.py

from typing import Optional
from .base import ModelRequest, ModelResponse
from .registry import ModelRegistry
from .adapter_factory import AdapterFactory

class ModelRouter:
    """模型路由器"""
    
    def __init__(self):
        self.registry = ModelRegistry()
        self.factory = AdapterFactory()
        self.default_model = "DeepSeek-V3"
    
    async def route(
        self, 
        request: ModelRequest,
        strategy: str = "default"
    ) -> ModelResponse:
        """
        路由请求到合适的模型
        
        Args:
            request: 模型请求
            strategy: 路由策略 (default, cost_based, quality_based, latency_based)
        """
        # 1. 根据策略选择模型
        model_name = self._select_model(request, strategy)
        
        # 2. 获取适配器
        adapter = self.factory.get_adapter(model_name)
        
        # 3. 检查配额
        quota = await adapter.get_quota()
        if quota.get("remaining", 0) <= 0:
            # 降级到备用模型
            model_name = self.registry.get_fallback(model_name)
            adapter = self.factory.get_adapter(model_name)
        
        # 4. 调用模型
        response = await adapter.chat_completion(request)
        
        # 5. 记录调用日志
        await self._log_call(request, response, model_name)
        
        return response
    
    def _select_model(self, request: ModelRequest, strategy: str) -> str:
        """根据策略选择模型"""
        if strategy == "cost_based":
            return self.registry.get_cheapest_model()
        elif strategy == "quality_based":
            return self.registry.get_best_model()
        elif strategy == "latency_based":
            return self.registry.get_fastest_model()
        else:
            return self.default_model
```


## 六、多模态输入支持

```yaml
# 多模态输入规范

multimodal:
  supported_formats:
    image:
      - "image/jpeg"
      - "image/png"
      - "image/webp"
      - "image/gif"
    audio:
      - "audio/mpeg"
      - "audio/wav"
    video:
      - "video/mp4"
  
  max_size:
    image: "20MB"
    audio: "50MB"
    video: "100MB"
  
  processing:
    - "自动压缩大图"
    - "Base64编码"
    - "URL转换"

# 多模态请求示例
multimodal_request_example:
  messages:
    - role: "user"
      content: "这张图片里有什么？"
      images:
        - "https://example.com/image.jpg"
        - "base64_encoded_image_data"
```


## 七、流式输出支持

```yaml
# 流式输出规范

streaming:
  protocol: "Server-Sent Events (SSE)"
  
  event_types:
    - type: "thinking"
      description: "思考过程"
    - type: "content"
      description: "内容片段"
    - type: "tool_call"
      description: "工具调用"
    - type: "done"
      description: "完成"
    - type: "error"
      description: "错误"
  
  sse_format: |
    event: content
    data: {"text": "Hello", "index": 0}
    
    event: content
    data: {"text": " world", "index": 1}
    
    event: done
    data: {}
```


## 八、函数调用支持

```yaml
# 函数调用规范

function_calling:
  # 工具定义格式
  tool_definition:
    type: "function"
    function:
      name: "get_weather"
      description: "获取指定城市的天气信息"
      parameters:
        type: "object"
        properties:
          city:
            type: "string"
            description: "城市名称"
        required: ["city"]
  
  # 工具调用响应格式
  tool_call_response:
    role: "assistant"
    content: null
    tool_calls:
      - id: "call_abc123"
        type: "function"
        function:
          name: "get_weather"
          arguments: '{"city": "北京"}'
  
  # 工具执行结果格式
  tool_result:
    role: "tool"
    tool_call_id: "call_abc123"
    content: '{"temperature": 25, "condition": "晴"}'
```


## 九、成本控制与配额管理

```yaml
# 成本控制配置

cost_control:
  enabled: true
  
  # 预算限制
  budget:
    daily: 10.0      # 每日预算（美元）
    monthly: 200.0   # 每月预算
    project: 500.0   # 项目预算
  
  # 配额限制
  quotas:
    per_user:
      daily: 1000    # 每用户每日请求数
      monthly: 30000
    per_model:
      daily: 10000   # 每模型每日请求数
  
  # 成本优化策略
  optimization:
    - "优先使用低成本模型处理简单任务"
    - "启用请求缓存减少重复调用"
    - "批量处理合并相似请求"
    - "非紧急任务使用异步处理"
  
  # 告警阈值
  alerts:
    - threshold: 0.8   # 80%预算使用告警
    - threshold: 0.95  # 95%预算使用紧急告警
```


## 十、在Cursor中使用

### 10.1 添加新模型

```
@docs/LLM_INTEGRATION_SPEC_v1.0.md 添加一个新模型，名称：GLM-4，提供商：智谱AI，按照模板格式配置
```

### 10.2 实现适配器

```
@docs/LLM_INTEGRATION_SPEC_v1.0.md 实现DeepSeek适配器的完整代码
```

### 10.3 测试模型调用

```
@docs/LLM_INTEGRATION_SPEC_v1.0.md 测试DeepSeek-V3模型的调用，发送消息"你好"
```


## 十一、API接口定义

```python
# API端点

# 获取可用模型列表
GET /api/v1/models
Response: List[ModelInfo]

# 模型调用（非流式）
POST /api/v1/chat/completions
Request: ModelRequest
Response: ModelResponse

# 模型调用（流式）
POST /api/v1/chat/completions/stream
Request: ModelRequest
Response: SSE Stream

# 获取模型配额
GET /api/v1/models/{model_id}/quota
Response: { "remaining": 1000, "concurrent": 5, "current": 2 }

# 获取调用统计
GET /api/v1/models/stats
Response: { "total_calls": 10000, "total_cost": 12.5, "avg_latency": 234 }
```


## 十二、配置文件示例

```yaml
# config/models.yaml

models:
  default: "DeepSeek-V3"
  fallback: "GPT-4"
  
  providers:
    openai:
      api_key: "${OPENAI_API_KEY}"
      base_url: "https://api.openai.com/v1"
      
    deepseek:
      api_key: "${DEEPSEEK_API_KEY}"
      base_url: "https://api.deepseek.com"
      
    anthropic:
      api_key: "${ANTHROPIC_API_KEY}"
      base_url: "https://api.anthropic.com"
      
    alibaba:
      api_key: "${ALIBABA_API_KEY}"
      base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      
    baidu:
      api_key: "${BAIDU_API_KEY}"
      secret_key: "${BAIDU_SECRET_KEY}"
      
    google:
      api_key: "${GOOGLE_API_KEY}"
  
  routing:
    strategy: "cost_based"
    fallback_enabled: true
    
  caching:
    enabled: true
    ttl: 3600  # 缓存1小时
    max_size: 1000
    
  monitoring:
    enabled: true
    metrics_port: 9090
```


**文档结束**