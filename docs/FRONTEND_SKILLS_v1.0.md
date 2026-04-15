# 前端部员工专属能力 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\FRONTEND_SKILLS_v1.0.md
```


# 前端部员工专属能力 v1.0

## 一、能力总览

```yaml
department: "前端部"
layer: "L5_员工"
description: "前端部员工专属技术能力，用于组件开发、状态管理、响应式设计、性能优化"

skills:
  total_count: 32
  categories:
    - "组件开发"
    - "状态管理"
    - "响应式设计"
    - "性能优化"
    - "路由管理"
    - "UI组件库"
    - "构建工具"
    - "测试与调试"
    - "动画与交互"
    - "国际化"
    - "SEO优化"
    - "安全防护"
    - "文档与规范"
```


## 二、组件开发能力

```yaml
# 组件开发能力集

category: "组件开发"
description: "开发Vue/React组件，包括设计、实现、复用、测试"

skills:
  - id: "FE-COMP-01"
    name: "Vue组件开发"
    description: "开发Vue 3组件，使用Composition API"
    input: "UI设计、业务需求"
    output: "Vue组件代码"
    implementation: "Vue 3 + TypeScript"
    examples:
      - "开发数据表格组件，支持排序、筛选、分页"
      - "开发模态框组件，支持拖拽和自定义内容"
    priority: "P0"
    
  - id: "FE-COMP-02"
    name: "React组件开发"
    description: "开发React组件，使用Hooks"
    input: "UI设计、业务需求"
    output: "React组件代码"
    implementation: "React 18 + TypeScript"
    examples:
      - "开发表单组件，支持验证和提交"
      - "开发无限滚动列表组件"
    priority: "P0"
    
  - id: "FE-COMP-03"
    name: "组件通信"
    description: "实现组件间通信（Props、事件、Provide/Inject、Context）"
    input: "组件层级关系"
    output: "通信实现代码"
    implementation: "Props/Events/Provide/Context"
    examples:
      - "父子组件通过Props和事件通信"
      - "跨层级组件使用Provide/Inject"
    priority: "P0"
    
  - id: "FE-COMP-04"
    name: "组件复用"
    description: "设计可复用的高阶组件/组合式函数"
    input: "重复逻辑"
    output: "复用代码"
    implementation: "HOC、Render Props、Composables"
    examples:
      - "封装数据请求的Composable"
      - "开发权限控制的高阶组件"
    priority: "P0"
    
  - id: "FE-COMP-05"
    name: "组件库开发"
    description: "开发企业内部组件库"
    input: "设计规范"
    output: "组件库代码"
    implementation: "Vite + TypeScript"
    examples:
      - "开发Button、Input、Modal等基础组件"
      - "组件库的按需加载配置"
    priority: "P1"
    
  - id: "FE-COMP-06"
    name: "Web Components"
    description: "开发原生Web Components"
    input: "跨框架复用需求"
    output: "Web Component"
    implementation: "Custom Elements + Shadow DOM"
    examples:
      - "开发跨框架的日期选择器"
      - "封装第三方SDK为Web Component"
    priority: "P2"
    
  - id: "FE-COMP-07"
    name: "虚拟滚动"
    description: "实现大数据量列表的虚拟滚动"
    input: "长列表数据"
    output: "虚拟滚动组件"
    implementation: "react-window、vue-virtual-scroller"
    examples:
      - "实现10万条数据的表格渲染"
      - "实现聊天记录的无限滚动"
    priority: "P1"
    
  - id: "FE-COMP-08"
    name: "动态组件"
    description: "实现动态组件加载和渲染"
    input: "组件映射配置"
    output: "动态加载代码"
    implementation: "defineAsyncComponent、React.lazy"
    examples:
      - "根据配置动态渲染表单组件"
      - "实现可视化拖拽的组件渲染"
    priority: "P1"
```


## 三、状态管理能力

```yaml
# 状态管理能力集

category: "状态管理"
description: "配置Pinia/Vuex/Redux，管理应用状态"

skills:
  - id: "FE-STATE-01"
    name: "Pinia配置"
    description: "配置和管理Pinia状态"
    input: "应用状态需求"
    output: "Pinia Store代码"
    implementation: "Pinia + TypeScript"
    examples:
      - "配置用户认证Store"
      - "配置购物车Store"
    priority: "P0"
    
  - id: "FE-STATE-02"
    name: "Vuex配置"
    description: "配置和管理Vuex状态"
    input: "应用状态需求"
    output: "Vuex Store代码"
    implementation: "Vuex 4 + TypeScript"
    examples:
      - "配置模块化的Vuex Store"
      - "配置持久化插件"
    priority: "P1"
    
  - id: "FE-STATE-03"
    name: "Redux配置"
    description: "配置和管理Redux状态"
    input: "应用状态需求"
    output: "Redux Store代码"
    implementation: "Redux Toolkit + TypeScript"
    examples:
      - "配置Slice和Reducer"
      - "配置Redux Thunk处理异步"
    priority: "P0"
    
  - id: "FE-STATE-04"
    name: "Zustand配置"
    description: "配置和管理Zustand状态"
    input: "轻量级状态需求"
    output: "Zustand Store代码"
    implementation: "Zustand"
    examples:
      - "配置主题切换Store"
      - "配置通知管理Store"
    priority: "P1"
    
  - id: "FE-STATE-05"
    name: "状态持久化"
    description: "实现状态的本地持久化"
    input: "需要持久化的状态"
    output: "持久化配置"
    implementation: "localStorage、IndexedDB"
    examples:
      - "持久化用户登录状态"
      - "持久化用户偏好设置"
    priority: "P0"
    
  - id: "FE-STATE-06"
    name: "跨组件状态共享"
    description: "实现跨层级组件的状态共享"
    input: "共享状态需求"
    output: "状态共享方案"
    implementation: "Context、Provide/Inject"
    examples:
      - "全局主题色共享"
      - "全局用户信息共享"
    priority: "P0"
```


## 四、响应式设计能力

```yaml
# 响应式设计能力集

category: "响应式设计"
description: "适配多端屏幕，实现响应式布局"

skills:
  - id: "FE-RESP-01"
    name: "Flexbox布局"
    description: "使用Flexbox实现弹性布局"
    input: "设计稿"
    output: "Flexbox CSS"
    implementation: "CSS Flexbox"
    examples:
      - "实现导航栏的等宽分布"
      - "实现垂直居中的卡片内容"
    priority: "P0"
    
  - id: "FE-RESP-02"
    name: "Grid布局"
    description: "使用CSS Grid实现网格布局"
    input: "设计稿"
    output: "Grid CSS"
    implementation: "CSS Grid"
    examples:
      - "实现相册网格布局"
      - "实现仪表盘卡片布局"
    priority: "P0"
    
  - id: "FE-RESP-03"
    name: "媒体查询"
    description: "使用媒体查询适配不同屏幕尺寸"
    input: "断点设计"
    output: "响应式CSS"
    implementation: "@media queries"
    examples:
      - "移动端单列布局，桌面端多列布局"
      - "根据屏幕宽度隐藏/显示元素"
    priority: "P0"
    
  - id: "FE-RESP-04"
    name: "移动端适配"
    description: "实现移动端H5页面适配"
    input: "移动端设计稿"
    output: "移动端CSS"
    implementation: "viewport、rem、vw/vh"
    examples:
      - "使用rem实现移动端适配"
      - "配置viewport确保正确缩放"
    priority: "P0"
    
  - id: "FE-RESP-05"
    name: "响应式图片"
    description: "实现响应式图片加载"
    input: "不同尺寸图片"
    output: "响应式图片代码"
    implementation: "srcset、picture、loading"
    examples:
      - "根据设备宽度加载不同尺寸图片"
      - "实现图片懒加载"
    priority: "P1"
    
  - id: "FE-RESP-06"
    name: "暗色主题"
    description: "实现暗色/亮色主题切换"
    input: "主题配色"
    output: "主题切换代码"
    implementation: "CSS变量、prefers-color-scheme"
    examples:
      - "根据系统偏好自动切换主题"
      - "提供手动切换主题按钮"
    priority: "P1"
    
  - id: "FE-RESP-07"
    name: "多端适配"
    description: "适配PC、平板、手机多种设备"
    input: "多端设计稿"
    output: "多端适配CSS"
    implementation: "响应式框架、设备检测"
    examples:
      - "PC端显示完整侧边栏，移动端收起为汉堡菜单"
      - "平板端双列布局"
    priority: "P0"
```


## 五、性能优化能力

```yaml
# 性能优化能力集

category: "性能优化"
description: "首屏加载、打包优化、运行时性能"

skills:
  - id: "FE-PERF-01"
    name: "代码分割"
    description: "实现路由级别的代码分割"
    input: "路由配置"
    output: "动态导入代码"
    implementation: "React.lazy、Vue异步组件"
    examples:
      - "按路由拆分打包文件"
      - "实现组件的懒加载"
    priority: "P0"
    
  - id: "FE-PERF-02"
    name: "Tree Shaking"
    description: "配置打包工具实现Tree Shaking"
    input: "package.json、构建配置"
    output: "优化后打包配置"
    implementation: "Webpack、Vite、Rollup"
    examples:
      - "确保使用ES modules"
      - "标记sideEffects: false"
    priority: "P0"
    
  - id: "FE-PERF-03"
    name: "打包优化"
    description: "优化打包体积和构建速度"
    input: "构建配置"
    output: "优化后配置"
    implementation: "Webpack、Vite"
    examples:
      - "配置CDN加载第三方库"
      - "启用gzip压缩"
    priority: "P0"
    
  - id: "FE-PERF-04"
    name: "首屏优化"
    description: "优化首屏加载时间"
    input: "LCP、FCP指标"
    output: "优化方案"
    implementation: "预加载、关键内联"
    examples:
      - "预加载关键资源"
      - "内联关键CSS"
    priority: "P0"
    
  - id: "FE-PERF-05"
    name: "缓存策略"
    description: "配置静态资源缓存策略"
    input: "资源类型"
    output: "缓存配置"
    implementation: "HTTP缓存、Service Worker"
    examples:
      - "配置强缓存和协商缓存"
      - "实现Service Worker离线缓存"
    priority: "P1"
    
  - id: "FE-PERF-06"
    name: "图片优化"
    description: "优化图片加载性能"
    input: "图片资源"
    output: "优化方案"
    implementation: "图片压缩、WebP、懒加载"
    examples:
      - "将图片转换为WebP格式"
      - "实现图片懒加载"
    priority: "P0"
    
  - id: "FE-PERF-07"
    name: "渲染优化"
    description: "优化组件渲染性能"
    input: "渲染慢的组件"
    output: "优化代码"
    implementation: "虚拟滚动、memo、useMemo"
    examples:
      - "使用React.memo避免不必要的重渲染"
      - "使用useMemo缓存计算结果"
    priority: "P1"
    
  - id: "FE-PERF-08"
    name: "性能监控"
    description: "监控前端性能指标"
    input: "性能API"
    output: "监控报告"
    implementation: "Performance API、Web Vitals"
    examples:
      - "上报Core Web Vitals指标"
      - "监控API请求耗时"
    priority: "P1"
```


## 六、路由管理能力

```yaml
# 路由管理能力集

category: "路由管理"
description: "配置和管理前端路由"

skills:
  - id: "FE-ROUTE-01"
    name: "Vue Router配置"
    description: "配置Vue Router"
    input: "页面组件"
    output: "路由配置代码"
    implementation: "Vue Router 4"
    examples:
      - "配置嵌套路由"
      - "配置路由守卫实现权限控制"
    priority: "P0"
    
  - id: "FE-ROUTE-02"
    name: "React Router配置"
    description: "配置React Router"
    input: "页面组件"
    output: "路由配置代码"
    implementation: "React Router 6"
    examples:
      - "配置动态路由"
      - "配置路由懒加载"
    priority: "P0"
    
  - id: "FE-ROUTE-03"
    name: "路由守卫"
    description: "实现路由守卫进行权限控制"
    input: "权限规则"
    output: "路由守卫代码"
    implementation: "beforeEach、loader"
    examples:
      - "未登录跳转到登录页"
      - "根据角色限制页面访问"
    priority: "P0"
```


## 七、UI组件库能力

```yaml
# UI组件库能力集

category: "UI组件库"
description: "使用和配置UI组件库"

skills:
  - id: "FE-UI-01"
    name: "Element Plus配置"
    description: "配置和使用Element Plus"
    input: "组件需求"
    output: "组件使用代码"
    implementation: "Element Plus"
    examples:
      - "按需引入Element Plus组件"
      - "自定义主题色"
    priority: "P0"
    
  - id: "FE-UI-02"
    name: "Ant Design配置"
    description: "配置和使用Ant Design"
    input: "组件需求"
    output: "组件使用代码"
    implementation: "Ant Design"
    examples:
      - "配置国际化"
      - "自定义主题"
    priority: "P0"
    
  - id: "FE-UI-03"
    name: "Tailwind CSS"
    description: "使用Tailwind CSS进行样式开发"
    input: "设计稿"
    output: "Tailwind类名"
    implementation: "Tailwind CSS"
    examples:
      - "使用Tailwind快速搭建布局"
      - "配置自定义主题"
    priority: "P1"
    
  - id: "FE-UI-04"
    name: "Vant配置"
    description: "配置和使用Vant移动端组件库"
    input: "移动端需求"
    output: "Vant组件使用"
    implementation: "Vant"
    examples:
      - "移动端表单组件"
      - "移动端弹窗组件"
    priority: "P1"
```


## 八、构建工具能力

```yaml
# 构建工具能力集

category: "构建工具"
description: "配置构建工具和环境"

skills:
  - id: "FE-BUILD-01"
    name: "Vite配置"
    description: "配置Vite构建工具"
    input: "项目需求"
    output: "vite.config.ts"
    implementation: "Vite"
    examples:
      - "配置代理解决跨域"
      - "配置路径别名"
    priority: "P0"
    
  - id: "FE-BUILD-02"
    name: "Webpack配置"
    description: "配置Webpack构建工具"
    input: "项目需求"
    output: "webpack.config.js"
    implementation: "Webpack 5"
    examples:
      - "配置loader处理各类文件"
      - "配置插件优化打包"
    priority: "P1"
    
  - id: "FE-BUILD-03"
    name: "环境变量配置"
    description: "配置多环境变量"
    input: "环境区分"
    output: ".env文件"
    implementation: "dotenv"
    examples:
      - "配置开发/测试/生产环境API地址"
      - "配置不同环境的构建参数"
    priority: "P0"
    
  - id: "FE-BUILD-04"
    name: "ESLint配置"
    description: "配置ESLint代码规范"
    input: "编码规范"
    output: ".eslintrc.js"
    implementation: "ESLint"
    examples:
      - "配置Airbnb规范"
      - "配置TypeScript规则"
    priority: "P0"
```


## 九、测试与调试能力

```yaml
# 测试与调试能力集

category: "测试与调试"
description: "前端单元测试和调试"

skills:
  - id: "FE-TEST-01"
    name: "Vitest配置"
    description: "配置Vitest单元测试"
    input: "组件代码"
    output: "测试代码"
    implementation: "Vitest"
    examples:
      - "测试组件渲染"
      - "测试用户交互"
    priority: "P1"
    
  - id: "FE-TEST-02"
    name: "Jest配置"
    description: "配置Jest单元测试"
    input: "组件代码"
    output: "测试代码"
    implementation: "Jest"
    examples:
      - "测试工具函数"
      - "快照测试"
    priority: "P1"
    
  - id: "FE-TEST-03"
    name: "Vue Test Utils"
    description: "使用Vue Test Utils测试Vue组件"
    input: "Vue组件"
    output: "测试代码"
    implementation: "Vue Test Utils"
    examples:
      - "测试组件Props"
      - "测试组件事件"
    priority: "P1"
    
  - id: "FE-TEST-04"
    name: "React Testing Library"
    description: "使用React Testing Library测试React组件"
    input: "React组件"
    output: "测试代码"
    implementation: "React Testing Library"
    examples:
      - "测试组件渲染"
      - "测试用户行为"
    priority: "P1"
    
  - id: "FE-TEST-05"
    name: "E2E测试"
    description: "使用Playwright/Cypress进行端到端测试"
    input: "用户流程"
    output: "E2E测试代码"
    implementation: "Playwright、Cypress"
    examples:
      - "测试登录流程"
      - "测试购物车流程"
    priority: "P2"
    
  - id: "FE-DEBUG-01"
    name: "DevTools调试"
    description: "使用浏览器DevTools调试"
    input: "Bug复现步骤"
    output: "Bug修复"
    implementation: "Chrome DevTools"
    examples:
      - "断点调试JavaScript"
      - "分析网络请求"
    priority: "P0"
```


## 十、动画与交互能力

```yaml
# 动画与交互能力集

category: "动画与交互"
description: "实现交互动画和过渡效果"

skills:
  - id: "FE-ANIM-01"
    name: "CSS动画"
    description: "使用CSS实现动画效果"
    input: "动画需求"
    output: "CSS动画代码"
    implementation: "transition、animation、keyframes"
    examples:
      - "实现按钮悬停效果"
      - "实现加载动画"
    priority: "P1"
    
  - id: "FE-ANIM-02"
    name: "Vue过渡"
    description: "使用Vue的过渡系统"
    input: "过渡需求"
    output: "过渡代码"
    implementation: "Vue Transition"
    examples:
      - "实现列表进入/离开动画"
      - "实现路由切换过渡"
    priority: "P1"
    
  - id: "FE-ANIM-03"
    name: "React Spring"
    description: "使用React Spring实现动画"
    input: "动画需求"
    output: "动画代码"
    implementation: "React Spring"
    examples:
      - "实现拖拽动画"
      - "实现弹簧效果"
    priority: "P2"
    
  - id: "FE-ANIM-04"
    name: "GSAP"
    description: "使用GSAP实现复杂动画"
    input: "高级动画需求"
    output: "GSAP动画代码"
    implementation: "GSAP"
    examples:
      - "实现滚动视差效果"
      - "实现时间线动画"
    priority: "P2"
```


## 十一、国际化能力

```yaml
# 国际化能力集

category: "国际化"
description: "实现多语言支持"

skills:
  - id: "FE-I18N-01"
    name: "Vue I18n配置"
    description: "配置Vue国际化"
    input: "多语言文本"
    output: "国际化配置"
    implementation: "Vue I18n"
    examples:
      - "配置中英文切换"
      - "动态加载语言包"
    priority: "P1"
    
  - id: "FE-I18N-02"
    name: "React i18next配置"
    description: "配置React国际化"
    input: "多语言文本"
    output: "国际化配置"
    implementation: "i18next、react-i18next"
    examples:
      - "配置语言切换"
      - "支持变量替换"
    priority: "P1"
    
  - id: "FE-I18N-03"
    name: "日期/数字格式化"
    description: "国际化日期和数字格式"
    input: "日期、数字"
    output: "格式化结果"
    implementation: "Intl API"
    examples:
      - "根据不同地区格式化日期"
      - "根据不同地区格式化货币"
    priority: "P1"
```


## 十二、SEO优化能力

```yaml
# SEO优化能力集

category: "SEO优化"
description: "优化搜索引擎排名"

skills:
  - id: "FE-SEO-01"
    name: "元标签配置"
    description: "配置SEO元标签"
    input: "页面信息"
    output: "Meta标签代码"
    implementation: "Vue Meta、React Helmet"
    examples:
      - "配置title和description"
      - "配置Open Graph标签"
    priority: "P1"
    
  - id: "FE-SEO-02"
    name: "SSR配置"
    description: "配置服务端渲染"
    input: "Vue/React应用"
    output: "SSR配置"
    implementation: "Nuxt.js、Next.js"
    examples:
      - "配置Nuxt.js SSR"
      - "配置Next.js SSR"
    priority: "P2"
    
  - id: "FE-SEO-03"
    name: "站点地图生成"
    description: "生成sitemap.xml"
    input: "页面路由"
    output: "sitemap.xml"
    implementation: "sitemap生成器"
    examples:
      - "自动生成静态页面sitemap"
      - "动态生成动态路由sitemap"
    priority: "P2"
```


## 十三、安全防护能力

```yaml
# 安全防护能力集

category: "安全防护"
description: "防范前端安全漏洞"

skills:
  - id: "FE-SEC-01"
    name: "XSS防护"
    description: "防止XSS攻击"
    input: "用户输入"
    output: "转义/净化后的内容"
    implementation: "DOMPurify、转义函数"
    examples:
      - "转义用户输入的HTML"
      - "使用DOMPurify净化富文本"
    priority: "P0"
    
  - id: "FE-SEC-02"
    name: "CSRF防护"
    description: "防止CSRF攻击"
    input: "请求"
    output: "带Token的请求"
    implementation: "CSRF Token、SameSite"
    examples:
      - "在请求头中添加CSRF Token"
      - "配置Cookie SameSite属性"
    priority: "P1"
    
  - id: "FE-SEC-03"
    name: "敏感信息保护"
    description: "保护前端敏感信息"
    input: "敏感数据"
    output: "安全存储"
    implementation: "环境变量、加密存储"
    examples:
      - "不在前端存储密码"
      - "API密钥放在环境变量中"
    priority: "P0"
```


## 十四、文档与规范能力

```yaml
# 文档与规范能力集

category: "文档与规范"
description: "编写技术文档和规范"

skills:
  - id: "FE-DOC-01"
    name: "组件文档"
    description: "编写组件使用文档"
    input: "组件代码"
    output: "组件文档"
    implementation: "Storybook、Markdown"
    examples:
      - "使用Storybook展示组件"
      - "编写组件API文档"
    priority: "P1"
    
  - id: "FE-DOC-02"
    name: "代码规范"
    description: "制定前端代码规范"
    input: "团队约定"
    output: "规范文档"
    implementation: "Markdown"
    examples:
      - "制定命名规范"
      - "制定目录结构规范"
    priority: "P1"
    
  - id: "FE-DOC-03"
    name: "项目README"
    description: "编写项目README文档"
    input: "项目信息"
    output: "README.md"
    implementation: "Markdown"
    examples:
      - "包含项目简介、安装、运行说明"
      - "包含API文档链接"
    priority: "P1"
```


## 十五、能力优先级汇总

```yaml
# 按优先级排序

P0_skills:  # 必须实现（20项）
  - FE-COMP-01: "Vue组件开发"
  - FE-COMP-02: "React组件开发"
  - FE-COMP-03: "组件通信"
  - FE-COMP-04: "组件复用"
  - FE-STATE-01: "Pinia配置"
  - FE-STATE-03: "Redux配置"
  - FE-STATE-05: "状态持久化"
  - FE-STATE-06: "跨组件状态共享"
  - FE-RESP-01: "Flexbox布局"
  - FE-RESP-02: "Grid布局"
  - FE-RESP-03: "媒体查询"
  - FE-RESP-04: "移动端适配"
  - FE-RESP-07: "多端适配"
  - FE-PERF-01: "代码分割"
  - FE-PERF-02: "Tree Shaking"
  - FE-PERF-03: "打包优化"
  - FE-PERF-04: "首屏优化"
  - FE-PERF-06: "图片优化"
  - FE-ROUTE-01: "Vue Router配置"
  - FE-ROUTE-02: "React Router配置"
  - FE-ROUTE-03: "路由守卫"
  - FE-UI-01: "Element Plus配置"
  - FE-UI-02: "Ant Design配置"
  - FE-BUILD-01: "Vite配置"
  - FE-BUILD-03: "环境变量配置"
  - FE-BUILD-04: "ESLint配置"
  - FE-DEBUG-01: "DevTools调试"
  - FE-SEC-01: "XSS防护"
  - FE-SEC-03: "敏感信息保护"

P1_skills:  # 近期实现（24项）
  - FE-COMP-05: "组件库开发"
  - FE-COMP-07: "虚拟滚动"
  - FE-COMP-08: "动态组件"
  - FE-STATE-02: "Vuex配置"
  - FE-STATE-04: "Zustand配置"
  - FE-RESP-05: "响应式图片"
  - FE-RESP-06: "暗色主题"
  - FE-PERF-05: "缓存策略"
  - FE-PERF-07: "渲染优化"
  - FE-PERF-08: "性能监控"
  - FE-UI-03: "Tailwind CSS"
  - FE-UI-04: "Vant配置"
  - FE-BUILD-02: "Webpack配置"
  - FE-TEST-01: "Vitest配置"
  - FE-TEST-02: "Jest配置"
  - FE-TEST-03: "Vue Test Utils"
  - FE-TEST-04: "React Testing Library"
  - FE-ANIM-01: "CSS动画"
  - FE-ANIM-02: "Vue过渡"
  - FE-I18N-01: "Vue I18n配置"
  - FE-I18N-02: "React i18next配置"
  - FE-I18N-03: "日期/数字格式化"
  - FE-SEO-01: "元标签配置"
  - FE-SEC-02: "CSRF防护"
  - FE-DOC-01: "组件文档"
  - FE-DOC-02: "代码规范"
  - FE-DOC-03: "项目README"

P2_skills:  # 远期规划（7项）
  - FE-COMP-06: "Web Components"
  - FE-TEST-05: "E2E测试"
  - FE-ANIM-03: "React Spring"
  - FE-ANIM-04: "GSAP"
  - FE-SEO-02: "SSR配置"
  - FE-SEO-03: "站点地图生成"
```


## 十六、在Cursor中使用

将本文档保存后，在Cursor中使用以下命令：

```
# 查看前端部所有能力
@docs/FRONTEND_SKILLS_v1.0.md 列出前端部所有P0级能力

# 实现特定能力
@docs/FRONTEND_SKILLS_v1.0.md 实现FE-COMP-01 Vue组件开发能力

# 创建带技能的前端工程师
@docs/FRONTEND_SKILLS_v1.0.md 根据P0能力创建资深前端工程师智能体

# 实现组件开发能力集
@docs/FRONTEND_SKILLS_v1.0.md 实现category 组件开发下的所有能力
```

---

**文档结束**