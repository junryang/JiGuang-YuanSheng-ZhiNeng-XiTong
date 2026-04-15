# 对话系统模块 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\CHAT_SYSTEM_MODULE_v1.0.md
```


# 对话系统模块 v1.0

## 一、模块概述

```yaml
module:
  name: "对话系统模块"
  description: |
    负责用户与CEO智能体（主脑）的自然语言交互，支持任务下达、进度查询、
    对话历史、语音交互等功能。基于通用能力规范中的感知、认知、决策能力实现。
  domain: "D03"
  priority: "P0"

  related_abilities:
    - "PC-01: 自然语言理解"
    - "PC-04: 意图识别"
    - "PC-05: 实体抽取"
    - "PC-09: 情感分析"
    - "CG-01: 推理能力"
    - "CG-02: 类比推理"
    - "DC-01: 任务规划"
    - "DC-06: 方案生成"
    - "DC-12: 决策解释"
    - "AGENT-RUNTIME-01: 智能体主循环"
    - "AGENT-RUNTIME-03: 决策可解释性"
    - "AGENT-RUNTIME-07: 反事实思考"
    - "AGENT-RUNTIME-10: 情感模拟"
    - "MM-01: 工作记忆"
    - "MM-02: 短期记忆"
    - "MM-03: 长期记忆"
    - "EM-13: 模型流式处理"
```


## 二、模块数据模型

```python
# 会话数据模型 - 对齐MM-01工作记忆
class Session:
    id: str                    # 会话ID，格式：SESS-YYYYMMDD-XXX
    user_id: str               # 用户ID（老板）
    agent_id: str              # 智能体ID（通常是CEO主脑）
    title: str                 # 会话标题
    status: SessionStatus      # 会话状态
    context: SessionContext    # 会话上下文（工作记忆）
    created_at: datetime       # 创建时间
    updated_at: datetime       # 更新时间
    last_message_at: datetime  # 最后消息时间

# 会话状态枚举
class SessionStatus:
    ACTIVE = "active"          # 活跃
    ARCHIVED = "archived"      # 已归档
    CLOSED = "closed"          # 已关闭

# 会话上下文 - 对齐MM-01工作记忆
class SessionContext:
    current_project_id: str    # 当前讨论的项目ID
    current_task_id: str       # 当前讨论的任务ID
    pending_actions: List      # 待处理操作列表
    mentioned_agents: List     # 提及的智能体列表
    entities: Dict             # 识别的实体（对齐PC-05）
    conversation_history: List # 对话历史（工作记忆）
    intent_stack: List         # 意图栈（多轮对话）

# 消息数据模型
class Message:
    id: str                    # 消息ID
    session_id: str            # 所属会话ID
    sender_type: str           # 发送者类型：human/agent
    sender_id: str             # 发送者ID
    content: str               # 消息内容
    message_type: MessageType  # 消息类型
    metadata: MessageMetadata  # 消息元数据
    created_at: datetime       # 创建时间

# 消息类型枚举
class MessageType:
    TEXT = "text"              # 纯文本
    COMMAND = "command"        # 命令
    QUESTION = "question"      # 问题
    RESPONSE = "response"      # 响应
    SYSTEM = "system"          # 系统消息
    ACTION = "action"          # 操作消息
    THINKING = "thinking"      # 思考过程（对齐AGENT-RUNTIME-03）
    EMOTIONAL = "emotional"    # 情感表达（对齐AGENT-RUNTIME-10）

# 消息元数据 - 对齐AGENT-RUNTIME-03决策可解释性
class MessageMetadata:
    intent: str                # 识别出的意图（对齐PC-04）
    entities: Dict             # 识别的实体（对齐PC-05）
    sentiment: Dict            # 情感分析结果（对齐PC-09）
    action_result: Dict        # 操作执行结果
    thinking_steps: List       # 思考步骤（流式输出时，对齐AGENT-RUNTIME-03）
    confidence: float          # 置信度（对齐CG-09）
    tokens_used: int           # Token使用量
    model_used: str            # 使用的模型（对齐EM-01）
    response_time: int         # 响应时间(ms)
    counterfactual_analysis: Dict  # 反事实分析（对齐AGENT-RUNTIME-07）

# 意图识别结果 - 对齐PC-04意图识别
class IntentResult:
    intent: str                # 意图类型
    confidence: float          # 置信度
    entities: Dict             # 提取的实体
    slots: Dict                # 槽位信息
    alternative_intents: List  # 备选意图
```


## 三、功能详细定义

### 3.1 CH-01 智能对话

```yaml
# CH-01 智能对话
function_id: "CH-01"
name: "智能对话"
description: "与CEO智能体自然语言对话，基于PC-01自然语言理解和AGENT-RUNTIME-01主循环"
priority: "P0"
assigned_to: "L1 CEO（主脑）"

related_abilities:
  - "PC-01: 自然语言理解"
  - "PC-04: 意图识别"
  - "PC-09: 情感分析"
  - "AGENT-RUNTIME-01: 智能体主循环"
  - "AGENT-RUNTIME-03: 决策可解释性"
  - "AGENT-RUNTIME-10: 情感模拟"
  - "MM-01: 工作记忆"
  - "EM-13: 模型流式处理"

# API接口
api:
  # 创建会话
  - method: "POST"
    endpoint: "/api/v1/chat/sessions"
    description: "创建新会话"
    request_body:
      agent_id: "string"       # 默认CEO主脑
      title: "string"          # 可选，自动生成
    response: "Session"
    
  # 发送消息（SSE流式）- 对齐EM-13流式处理
  - method: "POST"
    endpoint: "/api/v1/chat/sessions/{session_id}/messages"
    description: "发送消息，SSE流式响应"
    request_body:
      content: "string"        # 用户消息
      stream: true             # 是否流式
    response: "SSE Stream"
    
  # 获取会话列表
  - method: "GET"
    endpoint: "/api/v1/chat/sessions"
    description: "获取会话列表"
    query_params:
      status: "active|archived"
      limit: 20
      offset: 0
    response: "List[Session]"
    
  # 获取会话消息
  - method: "GET"
    endpoint: "/api/v1/chat/sessions/{session_id}/messages"
    description: "获取会话历史消息"
    query_params:
      limit: 50
      before: "timestamp"
    response: "List[Message]"
    
  # 获取思考过程（对齐AGENT-RUNTIME-03）
  - method: "GET"
    endpoint: "/api/v1/chat/sessions/{session_id}/thinking"
    description: "获取智能体的思考过程"
    response:
      thinking_steps: List
      reasoning_chain: List

# 意图识别类型 - 对齐PC-04意图识别
intent_types:
  - intent: "create_project"
    description: "创建项目"
    examples:
      - "创建一个AI客服系统"
      - "帮我开发一个智能体市场"
    related_ability: "DC-01"
    
  - intent: "query_progress"
    description: "查询进度"
    examples:
      - "当前项目进度如何"
      - "智能体市场开发到哪了"
    related_ability: "PM-04"
    
  - intent: "assign_task"
    description: "分配任务"
    examples:
      - "把前端任务分配给张三"
      - "让后端工程师处理这个"
    related_ability: "CL-01"
    
  - intent: "approve_request"
    description: "审批请求"
    examples:
      - "批准这个项目"
      - "同意预算申请"
    related_ability: "APPROVE-02"
    
  - intent: "status_check"
    description: "状态检查"
    examples:
      - "系统状态怎么样"
      - "有多少智能体在线"
    related_ability: "AGENT-RUNTIME-04"
    
  - intent: "knowledge_query"
    description: "知识查询"
    examples:
      - "什么是多智能体系统"
      - "如何优化数据库查询"
    related_ability: "KNOW-02"
    
  - intent: "report_generate"
    description: "生成报告"
    examples:
      - "生成周报"
      - "给我一份项目总结"
    related_ability: "EX-14"
    
  - intent: "what_if_analysis"
    description: "反事实分析"
    examples:
      - "如果提前一周开始会怎样"
      - "如果不采用这个方案呢"
    related_ability: "AGENT-RUNTIME-07"
    
  - intent: "explain_decision"
    description: "解释决策"
    examples:
      - "为什么选择这个方案"
      - "能解释一下你的决定吗"
    related_ability: "AGENT-RUNTIME-03"
    
  - intent: "casual_chat"
    description: "闲聊"
    examples:
      - "你好"
      - "今天天气不错"
    related_ability: "AGENT-RUNTIME-10"

# SSE流式响应格式 - 对齐EM-13
sse_stream_format:
  - event: "thinking"
    data: "正在分析您的需求..."
    related_ability: "AGENT-RUNTIME-03"
    
  - event: "intent"
    data: '{"intent": "create_project", "confidence": 0.95}'
    related_ability: "PC-04"
    
  - event: "sentiment"
    data: '{"emotion": "positive", "confidence": 0.87}'
    related_ability: "PC-09"
    
  - event: "action"
    data: '{"action": "creating_project", "progress": 30}'
    related_ability: "DC-01"
    
  - event: "counterfactual"
    data: '{"alternative": "如果选择不同方案..."}'
    related_ability: "AGENT-RUNTIME-07"
    
  - event: "message_chunk"
    data: "好的，我已理解您的需求..."
    
  - event: "action_result"
    data: '{"project_id": "JYIS-2026-001", "status": "created"}'
    
  - event: "explanation"
    data: '{"reason": "选择此方案因为..."}'
    related_ability: "AGENT-RUNTIME-03"
    
  - event: "done"
    data: ""

# 前端组件
frontend:
  component: "ChatWindow.vue"
  features:
    - "消息列表（支持滚动加载）"
    - "消息气泡（区分用户/AI）"
    - "流式消息打字效果（对齐EM-13）"
    - "思考过程折叠面板（对齐AGENT-RUNTIME-03）"
    - "情感状态指示器（对齐AGENT-RUNTIME-10）"
    - "反事实分析面板（对齐AGENT-RUNTIME-07）"
    - "输入框（支持多行）"
    - "发送按钮"
    - "快捷指令按钮"
    - "会话切换侧边栏"
    - "新会话按钮"
```

### 3.2 CH-02 任务下达

```yaml
# CH-02 任务下达
function_id: "CH-02"
name: "任务下达"
description: "通过对话创建项目和任务，基于DC-01任务规划和DC-06方案生成"
priority: "P0"
assigned_to: "L1 CEO（主脑）"

related_abilities:
  - "PC-04: 意图识别"
  - "PC-05: 实体抽取"
  - "DC-01: 任务规划"
  - "DC-06: 方案生成"
  - "AGENT-RUNTIME-07: 反事实思考"
  - "PM-01: 项目创建"
  - "PM-03: 任务分解"

# API接口
api:
  # 通过对话创建项目
  - method: "POST"
    endpoint: "/api/v1/chat/actions/create-project"
    description: "通过对话创建项目"
    request_body:
      session_id: "string"
      intent_data: "IntentResult"
    response:
      project: "Project"
      message: "string"
      
  # 通过对话创建任务
  - method: "POST"
    endpoint: "/api/v1/chat/actions/create-task"
    description: "通过对话创建任务"
    request_body:
      session_id: "string"
      project_id: "string"
      intent_data: "IntentResult"
    response:
      task: "Task"
      message: "string"
      
  # 通过对话分配任务
  - method: "POST"
    endpoint: "/api/v1/chat/actions/assign-task"
    description: "通过对话分配任务"
    request_body:
      session_id: "string"
      task_id: "string"
      assignee: "string"
    response:
      assignment: "Assignment"
      message: "string"
      
  # 方案对比（基于DC-07）
  - method: "POST"
    endpoint: "/api/v1/chat/actions/compare-plans"
    description: "对比不同方案"
    request_body:
      session_id: "string"
      alternatives: "List[str]"
    response:
      comparison: "dict"

# 任务下达流程 - 对齐DC-01任务规划
task_creation_flow:
  - step: 1
    name: "意图识别"
    action: "识别用户意图"
    output: "intent: create_project/create_task"
    related_ability: "PC-04"
    
  - step: 2
    name: "实体抽取"
    action: "抽取项目名称、描述、类型"
    output: "entities: {name, description, type}"
    related_ability: "PC-05"
    
  - step: 3
    name: "信息补全"
    action: "询问缺失的必要信息"
    output: "missing_fields: []"
    
  - step: 4
    name: "方案生成"
    action: "生成项目计划书或任务方案"
    output: "plan/preview"
    related_ability: "DC-06"
    
  - step: 5
    name: "反事实评估"
    action: "评估不同方案的优劣"
    output: "counterfactual_analysis"
    related_ability: "AGENT-RUNTIME-07"
    
  - step: 6
    name: "确认执行"
    action: "等待用户确认"
    output: "confirmation_message"
    
  - step: 7
    name: "执行创建"
    action: "调用创建API"
    output: "project/task created"
    related_ability: "PM-01"

# 对话示例
dialog_examples:
  - user: "帮我创建一个AI客服系统"
    assistant: |
      好的，我将为您创建一个AI客服系统项目。
      
      📋 项目信息：
      - 项目名称：AI客服系统
      - 所属领域：D01 网站开发
      - 项目类型：新功能开发
      
      💡 方案分析：
      - 方案A：使用成熟框架，开发快但定制性差
      - 方案B：自研核心模块，灵活性高但周期长
      
      您更倾向于哪个方案？
      
  - user: "选择方案B"
    assistant: |
      好的，已选择方案B（自研核心模块）。
      
      ✅ 项目已创建！
      - 项目编号：JYIS-2026-001
      - 项目负责人：Web总经理
      - 预计工期：3周
      
      是否现在进行任务分解？
```

### 3.3 CH-03 进度查询

```yaml
# CH-03 进度查询
function_id: "CH-03"
name: "进度查询"
description: "通过对话查询项目进度"
priority: "P0"
assigned_to: "L1 CEO（主脑）"

related_abilities:
  - "PC-04: 意图识别"
  - "PM-04: 进度跟踪"
  - "CG-01: 推理能力"

# API接口
api:
  # 查询项目进度
  - method: "GET"
    endpoint: "/api/v1/chat/actions/query-progress"
    description: "通过对话查询进度"
    query_params:
      session_id: "string"
      project_name: "string"
    response:
      projects: "List[Progress]"
      summary: "string"
      
  # 查询任务进度
  - method: "GET"
    endpoint: "/api/v1/chat/actions/query-task-progress"
    description: "查询任务进度"
    query_params:
      session_id: "string"
      task_name: "string"
    response:
      task: "TaskProgress"
      message: "string"
      
  # 预测完成时间（基于CG-04数值推理）
  - method: "GET"
    endpoint: "/api/v1/chat/actions/predict-completion"
    description: "预测项目完成时间"
    query_params:
      session_id: "string"
      project_id: "string"
    response:
      predicted_date: "date"
      confidence: "float"

# 进度查询意图 - 基于PC-04
query_intents:
  - pattern: "查看.*进度"
    example: "查看AI客服系统的进度"
    response_template: |
      【{{project_name}}】项目进度报告
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      📊 整体进度：{{progress}}% ████████░░░░
      ✅ 完成任务：{{completed}}/{{total}}
      ⏰ 已用时间：{{elapsed_days}}天 / 计划{{planned_days}}天
      🎯 预计完成：{{estimated_completion}}（置信度：{{confidence}}%）
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      
      当前进行中的任务：
      {{#each tasks}}
      • {{name}} - {{progress}}%
      {{/each}}
    related_ability: "PM-04"
    
  - pattern: "什么时候能.*"
    example: "什么时候能上线"
    response_template: |
      根据当前进度和趋势分析：
      - 预计完成时间：{{estimated_date}}
      - 置信度：{{confidence}}%
      - 剩余主要工作：
      {{#each remaining_work}}
      • {{this}}
      {{/each}}
    related_ability: "CG-04"
```

### 3.4 CH-04 对话历史

```yaml
# CH-04 对话历史
function_id: "CH-04"
name: "对话历史"
description: "查看历史对话记录，基于MM-02短期记忆和MM-03长期记忆"
priority: "P1"
assigned_to: "L0 老板"

related_abilities:
  - "MM-02: 短期记忆"
  - "MM-03: 长期记忆"
  - "MM-04: 记忆检索"

# API接口
api:
  # 获取历史会话列表
  - method: "GET"
    endpoint: "/api/v1/chat/history/sessions"
    description: "获取历史会话列表"
    query_params:
      start_date: "date"
      end_date: "date"
      keyword: "string"
      limit: 20
      offset: 0
    response: "List[Session]"
    
  # 获取会话详情
  - method: "GET"
    endpoint: "/api/v1/chat/history/sessions/{session_id}"
    description: "获取会话详情（含消息）"
    response: "SessionWithMessages"
    
  # 语义搜索历史消息（基于MM-04）
  - method: "GET"
    endpoint: "/api/v1/chat/history/search"
    description: "语义搜索历史消息"
    query_params:
      q: "string"              # 搜索关键词
      session_id: "string"
      start_date: "date"
      end_date: "date"
      semantic: "bool"         # 是否使用语义搜索
    response: "SearchResult"
    
  # 导出对话历史
  - method: "POST"
    endpoint: "/api/v1/chat/history/export"
    description: "导出对话历史"
    request_body:
      session_ids: "List[str]"
      format: "json|markdown|pdf"
    response: "file"

# 前端页面
frontend:
  page: "/chat/history"
  component: "ChatHistory.vue"
  features:
    - "会话列表（按时间分组）"
    - "语义搜索框（基于MM-04）"
    - "日期筛选器"
    - "会话预览（显示前几条消息）"
    - "记忆强度指示器（基于重要性评分）"
    - "点击进入会话详情"
    - "导出按钮"
    - "删除会话"
    - "归档会话"

# 搜索功能 - 对齐MM-04记忆检索
search_features:
  - "全文搜索（消息内容）"
  - "语义搜索（基于向量嵌入）"
  - "按会话搜索"
  - "按日期范围搜索"
  - "按意图类型筛选"
  - "搜索结果高亮"
  - "搜索结果上下文预览"
  - "相关性排序（基于时间衰减和重要性）"
```

### 3.5 CH-05 语音交互

```yaml
# CH-05 语音交互
function_id: "CH-05"
name: "语音交互"
description: "语音输入和播报"
priority: "P2"
assigned_to: "L0 老板"

related_abilities:
  - "PC-04: 语音理解"
  - "EX-16: 音频生成"

# API接口
api:
  # 语音转文字（ASR）- 对齐PC-04
  - method: "POST"
    endpoint: "/api/v1/chat/voice/asr"
    description: "语音转文字"
    request_body:
      audio: "file"
      format: "wav|mp3|m4a"
    response:
      text: "string"
      confidence: "float"
      segments: "List[Segment]"
      
  # 文字转语音（TTS）- 对齐EX-16
  - method: "POST"
    endpoint: "/api/v1/chat/voice/tts"
    description: "文字转语音"
    request_body:
      text: "string"
      voice: "string"
      speed: "float"
      emotion: "string"        # 情感参数（对齐AGENT-RUNTIME-10）
    response:
      audio: "base64"
      
  # 情感语音合成（对齐AGENT-RUNTIME-10）
  - method: "POST"
    endpoint: "/api/v1/chat/voice/emotion-tts"
    description: "情感语音合成"
    request_body:
      text: "string"
      emotion: "happy|sad|angry|neutral"
    response:
      audio: "base64"

# 前端组件
frontend:
  component: "VoiceInput.vue"
  features:
    - "麦克风权限请求"
    - "录音按钮（按住说话）"
    - "录音波形可视化"
    - "录音时长显示"
    - "语音识别结果预览（实时转写）"
    - "语音置信度指示器"
    - "语音播报按钮"
    - "情感语音切换"
    - "音色选择器"
    - "语速调节滑块"
    - "音量调节滑块"

# 语音配置
voice_config:
  asr:
    engine: "Whisper"
    language: "zh"
    sample_rate: 16000
    format: "wav"
    real_time: true
    related_ability: "PC-04"
    
  tts:
    engine: "EdgeTTS"
    default_voice: "zh-CN-XiaoxiaoNeural"
    default_speed: 1.0
    default_volume: 1.0
    emotion_support: true
    related_ability: "EX-16"
```


## 四、通用能力映射总表

```yaml
# 对话系统功能与通用能力映射
chat_ability_mapping:
  CH-01_智能对话:
    primary:
      - "PC-01: 自然语言理解"
      - "PC-04: 意图识别"
      - "AGENT-RUNTIME-01: 智能体主循环"
      - "EM-13: 模型流式处理"
    secondary:
      - "PC-09: 情感分析"
      - "AGENT-RUNTIME-03: 决策可解释性"
      - "AGENT-RUNTIME-10: 情感模拟"
      - "MM-01: 工作记忆"
      
  CH-02_任务下达:
    primary:
      - "PC-04: 意图识别"
      - "PC-05: 实体抽取"
      - "DC-01: 任务规划"
      - "DC-06: 方案生成"
    secondary:
      - "AGENT-RUNTIME-07: 反事实思考"
      - "PM-01: 项目创建"
      
  CH-03_进度查询:
    primary:
      - "PC-04: 意图识别"
      - "PM-04: 进度跟踪"
    secondary:
      - "CG-04: 数值推理"
      - "CG-01: 推理能力"
      
  CH-04_对话历史:
    primary:
      - "MM-02: 短期记忆"
      - "MM-03: 长期记忆"
      - "MM-04: 记忆检索"
    secondary:
      - "MM-11: 记忆编码"
      
  CH-05_语音交互:
    primary:
      - "PC-04: 语音理解"
      - "EX-16: 音频生成"
    secondary:
      - "AGENT-RUNTIME-10: 情感模拟"
```


## 五、API接口汇总

```yaml
# 对话系统模块API汇总 - 标注关联通用能力

api_summary:
  base_path: "/api/v1/chat"
  
  sessions:
    - method: "POST"
      path: "/sessions"
      function: "CH-01"
      related_ability: "MM-01"
      
    - method: "GET"
      path: "/sessions"
      function: "CH-01/CH-04"
      
    - method: "GET"
      path: "/sessions/{id}/thinking"
      function: "CH-01"
      related_ability: "AGENT-RUNTIME-03"
      
  messages:
    - method: "POST"
      path: "/sessions/{id}/messages"
      function: "CH-01"
      related_ability: "EM-13"
      
  actions:
    - method: "POST"
      path: "/actions/create-project"
      function: "CH-02"
      related_ability: "DC-01"
      
    - method: "POST"
      path: "/actions/compare-plans"
      function: "CH-02"
      related_ability: "DC-07"
      
    - method: "GET"
      path: "/actions/predict-completion"
      function: "CH-03"
      related_ability: "CG-04"
      
  history:
    - method: "GET"
      path: "/history/search"
      function: "CH-04"
      related_ability: "MM-04"
      
  voice:
    - method: "POST"
      path: "/voice/emotion-tts"
      function: "CH-05"
      related_ability: "AGENT-RUNTIME-10"
```


## 六、数据库表结构

```sql
-- 会话表 - 对齐MM-01工作记忆
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    agent_id UUID REFERENCES agents(id),
    title VARCHAR(200),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    context JSONB,  -- 工作记忆内容
    importance_score FLOAT DEFAULT 0.5,  -- 重要性评分（用于记忆巩固）
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    last_message_at TIMESTAMP NOT NULL
);

-- 消息表
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(id),
    sender_type VARCHAR(20) NOT NULL,
    sender_id UUID NOT NULL,
    content TEXT NOT NULL,
    message_type VARCHAR(20) NOT NULL,
    metadata JSONB,  -- 包含intent, entities, sentiment, thinking_steps等
    embedding VECTOR(1536),  -- 向量嵌入（用于语义搜索，对齐MM-11）
    importance_score FLOAT DEFAULT 0.5,  -- 重要性评分
    created_at TIMESTAMP NOT NULL
);

-- 会话记忆巩固记录（对齐MM-06）
CREATE TABLE session_consolidations (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(id),
    consolidated_at TIMESTAMP NOT NULL,
    key_learnings TEXT,
    memory_ids UUID[]
);

-- 索引
CREATE INDEX idx_chat_sessions_user ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_importance ON chat_sessions(importance_score);
CREATE INDEX idx_chat_messages_session ON chat_messages(session_id);
CREATE INDEX idx_chat_messages_embedding ON chat_messages USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_chat_messages_importance ON chat_messages(importance_score);
```


## 七、前端组件结构

```
frontend/src/components/chat/
├── ChatWindow.vue           # 主对话窗口
├── ChatMessage.vue          # 消息气泡组件
├── ThinkingSteps.vue        # 思考过程折叠面板（对齐AGENT-RUNTIME-03）
├── EmotionalIndicator.vue   # 情感状态指示器（对齐AGENT-RUNTIME-10）
├── CounterfactualPanel.vue  # 反事实分析面板（对齐AGENT-RUNTIME-07）
├── ChatInput.vue            # 输入框组件
├── ChatSidebar.vue          # 会话侧边栏
├── SessionList.vue          # 会话列表
├── QuickCommands.vue        # 快捷指令
├── VoiceInput.vue           # 语音输入（对齐PC-04）
├── VoiceSettings.vue        # 语音设置
└── ChatHistory.vue          # 历史对话页面
```


## 八、在Cursor中使用

```bash
# 1. 实现智能对话核心（对齐通用能力）
@docs/CHAT_SYSTEM_MODULE_v1.0.md 实现CH-01智能对话功能，基于PC-01自然语言理解和AGENT-RUNTIME-01主循环

# 2. 实现思考过程展示（对齐AGENT-RUNTIME-03）
@docs/CHAT_SYSTEM_MODULE_v1.0.md 根据AGENT-RUNTIME-03，在对话中展示智能体的思考过程

# 3. 实现任务下达（对齐DC-01）
@docs/CHAT_SYSTEM_MODULE_v1.0.md 实现CH-02任务下达，基于DC-01任务规划能力

# 4. 实现反事实分析（对齐AGENT-RUNTIME-07）
@docs/CHAT_SYSTEM_MODULE_v1.0.md 根据AGENT-RUNTIME-07，在方案选择时提供反事实分析

# 5. 实现语义搜索（对齐MM-04）
@docs/CHAT_SYSTEM_MODULE_v1.0.md 实现CH-04对话历史，基于MM-04记忆检索支持语义搜索

# 6. 实现情感语音（对齐AGENT-RUNTIME-10）
@docs/CHAT_SYSTEM_MODULE_v1.0.md 实现CH-05语音交互，支持情感语音合成
```


## 九、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，对齐AGENT_ABILITY_SPEC_v1.0.md通用能力 |

---

**文档结束**