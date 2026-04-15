# 安全需求规范 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\SECURITY_REQUIREMENTS_v1.0.md
```


# 安全需求规范 v1.0

## 一、概述

```yaml
module: "安全需求"
description: "定义系统的安全要求和防护措施"
priority: "P0"
domain: "非功能需求"

# 关联的通用能力
related_abilities:
  - "SC-01: 代码沙箱"
  - "SC-02: 命令沙箱"
  - "SC-03: 敏感信息检测"
  - "SC-04: 权限检查"
  - "SC-05: 操作审计粒度"
  - "SC-06: 速率限制"
  - "SC-07: 操作审计"
  - "SC-08: 输出过滤"
  - "SC-09: 速率限制"
  - "SC-10: 资源限制"
  - "SC-11: 时间限制"
  - "SC-13: 内容审核"
  - "SC-14: 隐私保护"
  - "SC-16: 数据脱敏"
  - "SC-19: 数据加密"
  - "SC-20: 访问令牌管理"
  - "LAW-01: 内容合规审核"
  - "LAW-02: 数据隐私保护"
  - "LAW-04: 访问合法性检查"

security_requirements:
  total_count: 3
  categories:
    - "密码安全"
    - "API安全"
    - "配置安全"
```


## 二、安全需求详细设计

### 2.1 密码加密存储

```yaml
# 密码加密存储要求
requirement_id: "SEC-01"
name: "密码加密存储"
description: "用户密码必须使用bcrypt算法加密存储，禁止明文存储"
priority: "P0"
related_abilities: ["SC-03", "SC-19"]

# 加密配置
encryption_config:
  algorithm: "bcrypt"
  version: "2b"
  work_factor: 12
  salt_rounds: 10
  encoding: "utf-8"

# 密码强度要求
password_strength:
  min_length: 8
  max_length: 64
  require_uppercase: true
  require_lowercase: true
  require_digits: true
  require_special: true
  special_chars: "!@#$%^&*()_+-=[]{}|;:,.<>?"
  common_password_blocklist: true

# 实现示例
class PasswordManager:
    """密码管理器 - 对齐SC-03敏感信息检测、SC-19数据加密"""
    
    def __init__(self):
        self.bcrypt = bcrypt
        self.password_validator = PasswordValidator()
    
    async def hash_password(self, plain_password: str) -> str:
        """加密密码 - 使用bcrypt"""
        # 验证密码强度
        is_valid, message = await self.password_validator.validate(plain_password)
        if not is_valid:
            raise ValueError(f"密码不符合要求: {message}")
        
        # 生成盐值并加密
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        
        return hashed.decode('utf-8')
    
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False
    
    async def check_common_password(self, password: str) -> bool:
        """检查是否为常见弱密码"""
        common_passwords = await self._load_common_passwords()
        return password.lower() in common_passwords

# 数据模型
class UserPassword:
    user_id: str
    password_hash: str
    created_at: datetime
    updated_at: datetime
    last_changed_at: datetime
    password_history: List[str]  # 历史密码哈希，防重用
```

### 2.2 API认证授权

```yaml
# API认证授权要求
requirement_id: "SEC-02"
name: "API认证授权"
description: "所有API必须进行认证和授权检查"
priority: "P0"
related_abilities: ["SC-04", "SC-20", "LAW-04"]

# JWT配置
jwt_config:
  algorithm: "RS256"
  issuer: "jyis-system"
  audience: "jyis-api"
  access_token_expiry: 3600  # 1小时
  refresh_token_expiry: 604800  # 7天
  secret_key_env: "JWT_PRIVATE_KEY"

# 认证方式
auth_methods:
  - type: "jwt"
    name: "JWT Bearer Token"
    header: "Authorization"
    scheme: "Bearer"
    priority: "primary"
    
  - type: "apikey"
    name: "API Key"
    header: "X-API-Key"
    priority: "secondary"
    rate_limit: "更低"
    
  - type: "oauth2"
    name: "OAuth 2.0"
    providers: ["google", "github", "feishu", "wechat"]
    priority: "social"

# RBAC权限配置
rbac_config:
  roles:
    - name: "boss"
      permissions: ["*"]
      level: 0
      
    - name: "ceo"
      permissions: ["approve.*", "project.*", "agent.*", "resource.*"]
      level: 1
      
    - name: "gm"
      permissions: ["project.*", "agent.list", "resource.request"]
      level: 2
      
    - name: "manager"
      permissions: ["task.*", "project.view", "team.manage"]
      level: 3
      
    - name: "lead"
      permissions: ["task.assign", "code.review", "team.view"]
      level: 4
      
    - name: "employee"
      permissions: ["task.execute", "code.write", "doc.write"]
      level: 5
      
    - name: "intern"
      permissions: ["task.view", "code.read", "doc.read"]
      level: 6

# 实现示例
class AuthenticationManager:
    """认证管理器 - 对齐SC-04权限检查、SC-20访问令牌管理"""
    
    def __init__(self):
        self.jwt_handler = JWTHandler()
        self.api_key_manager = APIKeyManager()  # 对齐SC-20
        self.permission_checker = PermissionChecker()  # 对齐SC-04
    
    async def authenticate(self, token: str, auth_type: str = "jwt") -> Optional[User]:
        """认证用户"""
        if auth_type == "jwt":
            payload = await self.jwt_handler.verify(token)
            if payload:
                return await self._get_user_from_payload(payload)
        
        elif auth_type == "apikey":
            api_key = await self.api_key_manager.validate(token)
            if api_key:
                return await self._get_user_by_api_key(api_key)
        
        return None
    
    async def authorize(self, user: User, action: str, resource: str) -> bool:
        """授权检查 - 对齐SC-04权限检查"""
        return await self.permission_checker.check(user, action, resource)
    
    async def refresh_token(self, refresh_token: str) -> dict:
        """刷新访问令牌"""
        return await self.jwt_handler.refresh(refresh_token)

# API安全中间件
class SecurityMiddleware:
    """安全中间件"""
    
    async def authenticate_request(self, request: Request, call_next):
        """请求认证中间件"""
        # 白名单路径跳过认证
        if request.url.path in WHITELIST_PATHS:
            return await call_next(request)
        
        # 提取Token
        token = self._extract_token(request)
        if not token:
            return JSONResponse(
                status_code=401,
                content={"code": 401, "message": "Missing authentication token"}
            )
        
        # 验证Token
        user = await auth_manager.authenticate(token)
        if not user:
            return JSONResponse(
                status_code=401,
                content={"code": 401, "message": "Invalid or expired token"}
            )
        
        # 注入用户信息
        request.state.user = user
        
        return await call_next(request)
    
    async def authorize_request(self, request: Request, call_next):
        """请求授权中间件 - 对齐SC-04"""
        if not hasattr(request.state, 'user'):
            return await call_next(request)
        
        user = request.state.user
        action = self._extract_action(request)
        resource = self._extract_resource(request)
        
        if not await auth_manager.authorize(user, action, resource):
            return JSONResponse(
                status_code=403,
                content={"code": 403, "message": "Insufficient permissions"}
            )
        
        return await call_next(request)
```

### 2.3 敏感配置安全

```yaml
# 敏感配置安全要求
requirement_id: "SEC-03"
name: "敏感配置安全"
description: "数据库密码、API密钥等敏感配置不能硬编码，必须使用环境变量或密钥管理服务"
priority: "P0"
related_abilities: ["SC-03", "SC-19", "LAW-02"]

# 敏感配置分类
sensitive_configs:
  - category: "数据库"
    items:
      - "DB_PASSWORD"
      - "DB_USER"
      - "DB_HOST"
      
  - category: "API密钥"
    items:
      - "DEEPSEEK_API_KEY"
      - "OPENAI_API_KEY"
      - "GITHUB_TOKEN"
      - "WEBSITE_API_KEY"
      
  - category: "认证密钥"
    items:
      - "JWT_PRIVATE_KEY"
      - "JWT_PUBLIC_KEY"
      - "ENCRYPTION_KEY"
      
  - category: "第三方服务"
    items:
      - "REDIS_PASSWORD"
      - "RABBITMQ_PASSWORD"
      - "S3_SECRET_KEY"

# 配置加载方式
config_loading:
  development:
    method: ".env文件"
    location: ".env.local"
    git_ignore: true
    
  test:
    method: ".env.test"
    location: ".env.test"
    git_ignore: true
    
  production:
    method: "环境变量"
    source: "K8s Secrets"
    rotation: "每90天"

# 实现示例
class ConfigManager:
    """配置管理器 - 对齐SC-03敏感信息检测、SC-19数据加密"""
    
    def __init__(self):
        self.secrets = {}
        self.encryption = EncryptionService()  # 对齐SC-19
    
    async def load_config(self):
        """加载配置 - 从环境变量或密钥管理服务"""
        # 从环境变量加载
        for key in self._get_required_keys():
            value = os.environ.get(key)
            if not value:
                raise ValueError(f"Missing required config: {key}")
            
            # 敏感配置加密存储（对齐SC-19）
            if key in SENSITIVE_KEYS:
                value = await self.encryption.encrypt(value)
            
            self.secrets[key] = value
        
        # 从K8s Secrets加载（生产环境）
        if os.environ.get("KUBERNETES_SERVICE_HOST"):
            await self._load_from_k8s_secrets()
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        value = self.secrets.get(key, default)
        
        # 敏感配置自动脱敏（对齐SC-03）
        if key in SENSITIVE_KEYS and value and value != default:
            return self._mask_value(value)
        
        return value
    
    def _mask_value(self, value: str) -> str:
        """脱敏显示"""
        if len(value) <= 8:
            return "***"
        return value[:4] + "***" + value[-4:]

# 环境变量模板
env_template: |
  # .env.example - 配置模板
  # 复制为 .env 并填写实际值
  
  # 数据库配置
  DB_HOST=localhost
  DB_PORT=5432
  DB_USER=jyis
  DB_PASSWORD=change_me
  
  # API密钥
  DEEPSEEK_API_KEY=sk-xxx
  OPENAI_API_KEY=sk-xxx
  
  # JWT配置
  JWT_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----
  # 请填写您的私钥
  -----END PRIVATE KEY-----
  
  # 加密密钥
  ENCRYPTION_KEY=change_me_32_bytes_key
```


## 三、安全增强建议

```yaml
# 额外安全建议
security_enhancements:
  # 1. API限流 - 对齐SC-06速率限制
  rate_limiting:
    enabled: true
    default: "100/分钟"
    authenticated: "1000/分钟"
    admin: "5000/分钟"
    
  # 2. 请求超时 - 对齐SC-11时间限制
  request_timeout:
    default: 30
    long_running: 300
    
  # 3. 请求大小限制
  request_size_limit:
    default: "10MB"
    upload: "100MB"
    
  # 4. CORS配置
  cors_config:
    allowed_origins:
      - "https://jyis.com"
      - "https://*.jyis.com"
    allowed_methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allowed_headers: ["*"]
    allow_credentials: true
    max_age: 3600
    
  # 5. 安全头
  security_headers:
    - name: "X-Content-Type-Options"
      value: "nosniff"
    - name: "X-Frame-Options"
      value: "DENY"
    - name: "X-XSS-Protection"
      value: "1; mode=block"
    - name: "Strict-Transport-Security"
      value: "max-age=31536000; includeSubDomains"
    - name: "Content-Security-Policy"
      value: "default-src 'self'"
      
  # 6. 会话管理
  session_management:
    cookie_secure: true
    cookie_httponly: true
    cookie_samesite: "lax"
    
  # 7. 数据加密传输 - 对齐SC-19
  tls_config:
    min_version: "TLSv1.2"
    ciphers: ["ECDHE-RSA-AES128-GCM-SHA256", "ECDHE-RSA-AES256-GCM-SHA384"]
    
  # 8. 审计日志 - 对齐SC-05操作审计粒度
  audit_logging:
    enabled: true
    include:
      - "login_attempts"
      - "password_changes"
      - "permission_changes"
      - "sensitive_data_access"
      - "configuration_changes"
    retention_days: 90
```


## 四、安全测试用例

```yaml
# 安全测试用例
security_test_cases:
  - id: "ST-01"
    name: "SQL注入测试"
    description: "验证API对SQL注入攻击的防护"
    test_data:
      - "' OR '1'='1"
      - "'; DROP TABLE users; --"
      - "1' AND '1'='1"
    expected: "请求被拒绝或参数被转义"
    
  - id: "ST-02"
    name: "XSS攻击测试"
    description: "验证API对XSS攻击的防护"
    test_data:
      - "<script>alert('XSS')</script>"
      - "<img src=x onerror=alert(1)>"
      - "javascript:alert('XSS')"
    expected: "脚本被转义或过滤"
    
  - id: "ST-03"
    name: "越权访问测试"
    description: "验证用户无法访问未授权的资源"
    test_steps:
      - "使用普通用户Token访问管理员API"
      - "尝试访问其他用户的数据"
    expected: "返回403 Forbidden"
    
  - id: "ST-04"
    name: "密码强度测试"
    description: "验证密码强度要求"
    test_data:
      - "12345678"
      - "password"
      - "Aa1!"
    expected: "弱密码被拒绝"
    
  - id: "ST-05"
    name: "Token过期测试"
    description: "验证过期Token无法使用"
    test_steps:
      - "获取Token"
      - "等待Token过期"
      - "使用过期Token访问API"
    expected: "返回401 Unauthorized"
    
  - id: "ST-06"
    name: "暴力破解防护测试"
    description: "验证登录接口有暴力破解防护"
    test_steps:
      - "连续5次错误登录"
    expected: "触发验证码或账号锁定"
```


## 五、通用能力映射表

```yaml
# 安全需求与通用能力映射
general_ability_mapping:
  SC-03_敏感信息检测:
    mapped_requirements: ["SEC-01", "SEC-03"]
    description: "检测和处理敏感信息"
    
  SC-04_权限检查:
    mapped_requirements: ["SEC-02"]
    description: "API授权检查"
    
  SC-05_操作审计粒度:
    mapped_requirements: ["SEC-02"]
    description: "审计日志记录"
    
  SC-06_速率限制:
    mapped_requirements: ["SEC-02"]
    description: "API限流防护"
    
  SC-07_操作审计:
    mapped_requirements: ["SEC-02"]
    description: "安全操作审计"
    
  SC-11_时间限制:
    mapped_requirements: ["SEC-02"]
    description: "请求超时控制"
    
  SC-19_数据加密:
    mapped_requirements: ["SEC-01", "SEC-03"]
    description: "数据加密存储"
    
  SC-20_访问令牌管理:
    mapped_requirements: ["SEC-02"]
    description: "JWT和API Key管理"
    
  LAW-02_数据隐私保护:
    mapped_requirements: ["SEC-01", "SEC-03"]
    description: "密码和敏感数据保护"
    
  LAW-04_访问合法性检查:
    mapped_requirements: ["SEC-02"]
    description: "API访问合法性检查"
```


## 六、数据库表结构

```sql
-- 用户密码表
CREATE TABLE user_passwords (
    user_id UUID PRIMARY KEY REFERENCES users(id),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    last_changed_at TIMESTAMP NOT NULL,
    password_history TEXT[] DEFAULT '{}'
);

-- API密钥表
CREATE TABLE api_keys (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    user_id UUID REFERENCES users(id),
    permissions TEXT[],
    expires_at TIMESTAMP,
    last_used_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL
);

-- 审计日志表
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    details JSONB,
    created_at TIMESTAMP NOT NULL
);

-- 登录尝试表
CREATE TABLE login_attempts (
    id UUID PRIMARY KEY,
    username VARCHAR(100),
    ip_address INET,
    success BOOLEAN,
    failure_reason VARCHAR(100),
    created_at TIMESTAMP NOT NULL
);

-- 索引
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);
CREATE INDEX idx_login_attempts_ip ON login_attempts(ip_address);
CREATE INDEX idx_login_attempts_created ON login_attempts(created_at);
```


## 七、在Cursor中使用

```bash
# 1. 实现密码加密
@docs/SECURITY_REQUIREMENTS_v1.0.md 实现SEC-01密码加密存储，使用bcrypt算法，对齐SC-03敏感信息检测

# 2. 实现JWT认证
@docs/SECURITY_REQUIREMENTS_v1.0.md 实现SEC-02 JWT认证，配置RS256算法，对齐SC-20访问令牌管理

# 3. 实现RBAC权限
@docs/SECURITY_REQUIREMENTS_v1.0.md 实现SEC-02 RBAC权限检查，对齐SC-04权限检查能力

# 4. 实现敏感配置管理
@docs/SECURITY_REQUIREMENTS_v1.0.md 实现SEC-03敏感配置管理，使用环境变量，对齐SC-19数据加密

# 5. 配置安全中间件
@docs/SECURITY_REQUIREMENTS_v1.0.md 配置SecurityMiddleware，包含认证、授权、限流、审计
```


## 八、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，3项安全需求，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md |

---

**文档结束**