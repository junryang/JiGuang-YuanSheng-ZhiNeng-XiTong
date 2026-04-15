# 技能库结构规范 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\SKILL_LIBRARY_STRUCTURE_v1.0.md
```


# 技能库结构规范 v1.0

## 一、技能库目录结构

```yaml
# 完整技能库目录结构

skills/
├── common/                      # 通用技能（所有智能体共享）
│   ├── __init__.py
│   ├── communication/           # 通信类技能
│   │   ├── natural_language.py
│   │   ├── message_send.py
│   │   └── intent_recognition.py
│   ├── cognition/               # 认知类技能
│   │   ├── reasoning.py
│   │   ├── planning.py
│   │   └── decision_making.py
│   └── execution/               # 执行类技能
│       ├── task_execute.py
│       ├── result_report.py
│       └── error_handle.py
│
├── backend/                     # 后端部技能
│   ├── __init__.py
│   ├── api/                     # API开发
│   │   ├── restful_api.py
│   │   ├── graphql_api.py
│   │   └── api_document.py
│   ├── database/                # 数据库
│   │   ├── sql_optimize.py
│   │   ├── db_design.py
│   │   └── migration.py
│   ├── performance/             # 性能优化
│   │   ├── cache_strategy.py
│   │   ├── query_optimize.py
│   │   └── async_processing.py
│   └── security/                # 安全
│       ├── auth_security.py
│       ├── data_encrypt.py
│       └── vulnerability_scan.py
│
├── frontend/                    # 前端部技能
│   ├── __init__.py
│   ├── component/               # 组件开发
│   │   ├── vue_component.py
│   │   ├── react_component.py
│   │   └── web_component.py
│   ├── state/                   # 状态管理
│   │   ├── pinia_state.py
│   │   ├── redux_state.py
│   │   └── vuex_state.py
│   ├── style/                   # 样式
│   │   ├── responsive_design.py
│   │   ├── css_animation.py
│   │   └── theme_config.py
│   └── performance/             # 性能优化
│       ├── bundle_optimize.py
│       ├── lazy_load.py
│       └── seo_optimize.py
│
├── agent/                       # 智能体部技能
│   ├── __init__.py
│   ├── creation/                # 智能体创建
│   │   ├── agent_generate.py
│   │   ├── agent_config.py
│   │   └── agent_template.py
│   ├── orchestration/           # 智能体编排
│   │   ├── multi_agent_coord.py
│   │   ├── task_distribute.py
│   │   └── workflow_design.py
│   ├── memory/                  # 记忆系统
│   │   ├── memory_store.py
│   │   ├── memory_retrieve.py
│   │   └── memory_consolidate.py
│   └── skill/                   # 技能管理
│       ├── skill_register.py
│       ├── skill_execute.py
│       └── skill_learn.py
│
├── testing/                     # 测试部技能
│   ├── __init__.py
│   ├── unit/                    # 单元测试
│   │   ├── unit_test_gen.py
│   │   ├── test_coverage.py
│   │   └── mock_service.py
│   ├── integration/             # 集成测试
│   │   ├── api_test.py
│   │   ├── e2e_test.py
│   │   └── load_test.py
│   ├── quality/                 # 质量保障
│   │   ├── code_review.py
│   │   ├── bug_detect.py
│   │   └── quality_report.py
│   └── automation/              # 自动化
│       ├── ci_pipeline.py
│       ├── auto_deploy.py
│       └── regression_test.py
│
├── marketing/                   # 营销部技能
│   ├── __init__.py
│   ├── content/                 # 内容生成
│   │   ├── article_gen.py
│   │   ├── social_post.py
│   │   └── seo_content.py
│   ├── publish/                 # 内容发布
│   │   ├── multi_platform.py
│   │   ├── schedule_publish.py
│   │   └── content_audit.py
│   ├── analytics/               # 数据分析
│   │   ├── follower_analytics.py
│   │   ├── engagement_analytics.py
│   │   └── conversion_tracking.py
│   └── strategy/                # 营销策略
│       ├── market_research.py
│       ├── competitor_analysis.py
│       └── campaign_plan.py
│
├── data/                        # 数据部技能（新增）
│   ├── __init__.py
│   ├── etl/                     # 数据管道
│   │   ├── data_extract.py
│   │   ├── data_transform.py
│   │   └── data_load.py
│   ├── warehouse/               # 数据仓库
│   │   ├── dw_design.py
│   │   ├── data_modeling.py
│   │   └── data_quality.py
│   └── bi/                      # 商业智能
│       ├── dashboard_gen.py
│       ├── report_gen.py
│       └── data_visualize.py
│
├── mobile/                      # 移动端技能（新增）
│   ├── __init__.py
│   ├── ios/                     # iOS开发
│   │   ├── swift_dev.py
│   │   ├── swiftui_dev.py
│   │   └── appstore_deploy.py
│   ├── android/                 # Android开发
│   │   ├── kotlin_dev.py
│   │   ├── jetpack_dev.py
│   │   └── play_deploy.py
│   └── cross/                   # 跨平台
│       ├── react_native.py
│       ├── flutter_dev.py
│       └── uni_app.py
│
├── ai_model/                    # AI模型技能（新增）
│   ├── __init__.py
│   ├── training/                # 模型训练
│   │   ├── model_train.py
│   │   ├── model_finetune.py
│   │   └── model_distill.py
│   ├── inference/               # 模型推理
│   │   ├── model_deploy.py
│   │   ├── model_optimize.py
│   │   └── model_cache.py
│   └── data/                    # 数据处理
│       ├── data_augment.py
│       ├── data_label.py
│       └── data_clean.py
│
├── devops/                      # 运维技能（新增）
│   ├── __init__.py
│   ├── deploy/                  # 部署
│   │   ├── k8s_deploy.py
│   │   ├── docker_deploy.py
│   │   └── cloud_deploy.py
│   ├── monitor/                 # 监控
│   │   ├── prometheus_setup.py
│   │   ├── grafana_dashboard.py
│   │   └── alert_config.py
│   └── logging/                 # 日志
│       ├── log_analyze.py
│       ├── elk_stack.py
│       └── log_alert.py
│
├── product/                     # 产品部技能（新增）
│   ├── __init__.py
│   ├── requirement/             # 需求分析
│   │   ├── prd_gen.py
│   │   ├── user_story.py
│   │   └── requirement_analysis.py
│   ├── design/                  # 产品设计
│   │   ├── prototype_design.py
│   │   ├── ux_design.py
│   │   └── user_research.py
│   └── project/                 # 项目管理
│       ├── project_plan.py
│       ├── milestone_track.py
│       └── risk_manage.py
│
├── security/                    # 安全部技能（新增）
│   ├── __init__.py
│   ├── scan/                    # 安全扫描
│   │   ├── vuln_scan.py
│   │   ├── code_audit.py
│   │   └── dependency_check.py
│   ├── compliance/              # 合规
│   │   ├── gdpr_check.py
│   │   ├── soc2_compliance.py
│   │   └── security_policy.py
│   └── incident/                # 应急响应
│       ├── incident_response.py
│       ├── forensics.py
│       └── recovery_plan.py
│
├── hardware/                    # 硬件部技能（新增，D04具身智能）
│   ├── __init__.py
│   ├── robot/                   # 机器人
│   │   ├── ros_control.py
│   │   ├── motion_plan.py
│   │   └── slam_navigation.py
│   ├── sensor/                  # 传感器
│   │   ├── sensor_fusion.py
│   │   ├── data_acquisition.py
│   │   └── signal_processing.py
│   └── embedded/                # 嵌入式
│       ├── firmware_dev.py
│       ├── rtos_program.py
│       └── iot_comm.py
│
├── runtime_integrations/        # 运行时工具与适配器（与智能体「可调用工具」对齐；非部门编码技能）
│   ├── __init__.py
│   ├── mcp/                     # MCP / OpenAPI / 自定义适配器注册、探活与版本协商
│   ├── browser/                 # 浏览器自动化（会话隔离、可选沙箱）
│   ├── scm/                     # 代码库与变更（git / worktree / CI 触发）
│   ├── observability/           # 追踪、日志、指标、告警与特性开关
│   └── governance/              # 审批闸、配额、血缘登记与高风险留痕
│
├── index.json                   # 技能索引文件
└── README.md                    # 技能库说明文档
```


## 二、技能索引文件

```json
// skills/index.json

{
  "version": "1.0.0",
  "last_updated": "2026-01-20T10:00:00Z",
  "categories": {
    "common": {
      "name": "通用技能",
      "description": "所有智能体共享的基础能力",
      "count": 0,
      "skills": []
    },
    "backend": {
      "name": "后端部技能",
      "description": "后端开发相关技能",
      "count": 0,
      "skills": []
    },
    "frontend": {
      "name": "前端部技能",
      "description": "前端开发相关技能",
      "count": 0,
      "skills": []
    },
    "agent": {
      "name": "智能体部技能",
      "description": "智能体系统开发技能",
      "count": 0,
      "skills": []
    },
    "testing": {
      "name": "测试部技能",
      "description": "测试和质量保障技能",
      "count": 0,
      "skills": []
    },
    "marketing": {
      "name": "营销部技能",
      "description": "内容营销和数据分析技能",
      "count": 0,
      "skills": []
    },
    "data": {
      "name": "数据部技能",
      "description": "数据处理和BI技能",
      "count": 0,
      "skills": []
    },
    "mobile": {
      "name": "移动端技能",
      "description": "iOS/Android开发技能",
      "count": 0,
      "skills": []
    },
    "ai_model": {
      "name": "AI模型技能",
      "description": "模型训练和推理技能",
      "count": 0,
      "skills": []
    },
    "devops": {
      "name": "运维技能",
      "description": "部署和监控技能",
      "count": 0,
      "skills": []
    },
    "product": {
      "name": "产品部技能",
      "description": "需求分析和项目管理技能",
      "count": 0,
      "skills": []
    },
    "security": {
      "name": "安全部技能",
      "description": "安全扫描和合规技能",
      "count": 0,
      "skills": []
    },
    "hardware": {
      "name": "硬件部技能",
      "description": "机器人和嵌入式技能",
      "count": 0,
      "skills": []
    },
    "runtime_integrations": {
      "name": "运行时工具与集成",
      "description": "MCP/浏览器/SCM/可观测性/治理等执行期适配与安全边界",
      "count": 0,
      "skills": []
    }
  }
}
```


## 三、技能加载器

```python
# skills/loader.py

import json
from pathlib import Path
from typing import Dict, List, Optional
from .models import SkillDefinition
from .registry import SkillRegistry


class SkillLoader:
    """技能加载器 - 从文件系统加载技能"""
    
    def __init__(self, skills_root: str = "./skills"):
        self.skills_root = Path(skills_root)
        self.registry = SkillRegistry()
    
    def load_all(self) -> SkillRegistry:
        """加载所有技能"""
        # 遍历所有子目录
        for category_dir in self.skills_root.iterdir():
            if not category_dir.is_dir():
                continue
            if category_dir.name.startswith('_') or category_dir.name.startswith('.'):
                continue
            
            self._load_category(category_dir)
        
        # 更新索引
        self._update_index()
        
        return self.registry
    
    def _load_category(self, category_dir: Path):
        """加载分类目录下的所有技能"""
        for skill_file in category_dir.rglob("*.py"):
            if skill_file.name == "__init__.py":
                continue
            
            # 从文件路径提取技能ID
            skill_id = self._extract_skill_id(skill_file, category_dir)
            
            # 加载技能定义
            skill = self._load_skill_from_file(skill_file, skill_id, category_dir.name)
            if skill:
                self.registry.register(skill)
    
    def _extract_skill_id(self, skill_file: Path, category_dir: Path) -> str:
        """从文件路径提取技能ID"""
        relative_path = skill_file.relative_to(category_dir)
        # 例如: api/restful_api.py -> BE-01
        # 实际实现需要根据命名规则生成
        return f"{category_dir.name.upper()[:2]}-{skill_file.stem[:2].upper()}"
    
    def _load_skill_from_file(self, skill_file: Path, skill_id: str, 
                              category: str) -> Optional[SkillDefinition]:
        """从文件加载技能定义"""
        # 实际实现需要解析Python文件中的技能定义
        # 这里返回示例
        return SkillDefinition(
            id=skill_id,
            name=skill_file.stem.replace('_', ' ').title(),
            level="资深",
            description=f"{category}技能：{skill_file.stem}",
            tags=[category],
            input_schema={"type": "object", "properties": {}},
            output_schema={"type": "object", "properties": {}}
        )
    
    def _update_index(self):
        """更新技能索引文件"""
        index_path = self.skills_root / "index.json"
        
        # 加载现有索引
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
        else:
            index = self._create_empty_index()
        
        # 更新各分类技能数量
        for category, skills in self.registry.get_by_category().items():
            if category in index.get("categories", {}):
                index["categories"][category]["count"] = len(skills)
                index["categories"][category]["skills"] = [s.id for s in skills]
        
        index["last_updated"] = datetime.now().isoformat()
        
        # 保存索引
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    
    def _create_empty_index(self) -> dict:
        """创建空索引"""
        return {
            "version": "1.0.0",
            "last_updated": "",
            "categories": {
                "common": {"name": "通用技能", "description": "所有智能体共享的基础能力", "count": 0, "skills": []},
                "backend": {"name": "后端部技能", "description": "后端开发相关技能", "count": 0, "skills": []},
                "frontend": {"name": "前端部技能", "description": "前端开发相关技能", "count": 0, "skills": []},
                "agent": {"name": "智能体部技能", "description": "智能体系统开发技能", "count": 0, "skills": []},
                "testing": {"name": "测试部技能", "description": "测试和质量保障技能", "count": 0, "skills": []},
                "marketing": {"name": "营销部技能", "description": "内容营销和数据分析技能", "count": 0, "skills": []},
                "data": {"name": "数据部技能", "description": "数据处理和BI技能", "count": 0, "skills": []},
                "mobile": {"name": "移动端技能", "description": "iOS/Android开发技能", "count": 0, "skills": []},
                "ai_model": {"name": "AI模型技能", "description": "模型训练和推理技能", "count": 0, "skills": []},
                "devops": {"name": "运维技能", "description": "部署和监控技能", "count": 0, "skills": []},
                "product": {"name": "产品部技能", "description": "需求分析和项目管理技能", "count": 0, "skills": []},
                "security": {"name": "安全部技能", "description": "安全扫描和合规技能", "count": 0, "skills": []},
                "hardware": {"name": "硬件部技能", "description": "机器人和嵌入式技能", "count": 0, "skills": []}
            }
        }
```


## 四、技能文件模板

```python
# skills/backend/api/restful_api.py

"""
技能：RESTful API开发
技能ID：BE-01
分类：backend
等级：资深
"""

from typing import Dict, Any, List
from pydantic import BaseModel


class SkillMetadata:
    """技能元数据"""
    id = "BE-01"
    name = "RESTful API开发"
    name_en = "RESTful API Development"
    version = "1.0.0"
    level = "资深"
    description = "开发RESTful API，包括路由设计、请求验证、响应格式化"
    tags = ["后端", "API", "RESTful"]
    
    # 输入Schema
    input_schema = {
        "type": "object",
        "properties": {
            "endpoints": {
                "type": "array",
                "description": "端点列表",
                "items": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE"]},
                        "description": {"type": "string"}
                    }
                }
            },
            "request_schema": {"type": "object"},
            "response_schema": {"type": "object"}
        },
        "required": ["endpoints"]
    }
    
    # 输出Schema
    output_schema = {
        "type": "object",
        "properties": {
            "code": {"type": "integer"},
            "message": {"type": "string"},
            "data": {"type": "object"}
        }
    }


class SkillExecutor:
    """技能执行器"""
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行技能"""
        endpoints = input_data.get("endpoints", [])
        
        # 生成API代码
        code = self._generate_api_code(endpoints, input_data)
        
        return {
            "code": 200,
            "message": "success",
            "data": {
                "code": code,
                "endpoints": endpoints
            }
        }
    
    def _generate_api_code(self, endpoints: List[Dict], input_data: Dict) -> str:
        """生成API代码"""
        # 实际实现
        return "# API code generated"
```


## 五、在Cursor中使用

将本文档保存后，在Cursor中使用以下命令：

```
# 创建技能库目录结构
@docs/SKILL_LIBRARY_STRUCTURE_v1.0.md 在项目根目录创建skills文件夹及所有子目录

# 加载所有技能
@docs/SKILL_LIBRARY_STRUCTURE_v1.0.md 实现SkillLoader，从skills目录加载所有技能定义

# 创建新技能文件
@docs/SKILL_LIBRARY_STRUCTURE_v1.0.md 按照技能文件模板，在backend/api目录下创建graphql_api.py技能

# 更新技能索引
@docs/SKILL_LIBRARY_STRUCTURE_v1.0.md 实现技能索引的自动更新机制
```

---

**文档结束**