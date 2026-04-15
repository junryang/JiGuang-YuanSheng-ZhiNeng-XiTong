# 部署运维文档 - 纪光元生智能系统

| 文档版本 | 修改日期 | 修改人 | 修改内容 |
|---------|---------|--------|---------|
| v1.0 | 2026-01-13 | AI助手 | 完整版：基于所有子文件和对话内容，补充智能体运维、能力部署、安全运维、监控告警、容灾备份 |


## 一、概述

### 1.1 部署架构图

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                   用户访问                                          │
│                                      │                                              │
│                                      ▼                                              │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │                          CDN / 负载均衡 (Nginx/ALB)                            │ │
│  │                          + WAF + DDoS防护                                     │ │
│  └───────────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                              │
│              ┌───────────────────────┼───────────────────────┐                      │
│              ▼                       ▼                       ▼                      │
│  ┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐             │
│  │   前端服务        │   │   后端API服务     │   │   WebSocket服务   │             │
│  │   (Nginx + Vue)   │   │   (FastAPI)       │   │   (FastAPI/WS)    │             │
│  │   副本数: 2-5     │   │   副本数: 3-10    │   │   副本数: 2-5     │             │
│  │   HPA: CPU>70%    │   │   HPA: CPU>70%    │   │   HPA: CPU>60%    │             │
│  └───────────────────┘   └───────────────────┘   └───────────────────┘             │
│              │                       │                       │                      │
│              └───────────────────────┼───────────────────────┘                      │
│                                      ▼                                              │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │                              中间件层                                          │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │ │
│  │  │  PostgreSQL │ │    Redis    │ │   RabbitMQ  │ │   Chroma    │              │ │
│  │  │  (主从+备份)│ │   (集群)    │ │   (集群)    │ │  (向量库)   │              │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘              │ │
│  └───────────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                              │
│                                      ▼                                              │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │                           智能体运行时集群                                      │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │ │
│  │  │ 主脑(CEO)   │ │ 总经理(L2)  │ │ 经理(L3)    │ │ 员工(L4-L6) │              │ │
│  │  │ 副本: 2     │ │ 副本: 3     │ │ 副本: 5     │ │ 副本: 30+   │              │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘              │ │
│  └───────────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                              │
│                                      ▼                                              │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │                              存储层                                            │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │ │
│  │  │  对象存储   │ │   备份存储  │ │   日志存储  │ │  模型存储   │              │ │
│  │  │   (OSS)    │ │   (OSS)    │ │   (ELK)    │ │  (HuggingFace)│              │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘              │ │
│  └───────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 环境说明

| 环境 | 用途 | 域名 | 资源配置 | 智能体配置 |
|------|------|------|---------|-----------|
| dev | 开发环境 | dev.jyis.com | 2核4G x 2节点 | 10个测试智能体 |
| test | 测试环境 | test.jyis.com | 4核8G x 2节点 | 全部47个智能体 |
| staging | 预发布环境 | staging.jyis.com | 4核8G x 2节点 | 全部47个智能体 |
| prod | 生产环境 | jyis.com | 8核16G x 3节点+ | 全部47个智能体+弹性扩展 |

### 1.3 技术栈版本

| 组件 | 版本 | 说明 | 关联能力 |
|------|------|------|----------|
| Python | 3.11+ | 后端运行环境 | - |
| FastAPI | 0.115+ | Web框架 | EX-03 API调用 |
| PostgreSQL | 16+ | 主数据库 | EX-04 数据库操作 |
| Redis | 7+ | 缓存/队列 | MM-01 工作记忆 |
| RabbitMQ | 3.12+ | 消息队列 | EX-10 异步执行 |
| Chroma | 0.5+ | 向量数据库 | MM-03 长期记忆 |
| Nginx | 1.24+ | 反向代理 | - |
| Docker | 24+ | 容器化 | - |
| Kubernetes | 1.28+ | 容器编排 | - |
| Prometheus | 2.45+ | 监控 | AGENT-RUNTIME-04 |
| Grafana | 10+ | 可视化 | - |
| ELK | 8.10+ | 日志收集 | PC-03 日志理解 |
| Playwright | 1.40+ | 浏览器自动化 | WEB-01 |


## 二、智能体部署架构

### 2.1 智能体运行时部署

智能体作为独立的运行时单元部署，每个智能体类型有不同的资源需求和扩缩容策略。

| 智能体类型 | 层级 | 副本数 | 资源请求 | 资源限制 | HPA策略 | 关联能力 |
|-----------|------|--------|---------|---------|---------|----------|
| 主脑(CEO) | L1 | 2 | 1Gi/500m | 4Gi/2000m | CPU>60% | AGENT-RUNTIME-01 |
| 总经理 | L2 | 3 | 512Mi/250m | 2Gi/1000m | CPU>70% | DC-01 |
| 经理 | L3 | 5 | 512Mi/250m | 2Gi/1000m | CPU>70% | DC-02 |
| 主管 | L4 | 8 | 256Mi/100m | 1Gi/500m | CPU>75% | QL-05 |
| 员工 | L5 | 20+ | 256Mi/100m | 1Gi/500m | CPU>80% | EX-01~14 |
| 实习 | L6 | 5+ | 128Mi/50m | 512Mi/250m | CPU>80% | MM-04 |
| 安全工程师 | L5 | 3 | 512Mi/250m | 2Gi/1000m | CPU>70% | SC-01~20 |
| 财务专员 | L5 | 3 | 256Mi/100m | 1Gi/500m | CPU>70% | - |
| 营销专员 | L5 | 3 | 256Mi/100m | 1Gi/500m | CPU>70% | MK-01~30 |

### 2.2 智能体Deployment配置

**`k8s/agents/ceo-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-ceo
  namespace: jyis
  labels:
    app: agent
    agent-type: ceo
    agent-level: "1"
spec:
  replicas: 2
  selector:
    matchLabels:
      app: agent
      agent-type: ceo
  template:
    metadata:
      labels:
        app: agent
        agent-type: ceo
        agent-level: "1"
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: agent-ceo
        image: jyis/agent-runtime:latest
        imagePullPolicy: Always
        env:
        - name: AGENT_TYPE
          value: "ceo"
        - name: AGENT_LEVEL
          value: "1"
        - name: AGENT_ID
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        envFrom:
        - configMapRef:
            name: jyis-config
        - secretRef:
            name: jyis-secrets
        ports:
        - containerPort: 8000
          name: http
        - containerPort: 9090
          name: metrics
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        volumeMounts:
        - name: agent-storage
          mountPath: /app/data
      volumes:
      - name: agent-storage
        persistentVolumeClaim:
          claimName: agent-ceo-pvc
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: agent
                  agent-type: ceo
              topologyKey: kubernetes.io/hostname
```

### 2.3 智能体服务发现

**`k8s/agents/services.yaml`**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: agent-ceo-service
  namespace: jyis
spec:
  selector:
    app: agent
    agent-type: ceo
  ports:
  - port: 8000
    targetPort: 8000
    name: http
  - port: 9090
    targetPort: 9090
    name: metrics
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: agents-service
  namespace: jyis
spec:
  selector:
    app: agent
  ports:
  - port: 8000
    targetPort: 8000
    name: http
  type: ClusterIP
```

### 2.4 智能体HPA配置

**`k8s/agents/hpa.yaml`**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: agent-employee-hpa
  namespace: jyis
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-employee
  minReplicas: 20
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: agent_task_queue_length
      target:
        type: AverageValue
        averageValue: "10"
```


## 三、能力部署

### 3.1 能力服务部署

142 项能力在**逻辑上**独立注册与加载；**物理部署**按能力类别合并为少量可水平扩展的服务（见下表），避免「一能力一微服务」带来的运维与成本不可持续问题。支持进程内插件/动态加载与滚动热更新。

| 能力类别 | 服务名称 | 副本数 | 资源请求 | HPA策略 | 关联能力 |
|---------|---------|--------|---------|---------|----------|
| WEB能力 | capability-web | 3 | 512Mi/250m | CPU>70% | WEB-01~11 |
| 执行能力 | capability-execution | 3 | 512Mi/250m | CPU>70% | EX-01~14 |
| 记忆能力 | capability-memory | 2 | 1Gi/500m | CPU>70% | MM-01~08 |
| 学习能力 | capability-learning | 2 | 1Gi/500m | CPU>70% | LN-01~06 |
| 安全能力 | capability-security | 2 | 512Mi/250m | CPU>70% | SC-01~20 |

**`k8s/capabilities/web-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: capability-web
  namespace: jyis
  labels:
    app: capability
    capability-type: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: capability
      capability-type: web
  template:
    metadata:
      labels:
        app: capability
        capability-type: web
    spec:
      containers:
      - name: capability-web
        image: jyis/capability-web:latest
        imagePullPolicy: Always
        env:
        - name: CAPABILITY_TYPE
          value: "web"
        - name: PLAYWRIGHT_BROWSERS_PATH
          value: "/app/browsers"
        envFrom:
        - configMapRef:
            name: jyis-config
        - secretRef:
            name: jyis-secrets
        ports:
        - containerPort: 8000
          name: http
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        volumeMounts:
        - name: browsers-data
          mountPath: /app/browsers
      volumes:
      - name: browsers-data
        persistentVolumeClaim:
          claimName: browsers-pvc
```


## 四、Docker配置

### 4.1 后端Dockerfile

**`Dockerfile.backend`**

```dockerfile
# 多阶段构建
FROM python:3.11-slim as builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# 最终镜像
FROM python:3.11-slim

WORKDIR /app

# 安装运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 从builder复制依赖
COPY --from=builder /root/.local /root/.local

# 复制应用代码
COPY . .

# 设置环境变量
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 创建非root用户
RUN useradd -m -u 1000 jyis && chown -R jyis:jyis /app
USER jyis

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4.2 智能体运行时Dockerfile

**`Dockerfile.agent`**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements-agent.txt .
RUN pip install --no-cache-dir -r requirements-agent.txt

# 复制智能体代码
COPY agents/ /app/agents/
COPY core/ /app/core/

# 创建非root用户
RUN useradd -m -u 1000 agent && chown -R agent:agent /app
USER agent

# 暴露端口
EXPOSE 8000 9090

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动智能体
CMD ["python", "-m", "agents.runtime"]
```

### 4.3 前端Dockerfile

**`Dockerfile.frontend`**

```dockerfile
# 多阶段构建
FROM node:20-alpine as builder

WORKDIR /app

# 复制依赖文件
COPY frontend/package*.json ./
RUN npm ci --only=production

# 复制源码并构建
COPY frontend/ .
RUN npm run build

# 生产镜像
FROM nginx:1.24-alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 4.4 Nginx配置

**`nginx.conf`**

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # 安全头
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Gzip压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API代理
    location /api/ {
        proxy_pass http://backend-service:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # WebSocket代理
    location /ws/ {
        proxy_pass http://websocket-service:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_connect_timeout 3600s;
        proxy_send_timeout 3600s;
        proxy_read_timeout 3600s;
    }

    # 智能体代理
    location /agents/ {
        proxy_pass http://agents-service:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 能力代理
    location /capabilities/ {
        proxy_pass http://capabilities-service:8000/;
        proxy_set_header Host $host;
    }

    # 健康检查
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### 4.5 docker-compose.yml（完整开发环境）

**`docker-compose.yml`**

```yaml
version: '3.8'

services:
  # 数据库
  postgres:
    image: pgvector/pgvector:pg16
    container_name: jyis-postgres
    environment:
      POSTGRES_DB: jyis_dev
      POSTGRES_USER: jyis
      POSTGRES_PASSWORD: jyis123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U jyis"]
      interval: 10s
      timeout: 5s
      retries: 5

  # 缓存
  redis:
    image: redis:7-alpine
    container_name: jyis-redis
    command: redis-server --appendonly yes --requirepass jyis123
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "jyis123", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # 消息队列
  rabbitmq:
    image: rabbitmq:3.12-management-alpine
    container_name: jyis-rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: jyis
      RABBITMQ_DEFAULT_PASS: jyis123
    ports:
      - "5672:5672"
      - "15672:15672"
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # 向量数据库
  chroma:
    image: chromadb/chroma:latest
    container_name: jyis-chroma
    ports:
      - "8001:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      IS_PERSISTENT: "TRUE"
      PERSIST_DIRECTORY: /chroma/chroma
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 10s
      timeout: 5s
      retries: 5

  # 后端API
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: jyis-backend
    environment:
      DATABASE_URL: postgresql://jyis:jyis123@postgres:5432/jyis_dev
      REDIS_URL: redis://:jyis123@redis:6379/0
      RABBITMQ_URL: amqp://jyis:jyis123@rabbitmq:5672/
      CHROMA_URL: http://chroma:8000
      DEEPSEEK_API_KEY: ${DEEPSEEK_API_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
      chroma:
        condition: service_healthy
    volumes:
      - ./:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  # 智能体运行时
  agent-ceo:
    build:
      context: .
      dockerfile: Dockerfile.agent
    container_name: jyis-agent-ceo
    environment:
      AGENT_TYPE: ceo
      AGENT_LEVEL: "1"
      DATABASE_URL: postgresql://jyis:jyis123@postgres:5432/jyis_dev
      REDIS_URL: redis://:jyis123@redis:6379/0
    ports:
      - "8002:8000"
    depends_on:
      - backend
    volumes:
      - ./agents:/app/agents
    command: python -m agents.runtime --type ceo

  # 前端
  frontend:
    build:
      context: ./frontend
      dockerfile: ../Dockerfile.frontend
    container_name: jyis-frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    container_name: jyis-prometheus
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus/alerts.yml:/etc/prometheus/alerts.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  # Grafana
  grafana:
    image: grafana/grafana:latest
    container_name: jyis-grafana
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

volumes:
  postgres_data:
  redis_data:
  rabbitmq_data:
  chroma_data:
  prometheus_data:
  grafana_data:
```


## 五、Kubernetes配置

### 5.1 Namespace

**`k8s/namespace.yaml`**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: jyis
  labels:
    name: jyis
    environment: production
```

### 5.2 ConfigMap

**`k8s/configmap.yaml`**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: jyis-config
  namespace: jyis
data:
  DATABASE_URL: postgresql://jyis:${DB_PASSWORD}@postgres-service:5432/jyis_prod
  REDIS_URL: redis://:${REDIS_PASSWORD}@redis-service:6379/0
  RABBITMQ_URL: amqp://jyis:${RMQ_PASSWORD}@rabbitmq-service:5672/
  CHROMA_URL: http://chroma-service:8000
  LOG_LEVEL: INFO
  AGENT_HEARTBEAT_INTERVAL: "30"
  AGENT_MAX_RETRIES: "3"
  CAPABILITY_TIMEOUT: "60"
  MEMORY_CONSOLIDATION_TIME: "02:00"
```

### 5.3 Secrets

**`k8s/secrets.yaml`**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: jyis-secrets
  namespace: jyis
type: Opaque
stringData:
  DB_PASSWORD: "${DB_PASSWORD}"
  REDIS_PASSWORD: "${REDIS_PASSWORD}"
  RMQ_PASSWORD: "${RMQ_PASSWORD}"
  DEEPSEEK_API_KEY: "${DEEPSEEK_API_KEY}"
  OPENAI_API_KEY: "${OPENAI_API_KEY}"
  CLAUDE_API_KEY: "${CLAUDE_API_KEY}"
  JWT_SECRET_KEY: "${JWT_SECRET_KEY}"
  ENCRYPTION_KEY: "${ENCRYPTION_KEY}"
```

### 5.4 后端Deployment

**`k8s/backend-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: jyis
  labels:
    app: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: jyis-backend
      containers:
      - name: backend
        image: jyis/backend:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
        - containerPort: 9090
          name: metrics
        envFrom:
        - configMapRef:
            name: jyis-config
        - secretRef:
            name: jyis-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          capabilities:
            drop: ["ALL"]
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: backend
              topologyKey: kubernetes.io/hostname
```

### 5.5 前端Deployment

**`k8s/frontend-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: jyis
  labels:
    app: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: jyis/frontend:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 80
          name: http
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
        securityContext:
          runAsNonRoot: true
          runAsUser: 101
          allowPrivilegeEscalation: false
```

### 5.6 Services

**`k8s/services.yaml`**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: jyis
spec:
  selector:
    app: backend
  ports:
  - port: 8000
    targetPort: 8000
    name: http
  - port: 9090
    targetPort: 9090
    name: metrics
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: jyis
spec:
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 80
    name: http
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: websocket-service
  namespace: jyis
spec:
  selector:
    app: websocket
  ports:
  - port: 8000
    targetPort: 8000
    name: ws
  type: ClusterIP
```

### 5.7 Ingress

**`k8s/ingress.yaml`**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: jyis-ingress
  namespace: jyis
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "3600"
    nginx.ingress.kubernetes.io/proxy-body-size: "100m"
    nginx.ingress.kubernetes.io/enable-cors: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - jyis.com
    - api.jyis.com
    secretName: jyis-tls
  rules:
  - host: jyis.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
  - host: api.jyis.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8000
```

### 5.8 HPA自动扩缩容

**`k8s/hpa.yaml`**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: jyis
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: agent-employee-hpa
  namespace: jyis
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-employee
  minReplicas: 20
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: agent_task_queue_length
      target:
        type: AverageValue
        averageValue: "10"
```

### 5.9 PodDisruptionBudget

**`k8s/pdb.yaml`**

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: backend-pdb
  namespace: jyis
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: backend
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: agent-ceo-pdb
  namespace: jyis
spec:
  maxUnavailable: 0
  selector:
    matchLabels:
      app: agent
      agent-type: ceo
```

### 5.10 NetworkPolicy

**`k8s/network-policy.yaml`**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
  namespace: jyis
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - port: 8000
      protocol: TCP
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - port: 5432
      protocol: TCP
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - port: 6379
      protocol: TCP
  - to:
    - podSelector:
        matchLabels:
          app: rabbitmq
    ports:
    - port: 5672
      protocol: TCP
```


## 六、CI/CD流水线

### 6.1 GitHub Actions配置

**`.github/workflows/ci-cd.yml`**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME_BACKEND: ${{ github.repository }}/backend
  IMAGE_NAME_FRONTEND: ${{ github.repository }}/frontend
  IMAGE_NAME_AGENT: ${{ github.repository }}/agent

jobs:
  # 代码检查
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install ruff black mypy
      
      - name: Run Ruff
        run: ruff check .
      
      - name: Run Black
        run: black --check .
      
      - name: Run MyPy
        run: mypy .

  # 单元测试
  test:
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
        run: |
          pytest tests/ --cov=. --cov-report=xml --cov-report=html
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

  # 能力测试
  capability-test:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install Playwright
        run: |
          pip install playwright
          playwright install chromium
      
      - name: Run capability tests
        run: pytest tests/capabilities/ -v

  # 安全扫描
  security-scan:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r . -f json -o bandit-report.json
      
      - name: Check for high severity issues
        run: |
          if grep -q '"issue_severity": "HIGH"' bandit-report.json; then
            echo "High severity issues found"
            exit 1
          fi

  # 构建镜像
  build:
    runs-on: ubuntu-latest
    needs: [test, capability-test, security-scan]
    if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop')
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push Backend
        uses: docker/build-push-action@v5
        with:
          context: .
          file: Dockerfile.backend
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME_BACKEND }}:${{ github.sha }}
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME_BACKEND }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Build and push Frontend
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          file: Dockerfile.frontend
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME_FRONTEND }}:${{ github.sha }}
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME_FRONTEND }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Build and push Agent Runtime
        uses: docker/build-push-action@v5
        with:
          context: .
          file: Dockerfile.agent
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME_AGENT }}:${{ github.sha }}
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME_AGENT }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # 部署到开发环境
  deploy-dev:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment: development
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure kubectl
        uses: azure/setup-kubectl@v3
      
      - name: Set up kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBE_CONFIG_DEV }}" | base64 --decode > $HOME/.kube/config
      
      - name: Deploy to K8s
        run: |
          kubectl set image deployment/backend backend=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_BACKEND }}:${{ github.sha }} -n jyis-dev
          kubectl set image deployment/frontend frontend=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_FRONTEND }}:${{ github.sha }} -n jyis-dev
          kubectl set image deployment/agent-ceo agent-ceo=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_AGENT }}:${{ github.sha }} -n jyis-dev
      
      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/backend -n jyis-dev --timeout=5m
          kubectl rollout status deployment/frontend -n jyis-dev --timeout=5m

  # 部署到生产环境
  deploy-prod:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure kubectl
        uses: azure/setup-kubectl@v3
      
      - name: Set up kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBE_CONFIG_PROD }}" | base64 --decode > $HOME/.kube/config
      
      - name: Deploy to K8s (Canary)
        run: |
          kubectl set image deployment/backend-canary backend=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_BACKEND }}:${{ github.sha }} -n jyis
          kubectl rollout status deployment/backend-canary -n jyis --timeout=5m
      
      - name: Smoke test
        run: |
          curl -f https://canary.jyis.com/health
      
      - name: Promote to stable
        run: |
          kubectl set image deployment/backend backend=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_BACKEND }}:${{ github.sha }} -n jyis
          kubectl set image deployment/frontend frontend=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_FRONTEND }}:${{ github.sha }} -n jyis
          kubectl set image deployment/agent-ceo agent-ceo=${{ env.REGISTRY }}/${{ env.IMAGE_NAME_AGENT }}:${{ github.sha }} -n jyis
      
      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/backend -n jyis --timeout=10m
          kubectl rollout status deployment/frontend -n jyis --timeout=5m
          kubectl rollout status deployment/agent-ceo -n jyis --timeout=5m
```


## 七、监控与告警

### 7.1 Prometheus配置

**`prometheus/prometheus.yml`**

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: (.+):(?:\d+);(\d+)
        replacement: $1:$2
        target_label: __address__

  - job_name: 'agents'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: [jyis]
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: agent
      - source_labels: [__meta_kubernetes_pod_label_agent_type]
        action: replace
        target_label: agent_type
      - source_labels: [__meta_kubernetes_pod_label_agent_level]
        action: replace
        target_label: agent_level

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

### 7.2 告警规则

**`prometheus/alerts.yml`**

```yaml
groups:
  - name: jyis_alerts
    interval: 30s
    rules:
      # 系统告警
      - alert: HighCPUUsage
        expr: sum(rate(container_cpu_usage_seconds_total{namespace="jyis"}[5m])) by (pod) > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.pod }}"

      - alert: HighMemoryUsage
        expr: sum(container_memory_working_set_bytes{namespace="jyis"}) by (pod) / sum(container_spec_memory_limit_bytes{namespace="jyis"}) by (pod) > 0.9
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High memory usage on {{ $labels.pod }}"

      # API告警
      - alert: APIHighLatency
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint)) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High API latency on {{ $labels.endpoint }}"

      - alert: APIHighErrorRate
        expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High API error rate"

      # 智能体告警
      - alert: AgentOffline
        expr: agent_up == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Agent {{ $labels.agent_type }} is offline"

      - alert: AgentHighLoad
        expr: agent_cognitive_load > 0.8
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Agent {{ $labels.agent_type }} has high cognitive load"

      - alert: AgentTrustScoreLow
        expr: agent_trust_score < 70
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Agent {{ $labels.agent_type }} trust score is below 70"

      # 能力告警
      - alert: CapabilityFailure
        expr: rate(capability_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High capability failure rate for {{ $labels.capability }}"

      # 数据库告警
      - alert: DatabaseHighConnections
        expr: pg_stat_database_numbackends > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High database connections"

      # 预算告警
      - alert: BudgetExceeded
        expr: model_cost_daily > 500
        labels:
          severity: warning
        annotations:
          summary: "Daily model cost exceeded ¥500"
```


## 八、日志收集

### 8.1 ELK配置

**`docker-compose.elk.yml`**

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
      - ES_JAVA_OPTS=-Xms2g -Xmx2g
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
    volumes:
      - es_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

  logstash:
    image: docker.elastic.co/logstash/logstash:8.10.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5000:5000"
      - "5044:5044"
    environment:
      - XPACK_MONITORING_ENABLED=false
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=elastic
      - ELASTICSEARCH_PASSWORD=${ELASTIC_PASSWORD}
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.10.0
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    depends_on:
      - logstash

volumes:
  es_data:
```

### 8.2 智能体日志格式

```json
{
  "timestamp": "2026-01-13T10:30:00.000Z",
  "level": "INFO",
  "agent_id": "agent_ceo_001",
  "agent_type": "ceo",
  "agent_level": 1,
  "capability": "AGENT-RUNTIME-01",
  "action": "task_delegated",
  "task_id": "task_001",
  "target_agent": "agent_web_gm",
  "duration_ms": 234,
  "cognitive_load": 0.45,
  "trust_score": 100,
  "message": "Task delegated successfully"
}
```


## 九、备份与恢复

### 9.1 数据库备份脚本

**`scripts/backup.sh`**

```bash
#!/bin/bash

BACKUP_DIR="/backup/jyis"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR/{postgres,redis,chroma,config,models}

# PostgreSQL备份
echo "Backing up PostgreSQL..."
PGPASSWORD=$DB_PASSWORD pg_dump -h postgres-service -U jyis jyis_prod | gzip > $BACKUP_DIR/postgres/jyis_$DATE.sql.gz

# Redis备份
echo "Backing up Redis..."
redis-cli -h redis-service -a $REDIS_PASSWORD --rdb $BACKUP_DIR/redis/dump_$DATE.rdb

# Chroma备份
echo "Backing up Chroma..."
kubectl cp chroma-service:/chroma/chroma $BACKUP_DIR/chroma/chroma_$DATE -n jyis
tar -czf $BACKUP_DIR/chroma/chroma_$DATE.tar.gz -C $BACKUP_DIR/chroma chroma_$DATE

# 配置备份
echo "Backing up ConfigMaps and Secrets..."
kubectl get configmap -n jyis -o yaml > $BACKUP_DIR/config/configmaps_$DATE.yaml
kubectl get secret -n jyis -o yaml > $BACKUP_DIR/config/secrets_$DATE.yaml

# 模型备份（微调模型）
echo "Backing up fine-tuned models..."
tar -czf $BACKUP_DIR/models/models_$DATE.tar.gz /app/models/fine_tuned/

# 清理过期备份
find $BACKUP_DIR -type f -mtime +$RETENTION_DAYS -delete

echo "Backup completed: $DATE"
```

### 9.2 恢复脚本

**`scripts/restore.sh`**

```bash
#!/bin/bash

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

echo "Restoring from $BACKUP_FILE..."

# 解压备份
tar -xzf $BACKUP_FILE -C /tmp/restore

# 恢复PostgreSQL
echo "Restoring PostgreSQL..."
zcat /tmp/restore/postgres/*.sql.gz | PGPASSWORD=$DB_PASSWORD psql -h postgres-service -U jyis jyis_prod

# 恢复Redis
echo "Restoring Redis..."
redis-cli -h redis-service -a $REDIS_PASSWORD shutdown nosave
kubectl cp /tmp/restore/redis/dump.rdb redis-service:/data/dump.rdb -n jyis
kubectl delete pod -l app=redis -n jyis

# 恢复Chroma
echo "Restoring Chroma..."
kubectl cp /tmp/restore/chroma/ chroma-service:/chroma/ -n jyis
kubectl delete pod -l app=chroma -n jyis

echo "Restore completed"
```

### 9.3 定时备份CronJob

**`k8s/backup-cronjob.yaml`**

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup
  namespace: jyis
spec:
  schedule: "0 2 * * *"
  successfulJobsHistoryLimit: 7
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: jyis-backup
          containers:
          - name: backup
            image: postgres:16
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: jyis-secrets
                  key: DB_PASSWORD
            command:
            - /bin/sh
            - -c
            - |
              pg_dump -h postgres-service -U jyis jyis_prod | gzip > /backup/jyis_$(date +%Y%m%d_%H%M%S).sql.gz
              # 上传到OSS
              aws s3 cp /backup/ s3://jyis-backups/postgres/ --recursive
            volumeMounts:
            - name: backup-storage
              mountPath: /backup
          restartPolicy: OnFailure
          volumes:
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-pvc
```


## 十、故障排查

### 10.1 常见问题排查

| 问题 | 排查步骤 | 解决方案 | 关联能力 |
|------|---------|---------|----------|
| Pod启动失败 | `kubectl describe pod` | 检查镜像、资源、配置 | - |
| API响应慢 | `kubectl top pod` | 增加副本或资源 | PO-01 |
| 数据库连接失败 | 检查Secret和Service | 修正连接配置 | - |
| WebSocket断开 | 检查Ingress timeout | 增加超时时间 | - |
| 智能体离线 | `kubectl logs agent-xxx` | 检查心跳配置 | AGENT-RUNTIME-05 |
| 能力调用失败 | 检查能力服务日志 | 重启能力服务 | META-05 |
| 记忆检索慢 | 检查Chroma状态 | 优化索引 | MM-04 |
| 模型调用超时 | 检查API配额 | 切换备用模型 | EM-03 |

### 10.2 健康检查端点

| 端点 | 用途 | 预期响应 | 关联能力 |
|------|------|---------|----------|
| `/health` | 基础健康检查 | `{"status": "healthy"}` | - |
| `/ready` | 就绪检查 | `{"status": "ready", "dependencies": {...}}` | - |
| `/metrics` | Prometheus指标 | Prometheus格式数据 | - |
| `/agents/health` | 智能体健康 | `{"agents_online": 47, "agents_degraded": 1}` | AGENT-RUNTIME-05 |
| `/capabilities/health` | 能力健康 | `{"capabilities_active": 142, "capabilities_degraded": 3}` | META-05 |


## 十一、快速部署命令

### 11.1 开发环境启动

```bash
# 获取代码（推荐直接使用当前工作区）
cd d:/BaiduSyncdisk/JiGuang

# 如需从远端拉取，请使用已配置的企业仓库地址（示例）
# git clone https://git.example.com/your-org/JiGuang.git
# cd JiGuang

# 配置环境变量
cp .env.example .env
# 编辑.env文件，至少配置以下必填项：
# DATABASE_URL=
# REDIS_URL=
# JWT_SECRET=
# OPENAI_API_KEY=
# DEEPSEEK_API_KEY=
# DB_PASSWORD=
# REDIS_PASSWORD=
# ENCRYPTION_KEY=

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 初始化智能体
python scripts/init_agents.py

# 加载能力
python scripts/load_capabilities.py
```

### 11.2 生产环境部署

```bash
# 创建namespace
kubectl create namespace jyis

# 创建secrets
kubectl create secret generic jyis-secrets \
  --from-literal=DB_PASSWORD="${DB_PASSWORD}" \
  --from-literal=REDIS_PASSWORD="${REDIS_PASSWORD}" \
  --from-literal=DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY}" \
  -n jyis

# 部署中间件
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install jyis-postgres bitnami/postgresql -n jyis -f k8s/postgres-values.yaml
helm install jyis-redis bitnami/redis -n jyis -f k8s/redis-values.yaml

# 部署应用
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/agents/
kubectl apply -f k8s/capabilities/
kubectl apply -f k8s/services.yaml
kubectl apply -f k8s/ingress.yaml

# 等待所有Pod就绪
kubectl wait --for=condition=ready pod --all -n jyis --timeout=300s

# 初始化智能体
kubectl exec -it deployment/agent-ceo -n jyis -- python scripts/init_agents.py
```

### 11.3 金丝雀发布

```bash
# 部署金丝雀版本
kubectl apply -f k8s/backend-canary-deployment.yaml

# 等待金丝雀就绪
kubectl wait --for=condition=ready pod -l app=backend,version=canary -n jyis --timeout=60s

# 切换10%流量到金丝雀
kubectl patch ingress jyis-ingress -n jyis --type='json' \
  -p='[{"op": "add", "path": "/metadata/annotations/nginx.ingress.kubernetes.io~1canary", "value": "true"},
       {"op": "add", "path": "/metadata/annotations/nginx.ingress.kubernetes.io~1canary-weight", "value": "10"}]'

# 监控金丝雀指标
# 如果正常，逐步增加流量到100%

# 完成发布
kubectl set image deployment/backend backend=jyis/backend:latest -n jyis
kubectl delete deployment backend-canary -n jyis
```

### 11.4 回滚

```bash
# 查看历史版本
kubectl rollout history deployment/backend -n jyis

# 回滚到上一版本
kubectl rollout undo deployment/backend -n jyis

# 回滚到指定版本
kubectl rollout undo deployment/backend -n jyis --to-revision=3

# 查看回滚状态
kubectl rollout status deployment/backend -n jyis
```


## 十二、版本记录

| 版本 | 日期 | 修改内容 |
|------|------|---------|
| v1.0 | 2026-01-13 | 完整版：基于所有子文件和对话内容，补充智能体运维、能力部署、安全运维、监控告警、金丝雀发布、容灾备份 |