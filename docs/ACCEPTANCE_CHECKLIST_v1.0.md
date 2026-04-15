# 功能验收清单 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\ACCEPTANCE_CHECKLIST_v1.0.md
```


# 功能验收清单 v1.0

## 一、验收总览

```yaml
module: "功能验收清单"
description: "营销中心各功能模块的验收标准和测试方法"
priority: "P0"
domain: "营销中心"

# 关联的通用能力
related_abilities:
  - "EX-01: 代码生成"
  - "EX-03: API调用"
  - "EX-07: 测试执行"
  - "EX-08: 消息发送"
  - "EX-09: 并行执行"
  - "EX-11: 定时执行"
  - "EX-12: 批量执行"
  - "PC-01: 自然语言理解"
  - "CG-01: 推理能力"
  - "CG-04: 数值推理"
  - "WEB-04: API调用与集成"
  - "WEB-05: 社交媒体交互"
  - "QL-05: 质量验证"

functions:
  total_count: 5
  categories:
    - "内容生成验收"
    - "多平台分发验收"
    - "接单匹配验收"
    - "数据分析验收"
    - "自动化工作流验收"
```


## 二、验收标准详细定义

### 2.1 MK-01 文本内容生成

```yaml
# MK-01 文本内容生成验收
function_id: "MK-01"
name: "文本内容生成"
description: "基于输入主题生成文章、文案、脚本"
priority: "P0"

# 验收标准
acceptance_criteria:
  - id: "AC-01-01"
    criterion: "输入'AI营销趋势'，300秒内生成1500字文章"
    test_method: "功能测试"
    test_type: "functional"
    expected_result: "生成文章长度≥1500字，内容相关"
    
  - id: "AC-01-02"
    criterion: "生成内容无语法错误"
    test_method: "自动化测试"
    test_type: "quality"
    expected_result: "语法错误率<1%"
    
  - id: "AC-01-03"
    criterion: "生成内容原创度>85%"
    test_method: "工具检测"
    test_type: "quality"
    expected_result: "原创度≥85%"
    
  - id: "AC-01-04"
    criterion: "支持中英文双语生成"
    test_method: "功能测试"
    test_type: "functional"
    expected_result: "中英文均可生成"
    
  - id: "AC-01-05"
    criterion: "P95响应时间≤180秒，单次上限≤300秒"
    test_method: "性能测试"
    test_type: "performance"
    expected_result: "响应时间≤300秒"

# 测试用例
test_cases:
  - id: "TC-01-01"
    name: "基础生成测试"
    input: "AI营销趋势"
    steps:
      - "调用文本生成API"
      - "传入主题'AI营销趋势'"
      - "等待生成完成"
    expected:
      content_length: "≥1500字"
      time_limit: "≤300秒"
      relevance: "主题相关"
      
  - id: "TC-01-02"
    name: "边界测试"
    input: "空主题"
    steps:
      - "调用文本生成API"
      - "传入空主题"
    expected:
      error_code: "10001"
      message: "主题不能为空"
      
  - id: "TC-01-03"
    name: "性能测试"
    input: "长篇技术文章"
    steps:
      - "连续调用10次生成API"
      - "记录每次响应时间"
    expected:
      avg_response_time: "≤300秒"
      p95_response_time: "≤180秒"
      success_rate: "≥95%"

# 实现示例
class TextGenerationValidator:
    """文本生成验证器 - 对齐QL-05质量验证、EX-07测试执行"""
    
    def __init__(self):
        self.quality_checker = QualityChecker()  # 对齐QL-05
        self.test_runner = TestRunner()  # 对齐EX-07
    
    async def validate_generation(self, topic: str, expected_length: int) -> ValidationResult:
        """验证文本生成 - 对齐QL-05"""
        start_time = datetime.now()
        
        # 执行生成
        result = await self._generate_content(topic)
        
        # 验证长度
        length_valid = len(result.content) >= expected_length
        
        # 验证时间
        elapsed = (datetime.now() - start_time).total_seconds()
        time_valid = elapsed <= 300  # 5分钟
        
        # 验证质量（对齐QL-05）
        quality_score = await self.quality_checker.assess(result.content)
        
        return ValidationResult(
            passed=length_valid and time_valid and quality_score >= 0.7,
            details={
                "length": len(result.content),
                "elapsed_seconds": elapsed,
                "quality_score": quality_score
            }
        )
```

### 2.2 MK-08 国内平台分发

```yaml
# MK-08 国内平台分发验收
function_id: "MK-08"
name: "国内平台分发"
description: "一键发布到微信、抖音、知乎等国内平台"
priority: "P0"

# 验收标准
acceptance_criteria:
  - id: "AC-08-01"
    criterion: "一篇文章可在3个以上平台同时发布"
    test_method: "集成测试"
    test_type: "integration"
    expected_result: "3个平台发布成功"
    
  - id: "AC-08-02"
    criterion: "发布成功率>95%"
    test_method: "批量测试"
    test_type: "reliability"
    expected_result: "成功率≥95%"
    
  - id: "AC-08-03"
    criterion: "支持图文混合发布"
    test_method: "功能测试"
    test_type: "functional"
    expected_result: "图文正常显示"
    
  - id: "AC-08-04"
    criterion: "发布状态实时反馈"
    test_method: "UI测试"
    test_type: "ux"
    expected_result: "状态实时更新"
    
  - id: "AC-08-05"
    criterion: "发布失败自动重试"
    test_method: "故障注入测试"
    test_type: "resilience"
    expected_result: "自动重试最多3次"

# 测试用例
test_cases:
  - id: "TC-08-01"
    name: "多平台发布测试"
    input:
      content: "测试文章内容"
      platforms: ["wechat", "douyin", "zhihu"]
    steps:
      - "调用批量发布API"
      - "指定3个目标平台"
      - "等待发布完成"
    expected:
      success_count: 3
      failure_count: 0
      all_published: true
      
  - id: "TC-08-02"
    name: "失败重试测试"
    input:
      content: "测试文章"
      platforms: ["wechat"]
    steps:
      - "模拟平台API故障"
      - "调用发布API"
      - "观察重试行为"
    expected:
      retry_count: 3
      final_status: "failed"
      error_logged: true

# 实现示例
class DistributionValidator:
    """分发验证器 - 对齐EX-09并行执行、WEB-05社交媒体交互"""
    
    def __init__(self):
        self.distributor = DomesticDistributor()
        self.test_runner = TestRunner()
    
    async def validate_multi_platform(self, content: str, 
                                       platforms: List[str]) -> ValidationResult:
        """验证多平台发布 - 对齐EX-09"""
        start_time = datetime.now()
        
        # 执行批量发布（对齐EX-09）
        results = await self.distributor.batch_publish(content, platforms)
        
        # 统计成功数
        success_count = sum(1 for r in results if r.success)
        
        # 验证成功率
        success_rate = success_count / len(platforms)
        
        return ValidationResult(
            passed=success_rate >= 0.95,
            details={
                "total_platforms": len(platforms),
                "success_count": success_count,
                "success_rate": success_rate,
                "results": results
            }
        )
```

### 2.3 MK-14 项目筛选

```yaml
# MK-14 项目筛选验收
function_id: "MK-14"
name: "项目筛选"
description: "自动筛选匹配技术栈的项目"
priority: "P1"

# 验收标准
acceptance_criteria:
  - id: "AC-14-01"
    criterion: "自动筛选出匹配'Python后端'的项目"
    test_method: "功能测试"
    test_type: "functional"
    expected_result: "筛选出Python相关项目"
    
  - id: "AC-14-02"
    criterion: "匹配准确率>80%"
    test_method: "样本测试"
    test_type: "accuracy"
    expected_result: "准确率≥80%"
    
  - id: "AC-14-03"
    criterion: "支持多技能组合筛选"
    test_method: "功能测试"
    test_type: "functional"
    expected_result: "支持AND/OR逻辑"
    
  - id: "AC-14-04"
    criterion: "筛选响应时间<10秒"
    test_method: "性能测试"
    test_type: "performance"
    expected_result: "响应时间≤10秒"
    
  - id: "AC-14-05"
    criterion: "支持多平台项目源"
    test_method: "集成测试"
    test_type: "integration"
    expected_result: "至少支持3个平台"

# 测试用例
test_cases:
  - id: "TC-14-01"
    name: "技能匹配测试"
    input:
      skills: ["Python", "Django", "PostgreSQL"]
    steps:
      - "调用项目匹配API"
      - "传入技能列表"
      - "获取匹配结果"
    expected:
      matched_count: "≥3"
      top_match_score: "≥80"
      relevance: "技能相关"
      
  - id: "TC-14-02"
    name: "准确率测试"
    input:
      test_samples: 100
      skills: ["Python后端"]
    steps:
      - "对100个样本进行匹配"
      - "人工验证匹配结果"
    expected:
      accuracy: "≥80%"
      precision: "≥75%"
      recall: "≥70%"

# 实现示例
class ProjectMatchValidator:
    """项目匹配验证器 - 对齐CG-01推理能力"""
    
    def __init__(self):
        self.matcher = ProjectMatcher()
        self.accuracy_calculator = AccuracyCalculator()
    
    async def validate_match_accuracy(self, skills: List[str]) -> ValidationResult:
        """验证匹配准确率 - 对齐CG-01"""
        # 获取匹配结果
        matches = await self.matcher.match_projects(skills)
        
        # 人工验证样本
        sample_size = min(50, len(matches))
        sample = matches[:sample_size]
        
        # 计算准确率
        correct_count = 0
        for match in sample:
            is_correct = await self._verify_match(match, skills)
            if is_correct:
                correct_count += 1
        
        accuracy = correct_count / sample_size if sample_size > 0 else 0
        
        return ValidationResult(
            passed=accuracy >= 0.8,
            details={
                "total_matches": len(matches),
                "sample_size": sample_size,
                "correct_count": correct_count,
                "accuracy": accuracy
            }
        )
```

### 2.4 MK-22 数据看板

```yaml
# MK-22 数据看板验收
function_id: "MK-22"
name: "数据看板"
description: "粉丝增长、互动数据、收益统计的综合看板"
priority: "P0"

# 验收标准
acceptance_criteria:
  - id: "AC-22-01"
    criterion: "数据看板展示近7天粉丝增长趋势图"
    test_method: "UI测试"
    test_type: "visual"
    expected_result: "趋势图正确显示"
    
  - id: "AC-22-02"
    criterion: "数据刷新延迟<1分钟"
    test_method: "性能测试"
    test_type: "performance"
    expected_result: "延迟≤60秒"
    
  - id: "AC-22-03"
    criterion: "支持多平台数据切换"
    test_method: "UI测试"
    test_type: "functional"
    expected_result: "切换后数据更新"
    
  - id: "AC-22-04"
    criterion: "数据准确性>99%"
    test_method: "数据核对"
    test_type: "accuracy"
    expected_result: "误差<1%"
    
  - id: "AC-22-05"
    criterion: "支持数据导出"
    test_method: "功能测试"
    test_type: "functional"
    expected_result: "导出CSV/Excel"

# 测试用例
test_cases:
  - id: "TC-22-01"
    name: "趋势图显示测试"
    input:
      date_range: "last_7_days"
      metric: "followers"
    steps:
      - "打开数据看板页面"
      - "选择近7天时间范围"
      - "查看粉丝增长趋势图"
    expected:
      chart_visible: true
      x_axis: "7个日期点"
      y_axis: "粉丝数量"
      trend_line: "正确显示"
      
  - id: "TC-22-02"
    name: "数据准确性测试"
    input:
      platform: "wechat"
      date: "2026-01-10"
    steps:
      - "从数据看板获取数据"
      - "从平台API直接获取数据"
      - "对比两组数据"
    expected:
      error_rate: "<1%"
      consistent: true

# 实现示例
class DashboardValidator:
    """数据看板验证器 - 对齐CG-04数值推理"""
    
    def __init__(self):
        self.dashboard = DashboardEngine()
        self.data_verifier = DataVerifier()
    
    async def validate_accuracy(self, platform: str, date: date) -> ValidationResult:
        """验证数据准确性 - 对齐CG-04"""
        # 从看板获取数据
        dashboard_data = await self.dashboard.get_metrics(platform, date)
        
        # 从平台API直接获取数据
        platform_data = await self._fetch_raw_data(platform, date)
        
        # 计算误差率（对齐CG-04）
        errors = []
        for metric in ["followers", "views", "engagement"]:
            dashboard_value = dashboard_data.get(metric, 0)
            platform_value = platform_data.get(metric, 0)
            
            if platform_value > 0:
                error_rate = abs(dashboard_value - platform_value) / platform_value
            else:
                error_rate = 0 if dashboard_value == 0 else 1
            
            errors.append({
                "metric": metric,
                "dashboard_value": dashboard_value,
                "platform_value": platform_value,
                "error_rate": error_rate
            })
        
        max_error = max(e["error_rate"] for e in errors)
        
        return ValidationResult(
            passed=max_error < 0.01,
            details={
                "platform": platform,
                "date": date,
                "errors": errors,
                "max_error": max_error
            }
        )
```

### 2.5 MK-27 内容工作流

```yaml
# MK-27 内容工作流验收
function_id: "MK-27"
name: "内容工作流"
description: "从创意到分发的自动化流程"
priority: "P0"

# 验收标准
acceptance_criteria:
  - id: "AC-27-01"
    criterion: "从输入主题到发布全流程自动化，耗时<30分钟"
    test_method: "端到端测试"
    test_type: "e2e"
    expected_result: "全流程≤30分钟"
    
  - id: "AC-27-02"
    criterion: "支持人工审核节点"
    test_method: "功能测试"
    test_type: "functional"
    expected_result: "审核流程正常"
    
  - id: "AC-27-03"
    criterion: "支持并行步骤执行"
    test_method: "性能测试"
    test_type: "performance"
    expected_result: "并行步骤同时执行"
    
  - id: "AC-27-04"
    criterion: "失败步骤自动重试"
    test_method: "故障注入测试"
    test_type: "resilience"
    expected_result: "重试次数可配置"
    
  - id: "AC-27-05"
    criterion: "工作流状态可追踪"
    test_method: "UI测试"
    test_type: "ux"
    expected_result: "状态实时更新"

# 测试用例
test_cases:
  - id: "TC-27-01"
    name: "端到端流程测试"
    input:
      topic: "AI发展趋势"
      workflow: "standard_publish"
    steps:
      - "创建工作流实例"
      - "传入主题参数"
      - "启动工作流"
      - "监控执行过程"
      - "记录完成时间"
    expected:
      total_duration: "≤1800秒"
      all_steps_completed: true
      final_content_published: true
      
  - id: "TC-27-02"
    name: "并行执行测试"
    input:
      workflow: "parallel_publish"
      platforms: ["wechat", "douyin", "zhihu"]
    steps:
      - "启动并行发布工作流"
      - "观察执行顺序"
    expected:
      concurrent_execution: true
      all_completed: true
      time_saved: "相比串行≥50%"
      
  - id: "TC-27-03"
    name: "失败重试测试"
    input:
      workflow: "flaky_workflow"
      failure_step: "publish"
    steps:
      - "配置失败重试3次"
      - "模拟步骤失败"
      - "观察重试行为"
    expected:
      retry_count: 3
      final_status: "failed"
      error_logged: true

# 实现示例
class WorkflowValidator:
    """工作流验证器 - 对齐AUTO-03工作流编排、EX-09并行执行"""
    
    def __init__(self):
        self.workflow_engine = WorkflowEngine()
        self.timer = Timer()
    
    async def validate_e2e_workflow(self, topic: str, 
                                     workflow_id: str) -> ValidationResult:
        """验证端到端工作流 - 对齐AUTO-03"""
        start_time = datetime.now()
        
        # 执行工作流
        execution = await self.workflow_engine.execute_workflow(
            workflow_id=workflow_id,
            input_data={"topic": topic}
        )
        
        # 等待完成
        while execution.status not in ["completed", "failed"]:
            await asyncio.sleep(5)
            execution = await self.workflow_engine.get_execution(execution.id)
        
        # 计算耗时
        elapsed = (datetime.now() - start_time).total_seconds()
        
        # 验证结果
        all_completed = all(
            step.status == "completed" 
            for step in execution.step_results
        )
        
        return ValidationResult(
            passed=execution.status == "completed" and elapsed <= 1800,
            details={
                "execution_id": execution.id,
                "status": execution.status,
                "elapsed_seconds": elapsed,
                "steps_completed": len([s for s in execution.step_results if s.status == "completed"]),
                "total_steps": len(execution.step_results),
                "all_completed": all_completed
            }
        )
    
    async def validate_parallel_execution(self, workflow_id: str) -> ValidationResult:
        """验证并行执行 - 对齐EX-09"""
        # 执行工作流
        execution = await self.workflow_engine.execute_workflow(workflow_id)
        
        # 获取并行步骤的时间戳
        parallel_steps = [
            step for step in execution.step_results 
            if step.type == "parallel"
        ]
        
        # 验证并行执行
        is_parallel = True
        for step in parallel_steps:
            if len(step.sub_steps) > 1:
                start_times = [ss.started_at for ss in step.sub_steps]
                if len(set(start_times)) != len(start_times):
                    is_parallel = False
        
        return ValidationResult(
            passed=is_parallel,
            details={
                "parallel_steps_count": len(parallel_steps),
                "is_parallel": is_parallel
            }
        )
```


## 三、验收测试数据准备

```yaml
# 测试数据配置

test_data:
  # 内容生成测试数据
  text_generation:
    topics:
      - "AI营销趋势"
      - "数字化转型"
      - "智能体技术发展"
    expected_lengths:
      short: 500
      medium: 1500
      long: 3000
      
  # 多平台分发测试数据
  distribution:
    platforms:
      domestic: ["wechat", "douyin", "zhihu", "bilibili", "weibo"]
      international: ["facebook", "twitter", "linkedin", "instagram"]
    test_content:
      text: "这是测试文章内容，用于验证多平台发布功能"
      image: "test_image.jpg"
      video: "test_video.mp4"
      
  # 项目匹配测试数据
  project_matching:
    skills:
      - "Python后端"
      - "Java开发"
      - "前端React"
      - "移动端Flutter"
    test_samples: 100
    
  # 数据看板测试数据
  dashboard:
    platforms: ["wechat", "douyin", "zhihu", "weibo"]
    metrics: ["followers", "views", "engagement", "revenue"]
    date_ranges: ["today", "last_7_days", "last_30_days", "this_month"]
    
  # 工作流测试数据
  workflow:
    workflows:
      - id: "standard_publish"
        name: "标准发布流程"
        steps: 4
      - id: "parallel_publish"
        name: "并行发布流程"
        steps: 2
        parallel: true
      - id: "flaky_workflow"
        name: "故障测试流程"
        steps: 3
        retry_count: 3
```


## 四、验收测试环境

```yaml
# 测试环境配置

test_environment:
  development:
    url: "https://dev.jyis.com"
    database: "jyis_test"
    features:
      - "mock_external_apis"
      - "debug_mode"
      - "fast_fail"
      
  staging:
    url: "https://staging.jyis.com"
    database: "jyis_staging"
    features:
      - "real_external_apis"
      - "performance_logging"
      - "error_tracking"
      
  production_smoke:
    url: "https://jyis.com"
    database: "jyis_prod"
    features:
      - "read_only_tests"
      - "no_data_modification"
      - "limited_scope"
```


## 五、验收测试报告模板

```yaml
# 测试报告模板

report_template:
  header:
    title: "功能验收测试报告"
    version: "v1.0"
    date: "YYYY-MM-DD"
    tester: "测试人员"
    
  summary:
    total_functions: 5
    passed: 0
    failed: 0
    blocked: 0
    pass_rate: 0
    
  details:
    - function_id: "MK-01"
      name: "文本内容生成"
      status: "pending"
      acceptance_criteria:
        - id: "AC-01-01"
          result: "pass/fail"
          notes: ""
        - id: "AC-01-02"
          result: "pass/fail"
          notes: ""
      issues: []
      
    - function_id: "MK-08"
      name: "国内平台分发"
      status: "pending"
      acceptance_criteria: []
      issues: []
      
    - function_id: "MK-14"
      name: "项目筛选"
      status: "pending"
      acceptance_criteria: []
      issues: []
      
    - function_id: "MK-22"
      name: "数据看板"
      status: "pending"
      acceptance_criteria: []
      issues: []
      
    - function_id: "MK-27"
      name: "内容工作流"
      status: "pending"
      acceptance_criteria: []
      issues: []
      
  recommendations: []
  signoff:
    tester: ""
    reviewer: ""
    date: ""
```


## 六、在Cursor中使用

```bash
# 1. 运行MK-01验收测试
@docs/ACCEPTANCE_CHECKLIST_v1.0.md 运行MK-01文本内容生成的验收测试

# 2. 运行MK-08集成测试
@docs/ACCEPTANCE_CHECKLIST_v1.0.md 运行MK-08多平台分发的集成测试

# 3. 运行MK-22数据准确性验证
@docs/ACCEPTANCE_CHECKLIST_v1.0.md 运行MK-22数据看板的数据准确性验证

# 4. 运行MK-27端到端测试
@docs/ACCEPTANCE_CHECKLIST_v1.0.md 运行MK-27内容工作流的端到端测试

# 5. 生成验收报告
@docs/ACCEPTANCE_CHECKLIST_v1.0.md 生成功能验收测试报告
```


## 七、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，5项功能验收标准，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md |

---

**文档结束**