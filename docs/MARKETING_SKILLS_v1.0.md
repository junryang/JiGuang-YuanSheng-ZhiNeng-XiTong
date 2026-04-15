# 营销部员工专属能力 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\MARKETING_SKILLS_v1.0.md
```


# 营销部员工专属能力 v1.0

## 一、能力总览

```yaml
department: "营销部"
layer: "L5_员工"
description: "营销部员工专属技术能力，用于内容生成、多平台发布、数据分析、SEO优化"

skills:
  total_count: 56
  categories:
    - "内容生成"
    - "多平台发布"
    - "数据分析"
    - "SEO优化"
    - "社交媒体管理"
    - "活动策划"
    - "用户增长"
    - "品牌管理"
    - "舆情监控"
    - "广告投放"
    - "邮件营销"
    - "KOL管理"
    - "营销自动化"
    - "内容策略"
```


## 二、内容生成能力

```yaml
# 内容生成能力集

category: "内容生成"
description: "生成各类营销内容，包括文章、视频脚本、海报文案等"

skills:
  - id: "MK-CONTENT-01"
    name: "文章写作"
    description: "生成技术文章、产品介绍、行业洞察等内容"
    input: "主题、关键词、字数要求"
    output: "文章内容（Markdown格式）"
    implementation: "大模型 + 写作模板"
    examples:
      - "生成一篇关于多智能体系统的技术文章，2000字"
      - "生成产品发布会演讲稿"
    priority: "P0"
    
  - id: "MK-CONTENT-02"
    name: "短视频脚本"
    description: "生成短视频脚本，适配抖音、B站、视频号"
    input: "产品功能、目标人群"
    output: "分镜脚本、台词"
    implementation: "脚本模板 + 大模型"
    examples:
      - "生成30秒产品功能介绍视频脚本"
      - "生成程序员搞笑短剧脚本"
    priority: "P1"
    
  - id: "MK-CONTENT-03"
    name: "海报文案"
    description: "生成海报标题、副标题、宣传语"
    input: "活动主题、卖点"
    output: "多版本文案"
    implementation: "文案模板 + 大模型"
    examples:
      - "生成新品发布海报文案（3个版本）"
      - "生成双11促销海报文案"
    priority: "P1"
    
  - id: "MK-CONTENT-04"
    name: "产品说明书"
    description: "生成产品使用说明、FAQ文档"
    input: "产品功能、操作流程"
    output: "说明书文档"
    implementation: "文档模板 + 大模型"
    examples:
      - "生成智能体配置功能说明书"
      - "生成API接入指南"
    priority: "P1"
    
  - id: "MK-CONTENT-05"
    name: "案例研究"
    description: "生成客户成功案例、使用场景"
    input: "客户信息、使用效果"
    output: "案例文章"
    implementation: "案例模板 + 大模型"
    examples:
      - "生成某企业使用系统的成功案例"
      - "生成典型使用场景分析"
    priority: "P1"
    
  - id: "MK-CONTENT-06"
    name: "行业报告"
    description: "生成行业分析报告、趋势预测"
    input: "行业数据、分析维度"
    output: "报告文档"
    implementation: "数据分析 + 报告模板"
    examples:
      - "生成AI开发工具行业报告"
      - "生成智能体市场趋势分析"
    priority: "P2"
    
  - id: "MK-CONTENT-07"
    name: "多语言内容"
    description: "生成多语言版本的内容"
    input: "源语言内容、目标语言"
    output: "翻译后内容"
    implementation: "翻译API + 人工校对"
    examples:
      - "将中文文章翻译为英文"
      - "生成日语版产品介绍"
    priority: "P1"
    
  - id: "MK-CONTENT-08"
    name: "内容改写"
    description: "改写现有内容，适配不同平台"
    input: "原文、目标平台"
    output: "改写后内容"
    implementation: "大模型 + 风格适配"
    examples:
      - "将技术文章改写为知乎风格"
      - "将长文浓缩为微博短文"
    priority: "P0"
    
  - id: "MK-CONTENT-09"
    name: "标题优化"
    description: "生成多个标题选项并推荐最优"
    input: "文章主题、关键词"
    output: "标题列表（带评分）"
    implementation: "标题生成模型 + 点击率预测"
    examples:
      - "为技术文章生成10个标题"
      - "优化现有标题以提高点击率"
    priority: "P0"
    
  - id: "MK-CONTENT-10"
    name: "关键词提取"
    description: "从内容中提取核心关键词"
    input: "文章内容"
    output: "关键词列表（带权重）"
    implementation: "TF-IDF + 语义分析"
    examples:
      - "提取技术文章的核心关键词"
      - "为视频生成标签"
    priority: "P0"
```


## 三、多平台发布能力

```yaml
# 多平台发布能力集

category: "多平台发布"
description: "发布内容到多个平台，包括国内和海外平台"

skills:
  - id: "MK-PUBLISH-01"
    name: "微信公众号发布"
    description: "发布文章到微信公众号"
    input: "文章内容、封面图、摘要"
    output: "发布结果、文章链接"
    implementation: "微信公众平台API"
    examples:
      - "发布技术文章到公众号"
      - "设置定时发布"
    priority: "P0"
    
  - id: "MK-PUBLISH-02"
    name: "知乎发布"
    description: "发布文章、回答到知乎"
    input: "问题ID、回答内容/文章"
    output: "发布结果、链接"
    implementation: "知乎API"
    examples:
      - "回答知乎上关于多智能体的问题"
      - "发布专栏文章"
    priority: "P0"
    
  - id: "MK-PUBLISH-03"
    name: "掘金发布"
    description: "发布技术文章到掘金"
    input: "文章内容、标签"
    output: "发布结果"
    implementation: "掘金API"
    examples:
      - "发布技术教程到掘金"
      - "参与掘金活动投稿"
    priority: "P0"
    
  - id: "MK-PUBLISH-04"
    name: "B站发布"
    description: "发布视频到B站"
    input: "视频文件、标题、简介、标签"
    output: "发布结果、视频链接"
    implementation: "B站API"
    examples:
      - "发布产品演示视频"
      - "发布技术教程视频"
    priority: "P1"
    
  - id: "MK-PUBLISH-05"
    name: "抖音发布"
    description: "发布短视频到抖音"
    input: "视频文件、文案、话题"
    output: "发布结果"
    implementation: "抖音开放平台API"
    examples:
      - "发布产品功能短视频"
      - "发布活动预告视频"
    priority: "P1"
    
  - id: "MK-PUBLISH-06"
    name: "微博发布"
    description: "发布微博图文"
    input: "文字内容、图片"
    output: "发布结果"
    implementation: "微博API"
    examples:
      - "发布产品更新公告"
      - "发布活动预告"
    priority: "P1"
    
  - id: "MK-PUBLISH-07"
    name: "小红书发布"
    description: "发布笔记到小红书"
    input: "图文内容、标签"
    output: "发布结果"
    implementation: "小红书API"
    examples:
      - "发布产品使用体验笔记"
      - "发布办公效率提升技巧"
    priority: "P1"
    
  - id: "MK-PUBLISH-08"
    name: "CSDN发布"
    description: "发布技术文章到CSDN"
    input: "文章内容、标签"
    output: "发布结果"
    implementation: "CSDN API"
    examples:
      - "发布技术教程到CSDN"
      - "发布开源项目介绍"
    priority: "P1"
    
  - id: "MK-PUBLISH-09"
    name: "海外平台发布"
    description: "发布内容到海外社交媒体"
    input: "内容、平台选择"
    output: "多平台发布结果"
    implementation: "Buffer、Hootsuite API"
    examples:
      - "发布到Twitter、LinkedIn、Facebook"
      - "发布到Reddit技术社区"
    priority: "P2"
    
  - id: "MK-PUBLISH-10"
    name: "批量发布"
    description: "一键发布到多个平台"
    input: "内容、目标平台列表"
    output: "各平台发布结果"
    implementation: "聚合发布工具"
    examples:
      - "一篇文章同时发布到5个技术社区"
      - "批量发布产品更新到所有平台"
    priority: "P0"
    
  - id: "MK-PUBLISH-11"
    name: "定时发布"
    description: "设置内容定时发布"
    input: "发布时间、内容"
    output: "定时任务确认"
    implementation: "定时调度器"
    examples:
      - "设置早上9点发布文章"
      - "设置高峰期定时发布"
    priority: "P0"
    
  - id: "MK-PUBLISH-12"
    name: "平台适配"
    description: "自动适配各平台格式要求"
    input: "原始内容、目标平台"
    output: "适配后内容"
    implementation: "格式转换器"
    examples:
      - "自动将Markdown转换为知乎格式"
      - "自动调整图片尺寸适配各平台"
    priority: "P0"
```


## 四、数据分析能力

```yaml
# 数据分析能力集

category: "数据分析"
description: "分析粉丝增长、互动数据、转化效果"

skills:
  - id: "MK-ANALYTICS-01"
    name: "粉丝增长分析"
    description: "分析各平台粉丝增长趋势"
    input: "时间范围、平台"
    output: "增长报告、图表"
    implementation: "数据聚合 + 趋势分析"
    examples:
      - "生成本周各平台粉丝增长报告"
      - "分析粉丝增长与内容的关联"
    priority: "P0"
    
  - id: "MK-ANALYTICS-02"
    name: "互动数据分析"
    description: "分析点赞、评论、转发数据"
    input: "内容ID、时间范围"
    output: "互动分析报告"
    implementation: "数据统计 + 可视化"
    examples:
      - "分析哪类内容互动率最高"
      - "生成单篇文章互动分析"
    priority: "P0"
    
  - id: "MK-ANALYTICS-03"
    name: "转化分析"
    description: "分析内容到用户的转化效果"
    input: "内容链接、转化目标"
    output: "转化漏斗报告"
    implementation: "埋点数据 + 归因分析"
    examples:
      - "分析文章到产品注册的转化率"
      - "分析活动页面的转化效果"
    priority: "P1"
    
  - id: "MK-ANALYTICS-04"
    name: "竞品分析"
    description: "分析竞品的内容策略"
    input: "竞品账号"
    output: "竞品分析报告"
    implementation: "数据抓取 + 对比分析"
    examples:
      - "分析竞品的内容发布频率"
      - "分析竞品的高互动内容类型"
    priority: "P1"
    
  - id: "MK-ANALYTICS-05"
    name: "用户画像分析"
    description: "分析粉丝的用户画像"
    input: "平台、时间范围"
    output: "用户画像报告"
    implementation: "平台数据 + 聚类分析"
    examples:
      - "分析粉丝的年龄、地域分布"
      - "分析粉丝的技术栈偏好"
    priority: "P1"
    
  - id: "MK-ANALYTICS-06"
    name: "内容效果评估"
    description: "评估单篇内容的效果"
    input: "内容ID"
    output: "效果评分报告"
    implementation: "多维度评分模型"
    examples:
      - "给文章打出综合效果分"
      - "对比多篇内容的效果"
    priority: "P0"
    
  - id: "MK-ANALYTICS-07"
    name: "趋势预测"
    description: "预测粉丝增长和互动趋势"
    input: "历史数据"
    output: "预测报告"
    implementation: "时间序列预测"
    examples:
      - "预测下周粉丝增长量"
      - "预测下月互动趋势"
    priority: "P2"
    
  - id: "MK-ANALYTICS-08"
    name: "数据仪表盘"
    description: "生成营销数据仪表盘"
    input: "数据范围"
    output: "可视化仪表盘"
    implementation: "Grafana + 自定义图表"
    examples:
      - "展示全平台粉丝增长趋势"
      - "展示内容互动排行榜"
    priority: "P0"
```


## 五、SEO优化能力

```yaml
# SEO优化能力集

category: "SEO优化"
description: "优化内容搜索排名，提高自然流量"

skills:
  - id: "MK-SEO-01"
    name: "关键词研究"
    description: "研究搜索量高、竞争度低的关键词"
    input: "行业、主题"
    output: "关键词列表（带搜索量、难度）"
    implementation: "SEO工具API + 数据分析"
    examples:
      - "找出AI开发工具相关的长尾关键词"
      - "分析竞品的关键词策略"
    priority: "P0"
    
  - id: "MK-SEO-02"
    name: "内容优化"
    description: "优化文章的关键词布局"
    input: "文章、目标关键词"
    output: "优化后文章"
    implementation: "SEO规则 + 大模型"
    examples:
      - "在文章中自然插入目标关键词"
      - "优化标题和描述标签"
    priority: "P0"
    
  - id: "MK-SEO-03"
    name: "元标签优化"
    description: "优化网页的title、description、keywords"
    input: "页面内容"
    output: "优化后元标签"
    implementation: "SEO最佳实践"
    examples:
      - "生成SEO友好的标题和描述"
      - "优化图片alt标签"
    priority: "P0"
    
  - id: "MK-SEO-04"
    name: "内链优化"
    description: "优化网站内部链接结构"
    input: "网站结构"
    output: "内链优化方案"
    implementation: "链接分析 + 推荐"
    examples:
      - "在相关文章间添加链接"
      - "优化锚文本分布"
    priority: "P1"
    
  - id: "MK-SEO-05"
    name: "外链建设"
    description: "获取高质量外链"
    input: "目标网站"
    output: "外链建设计划"
    implementation: "外链工具 + 人工 outreach"
    examples:
      - "在技术社区发布带链接的文章"
      - "与行业博客交换链接"
    priority: "P2"
    
  - id: "MK-SEO-06"
    name: "技术SEO"
    description: "优化网站技术架构"
    input: "网站"
    output: "技术优化建议"
    implementation: "SEO检测工具"
    examples:
      - "优化页面加载速度"
      - "配置sitemap和robots.txt"
    priority: "P1"
    
  - id: "MK-SEO-07"
    name: "排名监控"
    description: "监控关键词排名变化"
    input: "关键词列表"
    output: "排名报告"
    implementation: "排名监控工具"
    examples:
      - "监控核心关键词的百度排名"
      - "监控竞品关键词排名变化"
    priority: "P1"
    
  - id: "MK-SEO-08"
    name: "搜索意图分析"
    description: "分析用户搜索背后的真实意图"
    input: "关键词"
    output: "意图分析报告"
    implementation: "SERP分析 + 大模型"
    examples:
      - "分析'智能体开发'关键词的搜索意图"
      - "区分信息型和交易型关键词"
    priority: "P1"
```


## 六、社交媒体管理能力

```yaml
# 社交媒体管理能力集

category: "社交媒体管理"
description: "管理社交媒体账号和内容"

skills:
  - id: "MK-SOCIAL-01"
    name: "账号管理"
    description: "管理多个社交媒体账号"
    input: "账号列表"
    output: "账号状态报告"
    implementation: "社交媒体管理工具"
    examples:
      - "统一管理5个平台的账号"
      - "监控账号健康状态"
    priority: "P0"
    
  - id: "MK-SOCIAL-02"
    name: "内容日历"
    description: "规划内容发布日历"
    input: "内容计划"
    output: "日历视图"
    implementation: "日历工具 + 提醒"
    examples:
      - "规划本月内容发布计划"
      - "设置重要节点提醒"
    priority: "P0"
    
  - id: "MK-SOCIAL-03"
    name: "互动管理"
    description: "管理粉丝评论和私信"
    input: "新消息"
    output: "回复建议、处理状态"
    implementation: "消息聚合 + 自动回复"
    examples:
      - "自动回复常见问题"
      - "标记需要人工处理的消息"
    priority: "P1"
    
  - id: "MK-SOCIAL-04"
    name: "热点追踪"
    description: "追踪行业热点话题"
    input: "行业关键词"
    output: "热点报告"
    implementation: "热点监控工具"
    examples:
      - "追踪AI领域的热点话题"
      - "发现可借势的热点事件"
    priority: "P1"
```


## 七、活动策划能力

```yaml
# 活动策划能力集

category: "活动策划"
description: "策划和执行营销活动"

skills:
  - id: "MK-EVENT-01"
    name: "活动方案生成"
    description: "生成活动策划方案"
    input: "活动目标、预算"
    output: "活动方案文档"
    implementation: "活动模板 + 大模型"
    examples:
      - "生成新品发布活动方案"
      - "生成用户增长活动方案"
    priority: "P1"
    
  - id: "MK-EVENT-02"
    name: "活动物料生成"
    description: "生成活动所需物料"
    input: "活动方案"
    output: "海报、文案、邀请函"
    implementation: "设计模板 + 文案生成"
    examples:
      - "生成活动海报和邀请函"
      - "生成活动宣传文案"
    priority: "P1"
    
  - id: "MK-EVENT-03"
    name: "活动效果评估"
    description: "评估活动效果"
    input: "活动数据"
    output: "效果报告"
    implementation: "数据分析 + 评分模型"
    examples:
      - "评估活动的参与率和转化率"
      - "生成活动复盘报告"
    priority: "P1"
```


## 八、用户增长能力

```yaml
# 用户增长能力集

category: "用户增长"
description: "通过各种手段获取新用户"

skills:
  - id: "MK-GROWTH-01"
    name: "获客渠道分析"
    description: "分析各渠道的获客效果"
    input: "渠道数据"
    output: "渠道分析报告"
    implementation: "归因分析 + ROI计算"
    examples:
      - "分析哪个渠道的获客成本最低"
      - "分析哪个渠道的用户质量最高"
    priority: "P1"
    
  - id: "MK-GROWTH-02"
    name: "裂变活动设计"
    description: "设计用户裂变活动"
    input: "裂变目标"
    output: "裂变方案"
    implementation: "裂变模型 + 活动模板"
    examples:
      - "设计分享有礼活动"
      - "设计邀请返现活动"
    priority: "P2"
    
  - id: "MK-GROWTH-03"
    name: "留存分析"
    description: "分析用户留存情况"
    input: "用户行为数据"
    output: "留存报告"
    implementation: "留存分析模型"
    examples:
      - "分析次日、7日、30日留存"
      - "分析流失用户的特征"
    priority: "P1"
```


## 九、品牌管理能力

```yaml
# 品牌管理能力集

category: "品牌管理"
description: "管理和维护品牌形象"

skills:
  - id: "MK-BRAND-01"
    name: "品牌一致性检查"
    description: "检查内容是否符合品牌规范"
    input: "内容"
    output: "合规性报告"
    implementation: "规则引擎 + 关键词匹配"
    examples:
      - "检查文章是否使用品牌标准术语"
      - "检查设计是否符合品牌色"
    priority: "P1"
    
  - id: "MK-BRAND-02"
    name: "品牌声量分析"
    description: "分析品牌在各平台的声量"
    input: "品牌关键词"
    output: "声量报告"
    implementation: "舆情监控工具"
    examples:
      - "分析品牌在社交媒体被提及次数"
      - "分析品牌声量的变化趋势"
    priority: "P1"
    
  - id: "MK-BRAND-03"
    name: "品牌健康度评估"
    description: "评估品牌的健康度"
    input: "多维度数据"
    output: "健康度评分"
    implementation: "品牌健康模型"
    examples:
      - "评估品牌的知名度、好感度"
      - "生成品牌健康度仪表盘"
    priority: "P2"
```


## 十、舆情监控能力

```yaml
# 舆情监控能力集

category: "舆情监控"
description: "监控和分析网络舆情"

skills:
  - id: "MK-SENTIMENT-01"
    name: "情感分析"
    description: "分析内容的情感倾向"
    input: "文本内容"
    output: "情感标签（正向/负向/中性）"
    implementation: "情感分析模型"
    examples:
      - "分析用户评论的情感倾向"
      - "监控品牌舆情的情感变化"
    priority: "P0"
    
  - id: "MK-SENTIMENT-02"
    name: "舆情预警"
    description: "检测负面舆情并预警"
    input: "监控关键词"
    output: "预警通知"
    implementation: "关键词监控 + 阈值触发"
    examples:
      - "检测到负面评论时自动预警"
      - "检测到竞品负面时通知"
    priority: "P1"
    
  - id: "MK-SENTIMENT-03"
    name: "危机公关"
    description: "生成危机公关回应建议"
    input: "危机事件描述"
    output: "回应方案"
    implementation: "公关模板 + 大模型"
    examples:
      - "生成产品故障的公关声明"
      - "生成负面舆情的回应话术"
    priority: "P2"
```


## 十一、广告投放能力

```yaml
# 广告投放能力集

category: "广告投放"
description: "管理和优化广告投放"

skills:
  - id: "MK-ADS-01"
    name: "广告文案生成"
    description: "生成广告文案"
    input: "产品信息、目标人群"
    output: "多版本广告文案"
    implementation: "文案模板 + 大模型"
    examples:
      - "生成百度搜索广告文案"
      - "生成信息流广告文案"
    priority: "P1"
    
  - id: "MK-ADS-02"
    name: "投放效果分析"
    description: "分析广告投放效果"
    input: "广告数据"
    output: "效果报告"
    implementation: "数据统计 + ROI计算"
    examples:
      - "分析各广告位的ROI"
      - "分析不同创意的点击率"
    priority: "P1"
    
  - id: "MK-ADS-03"
    name: "投放优化建议"
    description: "提供广告投放优化建议"
    input: "投放数据"
    output: "优化方案"
    implementation: "优化算法 + 最佳实践"
    examples:
      - "建议调整出价策略"
      - "建议暂停低效广告"
    priority: "P2"
```


## 十二、邮件营销能力

```yaml
# 邮件营销能力集

category: "邮件营销"
description: "设计和执行邮件营销活动"

skills:
  - id: "MK-EMAIL-01"
    name: "邮件模板生成"
    description: "生成营销邮件模板"
    input: "邮件类型、内容"
    output: "HTML邮件模板"
    implementation: "模板引擎 + 响应式设计"
    examples:
      - "生成产品更新通知邮件"
      - "生成用户欢迎邮件"
    priority: "P1"
    
  - id: "MK-EMAIL-02"
    name: "邮件列表管理"
    description: "管理订阅用户列表"
    input: "用户数据"
    output: "分组列表"
    implementation: "CRM集成 + 标签系统"
    examples:
      - "按用户兴趣分组"
      - "管理退订用户"
    priority: "P1"
    
  - id: "MK-EMAIL-03"
    name: "邮件效果分析"
    description: "分析邮件的打开率和点击率"
    input: "邮件发送数据"
    output: "效果报告"
    implementation: "埋点 + 数据分析"
    examples:
      - "分析不同标题的打开率"
      - "分析最佳发送时间"
    priority: "P1"
```


## 十三、KOL管理能力

```yaml
# KOL管理能力集

category: "KOL管理"
description: "管理和合作KOL"

skills:
  - id: "MK-KOL-01"
    name: "KOL发现"
    description: "发现行业相关KOL"
    input: "行业、领域"
    output: "KOL列表（带粉丝数、互动率）"
    implementation: "KOL数据库 + 爬虫"
    examples:
      - "发现AI技术领域的KOL"
      - "发现程序员社区的意见领袖"
    priority: "P2"
    
  - id: "MK-KOL-02"
    name: "KOL匹配"
    description: "匹配适合产品推广的KOL"
    input: "产品、目标人群"
    output: "推荐KOL列表"
    implementation: "匹配算法 + 评分"
    examples:
      - "匹配适合推广开发工具的KOL"
      - "匹配适合推广企业服务的KOL"
    priority: "P2"
    
  - id: "MK-KOL-03"
    name: "合作效果评估"
    description: "评估KOL合作效果"
    input: "合作数据"
    output: "效果报告"
    implementation: "ROI分析 + 归因"
    examples:
      - "评估KOL带来的转化"
      - "分析KOL的投入产出比"
    priority: "P2"
```


## 十四、营销自动化能力

```yaml
# 营销自动化能力集

category: "营销自动化"
description: "自动化营销流程"

skills:
  - id: "MK-AUTO-01"
    name: "触发式营销"
    description: "设置用户行为触发的营销"
    input: "触发条件、营销内容"
    output: "自动化流程"
    implementation: "规则引擎 + 工作流"
    examples:
      - "用户注册后自动发送欢迎邮件"
      - "用户7天未登录时发送召回推送"
    priority: "P1"
    
  - id: "MK-AUTO-02"
    name: "个性化推荐"
    description: "根据用户偏好推荐内容"
    input: "用户画像"
    output: "推荐内容"
    implementation: "协同过滤 + 内容推荐"
    examples:
      - "推荐用户可能感兴趣的文章"
      - "推荐相关产品功能"
    priority: "P2"
    
  - id: "MK-AUTO-03"
    name: "A/B测试"
    description: "对营销内容进行A/B测试"
    input: "多版本内容"
    output: "测试结果"
    implementation: "分流 + 统计分析"
    examples:
      - "测试两个版本的邮件标题"
      - "测试不同风格的广告文案"
    priority: "P1"
```


## 十五、内容策略能力

```yaml
# 内容策略能力集

category: "内容策略"
description: "制定内容发布策略"

skills:
  - id: "MK-STRATEGY-01"
    name: "选题规划"
    description: "规划内容选题"
    input: "行业趋势、用户需求"
    output: "选题列表"
    implementation: "热点分析 + 用户调研"
    examples:
      - "规划本月技术文章选题"
      - "规划视频内容系列"
    priority: "P1"
    
  - id: "MK-STRATEGY-02"
    name: "发布频率建议"
    description: "建议各平台最佳发布频率"
    input: "平台数据"
    output: "频率建议"
    implementation: "数据分析 + 最佳实践"
    examples:
      - "建议公众号每周发布3次"
      - "建议抖音每天发布2条"
    priority: "P1"
    
  - id: "MK-STRATEGY-03"
    name: "内容矩阵规划"
    description: "规划不同类型内容的组合"
    input: "目标人群"
    output: "内容矩阵"
    implementation: "用户旅程 + 内容类型"
    examples:
      - "规划认知-兴趣-转化-忠诚的内容矩阵"
      - "规划干货-案例-活动的内容组合"
    priority: "P2"
```


## 十六、能力优先级汇总

```yaml
# 按优先级排序

P0_skills:  # 必须实现（16项）
  # 内容生成
  - MK-CONTENT-01: "文章写作"
  - MK-CONTENT-08: "内容改写"
  - MK-CONTENT-09: "标题优化"
  - MK-CONTENT-10: "关键词提取"
  
  # 多平台发布
  - MK-PUBLISH-01: "微信公众号发布"
  - MK-PUBLISH-02: "知乎发布"
  - MK-PUBLISH-03: "掘金发布"
  - MK-PUBLISH-10: "批量发布"
  - MK-PUBLISH-11: "定时发布"
  - MK-PUBLISH-12: "平台适配"
  
  # 数据分析
  - MK-ANALYTICS-01: "粉丝增长分析"
  - MK-ANALYTICS-02: "互动数据分析"
  - MK-ANALYTICS-06: "内容效果评估"
  - MK-ANALYTICS-08: "数据仪表盘"
  
  # SEO优化
  - MK-SEO-01: "关键词研究"
  - MK-SEO-02: "内容优化"
  - MK-SEO-03: "元标签优化"
  
  # 社交媒体管理
  - MK-SOCIAL-01: "账号管理"
  - MK-SOCIAL-02: "内容日历"
  
  # 舆情监控
  - MK-SENTIMENT-01: "情感分析"

P1_skills:  # 近期实现（25项）
  - MK-CONTENT-02: "短视频脚本"
  - MK-CONTENT-03: "海报文案"
  - MK-CONTENT-04: "产品说明书"
  - MK-CONTENT-05: "案例研究"
  - MK-CONTENT-07: "多语言内容"
  - MK-PUBLISH-04: "B站发布"
  - MK-PUBLISH-05: "抖音发布"
  - MK-PUBLISH-06: "微博发布"
  - MK-PUBLISH-07: "小红书发布"
  - MK-PUBLISH-08: "CSDN发布"
  - MK-ANALYTICS-03: "转化分析"
  - MK-ANALYTICS-04: "竞品分析"
  - MK-ANALYTICS-05: "用户画像分析"
  - MK-SEO-04: "内链优化"
  - MK-SEO-06: "技术SEO"
  - MK-SEO-07: "排名监控"
  - MK-SEO-08: "搜索意图分析"
  - MK-SOCIAL-03: "互动管理"
  - MK-SOCIAL-04: "热点追踪"
  - MK-EVENT-01: "活动方案生成"
  - MK-EVENT-02: "活动物料生成"
  - MK-EVENT-03: "活动效果评估"
  - MK-GROWTH-01: "获客渠道分析"
  - MK-GROWTH-03: "留存分析"
  - MK-BRAND-01: "品牌一致性检查"
  - MK-BRAND-02: "品牌声量分析"
  - MK-SENTIMENT-02: "舆情预警"
  - MK-ADS-01: "广告文案生成"
  - MK-ADS-02: "投放效果分析"
  - MK-EMAIL-01: "邮件模板生成"
  - MK-EMAIL-02: "邮件列表管理"
  - MK-EMAIL-03: "邮件效果分析"
  - MK-AUTO-01: "触发式营销"
  - MK-AUTO-03: "A/B测试"
  - MK-STRATEGY-01: "选题规划"
  - MK-STRATEGY-02: "发布频率建议"

P2_skills:  # 远期规划（15项）
  - MK-CONTENT-06: "行业报告"
  - MK-PUBLISH-09: "海外平台发布"
  - MK-ANALYTICS-07: "趋势预测"
  - MK-SEO-05: "外链建设"
  - MK-GROWTH-02: "裂变活动设计"
  - MK-BRAND-03: "品牌健康度评估"
  - MK-SENTIMENT-03: "危机公关"
  - MK-ADS-03: "投放优化建议"
  - MK-KOL-01: "KOL发现"
  - MK-KOL-02: "KOL匹配"
  - MK-KOL-03: "合作效果评估"
  - MK-AUTO-02: "个性化推荐"
  - MK-STRATEGY-03: "内容矩阵规划"
```


## 十七、在Cursor中使用

将本文档保存后，在Cursor中使用以下命令：

```
# 查看营销部所有能力
@docs/MARKETING_SKILLS_v1.0.md 列出营销部所有P0级能力

# 实现特定能力
@docs/MARKETING_SKILLS_v1.0.md 实现MK-CONTENT-01文章写作能力

# 创建带技能的营销专员
@docs/MARKETING_SKILLS_v1.0.md 根据P0能力创建资深内容运营智能体

# 实现内容生成能力集
@docs/MARKETING_SKILLS_v1.0.md 实现category 内容生成下的所有能力

# 实现多平台发布系统
@docs/MARKETING_SKILLS_v1.0.md 根据MK-PUBLISH-01到MK-PUBLISH-12实现多平台发布系统
```

---

**文档结束**