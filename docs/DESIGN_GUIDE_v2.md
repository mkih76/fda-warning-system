# FDA 警告信监控系统 - 设计规范 v2.0

## 一、设计理念

### 核心定位
> **"专业、可信、精准"** — 服务于制药行业 QA、合规官、监管事务专家的高端数据平台

### 设计关键词
| 维度 | 关键词 | 实现方式 |
|------|--------|---------|
| **专业感** | 精准、严谨、权威 | 克制的色彩、清晰的层级、充足留白 |
| **科技感** | 智能、现代、高效 | 微妙的动效、数据可视化、深色模式 |
| **信任感** | 安全、合规、透明 | FDA 品牌关联、数据来源明确、更新时效 |

---

## 二、色彩系统

### 主色调 — 生命蓝绿 (Bio-Teal)

```javascript
// tailwind.config.js 扩展
colors: {
  // 主色 — 生命健康蓝绿
  bio: {
    50: '#e6f7f5',
    100: '#b3e8e0',
    200: '#80d9cb',
    300: '#4dcab6',
    400: '#26bfa4',   // 主强调色
    500: '#00a88a',   // 主按钮
    600: '#008f75',
    700: '#007560',
    800: '#005c4b',
    900: '#004236',
  },
  
  // 辅助色 — 深海蓝 (专业、沉稳)
  deep: {
    50: '#f0f4f8',
    100: '#d9e2ec',
    200: '#bcccdc',
    300: '#9fb3c8',
    400: '#829ab1',
    500: '#627d98',   // 次要文字
    600: '#486581',
    700: '#334e68',   // 标题
    800: '#243b53',
    900: '#102a43',   // 深色背景
  },
  
  // 功能色
  alert: {
    critical: '#dc2626',  // 严重违规
    major: '#ea580c',     // 主要违规  
    minor: '#0891b2',     // 轻微违规
    active: '#dc2626',    // 活跃警告信
    closed: '#16a34a',    // 已关闭
  },
  
  // 中性色
  slate: {
    50: '#f8fafc',
    100: '#f1f5f9',
    200: '#e2e8f0',
    300: '#cbd5e1',
    400: '#94a3b8',
    500: '#64748b',
    600: '#475569',
    700: '#334155',
    800: '#1e293b',
    900: '#0f172a',       // 深色模式背景
  }
}
```

### 色彩使用规范

| 场景 | 颜色 | 用途 |
|------|------|------|
| 主按钮/CTA | `bio-500` | 行动号召 |
| 链接/交互 | `bio-400` | 悬停状态 |
| 深色背景 | `slate-900` | Hero、深色卡片 |
| 卡片背景 | `white` / `slate-50` | 内容区域 |
| 边框/分隔 | `slate-200` | 微妙分隔 |
| 次要文字 | `slate-500` | 说明文字 |
| 禁用状态 | `slate-300` | 不可交互 |

---

## 三、字体系统

### 字体栈
```javascript
fontFamily: {
  sans: [
    'Inter',           // 主要 UI 字体
    'SF Pro Display',  // macOS 回退
    '-apple-system',
    'BlinkMacSystemFont',
    'system-ui',
    'sans-serif'
  ],
  mono: [
    'JetBrains Mono',  // 代码、数据
    'Fira Code',
    'monospace'
  ],
  display: [
    'Inter',           // 标题（可选加粗）
    'sans-serif'
  ]
}
```

### 字号层级

| 级别 | 大小 | 字重 | 行高 | 用途 |
|------|------|------|------|------|
| Display | 48-64px | 700 | 1.1 | Hero 主标题 |
| H1 | 32-40px | 700 | 1.2 | 页面标题 |
| H2 | 24-28px | 600 | 1.3 | 区块标题 |
| H3 | 18-20px | 600 | 1.4 | 卡片标题 |
| Body | 16px | 400 | 1.6 | 正文 |
| Small | 14px | 400 | 1.5 | 辅助文字 |
| Caption | 12px | 500 | 1.4 | 标签、时间 |

---

## 四、间距系统

基于 4px 网格，使用 Tailwind 默认间距：

| Token | 值 | 用途 |
|-------|-----|------|
| `space-1` | 4px | 图标与文字间距 |
| `space-2` | 8px | 紧凑元素间距 |
| `space-3` | 12px | 表单元素内边距 |
| `space-4` | 16px | 卡片内边距 |
| `space-6` | 24px | 区块间距 |
| `space-8` | 32px | 大区块间距 |
| `space-12` | 48px | 页面级间距 |
| `space-16` | 64px | Hero 区域 |

**容器宽度**：
- 最大内容宽度：`max-w-7xl` (1280px)
- 内容区边距：`px-6` (24px) / `px-8` (32px) 大屏

---

## 五、组件规范

### 1. 卡片 (Card)

```vue
<!-- 基础卡片 -->
<div class="bg-white rounded-xl border border-slate-200 shadow-sm 
            hover:shadow-md hover:border-bio-200 transition-all duration-200">
  <!-- 内容 -->
</div>

<!-- 深色卡片 (数据看板) -->
<div class="bg-slate-900 rounded-xl border border-slate-800">
  <!-- 内容 -->
</div>
```

**变体**：
- `card-flat` — 无阴影，用于列表项
- `card-elevated` — 明显阴影，用于重要数据
- `card-interactive` — 悬停效果，可点击

### 2. 按钮 (Button)

```vue
<!-- 主按钮 -->
<button class="inline-flex items-center justify-center gap-2 
               bg-bio-500 text-white px-6 py-2.5 rounded-lg font-medium
               hover:bg-bio-600 active:bg-bio-700 
               transition-colors duration-200
               disabled:bg-slate-300 disabled:cursor-not-allowed">
  <span>按钮文字</span>
  <IconChevronRight class="w-4 h-4" />
</button>

<!-- 次按钮 -->
<button class="inline-flex items-center justify-center gap-2 
               bg-white text-slate-700 border border-slate-300 px-6 py-2.5 rounded-lg font-medium
               hover:bg-slate-50 hover:border-slate-400
               transition-colors duration-200">
  次要操作
</button>

<!-- 文字按钮 -->
<button class="text-bio-500 font-medium hover:text-bio-600 
               inline-flex items-center gap-1 transition-colors">
  查看详情 <IconArrowRight class="w-4 h-4" />
</button>
```

### 3. 标签/徽章 (Badge)

```vue
<!-- 状态徽章 -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
      :class="status === 'active' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'">
  {{ status === 'active' ? '活跃' : '已关闭' }}
</span>

<!-- 办公室徽章 -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
             bg-blue-100 text-blue-700">
  {{ office }}
</span>

<!-- 严重度徽章 -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
      :class="{
        'bg-red-100 text-red-700': severity === 'critical',
        'bg-orange-100 text-orange-700': severity === 'major',
        'bg-cyan-100 text-cyan-700': severity === 'minor'
      }">
  {{ severity }}
</span>
```

### 4. 表单输入

```vue
<!-- 输入框 -->
<input class="w-full px-4 py-2.5 rounded-lg border border-slate-300 bg-white
               text-slate-900 placeholder-slate-400
               focus:outline-none focus:ring-2 focus:ring-bio-500/20 focus:border-bio-500
               transition-all duration-200" />

<!-- 下拉选择 -->
<select class="w-full px-4 py-2.5 rounded-lg border border-slate-300 bg-white
               text-slate-900 focus:outline-none focus:ring-2 focus:ring-bio-500/20 focus:border-bio-500
               appearance-none bg-[url('data:image/svg+xml,...')] bg-no-repeat bg-right-3">
  <!-- options -->
</select>
```

### 5. 表格 (Table) — 核心组件

```vue
<div class="overflow-x-auto rounded-xl border border-slate-200">
  <table class="w-full text-left text-sm">
    <thead class="bg-slate-50 border-b border-slate-200">
      <tr>
        <th class="px-4 py-3 font-semibold text-slate-700">状态</th>
        <th class="px-4 py-3 font-semibold text-slate-700">企业名称</th>
        <th class="px-4 py-3 font-semibold text-slate-700">主题</th>
        <th class="px-4 py-3 font-semibold text-slate-700">办公室</th>
        <th class="px-4 py-3 font-semibold text-slate-700">日期</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-slate-100">
      <tr v-for="item in items" :key="item.id"
          class="hover:bg-slate-50 transition-colors cursor-pointer">
        <td class="px-4 py-3"><Badge :status="item.status" /></td>
        <td class="px-4 py-3 font-medium text-slate-900">{{ item.company_name }}</td>
        <td class="px-4 py-3 text-slate-600">{{ item.subject }}</td>
        <td class="px-4 py-3"><BadgeOffice :office="item.issuing_office" /></td>
        <td class="px-4 py-3 text-slate-500 text-xs">{{ item.posted_date }}</td>
      </tr>
    </tbody>
  </table>
</div>
```

---

## 六、页面布局规范

### 导航栏 (Navbar)

```vue
<nav class="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200">
  <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
    <!-- Logo -->
    <router-link to="/" class="flex items-center gap-3">
      <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-bio-400 to-bio-600 
                  flex items-center justify-center text-white font-bold">
        F
      </div>
      <span class="font-semibold text-slate-900">FDA Monitor</span>
    </router-link>
    
    <!-- 导航链接 -->
    <div class="hidden md:flex items-center gap-1">
      <router-link v-for="link in navLinks" :key="link.to" :to="link.to"
                   class="px-4 py-2 rounded-lg text-sm font-medium text-slate-600
                          hover:text-slate-900 hover:bg-slate-100
                          transition-colors">
        {{ link.label }}
      </router-link>
    </div>
    
    <!-- 右侧操作 -->
    <div class="flex items-center gap-3">
      <button class="p-2 rounded-lg text-slate-500 hover:bg-slate-100">
        <IconMoon class="w-5 h-5" />
      </button>
    </div>
  </div>
</nav>
```

### Hero 区域

```vue
<section class="relative bg-slate-900 overflow-hidden">
  <!-- 背景装饰 -->
  <div class="absolute inset-0 opacity-30">
    <div class="absolute top-0 left-1/4 w-96 h-96 bg-bio-500/20 rounded-full blur-3xl"></div>
    <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl"></div>
  </div>
  
  <div class="relative max-w-7xl mx-auto px-6 py-24 md:py-32">
    <div class="max-w-3xl">
      <!-- 实时状态标签 -->
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full 
                  bg-bio-500/10 border border-bio-500/20 text-bio-400 text-sm mb-8">
        <span class="w-2 h-2 rounded-full bg-bio-400 animate-pulse"></span>
        数据实时同步 FDA 官方
      </div>
      
      <h1 class="text-4xl md:text-6xl font-bold text-white leading-tight">
        FDA 警告信<br>
        <span class="text-transparent bg-clip-text bg-gradient-to-r from-bio-400 to-cyan-400">
          智能监控
        </span>系统
      </h1>
      
      <p class="mt-6 text-xl text-slate-400 max-w-2xl">
        实时追踪 FDA 警告信动态 · AI 自动翻译分析 · 企业合规全链路监控
      </p>
      
      <div class="mt-10 flex flex-wrap gap-4">
        <router-link to="/letters" class="btn-primary text-lg px-8">
          浏览最新警告信
          <IconArrowRight class="w-5 h-5" />
        </router-link>
        <router-link to="/dashboard" class="btn-outline border-slate-600 text-slate-300 hover:bg-slate-800">
          查看数据看板
        </router-link>
      </div>
    </div>
  </div>
</section>
```

---

## 七、动效规范

### 过渡动画

```css
/* 页面切换 */
.page-enter-active, .page-leave-active {
  transition: opacity 0.2s ease;
}
.page-enter-from, .page-leave-to {
  opacity: 0;
}

/* 列表项进入 */
.list-item-enter-active {
  transition: all 0.3s ease;
}
.list-item-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

/* 卡片悬停 */
.card-hover {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card-hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.1);
}
```

### 微交互

| 元素 | 交互 | 效果 |
|------|------|------|
| 按钮 | hover | 背景色加深，轻微上移 |
| 卡片 | hover | 阴影加深，边框变色 |
| 链接 | hover | 颜色变化，下划线出现 |
| 表格行 | hover | 背景色变化 |
| 加载 | - | 骨架屏 shimmer 效果 |

---

## 八、深色模式

```javascript
// tailwind.config.js
darkMode: 'class',

// 使用
<html class="dark">
<body class="bg-slate-900 text-slate-100">
  <div class="bg-slate-800 border-slate-700">
    <!-- 深色模式内容 -->
  </div>
</body>
</html>
```

**深色模式映射**：
- `bg-white` → `bg-slate-900`
- `bg-slate-50` → `bg-slate-800`
- `border-slate-200` → `border-slate-700`
- `text-slate-900` → `text-slate-100`
- `text-slate-600` → `text-slate-400`

---

## 九、响应式断点

| 断点 | 宽度 | 调整 |
|------|------|------|
| `sm` | 640px | 基础移动端 |
| `md` | 768px | 平板，侧边栏展开 |
| `lg` | 1024px | 小桌面，完整布局 |
| `xl` | 1280px | 标准桌面 |
| `2xl` | 1536px | 大屏，更宽间距 |

---

## 十、实施路线图

### Phase 1: 基础重构（1-2天）
- [ ] 更新 `tailwind.config.js` 色彩系统
- [ ] 重构 `main.css` 组件类
- [ ] 更新 Navbar、Footer 组件

### Phase 2: 核心页面升级（2-3天）
- [ ] Home.vue — 新 Hero + 功能卡片
- [ ] Letters.vue — 表格化 + 高级筛选
- [ ] LetterDetail.vue — 信息层级优化

### Phase 3: 数据可视化（2-3天）
- [ ] Dashboard.vue — 图表集成（Chart.js/Recharts）
- [ ] 添加趋势图、热力图
- [ ] 统计卡片组件

### Phase 4: 体验优化（1-2天）
- [ ] 深色模式切换
- [ ] 加载状态（Skeleton）
- [ ] 动画过渡
- [ ] 错误状态处理

### Phase 5: 细节打磨（持续）
- [ ] 移动端适配
- [ ] 性能优化
- [ ] 可访问性改进

---

## 十一、关键设计决策

### 为什么选 Bio-Teal 作为主色？
1. **行业关联** — 蓝绿色是医疗、生命科学行业的经典色
2. **专业感** — 比纯蓝更温暖，比纯绿更专业
3. **差异化** — 区别于普通 SaaS 的蓝色系
4. **深色友好** — 在深色模式下依然清晰

### 为什么用 Slate 而非 Gray？
- Slate 带有轻微的蓝色调，与 bio 色系更协调
- 在深色模式下更柔和，不刺眼

### 为什么卡片用白色而非透明？
- 白色卡片在浅色背景上有清晰的边界
- 更容易建立层级感
- 深色模式下切换到 slate-800，保持一致性

---

*文档版本: v2.0*
*最后更新: 2026-04-28*
*适用于: FDA 警告信智能监控系统*
