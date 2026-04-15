# 记忆能力要求规范 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\MEMORY_CAPABILITY_SPEC_v1.0.md
```


# 记忆能力要求规范 v1.0

## 一、能力总览

```yaml
# 五大记忆核心能力

memory_capabilities:
  STORAGE:
    name: "记忆存储"
    description: "向量数据库存储（Chroma/Qdrant/Pinecone）"
    priority: "P0"
    
  RETRIEVAL:
    name: "记忆检索"
    description: "语义搜索 + 时间衰减排序"
    priority: "P0"
    
  SUMMARIZATION:
    name: "记忆总结"
    description: "自动压缩和总结长期记忆"
    priority: "P1"
    
  FORGETTING:
    name: "记忆遗忘"
    description: "自动清理低价值记忆"
    priority: "P1"
    
  SHARING:
    name: "记忆共享"
    description: "支持记忆在智能体间共享"
    priority: "P0"
```


## 二、记忆存储能力

```yaml
capability: "MEMORY_STORAGE"
name: "记忆存储"
description: "向量数据库存储，支持高效存储和检索向量化记忆"
priority: "P0"

# 支持的向量数据库
vector_databases:
  - name: "Chroma"
    type: "embedded"
    use_case: "开发测试、小规模部署"
    install: "pip install chromadb"
    config:
      persist_directory: "./data/chroma"
      collection_name: "jyis_memories"
      
  - name: "Qdrant"
    type: "server"
    use_case: "生产环境、中大规模"
    install: "docker run -p 6333:6333 qdrant/qdrant"
    config:
      host: "localhost"
      port: 6333
      collection_name: "jyis_memories"
      
  - name: "Pinecone"
    type: "cloud"
    use_case: "云原生、免运维"
    install: "pip install pinecone-client"
    config:
      api_key: "${PINECONE_API_KEY}"
      environment: "us-west1-gcp"
      index_name: "jyis-memories"

# 统一存储接口
storage_interface:
  class_name: "MemoryStorage"
  methods:
    - name: "store"
      description: "存储记忆"
      parameters:
        - name: "memory"
          type: "Memory"
        - name: "embedding"
          type: "List[float]"
      returns: "memory_id"
      
    - name: "batch_store"
      description: "批量存储记忆"
      parameters:
        - name: "memories"
          type: "List[Memory]"
        - name: "embeddings"
          type: "List[List[float]]"
      returns: "List[memory_id]"
      
    - name: "delete"
      description: "删除记忆"
      parameters:
        - name: "memory_id"
          type: "str"
      returns: "bool"
      
    - name: "update"
      description: "更新记忆"
      parameters:
        - name: "memory_id"
          type: "str"
        - name: "memory"
          type: "Memory"
        - name: "embedding"
          type: "List[float]"
      returns: "bool"

# 存储配置
storage_config:
  embedding_dimension: 1536
  distance_metric: "cosine"  # cosine/euclidean/dot
  batch_size: 100
  max_retries: 3

# 实现代码模板
implementation_code: |
  from abc import ABC, abstractmethod
  from typing import List, Optional
  import chromadb
  from qdrant_client import QdrantClient
  import pinecone
  
  class MemoryStorage(ABC):
      """记忆存储抽象基类"""
      
      @abstractmethod
      def store(self, memory: dict, embedding: List[float]) -> str:
          """存储记忆"""
          pass
      
      @abstractmethod
      def retrieve(self, query_embedding: List[float], limit: int) -> List[dict]:
          """检索记忆"""
          pass
      
      @abstractmethod
      def delete(self, memory_id: str) -> bool:
          """删除记忆"""
          pass
  
  class ChromaStorage(MemoryStorage):
      """Chroma存储实现"""
      
      def __init__(self, persist_directory: str = "./data/chroma"):
          self.client = chromadb.PersistentClient(path=persist_directory)
          self.collection = self.client.get_or_create_collection(
              name="jyis_memories",
              metadata={"hnsw:space": "cosine"}
          )
      
      def store(self, memory: dict, embedding: List[float]) -> str:
          memory_id = memory.get("id", str(uuid.uuid4()))
          self.collection.add(
              ids=[memory_id],
              embeddings=[embedding],
              metadatas=[memory.get("metadata", {})],
              documents=[memory.get("content", "")]
          )
          return memory_id
      
      def retrieve(self, query_embedding: List[float], limit: int = 10) -> List[dict]:
          results = self.collection.query(
              query_embeddings=[query_embedding],
              n_results=limit
          )
          return self._format_results(results)
```


## 三、记忆检索能力

```yaml
capability: "MEMORY_RETRIEVAL"
name: "记忆检索"
description: "语义搜索 + 时间衰减排序，支持混合检索"
priority: "P0"

# 检索策略
retrieval_strategies:
  - name: "semantic_search"
    description: "基于向量相似度的语义搜索"
    weight: 0.6
    
  - name: "time_decay"
    description: "基于时间衰减的排序"
    weight: 0.3
    
  - name: "importance_boost"
    description: "重要性加权"
    weight: 0.1

# 时间衰减公式
time_decay_formula:
  formula: "score = base_score * exp(-λ * t)"
  lambda: "0.1"  # 衰减率
  t: "time_in_days"
  half_life: "7天"

# 混合检索参数
hybrid_search_config:
  semantic_weight: 0.5
  bm25_weight: 0.3
  time_decay_weight: 0.2
  rerank_enabled: true
  rerank_model: "cross-encoder"

# 检索接口
retrieval_interface:
  class_name: "MemoryRetriever"
  methods:
    - name: "search"
      description: "混合检索"
      parameters:
        - name: "query"
          type: "str"
        - name: "query_embedding"
          type: "List[float]"
        - name: "limit"
          type: "int"
        - name: "filters"
          type: "dict"
        - name: "time_decay"
          type: "bool"
      returns: "List[Memory]"
      
    - name: "semantic_search"
      description: "纯语义搜索"
      parameters:
        - name: "query_embedding"
          type: "List[float]"
        - name: "limit"
          type: "int"
      returns: "List[Memory]"
      
    - name: "apply_time_decay"
      description: "应用时间衰减"
      parameters:
        - name: "memories"
          type: "List[Memory]"
      returns: "List[Memory]"
      
    - name: "rerank"
      description: "重排序结果"
      parameters:
        - name: "query"
          type: "str"
        - name: "memories"
          type: "List[Memory]"
      returns: "List[Memory]"

# 实现代码模板
implementation_code: |
  import numpy as np
  from datetime import datetime, timedelta
  from typing import List, Tuple
  
  class MemoryRetriever:
      """记忆检索器"""
      
      def __init__(self, storage: MemoryStorage):
          self.storage = storage
          self.decay_lambda = 0.1
      
      def semantic_search(self, query_embedding: List[float], limit: int = 10) -> List[dict]:
          """纯语义搜索"""
          return self.storage.retrieve(query_embedding, limit)
      
      def apply_time_decay(self, memories: List[dict]) -> List[dict]:
          """应用时间衰减"""
          now = datetime.now()
          for memory in memories:
              created_at = datetime.fromisoformat(memory.get("created_at", now.isoformat()))
              days_passed = (now - created_at).days
              decay_factor = np.exp(-self.decay_lambda * days_passed)
              memory["relevance_score"] = memory.get("similarity_score", 1.0) * decay_factor
          return sorted(memories, key=lambda x: x["relevance_score"], reverse=True)
      
      def hybrid_search(self, query: str, query_embedding: List[float], 
                        limit: int = 10, time_decay: bool = True) -> List[dict]:
          """混合检索：语义搜索 + 时间衰减"""
          # 1. 语义搜索
          memories = self.semantic_search(query_embedding, limit * 2)
          
          # 2. 添加相似度分数
          for i, memory in enumerate(memories):
              memory["similarity_score"] = 1.0 - (i / len(memories))
          
          # 3. 时间衰减
          if time_decay:
              memories = self.apply_time_decay(memories)
          
          return memories[:limit]
```


## 四、记忆总结能力

```yaml
capability: "MEMORY_SUMMARIZATION"
name: "记忆总结"
description: "自动压缩和总结长期记忆"
priority: "P1"

# 触发条件
trigger_conditions:
  - type: "count_threshold"
    description: "记忆数量超过阈值"
    threshold: 100
    
  - type: "time_threshold"
    description: "定期触发"
    schedule: "daily"
    
  - type: "manual"
    description: "用户手动触发"

# 总结策略
summarization_strategies:
  - name: "clustering"
    description: "聚类相似记忆后总结"
    method: "k-means"
    
  - name: "temporal"
    description: "按时间窗口总结"
    window: "week"
    
  - name: "hierarchical"
    description: "层次化总结"
    levels: 3

# 总结配置
summarization_config:
  model: "deepseek-chat"
  max_input_tokens: 8000
  max_output_tokens: 2000
  temperature: 0.3
  prompt_template: |
    请总结以下记忆内容，提取关键信息和模式：
    
    记忆列表：
    {memories}
    
    请输出：
    1. 核心主题
    2. 关键发现
    3. 重复模式
    4. 重要经验

# 总结接口
summarization_interface:
  class_name: "MemorySummarizer"
  methods:
    - name: "summarize"
      description: "总结记忆"
      parameters:
        - name: "memories"
          type: "List[Memory]"
        - name: "strategy"
          type: "str"
      returns: "Summary"
      
    - name: "cluster_memories"
      description: "聚类记忆"
      parameters:
        - name: "memories"
          type: "List[Memory]"
        - name: "n_clusters"
          type: "int"
      returns: "List[Cluster]"
      
    - name: "auto_summarize"
      description: "自动总结触发"
      parameters:
        - name: "agent_id"
          type: "str"
      returns: "bool"

# 数据模型
data_model:
  Summary:
    id: str
    agent_id: str
    title: str
    content: str
    key_findings: List[str]
    patterns: List[str]
    source_memory_ids: List[str]
    created_at: datetime

# 实现代码模板
implementation_code: |
  from sklearn.cluster import KMeans
  import numpy as np
  
  class MemorySummarizer:
      """记忆总结器"""
      
      def __init__(self, llm_client):
          self.llm_client = llm_client
      
      def cluster_memories(self, memories: List[dict], n_clusters: int = 5) -> List[List[dict]]:
          """K-means聚类"""
          embeddings = np.array([m["embedding"] for m in memories])
          kmeans = KMeans(n_clusters=min(n_clusters, len(memories)))
          labels = kmeans.fit_predict(embeddings)
          
          clusters = [[] for _ in range(n_clusters)]
          for memory, label in zip(memories, labels):
              clusters[label].append(memory)
          return clusters
      
      async def summarize(self, memories: List[dict]) -> dict:
          """调用大模型总结"""
          memories_text = "\n".join([m["content"] for m in memories[:50]])
          
          prompt = f"""
          请总结以下记忆内容，提取关键信息和模式：
          
          记忆列表：
          {memories_text}
          
          请输出JSON格式：
          {{
              "title": "总结标题",
              "key_findings": ["发现1", "发现2"],
              "patterns": ["模式1", "模式2"],
              "lessons": ["经验1", "经验2"]
          }}
          """
          
          response = await self.llm_client.chat(prompt)
          return json.loads(response)
```


## 五、记忆遗忘能力

```yaml
capability: "MEMORY_FORGETTING"
name: "记忆遗忘"
description: "自动清理低价值记忆"
priority: "P1"

# 遗忘策略
forgetting_strategies:
  - name: "importance_based"
    description: "基于重要性评分"
    threshold: 0.1
    action: "delete"
    
  - name: "ttl_based"
    description: "基于生存时间"
    ttl_days: 30
    action: "archive_or_delete"
    
  - name: "lru_based"
    description: "最少最近使用"
    max_size: 10000
    action: "evict_least_used"
    
  - name: "hybrid"
    description: "混合策略"
    formula: "score = importance * (1 - access_frequency/100) * exp(-time/30)"

# 遗忘配置
forgetting_config:
  importance_threshold: 0.1
  default_ttl_days: 30
  max_memories_per_agent: 10000
  cleanup_interval_hours: 24
  dry_run: false

# 遗忘接口
forgetting_interface:
  class_name: "MemoryForgetting"
  methods:
    - name: "evaluate_memory_value"
      description: "评估记忆价值"
      parameters:
        - name: "memory"
          type: "Memory"
      returns: "float"
      
    - name: "cleanup"
      description: "清理低价值记忆"
      parameters:
        - name: "agent_id"
          type: "str"
        - name: "dry_run"
          type: "bool"
      returns: "CleanupResult"
      
    - name: "archive_memory"
      description: "归档记忆"
      parameters:
        - name: "memory_id"
          type: "str"
      returns: "bool"
      
    - name: "restore_memory"
      description: "恢复归档记忆"
      parameters:
        - name: "memory_id"
          type: "str"
      returns: "bool"

# 数据模型
data_model:
  CleanupResult:
    agent_id: str
    deleted_count: int
    archived_count: int
    preserved_count: int
    execution_time: float
    details: List[dict]

# 实现代码模板
implementation_code: |
  from datetime import datetime, timedelta
  
  class MemoryForgetting:
      """记忆遗忘管理器"""
      
      def __init__(self, storage: MemoryStorage):
          self.storage = storage
          self.importance_threshold = 0.1
          self.ttl_days = 30
          self.max_memories = 10000
      
      def evaluate_memory_value(self, memory: dict) -> float:
          """评估记忆价值"""
          importance = memory.get("importance", 0.5)
          access_count = memory.get("access_count", 0)
          created_at = datetime.fromisoformat(memory.get("created_at", datetime.now().isoformat()))
          days_old = (datetime.now() - created_at).days
          
          # 价值公式：重要性 * 访问频率因子 * 时效因子
          frequency_factor = min(1.0, access_count / 100)
          recency_factor = max(0, 1 - days_old / self.ttl_days)
          
          value = importance * (0.5 + 0.5 * frequency_factor) * (0.3 + 0.7 * recency_factor)
          return value
      
      def cleanup(self, agent_id: str, dry_run: bool = False) -> dict:
          """清理低价值记忆"""
          memories = self.storage.get_by_agent(agent_id)
          
          deleted = []
          archived = []
          preserved = []
          
          for memory in memories:
              value = self.evaluate_memory_value(memory)
              
              if value < self.importance_threshold:
                  if dry_run:
                      deleted.append(memory["id"])
                  else:
                      self.storage.delete(memory["id"])
                      deleted.append(memory["id"])
              elif memory.get("days_old", 0) > self.ttl_days:
                  if dry_run:
                      archived.append(memory["id"])
                  else:
                      self.storage.archive(memory["id"])
                      archived.append(memory["id"])
              else:
                  preserved.append(memory["id"])
          
          return {
              "agent_id": agent_id,
              "deleted_count": len(deleted),
              "archived_count": len(archived),
              "preserved_count": len(preserved),
              "deleted_ids": deleted,
              "archived_ids": archived
          }
```


## 六、记忆共享能力

```yaml
capability: "MEMORY_SHARING"
name: "记忆共享"
description: "支持记忆在智能体间共享"
priority: "P0"

# 共享类型
sharing_types:
  - name: "peer_to_peer"
    description: "点对点共享"
    use_case: "两个智能体直接共享"
    
  - name: "broadcast"
    description: "广播共享"
    use_case: "向同范围所有智能体广播"
    
  - name: "publish_subscribe"
    description: "发布订阅"
    use_case: "基于兴趣的共享"

# 共享范围
sharing_scopes:
  - name: "global"
    description: "全系统共享"
    write_permission: ["L1", "L2"]
    read_permission: ["L1", "L2", "L3", "L4", "L5", "L6"]
    
  - name: "domain"
    description: "领域内共享"
    write_permission: ["L2", "L3"]
    read_permission: ["L2", "L3", "L4"]
    
  - name: "project"
    description: "项目内共享"
    write_permission: ["L3", "L4"]
    read_permission: ["L3", "L4", "L5"]
    
  - name: "department"
    description: "部门内共享"
    write_permission: ["L4", "L5"]
    read_permission: ["L4", "L5", "L6"]

# 共享接口
sharing_interface:
  class_name: "MemorySharing"
  methods:
    - name: "share_memory"
      description: "共享记忆"
      parameters:
        - name: "memory_id"
          type: "str"
        - name: "source_agent_id"
          type: "str"
        - name: "target_scope"
          type: "str"
        - name: "target_agent_ids"
          type: "List[str]"
      returns: "bool"
      
    - name: "get_shared_memories"
      description: "获取共享记忆"
      parameters:
        - name: "agent_id"
          type: "str"
        - name: "scope_filter"
          type: "List[str]"
      returns: "List[Memory]"
      
    - name: "subscribe_memory_topic"
      description: "订阅记忆主题"
      parameters:
        - name: "agent_id"
          type: "str"
        - name: "topic"
          type: "str"
      returns: "bool"
      
    - name: "publish_memory"
      description: "发布记忆到主题"
      parameters:
        - name: "memory"
          type: "Memory"
        - name: "topic"
          type: "str"
      returns: "bool"

# 权限检查
permission_check:
  class_name: "SharingPermission"
  methods:
    - name: "can_write"
      description: "检查写权限"
      parameters:
        - name: "agent_level"
          type: "str"
        - name: "target_scope"
          type: "str"
      returns: "bool"
      
    - name: "can_read"
      description: "检查读权限"
      parameters:
        - name: "agent_level"
          type: "str"
        - name: "source_scope"
          type: "str"
      returns: "bool"

# 实现代码模板
implementation_code: |
  class MemorySharing:
      """记忆共享管理器"""
      
      def __init__(self, storage: MemoryStorage, permission_checker):
          self.storage = storage
          self.permission_checker = permission_checker
          self.subscribers = {}  # topic -> List[agent_id]
      
      def share_memory(self, memory_id: str, source_agent_id: str, 
                       target_scope: str = None, target_agent_ids: List[str] = None) -> bool:
          """共享记忆"""
          memory = self.storage.get(memory_id)
          source_agent = self.get_agent(source_agent_id)
          
          # 检查源智能体是否有权限共享
          if not self.permission_checker.can_share(source_agent.level, memory):
              return False
          
          # 设置共享范围
          if target_scope:
              memory["shared_scope"] = target_scope
              memory["shared_to"] = []
          elif target_agent_ids:
              memory["shared_to"] = target_agent_ids
          
          return self.storage.update(memory_id, memory)
      
      def get_shared_memories(self, agent_id: str, scope_filter: List[str] = None) -> List[dict]:
          """获取智能体可访问的共享记忆"""
          agent = self.get_agent(agent_id)
          all_memories = self.storage.get_shared_memories()
          
          accessible = []
          for memory in all_memories:
              if self.permission_checker.can_access(agent.level, memory):
                  accessible.append(memory)
          
          return accessible
```


## 七、能力优先级汇总

```yaml
priority_summary:
  P0_required:
    - MEMORY_STORAGE
    - MEMORY_RETRIEVAL
    - MEMORY_SHARING
    
  P1_enhanced:
    - MEMORY_SUMMARIZATION
    - MEMORY_FORGETTING
```


## 八、在Cursor中使用

将本文档保存后，在Cursor中使用以下命令：

```
# 实现记忆存储
@docs/MEMORY_CAPABILITY_SPEC_v1.0.md 实现Chroma向量数据库的记忆存储功能

# 实现混合检索
@docs/MEMORY_CAPABILITY_SPEC_v1.0.md 实现语义搜索+时间衰减的混合检索

# 实现记忆共享
@docs/MEMORY_CAPABILITY_SPEC_v1.0.md 实现基于层级的记忆共享权限控制
```

---

**文档结束**