# 兼容性需求规范 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\COMPATIBILITY_REQUIREMENTS_v1.0.md
```


# 兼容性需求规范 v1.0

## 一、概述

```yaml
module: "兼容性需求"
description: "定义系统的浏览器和分辨率兼容性要求"
priority: "P0"
domain: "非功能需求"

# 关联的通用能力
related_abilities:
  - "PC-01: 自然语言理解"
  - "PC-02: 代码理解"
  - "PC-06: 网页理解"
  - "WEB-01: 浏览器自动化"
  - "WEB-03: 网页内容解析与提取"
  - "EX-03: API调用"
  - "EX-05: 文件操作"
  - "MT-01: 自我监控"
  - "MT-05: 能力扩展"
  - "PO-01: 响应时间优化"
  - "PO-02: 吞吐量优化"

compatibility_requirements:
  total_count: 2
  categories:
    - "浏览器兼容性"
    - "分辨率兼容性"
```


## 二、兼容性需求详细设计

### 2.1 浏览器兼容性

```yaml
# 浏览器兼容性要求
requirement_id: "COMPAT-01"
name: "浏览器兼容性"
description: "系统必须在主流浏览器的最新版本上正常运行"
priority: "P0"
related_abilities: ["WEB-01", "WEB-03", "PC-06"]

# 支持浏览器列表
browsers:
  - name: "Chrome"
    min_version: 120
    current_version: 124
    market_share: "65%"
    test_priority: "P0"
    features:
      - "现代CSS (Grid, Flexbox)"
      - "ES2020+"
      - "WebSocket"
      - "Web Workers"
      - "Intersection Observer"
      - "Resize Observer"
      
  - name: "Firefox"
    min_version: 115
    current_version: 124
    market_share: "15%"
    test_priority: "P0"
    features:
      - "现代CSS"
      - "ES2020+"
      - "WebSocket"
      - "Web Workers"
      
  - name: "Edge"
    min_version: 120
    current_version: 124
    market_share: "10%"
    test_priority: "P0"
    features:
      - "Chromium内核，与Chrome兼容"
      
  - name: "Safari"
    min_version: 16
    current_version: 17
    market_share: "8%"
    test_priority: "P1"
    features:
      - "现代CSS (部分特性需前缀)"
      - "ES2020+ (部分特性受限)"
    notes: "需特别测试WebSocket和Service Worker"

# 浏览器测试矩阵
test_matrix:
  - browser: "Chrome"
    versions: [120, 121, 122, 123, 124]
    os: ["Windows", "macOS", "Linux"]
    
  - browser: "Firefox"
    versions: [115, 116, 117, 118, 119, 120, 121, 122, 123, 124]
    os: ["Windows", "macOS", "Linux"]
    
  - browser: "Edge"
    versions: [120, 121, 122, 123, 124]
    os: ["Windows", "macOS"]
    
  - browser: "Safari"
    versions: [16, 17]
    os: ["macOS", "iOS"]

# 兼容性处理策略
compatibility_strategies:
  css_prefixing:
    tool: "Autoprefixer"
    browsers: ["last 2 versions", "> 1%"]
    
  javascript_transpilation:
    tool: "Babel"
    targets: "defaults"
    
  polyfills:
    - feature: "Promise"
      fallback: "core-js/promise"
    - feature: "fetch"
      fallback: "whatwg-fetch"
    - feature: "IntersectionObserver"
      fallback: "intersection-observer"
    - feature: "ResizeObserver"
      fallback: "resize-observer-polyfill"
    - feature: "WebSocket"
      fallback: "sockjs-client"
      
  feature_detection:
    method: "Modernizr"
    tests:
      - "flexbox"
      - "grid"
      - "websockets"
      - "webworkers"

# 实现示例
class BrowserCompatibilityChecker:
    """浏览器兼容性检查器 - 对齐PC-06网页理解、WEB-01浏览器自动化"""
    
    def __init__(self):
        self.browser_detector = BrowserDetector()  # 对齐PC-06
        self.feature_tester = FeatureTester()
    
    async def check_browser(self, user_agent: str) -> CompatibilityResult:
        """检查浏览器兼容性"""
        browser_info = await self.browser_detector.parse(user_agent)
        
        # 检查版本是否满足要求
        is_compatible = self._is_version_compatible(
            browser_info.name, 
            browser_info.version
        )
        
        if not is_compatible:
            return CompatibilityResult(
                compatible=False,
                browser=browser_info.name,
                current_version=browser_info.version,
                required_version=self._get_min_version(browser_info.name),
                upgrade_url=self._get_upgrade_url(browser_info.name),
                message=f"您的{browser_info.name}版本过低，请升级到最新版本"
            )
        
        # 检查关键特性支持
        features = await self.feature_tester.test_all()
        unsupported = [f for f in features if not f.supported]
        
        if unsupported:
            return CompatibilityResult(
                compatible=False,
                browser=browser_info.name,
                version=browser_info.version,
                unsupported_features=unsupported,
                message=f"您的浏览器不支持以下特性: {', '.join(unsupported)}"
            )
        
        return CompatibilityResult(
            compatible=True,
            browser=browser_info.name,
            version=browser_info.version
        )

# 前端兼容性配置
frontend_config:
  browserslist:
    production:
      - "> 0.5%"
      - "last 2 versions"
      - "Firefox ESR"
      - "not dead"
    development:
      - "last 1 version"
      
  build_config:
    target: "es2020"
    module: "esnext"
    polyfills: "usage"
    
  css_config:
    minify: true
    sourcemap: true
    modules: true
```

### 2.2 分辨率兼容性

```yaml
# 分辨率兼容性要求
requirement_id: "COMPAT-02"
name: "分辨率兼容性"
description: "系统必须在1920x1080及以上分辨率下正常显示和使用"
priority: "P0"
related_abilities: ["PC-06", "PO-01", "PO-02"]

# 支持分辨率列表
resolutions:
  - width: 3840
    height: 2160
    name: "4K"
    aspect_ratio: "16:9"
    test_priority: "P1"
    layout: "完整"
    
  - width: 2560
    height: 1440
    name: "2K"
    aspect_ratio: "16:9"
    test_priority: "P1"
    layout: "完整"
    
  - width: 1920
    height: 1080
    name: "Full HD"
    aspect_ratio: "16:9"
    test_priority: "P0"
    layout: "完整"
    
  - width: 1680
    height: 1050
    name: "WSXGA+"
    aspect_ratio: "16:10"
    test_priority: "P1"
    layout: "完整"
    
  - width: 1600
    height: 900
    name: "HD+"
    aspect_ratio: "16:9"
    test_priority: "P1"
    layout: "完整"
    
  - width: 1440
    height: 900
    name: "WXGA+"
    aspect_ratio: "16:10"
    test_priority: "P2"
    layout: "紧凑"

# 响应式断点
breakpoints:
  - name: "超大屏"
    min_width: 1920
    max_width: null
    columns: 24
    container_width: "1440px"
    
  - name: "大屏"
    min_width: 1440
    max_width: 1919
    columns: 24
    container_width: "1200px"
    
  - name: "中屏"
    min_width: 1024
    max_width: 1439
    columns: 12
    container_width: "100%"
    
  - name: "小屏"
    min_width: 768
    max_width: 1023
    columns: 12
    container_width: "100%"
    
  - name: "移动端"
    min_width: null
    max_width: 767
    columns: 4
    container_width: "100%"
    layout: "移动适配"

# 布局适配策略
layout_adaptation:
  # 侧边栏
  sidebar:
    1920px以上: "展开"
    1440px-1919px: "可折叠"
    1024px-1439px: "折叠为图标"
    768px-1023px: "隐藏（汉堡菜单）"
    
  # 内容区域
  content_area:
    1920px以上: "多列布局"
    1440px-1919px: "双列布局"
    1024px-1439px: "单列布局"
    
  # 字体大小
  font_sizes:
    1920px以上: "16px"
    1440px-1919px: "15px"
    1024px-1439px: "14px"
    
  # 表格
  tables:
    1920px以上: "完整显示"
    1440px-1919px: "横向滚动"
    1024px以下: "卡片视图"

# 实现示例
class ResponsiveLayout:
    """响应式布局管理器 - 对齐PC-06网页理解"""
    
    def __init__(self):
        self.breakpoints = BREAKPOINTS
        self.current_breakpoint = None
    
    async def get_layout_config(self, screen_width: int) -> LayoutConfig:
        """根据屏幕宽度获取布局配置"""
        breakpoint = self._get_breakpoint(screen_width)
        
        return LayoutConfig(
            breakpoint=breakpoint.name,
            columns=breakpoint.columns,
            sidebar_visible=self._is_sidebar_visible(breakpoint),
            sidebar_collapsed=self._is_sidebar_collapsed(breakpoint),
            font_size=self._get_font_size(breakpoint),
            container_width=breakpoint.container_width
        )
    
    def _get_breakpoint(self, width: int) -> Breakpoint:
        """获取匹配的断点"""
        for bp in self.breakpoints:
            if bp.min_width <= width < bp.max_width:
                return bp
        return self.breakpoints[0]  # 默认超大屏

# 响应式CSS示例
responsive_css: |
  /* 超大屏 (≥1920px) */
  @media (min-width: 1920px) {
    .container { max-width: 1440px; }
    .sidebar { width: 280px; }
    .main-content { margin-left: 280px; }
  }
  
  /* 大屏 (1440px - 1919px) */
  @media (min-width: 1440px) and (max-width: 1919px) {
    .container { max-width: 1200px; }
    .sidebar { width: 260px; }
    .main-content { margin-left: 260px; }
  }
  
  /* 中屏 (1024px - 1439px) */
  @media (min-width: 1024px) and (max-width: 1439px) {
    .container { width: 100%; padding: 0 20px; }
    .sidebar { width: 240px; }
    .main-content { margin-left: 240px; }
  }
  
  /* 小屏 (768px - 1023px) */
  @media (min-width: 768px) and (max-width: 1023px) {
    .sidebar { 
      position: fixed;
      left: -260px;
      transition: left 0.3s;
    }
    .sidebar.open { left: 0; }
    .main-content { margin-left: 0; }
  }
  
  /* 移动端 (<768px) */
  @media (max-width: 767px) {
    .sidebar { display: none; }
    .main-content { margin-left: 0; }
    .table-container { overflow-x: auto; }
  }
```


## 三、兼容性测试配置

```yaml
# 兼容性测试配置
compatibility_testing:
  # 自动化测试工具
  automation_tools:
    - name: "Selenium"
      version: "4.15"
     用途: "跨浏览器自动化测试"
      
    - name: "Playwright"
      version: "1.40"
     用途: "多浏览器E2E测试"
      
    - name: "BrowserStack"
      用途: "云端浏览器测试"
      
  # 测试场景
  test_scenarios:
    - name: "登录流程"
      browsers: ["Chrome", "Firefox", "Edge", "Safari"]
      resolutions: [1920, 1440, 1024]
      
    - name: "智能体管理"
      browsers: ["Chrome", "Firefox", "Edge"]
      resolutions: [1920, 1440]
      
    - name: "对话功能"
      browsers: ["Chrome", "Edge", "Safari"]
      resolutions: [1920, 1440, 1024]
      
    - name: "代码生成"
      browsers: ["Chrome", "Firefox"]
      resolutions: [1920, 1440]

# 兼容性测试用例
test_cases:
  - id: "CT-01"
    name: "Chrome兼容性测试"
    description: "验证Chrome最新版本所有功能正常"
    browsers: ["Chrome 124"]
    pass_criteria: "所有核心功能通过"
    
  - id: "CT-02"
    name: "Firefox兼容性测试"
    description: "验证Firefox最新版本所有功能正常"
    browsers: ["Firefox 124"]
    pass_criteria: "所有核心功能通过"
    
  - id: "CT-03"
    name: "Edge兼容性测试"
    description: "验证Edge最新版本所有功能正常"
    browsers: ["Edge 124"]
    pass_criteria: "所有核心功能通过"
    
  - id: "CT-04"
    name: "分辨率适配测试"
    description: "验证各分辨率下UI显示正常"
    resolutions: [3840, 2560, 1920, 1680, 1600, 1440]
    pass_criteria: "UI无错位、无溢出"
    
  - id: "CT-05"
    name: "响应式布局测试"
    description: "验证窗口缩放时布局自适应"
    test_steps:
      - "从1920px逐步缩小到320px"
    pass_criteria: "布局平滑过渡，无断裂"
```


## 四、兼容性监控配置

```yaml
# 兼容性监控
compatibility_monitoring:
  # 真实用户监控
  rum:
    enabled: true
    tool: "Sentry"
    metrics:
      - "浏览器分布"
      - "分辨率分布"
      - "JS错误率"
      - "首屏时间"
      
  # 错误追踪
  error_tracking:
    enabled: true
    tool: "Sentry"
    grouping:
      - "by_browser"
      - "by_version"
      - "by_os"
      
  # 性能监控
  performance_monitoring:
    enabled: true
    metrics:
      - name: "fcp_by_browser"
        description: "各浏览器首次内容绘制"
      - name: "lcp_by_browser"
        description: "各浏览器最大内容绘制"
      - name: "tti_by_browser"
        description: "各浏览器可交互时间"
```


## 五、通用能力映射表

```yaml
# 兼容性需求与通用能力映射
general_ability_mapping:
  PC-06_网页理解:
    mapped_requirements: ["COMPAT-01", "COMPAT-02"]
    description: "理解不同浏览器和分辨率下的网页渲染"
    
  WEB-01_浏览器自动化:
    mapped_requirements: ["COMPAT-01"]
    description: "自动化跨浏览器测试"
    
  WEB-03_网页内容解析与提取:
    mapped_requirements: ["COMPAT-01"]
    description: "解析不同浏览器下的网页结构"
    
  PO-01_响应时间优化:
    mapped_requirements: ["COMPAT-02"]
    description: "优化响应式布局性能"
    
  PO-02_吞吐量优化:
    mapped_requirements: ["COMPAT-02"]
    description: "优化不同分辨率下的渲染吞吐量"
    
  MT-01_自我监控:
    mapped_requirements: ["COMPAT-01", "COMPAT-02"]
    description: "监控浏览器兼容性错误"
    
  EX-03_API调用:
    mapped_requirements: ["COMPAT-01"]
    description: "跨浏览器API调用兼容"
```


## 六、在Cursor中使用

```bash
# 1. 实现浏览器兼容性检查
@docs/COMPATIBILITY_REQUIREMENTS_v1.0.md 实现COMPAT-01浏览器兼容性检查，支持Chrome/Firefox/Edge/Safari

# 2. 实现响应式布局
@docs/COMPATIBILITY_REQUIREMENTS_v1.0.md 实现COMPAT-02响应式布局，支持1920x1080及以上分辨率

# 3. 配置浏览器测试
@docs/COMPATIBILITY_REQUIREMENTS_v1.0.md 根据测试矩阵配置Playwright跨浏览器测试

# 4. 配置响应式断点
@docs/COMPATIBILITY_REQUIREMENTS_v1.0.md 根据断点配置实现响应式CSS

# 5. 配置兼容性监控
@docs/COMPATIBILITY_REQUIREMENTS_v1.0.md 配置Sentry监控浏览器兼容性错误
```


## 七、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，2项兼容性需求，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md |

---

**文档结束**