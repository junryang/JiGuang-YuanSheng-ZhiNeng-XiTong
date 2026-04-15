# 企业协作工具对接规范 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\ENTERPRISE_INTEGRATION_SPEC_v1.0.md
```


# 企业协作工具对接规范 v1.0


## 一、概述

```yaml
module:
  name: "企业协作工具对接模块"
  description: |
    提供企业协作工具的对接能力，包括飞书、微信、钉钉、企业微信等。
    基于通用能力规范中的消息发送、API调用、认证授权等能力实现。
  domain: "D03"
  priority: "P1"

  related_abilities:
    - "EX-08: 消息发送"
    - "EX-03: API调用"
    - "WEB-04: API调用与集成"
    - "SC-04: 权限检查"
    - "SC-07: 操作审计"
    - "APPROVE-02: 多级审批与流转"
    - "APPROVE-05: 审批通知与待办管理"
```


## 二、架构设计

```yaml
# 企业协作工具对接架构 - 对齐通用能力

architecture:
  pattern: "Adapter Pattern + Webhook"
  description: "统一的协作工具接口，支持飞书、微信、钉钉、企业微信"
  related_ability: "WEB-04"
  
  components:
    - name: "MessageAdapter"
      description: "消息适配器，统一不同平台的消息发送"
      related_ability: "EX-08"
      
    - name: "ApprovalAdapter"
      description: "审批适配器，统一审批流程对接"
      related_ability: "APPROVE-02"
      
    - name: "DocAdapter"
      description: "文档适配器，统一文档同步"
      related_ability: "FILE-01"
      
    - name: "AuthAdapter"
      description: "认证适配器，统一扫码登录"
      related_ability: "SC-04"
      
    - name: "WebhookReceiver"
      description: "Webhook接收器，处理平台回调"
      related_ability: "WEB-04"
      
    - name: "MessageRouter"
      description: "消息路由器，根据规则分发消息"
      related_ability: "DC-05"
```


## 三、统一接口定义

### 3.1 消息接口

```python
# integrations/base.py - 对齐EX-08消息发送

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum

class MessageType(str, Enum):
    TEXT = "text"
    MARKDOWN = "markdown"
    IMAGE = "image"
    FILE = "file"
    CARD = "card"                      # 卡片消息
    INTERACTIVE = "interactive"        # 交互式消息
    TEMPLATE = "template"              # 模板消息

class MessagePriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class MessageRecipient(BaseModel):
    """消息接收者"""
    type: str              # user, group, department
    id: str                # 用户ID/群ID/部门ID

class Message(BaseModel):
    """统一消息格式"""
    title: Optional[str] = None
    content: str
    type: MessageType = MessageType.TEXT
    priority: MessagePriority = MessagePriority.NORMAL
    recipients: List[MessageRecipient]
    sender: Optional[str] = None
    metadata: Optional[Dict] = None
    related_ability: str = "EX-08"

class MessageResult(BaseModel):
    """消息发送结果"""
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
    timestamp: str
    related_ability: str = "EX-08"

class BaseMessageAdapter(ABC):
    """消息适配器基类 - 对齐EX-08"""
    
    def __init__(self):
        self.related_ability = "EX-08"
    
    @abstractmethod
    async def send_message(self, message: Message) -> MessageResult:
        """发送消息"""
        pass
    
    @abstractmethod
    async def send_batch(self, messages: List[Message]) -> List[MessageResult]:
        """批量发送消息"""
        pass
    
    @abstractmethod
    async def get_message_status(self, message_id: str) -> Dict:
        """获取消息状态"""
        pass
```

### 3.2 审批接口

```python
# integrations/approval.py - 对齐APPROVE-02多级审批

class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class ApprovalRequest(BaseModel):
    """统一审批请求"""
    title: str
    content: str
    applicant: str                      # 申请人
    approvers: List[str]                # 审批人列表
    cc: Optional[List[str]] = None      # 抄送人
    form_data: Optional[Dict] = None    # 表单数据
    attachments: Optional[List[str]] = None
    callback_url: Optional[str] = None
    related_ability: str = "APPROVE-02"

class ApprovalResult(BaseModel):
    """审批结果"""
    success: bool
    approval_id: str
    status: ApprovalStatus
    error: Optional[str] = None
    related_ability: str = "APPROVE-02"

class BaseApprovalAdapter(ABC):
    """审批适配器基类 - 对齐APPROVE-02"""
    
    def __init__(self):
        self.related_ability = "APPROVE-02"
    
    @abstractmethod
    async def create_approval(self, request: ApprovalRequest) -> ApprovalResult:
        """创建审批"""
        pass
    
    @abstractmethod
    async def get_approval_status(self, approval_id: str) -> ApprovalStatus:
        """获取审批状态"""
        pass
    
    @abstractmethod
    async def cancel_approval(self, approval_id: str) -> bool:
        """取消审批"""
        pass
```

### 3.3 认证接口

```python
# integrations/auth.py - 对齐SC-04权限检查

class AuthRequest(BaseModel):
    """认证请求"""
    code: str
    redirect_uri: str
    state: Optional[str] = None
    related_ability: str = "SC-04"

class AuthResult(BaseModel):
    """认证结果"""
    success: bool
    user_id: str
    user_name: str
    avatar: Optional[str] = None
    access_token: str
    refresh_token: str
    expires_in: int
    related_ability: str = "SC-04"

class BaseAuthAdapter(ABC):
    """认证适配器基类 - 对齐SC-04"""
    
    def __init__(self):
        self.related_ability = "SC-04"
    
    @abstractmethod
    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        """获取授权URL"""
        pass
    
    @abstractmethod
    async def handle_callback(self, request: AuthRequest) -> AuthResult:
        """处理授权回调"""
        pass
    
    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> AuthResult:
        """刷新令牌"""
        pass
```


## 四、通用能力映射总表

```yaml
# 企业协作工具与通用能力映射

integration_ability_mapping:
  # 飞书对接
  feishu_message:
    related_ability: "EX-08"
    description: "飞书消息发送"
    
  feishu_approval:
    related_ability: "APPROVE-02"
    description: "飞书审批对接"
    
  feishu_document:
    related_ability: "FILE-01"
    description: "飞书文档同步"
    
  feishu_auth:
    related_ability: "SC-04"
    description: "飞书扫码登录"
    
  feishu_webhook:
    related_ability: "WEB-04"
    description: "飞书Webhook接收"
    
  # 微信对接
  wechat_message:
    related_ability: "EX-08"
    description: "微信模板消息发送"
    
  wechat_auth:
    related_ability: "SC-04"
    description: "微信扫码登录"
    
  wechat_webhook:
    related_ability: "WEB-04"
    description: "微信Webhook接收"
    
  # 钉钉对接
  dingtalk_message:
    related_ability: "EX-08"
    description: "钉钉消息发送"
    
  dingtalk_webhook:
    related_ability: "WEB-04"
    description: "钉钉Webhook接收"
    
  # 企业微信对接
  wecom_message:
    related_ability: "EX-08"
    description: "企业微信消息发送"
    
  wecom_auth:
    related_ability: "SC-04"
    description: "企业微信扫码登录"
```


## 五、飞书对接实现

```yaml
# 飞书配置 - 对齐WEB-04 API调用
feishu:
  name: "飞书"
  priority: "P1"
  related_ability: "WEB-04"
  
  # 应用配置
  app_config:
    app_id: "${FEISHU_APP_ID}"
    app_secret: "${FEISHU_APP_SECRET}"
    verification_token: "${FEISHU_VERIFICATION_TOKEN}"
    encrypt_key: "${FEISHU_ENCRYPT_KEY}"
  
  # API端点
  endpoints:
    base_url: "https://open.feishu.cn/open-apis"
    auth: "/auth/v3/tenant_access_token/internal"
    message: "/im/v1/messages"
    approval: "/approval/v4/instances"
    document: "/docx/v1/documents"
  
  # 能力配置
  capabilities:
    - message_send      # EX-08
    - message_receive   # WEB-04
    - approval_create   # APPROVE-02
    - approval_callback # WEB-04
    - document_sync     # FILE-01
    - login_qrcode      # SC-04
```

```python
# integrations/feishu/adapter.py - 对齐EX-08

import aiohttp
from ..base import BaseMessageAdapter, Message, MessageResult

class FeishuAdapter(BaseMessageAdapter):
    """飞书适配器 - 对齐EX-08"""
    
    def __init__(self, app_id: str, app_secret: str):
        super().__init__()
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_access_token = None
        self.token_expires_at = 0
        self.related_ability = "EX-08"
    
    async def _get_access_token(self) -> str:
        """获取租户访问令牌"""
        if self.tenant_access_token and time.time() < self.token_expires_at:
            return self.tenant_access_token
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
                json={
                    "app_id": self.app_id,
                    "app_secret": self.app_secret
                }
            ) as resp:
                data = await resp.json()
                self.tenant_access_token = data["tenant_access_token"]
                self.token_expires_at = time.time() + data["expire"]
                return self.tenant_access_token
    
    async def send_message(self, message: Message) -> MessageResult:
        """发送消息 - 对齐EX-08"""
        token = await self._get_access_token()
        
        feishu_message = self._convert_message(message)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://open.feishu.cn/open-apis/im/v1/messages",
                headers={"Authorization": f"Bearer {token}"},
                json=feishu_message
            ) as resp:
                data = await resp.json()
                if data.get("code") == 0:
                    return MessageResult(
                        success=True,
                        message_id=data["data"]["message_id"],
                        timestamp=datetime.now().isoformat(),
                        related_ability="EX-08"
                    )
                else:
                    return MessageResult(
                        success=False,
                        error=data.get("msg", "Unknown error"),
                        timestamp=datetime.now().isoformat(),
                        related_ability="EX-08"
                    )
    
    def _convert_message(self, message: Message) -> dict:
        """转换消息格式为飞书格式"""
        if message.type == MessageType.TEXT:
            return {
                "receive_id": message.recipients[0].id,
                "msg_type": "text",
                "content": json.dumps({"text": message.content})
            }
        elif message.type == MessageType.CARD:
            return {
                "receive_id": message.recipients[0].id,
                "msg_type": "interactive",
                "content": message.content
            }
        else:
            return {
                "receive_id": message.recipients[0].id,
                "msg_type": "text",
                "content": json.dumps({"text": message.content})
            }
```


## 六、微信对接实现

```yaml
# 微信配置 - 对齐SC-04权限检查
wechat:
  name: "微信"
  priority: "P1"
  related_ability: "SC-04"
  
  # 公众号配置
  official_account:
    app_id: "${WECHAT_APP_ID}"
    app_secret: "${WECHAT_APP_SECRET}"
    token: "${WECHAT_TOKEN}"
    encoding_aes_key: "${WECHAT_ENCODING_AES_KEY}"
  
  # 开放平台配置（扫码登录）
  open_platform:
    app_id: "${WECHAT_OPEN_APP_ID}"
    app_secret: "${WECHAT_OPEN_APP_SECRET}"
  
  # API端点
  endpoints:
    base_url: "https://api.weixin.qq.com"
    token: "/cgi-bin/token"
    message_send: "/cgi-bin/message/template/send"
    qrcode: "/cgi-bin/qrcode/create"
    auth: "/sns/oauth2/access_token"
    user_info: "/sns/userinfo"
  
  # 能力配置
  capabilities:
    - template_message_send  # EX-08
    - qrcode_login           # SC-04
    - user_info_get          # SC-04
```

```python
# integrations/wechat/adapter.py - 对齐SC-04

import hashlib
from ..base import BaseAuthAdapter, AuthRequest, AuthResult

class WechatAuthAdapter(BaseAuthAdapter):
    """微信认证适配器 - 对齐SC-04"""
    
    def __init__(self, app_id: str, app_secret: str):
        super().__init__()
        self.app_id = app_id
        self.app_secret = app_secret
        self.related_ability = "SC-04"
    
    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        """获取微信扫码授权URL"""
        import urllib.parse
        encoded_uri = urllib.parse.quote(redirect_uri)
        return f"https://open.weixin.qq.com/connect/qrconnect?appid={self.app_id}&redirect_uri={encoded_uri}&response_type=code&scope=snsapi_login&state={state}#wechat_redirect"
    
    async def handle_callback(self, request: AuthRequest) -> AuthResult:
        """处理微信授权回调"""
        # 1. 用code换取access_token
        token_url = f"https://api.weixin.qq.com/sns/oauth2/access_token?appid={self.app_id}&secret={self.app_secret}&code={request.code}&grant_type=authorization_code"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(token_url) as resp:
                token_data = await resp.json()
                if "errcode" in token_data:
                    return AuthResult(
                        success=False,
                        user_id="",
                        user_name="",
                        access_token="",
                        refresh_token="",
                        expires_in=0,
                        related_ability="SC-04"
                    )
            
            # 2. 获取用户信息
            user_url = f"https://api.weixin.qq.com/sns/userinfo?access_token={token_data['access_token']}&openid={token_data['openid']}"
            async with session.get(user_url) as resp:
                user_data = await resp.json()
                
                return AuthResult(
                    success=True,
                    user_id=user_data["openid"],
                    user_name=user_data.get("nickname", ""),
                    avatar=user_data.get("headimgurl"),
                    access_token=token_data["access_token"],
                    refresh_token=token_data.get("refresh_token", ""),
                    expires_in=token_data["expires_in"],
                    related_ability="SC-04"
                )
```


## 七、消息路由器实现

```python
# integrations/router.py - 对齐DC-05优先级排序

from typing import Dict, List, Optional
from .base import Message, MessageResult
from .feishu.adapter import FeishuAdapter
from .wechat.adapter import WechatMessageSender

class MessageRouter:
    """消息路由器 - 对齐DC-05"""
    
    def __init__(self):
        self.adapters: Dict[str, any] = {}
        self.rules: List[Dict] = []
        self.related_ability = "DC-05"
    
    def register_adapter(self, name: str, adapter):
        """注册适配器"""
        self.adapters[name] = adapter
    
    def add_rule(self, rule: Dict):
        """添加路由规则"""
        self.rules.append(rule)
    
    async def route(self, message: Message) -> List[MessageResult]:
        """
        路由消息到目标平台 - 根据优先级排序
        """
        results = []
        
        # 根据规则确定目标平台
        targets = self._get_targets(message)
        
        # 按优先级发送到各平台
        for target in targets:
            adapter = self.adapters.get(target)
            if adapter:
                result = await adapter.send_message(message)
                results.append(result)
        
        return results
    
    def _get_targets(self, message: Message) -> List[str]:
        """根据规则获取目标平台"""
        targets = ["feishu"]  # 默认发送到飞书
        
        # 高优先级消息发送到多个平台
        if message.priority == MessagePriority.URGENT:
            targets = ["feishu", "wechat"]
        
        for rule in self.rules:
            condition = rule.get("condition", {})
            matched = True
            
            for key, value in condition.items():
                if getattr(message, key, None) != value:
                    matched = False
                    break
            
            if matched:
                targets = rule.get("targets", targets)
                break
        
        return targets
```


## 八、配置管理

```yaml
# config/integrations.yaml - 对齐通用能力配置

integrations:
  # 飞书 - EX-08消息发送
  feishu:
    enabled: true
    related_ability: "EX-08"
    app_id: "${FEISHU_APP_ID}"
    app_secret: "${FEISHU_APP_SECRET}"
    webhook_enabled: true
    
  # 微信 - SC-04权限检查
  wechat:
    enabled: true
    related_ability: "SC-04"
    official_account:
      app_id: "${WECHAT_APP_ID}"
      app_secret: "${WECHAT_APP_SECRET}"
    open_platform:
      app_id: "${WECHAT_OPEN_APP_ID}"
      app_secret: "${WECHAT_OPEN_APP_SECRET}"
    
  # 钉钉 - 后续启用
  dingtalk:
    enabled: false
    related_ability: "EX-08"
    app_key: "${DINGTALK_APP_KEY}"
    app_secret: "${DINGTALK_APP_SECRET}"
    
  # 企业微信 - 后续启用
  wecom:
    enabled: false
    related_ability: "EX-08"
    corp_id: "${WECOM_CORP_ID}"
    agent_id: "${WECOM_AGENT_ID}"
    secret: "${WECOM_SECRET}"

# 消息路由规则 - 对齐DC-05优先级排序
routing_rules:
  - condition:
      priority: "urgent"
    targets: ["feishu", "wechat"]
    related_ability: "DC-05"
    
  - condition:
      type: "approval"
    targets: ["feishu"]
    related_ability: "APPROVE-02"
    
  - condition:
      type: "notification"
    targets: ["feishu"]
    related_ability: "EX-08"
```


## 九、在Cursor中使用

```bash
# 1. 配置飞书（对齐EX-08）
@docs/ENTERPRISE_INTEGRATION_SPEC_v1.0.md 配置飞书应用，基于EX-08消息发送能力

# 2. 实现消息路由器（对齐DC-05）
@docs/ENTERPRISE_INTEGRATION_SPEC_v1.0.md 实现MessageRouter，基于DC-05优先级排序

# 3. 配置微信扫码登录（对齐SC-04）
@docs/ENTERPRISE_INTEGRATION_SPEC_v1.0.md 配置微信开放平台扫码登录，基于SC-04权限检查

# 4. 集成审批对接（对齐APPROVE-02）
@docs/ENTERPRISE_INTEGRATION_SPEC_v1.0.md 集成飞书审批，基于APPROVE-02多级审批能力

# 5. 发送测试消息
@docs/ENTERPRISE_INTEGRATION_SPEC_v1.0.md 使用飞书适配器发送一条测试消息
```


## 十、API接口定义

```python
# API端点 - 标注关联通用能力

# 发送消息 - EX-08
POST /api/v1/integrations/message/send
Request: Message
Response: MessageResult
RelatedAbility: "EX-08"

# 批量发送 - EX-08
POST /api/v1/integrations/message/batch
Request: List[Message]
Response: List[MessageResult]
RelatedAbility: "EX-08"

# 创建审批 - APPROVE-02
POST /api/v1/integrations/approval/create
Request: ApprovalRequest
Response: ApprovalResult
RelatedAbility: "APPROVE-02"

# 获取审批状态 - APPROVE-02
GET /api/v1/integrations/approval/{approval_id}
Response: ApprovalStatus
RelatedAbility: "APPROVE-02"

# 获取登录二维码 - SC-04
GET /api/v1/integrations/auth/qrcode
Response: {"url": "https://...", "expires_in": 300}
RelatedAbility: "SC-04"

# 处理登录回调 - SC-04
POST /api/v1/integrations/auth/callback
Request: AuthRequest
Response: AuthResult
RelatedAbility: "SC-04"
```


## 十一、版本更新记录

| 版本 | 日期 | 修改内容 |
|------|------|---------|
| v1.0 | 2026-01-11 | 初始版本，对齐AGENT_ABILITY_SPEC_v1.0.md通用能力 |

---

**文档结束**