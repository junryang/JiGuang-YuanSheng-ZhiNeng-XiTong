# 自动化工作流能力 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\AUTOMATION_WORKFLOW_v1.0.md
```


# 自动化工作流能力 v1.0

## 一、能力总览

```yaml
module: "自动化工作流"
description: "支持内容创作到分发的自动化流程编排，定时/触发式任务执行，跨平台联动"
priority: "P0"
domain: "营销中心"

# 关联的通用能力
related_abilities:
  - "PC-01: 自然语言理解"
  - "CG-01: 推理能力"
  - "DC-01: 任务规划"
  - "DC-02: 子任务分解"
  - "DC-03: 工具选择"
  - "EX-09: 并行执行"
  - "EX-10: 异步执行"
  - "EX-11: 定时执行"
  - "EX-12: 批量执行"
  - "EX-21: 条件执行"
  - "AUTO-01: 任务自动规划"
  - "AUTO-03: 工作流自动化编排"
  - "AUTO-05: 智能定时与触发任务"
  - "CL-03: 消息通信"
  - "WEB-05: 社交媒体交互"
  - "WEB-06: 在线文档与协作工具"

functions:
  total_count: 4
  categories:
    - "内容工作流编排"
    - "定时任务调度"
    - "事件触发执行"
    - "跨平台联动"
```


## 二、数据模型定义

```yaml
# 工作流数据模型

data_models:
  # 工作流定义
  Workflow:
    id: str
    name: str
    description: str
    version: str
    status: str  # draft, active, paused, archived
    trigger: WorkflowTrigger
    steps: List[WorkflowStep]
    error_handling: ErrorHandlingConfig
    notifications: NotificationConfig
    created_at: datetime
    updated_at: datetime
    created_by: str

  # 工作流触发器
  WorkflowTrigger:
    type: str  # schedule, event, webhook, manual
    config:
      schedule: optional[CronExpression]  # 定时触发
      event_type: optional[str]           # 事件触发
      event_filter: optional[dict]        # 事件过滤
      webhook_url: optional[str]          # Webhook触发

  # 工作流步骤
  WorkflowStep:
    id: str
    name: str
    type: str  # generate, review, approve, publish, notify, condition, parallel, wait
    tool: str  # 使用的工具（自研或第三方）
    input_mapping: dict
    output_mapping: dict
    timeout: int
    retry_count: int
    retry_delay: int
    condition: optional[str]  # 条件表达式

  # 工作流执行实例
  WorkflowExecution:
    id: str
    workflow_id: str
    status: str  # pending, running, paused, completed, failed, cancelled
    current_step: int
    input_data: dict
    output_data: dict
    step_results: List[StepResult]
    error_message: optional[str]
    started_at: datetime
    completed_at: optional[datetime]
    triggered_by: str

  # 步骤执行结果
  StepResult:
    step_id: str
    status: str  # pending, running, completed, failed, skipped
    input: dict
    output: dict
    error: optional[str]
    duration_ms: int
    started_at: datetime
    completed_at: optional[datetime]

  # 触发式任务
  TriggerTask:
    id: str
    name: str
    description: str
    trigger_type: str  # event, webhook, condition
    trigger_config: dict
    actions: List[dict]
    status: str  # active, inactive
    last_triggered: optional[datetime]
    created_at: datetime

  # 跨平台联动规则
  CrossPlatformRule:
    id: str
    name: str
    source_platform: str
    source_action: str  # publish, update, delete
    target_platforms: List[str]
    target_action: str  # publish, update, delete
    content_mapping: dict
    delay_seconds: int
    enabled: bool
```


## 三、功能详细设计

### 3.1 MK-27 内容工作流

```yaml
# MK-27 内容工作流
function_id: "MK-27"
name: "内容工作流"
description: "从创意到分发的自动化流程编排，支持多Agent协作"
priority: "P0"
implementation: "自研Agent编排"
related_abilities: ["DC-01", "DC-02", "DC-03", "EX-09", "EX-10", "AUTO-01", "AUTO-03", "CL-03"]

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/workflows"
    description: "创建工作流"
    request_body:
      name: "str"
      description: "str"
      steps: "List[WorkflowStep]"
      trigger: "WorkflowTrigger"
    response:
      workflow: "Workflow"

  - method: "GET"
    endpoint: "/api/v1/marketing/workflows"
    description: "获取工作流列表"
    query_params:
      status: "str"
      page: "int"
      page_size: "int"
    response:
      workflows: "List[Workflow]"
      pagination: "dict"

  - method: "GET"
    endpoint: "/api/v1/marketing/workflows/{id}"
    description: "获取工作流详情"
    response:
      workflow: "Workflow"

  - method: "PUT"
    endpoint: "/api/v1/marketing/workflows/{id}"
    description: "更新工作流"
    response:
      workflow: "Workflow"

  - method: "DELETE"
    endpoint: "/api/v1/marketing/workflows/{id}"
    description: "删除工作流"

  - method: "POST"
    endpoint: "/api/v1/marketing/workflows/{id}/execute"
    description: "手动执行工作流"
    request_body:
      input_data: "dict"
    response:
      execution: "WorkflowExecution"

  - method: "GET"
    endpoint: "/api/v1/marketing/workflows/executions/{id}"
    description: "获取执行状态"
    response:
      execution: "WorkflowExecution"

  - method: "POST"
    endpoint: "/api/v1/marketing/workflows/executions/{id}/cancel"
    description: "取消执行"
    response:
      success: "bool"

# 预置工作流模板
workflow_templates:
  - id: "WF-01"
    name: "标准内容发布流程"
    description: "策划→写作→审核→分发的完整流程"
    steps:
      - step: 1
        name: "内容策划"
        agent: "策划Agent"
        tool: "deepseek"
        action: "generate_plan"
        
      - step: 2
        name: "内容生成"
        agent: "写作Agent"
        tool: "deepseek"
        action: "generate"
        
      - step: 3
        name: "内容审核"
        agent: "审核Agent"
        tool: "builtin"
        action: "review"
        require_approval: true
        
      - step: 4
        name: "多平台分发"
        agent: "分发Agent"
        tool: "jumeitong"
        action: "publish"
        
  - id: "WF-02"
    name: "视频内容制作流程"
    description: "脚本→视频生成→审核→发布"
    steps:
      - step: 1
        name: "脚本生成"
        agent: "写作Agent"
        tool: "deepseek"
        action: "generate_script"
        
      - step: 2
        name: "视频生成"
        agent: "视频Agent"
        tool: "qianmeng"
        action: "generate_video"
        
      - step: 3
        name: "内容审核"
        agent: "审核Agent"
        tool: "builtin"
        action: "review"
        
      - step: 4
        name: "视频分发"
        agent: "分发Agent"
        tool: "jumeitong"
        action: "publish_video"

  - id: "WF-03"
    name: "数据报告生成流程"
    description: "数据采集→分析→报告生成→分发"
    steps:
      - step: 1
        name: "数据采集"
        agent: "数据Agent"
        tool: "platform_api"
        action: "collect"
        
      - step: 2
        name: "数据分析"
        agent: "分析Agent"
        tool: "builtin"
        action: "analyze"
        
      - step: 3
        name: "报告生成"
        agent: "写作Agent"
        tool: "deepseek"
        action: "generate_report"
        
      - step: 4
        name: "报告分发"
        agent: "分发Agent"
        tool: "email"
        action: "send"

# 实现示例
class WorkflowEngine:
    """工作流引擎 - 对齐DC-01任务规划、DC-02子任务分解、AUTO-03工作流编排"""
    
    def __init__(self):
        self.execution_store = ExecutionStore()
        self.step_executors = {
            "generate": GenerateExecutor(),
            "review": ReviewExecutor(),
            "approve": ApproveExecutor(),
            "publish": PublishExecutor(),
            "notify": NotifyExecutor(),
            "condition": ConditionExecutor(),
            "parallel": ParallelExecutor(),
            "wait": WaitExecutor()
        }
    
    async def execute_workflow(self, workflow_id: str, 
                                input_data: dict,
                                trigger_info: dict = None) -> WorkflowExecution:
        """执行工作流 - 对齐DC-01、DC-02"""
        workflow = await self._get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # 创建工作流执行实例
        execution = WorkflowExecution(
            id=self._generate_id(),
            workflow_id=workflow_id,
            status="pending",
            current_step=0,
            input_data=input_data,
            step_results=[],
            started_at=datetime.now(),
            triggered_by=trigger_info.get("triggered_by", "manual") if trigger_info else "manual"
        )
        await self.execution_store.save(execution)
        
        # 异步执行工作流（对齐EX-10）
        asyncio.create_task(self._run_workflow(execution, workflow))
        
        return execution
    
    async def _run_workflow(self, execution: WorkflowExecution, workflow: Workflow):
        """运行工作流 - 对齐AUTO-03"""
        execution.status = "running"
        await self.execution_store.update(execution)
        
        try:
            # 准备上下文
            context = {
                "input": execution.input_data,
                "step_results": {},
                "variables": {}
            }
            
            # 按顺序执行步骤（对齐DC-02）
            for i, step in enumerate(workflow.steps):
                execution.current_step = i
                await self.execution_store.update(execution)
                
                # 执行步骤
                step_result = await self._execute_step(step, context)
                execution.step_results.append(step_result)
                
                # 更新上下文
                context["step_results"][step.id] = step_result.output
                if step_result.output:
                    context["variables"].update(step_result.output)
                
                # 检查步骤状态
                if step_result.status == "failed":
                    # 错误处理
                    if workflow.error_handling.get("action") == "stop":
                        execution.status = "failed"
                        execution.error_message = step_result.error
                        break
                    elif workflow.error_handling.get("action") == "continue":
                        continue
                    elif workflow.error_handling.get("action") == "retry":
                        # 重试逻辑
                        for retry in range(step.retry_count):
                            step_result = await self._execute_step(step, context, retry=retry+1)
                            if step_result.status == "completed":
                                break
                        if step_result.status != "completed":
                            execution.status = "failed"
                            execution.error_message = step_result.error
                            break
            
            # 检查是否所有步骤完成
            if execution.status != "failed":
                execution.status = "completed"
            
        except Exception as e:
            execution.status = "failed"
            execution.error_message = str(e)
        
        finally:
            execution.completed_at = datetime.now()
            await self.execution_store.update(execution)
            
            # 发送通知
            await self._send_notification(execution, workflow)
    
    async def _execute_step(self, step: WorkflowStep, context: dict, retry: int = 0) -> StepResult:
        """执行单个步骤 - 对齐DC-03工具选择"""
        step_result = StepResult(
            step_id=step.id,
            status="running",
            input=context,
            started_at=datetime.now()
        )
        
        try:
            # 解析输入
            resolved_input = self._resolve_input(step.input_mapping, context)
            
            # 获取执行器（对齐DC-03）
            executor = self.step_executors.get(step.type)
            if not executor:
                raise ValueError(f"Unknown step type: {step.type}")
            
            # 执行（带超时控制）
            output = await asyncio.wait_for(
                executor.execute(step, resolved_input),
                timeout=step.timeout
            )
            
            step_result.status = "completed"
            step_result.output = output
            
        except asyncio.TimeoutError:
            step_result.status = "failed"
            step_result.error = f"Step timeout after {step.timeout}s"
        except Exception as e:
            step_result.status = "failed"
            step_result.error = str(e)
        
        finally:
            step_result.completed_at = datetime.now()
            step_result.duration_ms = int((step_result.completed_at - step_result.started_at).total_seconds() * 1000)
        
        return step_result
```

### 3.2 MK-28 定时任务

```yaml
# MK-28 定时任务
function_id: "MK-28"
name: "定时任务"
description: "定时生成、定时发布内容"
priority: "P0"
implementation: "自研定时调度器"
related_abilities: ["EX-11", "AUTO-05"]

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/schedule/tasks"
    description: "创建定时任务"
    request_body:
      name: "str"
      workflow_id: "str"
      cron: "str"
      input_data: "dict"
      enabled: "bool"
    response:
      task: "ScheduledTask"

  - method: "GET"
    endpoint: "/api/v1/marketing/schedule/tasks"
    description: "获取定时任务列表"
    response:
      tasks: "List[ScheduledTask]"

  - method: "PUT"
    endpoint: "/api/v1/marketing/schedule/tasks/{id}"
    description: "更新定时任务"
    response:
      task: "ScheduledTask"

  - method: "DELETE"
    endpoint: "/api/v1/marketing/schedule/tasks/{id}"
    description: "删除定时任务"

  - method: "POST"
    endpoint: "/api/v1/marketing/schedule/tasks/{id}/toggle"
    description: "启用/禁用定时任务"
    request_body:
      enabled: "bool"
    response:
      success: "bool"

# 实现示例
class ScheduleManager:
    """定时任务管理器 - 对齐EX-11定时执行、AUTO-05智能定时触发"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.task_store = TaskStore()
        self._init_scheduler()
    
    def _init_scheduler(self):
        """初始化调度器"""
        # 加载所有启用的定时任务
        tasks = await self.task_store.get_enabled_tasks()
        for task in tasks:
            self._add_job(task)
        
        # 启动调度器
        self.scheduler.start()
    
    async def create_task(self, name: str, workflow_id: str, 
                          cron: str, input_data: dict) -> ScheduledTask:
        """创建定时任务"""
        task = ScheduledTask(
            id=self._generate_id(),
            name=name,
            workflow_id=workflow_id,
            cron=cron,
            input_data=input_data,
            enabled=True,
            created_at=datetime.now()
        )
        
        await self.task_store.save(task)
        self._add_job(task)
        
        return task
    
    def _add_job(self, task: ScheduledTask):
        """添加定时任务"""
        self.scheduler.add_job(
            func=self._execute_scheduled_task,
            trigger="cron",
            **self._parse_cron(task.cron),
            id=task.id,
            args=[task.id],
            replace_existing=True
        )
    
    async def _execute_scheduled_task(self, task_id: str):
        """执行定时任务"""
        task = await self.task_store.get(task_id)
        if not task or not task.enabled:
            return
        
        # 记录执行历史
        execution_record = {
            "task_id": task_id,
            "started_at": datetime.now(),
            "status": "running"
        }
        
        try:
            # 执行工作流（对齐EX-11）
            workflow_engine = WorkflowEngine()
            execution = await workflow_engine.execute_workflow(
                workflow_id=task.workflow_id,
                input_data=task.input_data,
                trigger_info={"triggered_by": "schedule", "task_id": task_id}
            )
            
            execution_record["execution_id"] = execution.id
            execution_record["status"] = execution.status
            execution_record["completed_at"] = datetime.now()
            
        except Exception as e:
            execution_record["status"] = "failed"
            execution_record["error"] = str(e)
            execution_record["completed_at"] = datetime.now()
        
        # 保存执行记录
        await self.task_store.add_execution_record(execution_record)
```

### 3.3 MK-29 触发式任务

```yaml
# MK-29 触发式任务
function_id: "MK-29"
name: "触发式任务"
description: "事件触发自动营销，支持Webhook、条件触发"
priority: "P1"
implementation: "自研事件驱动引擎"
related_abilities: ["EX-21", "CL-03", "AUTO-05"]

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/triggers"
    description: "创建触发式任务"
    request_body:
      name: "str"
      trigger_type: "str"  # event, webhook, condition
      trigger_config: "dict"
      actions: "List[dict]"
    response:
      trigger: "TriggerTask"

  - method: "GET"
    endpoint: "/api/v1/marketing/triggers"
    description: "获取触发式任务列表"
    response:
      triggers: "List[TriggerTask]"

  - method: "POST"
    endpoint: "/api/v1/marketing/triggers/webhook/{token}"
    description: "Webhook接收端点"
    request_body: "dict"
    response:
      received: "bool"

  - method: "POST"
    endpoint: "/api/v1/marketing/triggers/test"
    description: "测试触发条件"
    request_body:
      trigger_id: "str"
      event_data: "dict"
    response:
      matched: "bool"
      actions: "List[dict]"

# 实现示例
class TriggerEngine:
    """触发式任务引擎 - 对齐EX-21条件执行、CL-03消息通信"""
    
    def __init__(self):
        self.trigger_store = TriggerStore()
        self.event_bus = EventBus()  # 对齐CL-03
        self._init_event_listeners()
    
    def _init_event_listeners(self):
        """初始化事件监听器"""
        # 监听平台事件
        self.event_bus.subscribe("platform.publish", self._on_platform_publish)
        self.event_bus.subscribe("platform.comment", self._on_platform_comment)
        self.event_bus.subscribe("platform.follow", self._on_platform_follow)
        self.event_bus.subscribe("data.threshold", self._on_data_threshold)
        self.event_bus.subscribe("time.condition", self._on_time_condition)
    
    async def create_trigger(self, name: str, trigger_type: str,
                             trigger_config: dict, actions: List[dict]) -> TriggerTask:
        """创建触发式任务"""
        trigger = TriggerTask(
            id=self._generate_id(),
            name=name,
            trigger_type=trigger_type,
            trigger_config=trigger_config,
            actions=actions,
            status="active",
            created_at=datetime.now()
        )
        
        await self.trigger_store.save(trigger)
        
        # 如果是Webhook类型，注册端点
        if trigger_type == "webhook":
            await self._register_webhook(trigger.id, trigger_config.get("url"))
        
        return trigger
    
    async def _on_platform_publish(self, event: dict):
        """平台发布事件处理"""
        await self._evaluate_triggers("event", {
            "type": "platform.publish",
            "platform": event.get("platform"),
            "content_id": event.get("content_id"),
            "timestamp": event.get("timestamp")
        })
    
    async def _on_data_threshold(self, event: dict):
        """数据阈值事件处理 - 对齐EX-21条件执行"""
        await self._evaluate_triggers("condition", {
            "metric": event.get("metric"),
            "value": event.get("value"),
            "threshold": event.get("threshold"),
            "operator": event.get("operator")
        })
    
    async def _evaluate_triggers(self, trigger_type: str, event_data: dict):
        """评估触发条件"""
        triggers = await self.trigger_store.get_by_type(trigger_type)
        
        for trigger in triggers:
            if trigger.status != "active":
                continue
            
            # 检查条件是否满足（对齐EX-21）
            matched = await self._evaluate_condition(trigger.trigger_config, event_data)
            
            if matched:
                # 执行动作
                asyncio.create_task(self._execute_actions(trigger.actions, event_data))
                
                # 更新最后触发时间
                trigger.last_triggered = datetime.now()
                await self.trigger_store.update(trigger)
    
    async def _evaluate_condition(self, config: dict, event_data: dict) -> bool:
        """评估条件 - 对齐EX-21"""
        condition_type = config.get("type")
        
        if condition_type == "threshold":
            metric = config.get("metric")
            threshold = config.get("threshold")
            operator = config.get("operator", ">=")
            
            value = event_data.get(metric)
            if value is None:
                return False
            
            if operator == ">=":
                return value >= threshold
            elif operator == ">":
                return value > threshold
            elif operator == "<=":
                return value <= threshold
            elif operator == "<":
                return value < threshold
            elif operator == "==":
                return value == threshold
        
        elif condition_type == "event_match":
            event_type = config.get("event_type")
            return event_data.get("type") == event_type
        
        elif condition_type == "webhook":
            # Webhook总是触发
            return True
        
        return False
```

### 3.4 MK-30 跨平台联动

```yaml
# MK-30 跨平台联动
function_id: "MK-30"
name: "跨平台联动"
description: "一个平台发布触发其他平台自动发布"
priority: "P2"
implementation: "自研联动引擎"
related_abilities: ["EX-09", "EX-10", "CL-03", "WEB-05"]

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/cross-platform/rules"
    description: "创建跨平台联动规则"
    request_body:
      name: "str"
      source_platform: "str"
      source_action: "str"
      target_platforms: "List[str]"
      target_action: "str"
      content_mapping: "dict"
      delay_seconds: "int"
    response:
      rule: "CrossPlatformRule"

  - method: "GET"
    endpoint: "/api/v1/marketing/cross-platform/rules"
    description: "获取联动规则列表"
    response:
      rules: "List[CrossPlatformRule]"

  - method: "PUT"
    endpoint: "/api/v1/marketing/cross-platform/rules/{id}"
    description: "更新联动规则"
    response:
      rule: "CrossPlatformRule"

  - method: "DELETE"
    endpoint: "/api/v1/marketing/cross-platform/rules/{id}"
    description: "删除联动规则"

  - method: "POST"
    endpoint: "/api/v1/marketing/cross-platform/sync"
    description: "手动同步内容到其他平台"
    request_body:
      source_content_id: "str"
      target_platforms: "List[str]"
    response:
      task_id: "str"

# 实现示例
class CrossPlatformEngine:
    """跨平台联动引擎 - 对齐WEB-05社交媒体交互、CL-03消息通信"""
    
    def __init__(self):
        self.rule_store = RuleStore()
        self.event_bus = EventBus()  # 对齐CL-03
        self._init_listeners()
    
    def _init_listeners(self):
        """初始化监听器"""
        self.event_bus.subscribe("platform.publish", self._on_platform_publish)
        self.event_bus.subscribe("platform.update", self._on_platform_update)
        self.event_bus.subscribe("platform.delete", self._on_platform_delete)
    
    async def create_rule(self, name: str, source_platform: str,
                          source_action: str, target_platforms: List[str],
                          target_action: str, content_mapping: dict,
                          delay_seconds: int = 0) -> CrossPlatformRule:
        """创建联动规则"""
        rule = CrossPlatformRule(
            id=self._generate_id(),
            name=name,
            source_platform=source_platform,
            source_action=source_action,
            target_platforms=target_platforms,
            target_action=target_action,
            content_mapping=content_mapping,
            delay_seconds=delay_seconds,
            enabled=True,
            created_at=datetime.now()
        )
        
        await self.rule_store.save(rule)
        return rule
    
    async def _on_platform_publish(self, event: dict):
        """平台发布事件处理"""
        platform = event.get("platform")
        action = "publish"
        content = event.get("content")
        content_id = event.get("content_id")
        
        await self._apply_rules(platform, action, content, content_id)
    
    async def _apply_rules(self, source_platform: str, source_action: str,
                           content: dict, source_content_id: str):
        """应用联动规则"""
        rules = await self.rule_store.get_by_source(source_platform, source_action)
        
        for rule in rules:
            if not rule.enabled:
                continue
            
            # 应用内容映射
            mapped_content = self._apply_content_mapping(content, rule.content_mapping)
            
            # 延迟执行（对齐EX-10异步执行）
            if rule.delay_seconds > 0:
                asyncio.create_task(self._delayed_publish(
                    rule, mapped_content, source_content_id
                ))
            else:
                asyncio.create_task(self._publish_to_targets(
                    rule, mapped_content, source_content_id
                ))
    
    async def _delayed_publish(self, rule: CrossPlatformRule, 
                                content: dict, source_content_id: str):
        """延迟发布"""
        await asyncio.sleep(rule.delay_seconds)
        await self._publish_to_targets(rule, content, source_content_id)
    
    async def _publish_to_targets(self, rule: CrossPlatformRule,
                                   content: dict, source_content_id: str):
        """发布到目标平台 - 对齐EX-09并行执行"""
        tasks = []
        for target_platform in rule.target_platforms:
            task = self._publish_to_platform(
                target_platform, 
                rule.target_action,
                content,
                source_content_id
            )
            tasks.append(task)
        
        # 并行执行（对齐EX-09）
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 记录联动结果
        await self._record_sync_result(source_content_id, rule.id, results)
    
    async def _publish_to_platform(self, platform: str, action: str,
                                    content: dict, source_content_id: str):
        """发布到单个平台 - 对齐WEB-05"""
        # 获取平台API
        platform_api = self._get_platform_api(platform)
        if not platform_api:
            raise ValueError(f"Unsupported platform: {platform}")
        
        if action == "publish":
            result = await platform_api.post(content)
        elif action == "update":
            result = await platform_api.update(content.get("id"), content)
        elif action == "delete":
            result = await platform_api.delete(content.get("id"))
        else:
            raise ValueError(f"Unknown action: {action}")
        
        return {
            "platform": platform,
            "action": action,
            "success": True,
            "content_id": result.get("id"),
            "url": result.get("url")
        }
```

## 四、自动化工作流架构图

```yaml
architecture: |
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                           自动化工作流架构                                  │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │                                                                             │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         触发层                                       │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 定时触发    │  │ 事件触发    │  │ Webhook触发 │                  │   │
  │  │  │ (EX-11)     │  │ (CL-03)     │  │ (AUTO-05)   │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         编排层                                       │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 工作流引擎  │  │ 任务规划    │  │ 步骤执行    │                  │   │
  │  │  │ (AUTO-03)   │  │ (DC-01)     │  │ (DC-02)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         执行层                                       │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 内容生成    │  │ 审核批准    │  │ 平台分发    │                  │   │
  │  │  │ (EX-01)     │  │ (APPROVE)   │  │ (WEB-05)    │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         联动层                                       │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 跨平台联动  │  │ 内容同步    │  │ 数据反馈    │                  │   │
  │  │  │ (MK-30)     │  │ (EX-12)     │  │ (CL-03)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                                                             │
  └─────────────────────────────────────────────────────────────────────────────┘
```

## 五、通用能力映射表

```yaml
# 自动化工作流功能与通用能力映射
general_ability_mapping:
  DC-01_任务规划:
    mapped_functions: ["MK-27"]
    description: "工作流整体规划"
    
  DC-02_子任务分解:
    mapped_functions: ["MK-27"]
    description: "将工作流分解为可执行步骤"
    
  DC-03_工具选择:
    mapped_functions: ["MK-27"]
    description: "为每个步骤选择合适工具"
    
  EX-09_并行执行:
    mapped_functions: ["MK-27", "MK-30"]
    description: "并行执行多个步骤或平台发布"
    
  EX-10_异步执行:
    mapped_functions: ["MK-27", "MK-28", "MK-29", "MK-30"]
    description: "异步执行工作流和任务"
    
  EX-11_定时执行:
    mapped_functions: ["MK-28"]
    description: "按Cron表达式定时执行"
    
  EX-12_批量执行:
    mapped_functions: ["MK-27"]
    description: "批量处理多个任务"
    
  EX-21_条件执行:
    mapped_functions: ["MK-29"]
    description: "条件触发执行"
    
  AUTO-01_任务自动规划:
    mapped_functions: ["MK-27"]
    description: "自动规划工作流步骤"
    
  AUTO-03_工作流自动化编排:
    mapped_functions: ["MK-27"]
    description: "工作流编排引擎"
    
  AUTO-05_智能定时与触发:
    mapped_functions: ["MK-28", "MK-29"]
    description: "智能定时和事件触发"
    
  CL-03_消息通信:
    mapped_functions: ["MK-29", "MK-30"]
    description: "事件总线通信"
    
  WEB-05_社交媒体交互:
    mapped_functions: ["MK-30"]
    description: "跨平台内容发布"
    
  WEB-06_在线文档协作:
    mapped_functions: ["MK-27"]
    description: "文档协作工作流"
```

## 六、数据库表结构

```sql
-- 工作流定义表
CREATE TABLE workflows (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    version VARCHAR(20),
    status VARCHAR(20) DEFAULT 'draft',
    trigger_config JSONB,
    steps JSONB NOT NULL,
    error_handling JSONB,
    notifications JSONB,
    created_by UUID REFERENCES agents(id),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 工作流执行记录表
CREATE TABLE workflow_executions (
    id UUID PRIMARY KEY,
    workflow_id UUID REFERENCES workflows(id),
    status VARCHAR(20) DEFAULT 'pending',
    current_step INTEGER,
    input_data JSONB,
    output_data JSONB,
    step_results JSONB,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    triggered_by VARCHAR(100),
    created_at TIMESTAMP NOT NULL
);

-- 定时任务表
CREATE TABLE scheduled_tasks (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    workflow_id UUID REFERENCES workflows(id),
    cron VARCHAR(100) NOT NULL,
    input_data JSONB,
    enabled BOOLEAN DEFAULT TRUE,
    last_run TIMESTAMP,
    next_run TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 定时任务执行记录表
CREATE TABLE scheduled_task_logs (
    id UUID PRIMARY KEY,
    task_id UUID REFERENCES scheduled_tasks(id),
    execution_id UUID,
    status VARCHAR(20),
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL
);

-- 触发式任务表
CREATE TABLE trigger_tasks (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    trigger_type VARCHAR(50) NOT NULL,
    trigger_config JSONB,
    actions JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    last_triggered TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 跨平台联动规则表
CREATE TABLE cross_platform_rules (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    source_platform VARCHAR(50) NOT NULL,
    source_action VARCHAR(50) NOT NULL,
    target_platforms TEXT[] NOT NULL,
    target_action VARCHAR(50) NOT NULL,
    content_mapping JSONB,
    delay_seconds INTEGER DEFAULT 0,
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 跨平台联动记录表
CREATE TABLE cross_platform_sync_logs (
    id UUID PRIMARY KEY,
    rule_id UUID REFERENCES cross_platform_rules(id),
    source_content_id VARCHAR(200),
    source_platform VARCHAR(50),
    target_results JSONB,
    status VARCHAR(20),
    created_at TIMESTAMP NOT NULL
);

-- 索引
CREATE INDEX idx_workflows_status ON workflows(status);
CREATE INDEX idx_workflow_executions_workflow ON workflow_executions(workflow_id);
CREATE INDEX idx_workflow_executions_status ON workflow_executions(status);
CREATE INDEX idx_scheduled_tasks_enabled ON scheduled_tasks(enabled);
CREATE INDEX idx_scheduled_tasks_next_run ON scheduled_tasks(next_run);
CREATE INDEX idx_trigger_tasks_status ON trigger_tasks(status);
CREATE INDEX idx_cross_platform_rules_source ON cross_platform_rules(source_platform, source_action);
CREATE INDEX idx_cross_platform_rules_enabled ON cross_platform_rules(enabled);
```

## 七、预置工作流模板

```sql
-- 预置工作流模板数据
INSERT INTO workflows (id, name, description, version, status, steps, created_at) VALUES
('wf_standard_publish', '标准内容发布流程', '策划→写作→审核→分发的完整流程', '1.0', 'active', 
 '[{"id":"step1","name":"内容策划","type":"generate","tool":"deepseek","action":"generate_plan"},
   {"id":"step2","name":"内容生成","type":"generate","tool":"deepseek","action":"generate"},
   {"id":"step3","name":"内容审核","type":"review","tool":"builtin","action":"review","require_approval":true},
   {"id":"step4","name":"多平台分发","type":"publish","tool":"jumeitong","action":"publish"}]',
 NOW()),

('wf_video_publish', '视频内容制作流程', '脚本→视频生成→审核→发布', '1.0', 'active',
 '[{"id":"step1","name":"脚本生成","type":"generate","tool":"deepseek","action":"generate_script"},
   {"id":"step2","name":"视频生成","type":"generate","tool":"qianmeng","action":"generate_video"},
   {"id":"step3","name":"内容审核","type":"review","tool":"builtin","action":"review"},
   {"id":"step4","name":"视频分发","type":"publish","tool":"jumeitong","action":"publish_video"}]',
 NOW()),

('wf_report_generate', '数据报告生成流程', '数据采集→分析→报告生成→分发', '1.0', 'active',
 '[{"id":"step1","name":"数据采集","type":"collect","tool":"platform_api","action":"collect"},
   {"id":"step2","name":"数据分析","type":"analyze","tool":"builtin","action":"analyze"},
   {"id":"step3","name":"报告生成","type":"generate","tool":"deepseek","action":"generate_report"},
   {"id":"step4","name":"报告分发","type":"publish","tool":"email","action":"send"}]',
 NOW());
```

## 八、在Cursor中使用

```bash
# 1. 实现内容工作流
@docs/AUTOMATION_WORKFLOW_v1.0.md 实现MK-27内容工作流，支持多步骤编排和Agent协作

# 2. 实现定时任务
@docs/AUTOMATION_WORKFLOW_v1.0.md 实现MK-28定时任务，支持Cron表达式调度

# 3. 实现触发式任务
@docs/AUTOMATION_WORKFLOW_v1.0.md 实现MK-29触发式任务，支持事件和Webhook触发

# 4. 实现跨平台联动
@docs/AUTOMATION_WORKFLOW_v1.0.md 实现MK-30跨平台联动，一个平台发布触发其他平台

# 5. 创建工作流模板
@docs/AUTOMATION_WORKFLOW_v1.0.md 根据预置模板创建标准内容发布工作流
```

## 九、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，4项自动化工作流功能，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md |

---

**文档结束**