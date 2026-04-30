<template>
  <div class="home-page">
    <!-- 导航栏 -->
    <header class="header" :class="{ scrolled: isScrolled }">
      <div class="container">
        <nav class="nav-content">
          <!-- Logo -->
          <router-link to="/" class="logo">
            <div class="logo-icon">
              <svg viewBox="0 0 32 32" fill="none">
                <rect width="32" height="32" rx="8" fill="url(#logo-gradient)" />
                <path d="M8 12h16M8 16h16M8 20h12" stroke="white" stroke-width="2" stroke-linecap="round" />
                <defs>
                  <linearGradient id="logo-gradient" x1="0" y1="0" x2="32" y2="32">
                    <stop stop-color="#3b82f6" />
                    <stop offset="1" stop-color="#06b6d4" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <div class="logo-text">
              <span class="logo-title">FDA</span>
              <span class="logo-subtitle">警告信智能平台</span>
            </div>
          </router-link>

          <!-- 桌面导航 -->
          <div class="desktop-nav">
            <router-link to="/letters" class="nav-link">
              警告信
              <span class="nav-badge">986+</span>
            </router-link>
            <router-link to="/dashboard" class="nav-link">数据看板</router-link>
            <router-link to="/articles" class="nav-link">深度内容</router-link>
            <router-link to="/regulations" class="nav-link">法规信息</router-link>
            <router-link to="/news" class="nav-link">行业资讯</router-link>
          </div>

          <!-- 右侧操作 -->
          <div class="nav-actions">
            <router-link to="/favorites" class="action-btn favorites-btn">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              <span v-if="favoritesCount > 0" class="favorites-count">{{ favoritesCount }}</span>
            </router-link>

            <button @click="toggleDark" class="action-btn theme-toggle" :title="isDark ? '切换到浅色模式' : '切换到暗色模式'">
              <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            </button>

            <router-link to="/letters" class="btn btn-primary btn-sm cta-btn">
              开始探索
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </router-link>

            <!-- 移动端菜单按钮 -->
            <button @click="toggleMobileMenu" class="mobile-menu-btn">
              <svg v-if="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </nav>
      </div>

      <!-- 移动端菜单 -->
      <div class="mobile-menu" :class="{ open: mobileMenuOpen }">
        <div class="mobile-menu-content">
          <router-link to="/letters" class="mobile-nav-link" @click="closeMobileMenu">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            警告信列表
          </router-link>
          <router-link to="/dashboard" class="mobile-nav-link" @click="closeMobileMenu">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            数据看板
          </router-link>
          <router-link to="/favorites" class="mobile-nav-link" @click="closeMobileMenu">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            我的收藏
            <span v-if="favoritesCount > 0" class="mobile-favorites-count">{{ favoritesCount }}</span>
          </router-link>
          <router-link to="/articles" class="mobile-nav-link" @click="closeMobileMenu">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
            </svg>
            深度内容
          </router-link>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-bg">
        <div class="hero-gradient"></div>
        <div class="hero-pattern"></div>
      </div>

      <div class="container">
        <div class="hero-content">
          <div class="hero-text animate-fade-in-up">
            <div class="hero-badge">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              AI 驱动的智能分析
            </div>

            <h1 class="hero-title">
              <span class="gradient-text">FDA 警告信</span>
              <br />
              智能监控平台
            </h1>

            <p class="hero-description">
              实时追踪 FDA 警告信动态，AI 智能翻译与分析，助力中国制药企业合规出海。
              覆盖 <strong>986+ 封警告信</strong>，100% 中文翻译。
            </p>

            <div class="hero-actions">
              <router-link to="/letters" class="btn btn-primary btn-xl">
                开始探索
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </router-link>
              <router-link to="/dashboard" class="btn btn-secondary btn-xl">
                查看数据看板
              </router-link>
            </div>

            <div class="hero-stats">
              <div class="stat-item">
                <span class="stat-number">986+</span>
                <span class="stat-label">警告信</span>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-item">
                <span class="stat-number">100%</span>
                <span class="stat-label">中文翻译</span>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-item">
                <span class="stat-number">24h</span>
                <span class="stat-label">实时同步</span>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-item">
                <span class="stat-number">AI</span>
                <span class="stat-label">智能分析</span>
              </div>
            </div>
          </div>

          <div class="hero-visual animate-fade-in-right delay-300">
            <div class="hero-card-stack">
              <div class="hero-card card-1">
                <div class="card-header">
                  <span class="badge badge-danger badge-dot">高风险</span>
                  <span class="card-id">WL#2024-0892</span>
                </div>
                <h4>某制药有限公司</h4>
                <p>CGMP 违规 - 数据完整性问题</p>
                <div class="card-footer">
                  <span>CDER</span>
                  <span>2024-03-15</span>
                </div>
              </div>
              <div class="hero-card card-2">
                <div class="card-header">
                  <span class="badge badge-warning badge-dot">中风险</span>
                  <span class="card-id">WL#2024-0756</span>
                </div>
                <h4>某生物科技公司</h4>
                <p>生产过程控制不符合要求</p>
                <div class="card-footer">
                  <span>CDRH</span>
                  <span>2024-02-28</span>
                </div>
              </div>
              <div class="hero-card card-3">
                <div class="card-header">
                  <span class="badge badge-success badge-dot">低风险</span>
                  <span class="card-id">WL#2024-0634</span>
                </div>
                <h4>某食品有限公司</h4>
                <p>标签标识不符合规定</p>
                <div class="card-footer">
                  <span>CFSAN</span>
                  <span>2024-02-10</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 核心功能 -->
    <section class="features-section">
      <div class="container">
        <div class="section-header animate-fade-in-up">
          <span class="section-badge">核心功能</span>
          <h2 class="section-title">全方位合规保障</h2>
          <p class="section-description">
            我们提供完整的 FDA 警告信监控和分析解决方案，帮助您及时发现风险、快速响应
          </p>
        </div>

        <div class="features-grid">
          <div v-for="(feature, index) in features" :key="index"
               class="feature-card animate-fade-in-up"
               :style="{ animationDelay: `${index * 100}ms` }">
            <div class="feature-icon" :style="{ background: feature.gradient }">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="feature.icon" />
              </svg>
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
            <router-link to="/letters" class="feature-link">
              了解更多
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- 数据展示 -->
    <section class="stats-section">
      <div class="container">
        <div class="stats-content">
          <div class="stats-text animate-fade-in-left">
            <span class="section-badge">数据洞察</span>
            <h2>用数据驱动合规决策</h2>
            <p>
              我们的平台实时同步 FDA 官方数据，通过 AI 智能分析，为您提供深度的行业洞察和风险预警。
            </p>

            <div class="stats-highlights">
              <div class="highlight-item">
                <div class="highlight-icon">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </div>
                <div>
                  <h4>年度趋势分析</h4>
                  <p>追踪 FDA 执法力度变化，预测未来趋势</p>
                </div>
              </div>
              <div class="highlight-item">
                <div class="highlight-icon">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <div>
                  <h4>风险企业画像</h4>
                  <p>识别高风险企业，提前预警潜在风险</p>
                </div>
              </div>
              <div class="highlight-item">
                <div class="highlight-icon">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                  </svg>
                </div>
                <div>
                  <h4>违规类型分布</h4>
                  <p>深入了解常见违规类型和解决方案</p>
                </div>
              </div>
            </div>

            <router-link to="/dashboard" class="btn btn-primary btn-lg">
              查看完整数据看板
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </router-link>
          </div>

          <div class="stats-visual animate-fade-in-right delay-300">
            <div class="stats-cards">
              <div class="stats-card">
                <div class="stats-card-icon" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div class="stats-card-content">
                  <span class="stats-card-number">986</span>
                  <span class="stats-card-label">警告信总数</span>
                </div>
                <span class="stats-card-trend up">+12%</span>
              </div>

              <div class="stats-card">
                <div class="stats-card-icon" style="background: rgba(239, 68, 68, 0.1); color: #ef4444;">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <div class="stats-card-content">
                  <span class="stats-card-number">234</span>
                  <span class="stats-card-label">活跃警告信</span>
                </div>
                <span class="stats-card-trend down">-5%</span>
              </div>

              <div class="stats-card">
                <div class="stats-card-icon" style="background: rgba(34, 197, 94, 0.1); color: #22c55e;">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <div class="stats-card-content">
                  <span class="stats-card-number">752</span>
                  <span class="stats-card-label">已关闭</span>
                </div>
                <span class="stats-card-trend up">+8%</span>
              </div>

              <div class="stats-card">
                <div class="stats-card-icon" style="background: rgba(168, 85, 247, 0.1); color: #a855f7;">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <div class="stats-card-content">
                  <span class="stats-card-number">12</span>
                  <span class="stats-card-label">签发办公室</span>
                </div>
              </div>
            </div>

            <!-- 迷你图表 -->
            <div class="mini-chart">
              <div class="mini-chart-header">
                <span>年度趋势</span>
                <span class="trend-indicator up">↑ 12%</span>
              </div>
              <div class="mini-chart-bars">
                <div v-for="(height, index) in chartBars" :key="index"
                     class="chart-bar"
                     :style="{ height: height + '%', animationDelay: index * 50 + 'ms' }">
                </div>
              </div>
              <div class="mini-chart-labels">
                <span>2019</span>
                <span>2020</span>
                <span>2021</span>
                <span>2022</span>
                <span>2023</span>
                <span>2024</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 工作流程 -->
    <section class="workflow-section">
      <div class="container">
        <div class="section-header animate-fade-in-up">
          <span class="section-badge">工作流程</span>
          <h2 class="section-title">从数据到洞察</h2>
          <p class="section-description">
            我们的三步流水线确保您获得最准确、最及时的 FDA 警告信信息
          </p>
        </div>

        <div class="workflow-grid">
          <div v-for="(step, index) in workflowSteps" :key="index"
               class="workflow-card animate-fade-in-up"
               :style="{ animationDelay: `${index * 150}ms` }">
            <div class="workflow-number">{{ String(index + 1).padStart(2, '0') }}</div>
            <div class="workflow-icon" :style="{ background: step.gradient }">
              <svg class="w-8 h-8" fill="none" stroke="white" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="step.icon" />
              </svg>
            </div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 最新警告信 -->
    <section class="latest-section">
      <div class="container">
        <div class="section-header animate-fade-in-up">
          <span class="section-badge">最新动态</span>
          <h2 class="section-title">最新警告信</h2>
          <p class="section-description">
            实时追踪 FDA 最新发布的警告信，第一时间了解行业动态
          </p>
        </div>

        <div class="latest-grid">
          <div v-for="(letter, index) in latestLetters" :key="index"
               class="letter-card animate-fade-in-up"
               :style="{ animationDelay: `${index * 100}ms` }"
               @click="$router.push(`/letters/${letter.id}`)">
            <div class="letter-header">
              <span class="badge" :class="getRiskBadgeClass(letter.risk_level)">
                {{ letter.risk_level || '待评估' }}
              </span>
              <span class="letter-id">{{ letter.fda_id }}</span>
            </div>
            <h4 class="letter-company">{{ letter.company_name }}</h4>
            <p class="letter-subject">{{ letter.subject }}</p>
            <div class="letter-footer">
              <div class="letter-meta">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>{{ letter.issue_date }}</span>
              </div>
              <span class="letter-office">{{ letter.issuing_office }}</span>
            </div>
          </div>
        </div>

        <div class="section-footer animate-fade-in-up delay-500">
          <router-link to="/letters" class="btn btn-secondary btn-lg">
            查看所有警告信
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content animate-fade-in-up">
          <h2>准备好开始了吗？</h2>
          <p>
            立即探索 FDA 警告信数据库，利用 AI 智能分析保障您的合规之路
          </p>
          <div class="cta-actions">
            <router-link to="/letters" class="btn btn-primary btn-xl">
              免费开始使用
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </router-link>
            <router-link to="/dashboard" class="btn btn-secondary btn-xl">
              查看演示
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <div class="footer-logo">
              <div class="logo-icon">
                <svg viewBox="0 0 32 32" fill="none">
                  <rect width="32" height="32" rx="8" fill="url(#footer-logo-gradient)" />
                  <path d="M8 12h16M8 16h16M8 20h12" stroke="white" stroke-width="2" stroke-linecap="round" />
                  <defs>
                    <linearGradient id="footer-logo-gradient" x1="0" y1="0" x2="32" y2="32">
                      <stop stop-color="#60a5fa" />
                      <stop offset="1" stop-color="#22d3ee" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
              <span>FDA 警告信智能平台</span>
            </div>
            <p>AI 驱动的 FDA 警告信监控与分析系统，助力中国药企合规出海。</p>
          </div>

          <div class="footer-links">
            <div class="footer-column">
              <h4>快速链接</h4>
              <router-link to="/letters">警告信列表</router-link>
              <router-link to="/dashboard">数据看板</router-link>
              <router-link to="/articles">深度内容</router-link>
              <router-link to="/news">行业资讯</router-link>
            </div>
            <div class="footer-column">
              <h4>资源</h4>
              <router-link to="/regulations">法规信息</router-link>
              <a href="https://github.com/mkih76/fda-warning-system" target="_blank">GitHub</a>
              <a href="mailto:contact@example.com">联系我们</a>
            </div>
          </div>
        </div>

        <div class="footer-bottom">
          <p>&copy; {{ new Date().getFullYear() }} FDA 警告信智能平台. All rights reserved.</p>
          <p>
            <a href="https://github.com/mkih76/fda-warning-system" target="_blank">GitHub</a>
            <span class="mx-2">·</span>
            <span>Made with ❤️ for compliance</span>
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useDarkMode } from '../composables/useDarkMode.js'
import { useFavorites } from '../composables/useFavorites.js'

const { isDark, toggleDark } = useDarkMode()
const { favoritesCount } = useFavorites()

const isScrolled = ref(false)
const mobileMenuOpen = ref(false)

// 滚动检测
const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

function closeMobileMenu() {
  mobileMenuOpen.value = false
}

// 核心功能数据
const features = [
  {
    title: '实时数据同步',
    description: '每日自动同步 FDA 官方数据，确保您获取最新的警告信信息。',
    icon: 'M13 10V3L4 14h7v7l9-11h-7z',
    gradient: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
  },
  {
    title: 'AI 智能翻译',
    description: '先进的 AI 翻译引擎，100% 准确翻译警告信内容为中文。',
    icon: 'M3 5h12M9 3v2m3.356 9.356l2.293 2.293M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9 14l2 2 4-4',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)'
  },
  {
    title: '智能分类',
    description: '基于 CGMP 六大系统自动分类，精准定位违规类型。',
    icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4',
    gradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
  },
  {
    title: '风险评估',
    description: 'AI 驱动的风险评分，自动识别高风险企业和违规项。',
    icon: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z M9 12l2 2 4-4',
    gradient: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)'
  },
  {
    title: '全文检索',
    description: '支持按企业名称、产品类型、违规关键词全文检索。',
    icon: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z M10 10l4 4',
    gradient: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)'
  },
  {
    title: '数据可视化',
    description: '交互式仪表盘展示年度趋势、办公室排名、状态分布。',
    icon: 'M3 3v18h18 M9 17V9m4 8V5m4 12v-4',
    gradient: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)'
  }
]

// 工作流程数据
const workflowSteps = [
  {
    title: '数据采集',
    description: '爬虫每日从 FDA 官方来源抓取最新警告信并更新数据库',
    icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4',
    gradient: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
  },
  {
    title: 'AI 处理',
    description: '每封信经过翻译→分类→摘要流水线处理，采用最先进的 LLM 模型',
    icon: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
    gradient: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)'
  },
  {
    title: '洞察呈现',
    description: '通过简洁的 Web 界面查看结构化数据、违规趋势和 AI 生成的摘要',
    icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    gradient: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)'
  }
]

// 最新警告信（示例数据）
const latestLetters = ref([
  {
    id: 1,
    fda_id: 'WL#2024-0892',
    company_name: '某制药有限公司',
    subject: 'CGMP 违规 - 数据完整性问题',
    issue_date: '2024-03-15',
    issuing_office: 'CDER',
    risk_level: 'High'
  },
  {
    id: 2,
    fda_id: 'WL#2024-0756',
    company_name: '某生物科技公司',
    subject: '生产过程控制不符合要求',
    issue_date: '2024-02-28',
    issuing_office: 'CDRH',
    risk_level: 'Medium'
  },
  {
    id: 3,
    fda_id: 'WL#2024-0634',
    company_name: '某食品有限公司',
    subject: '标签标识不符合规定',
    issue_date: '2024-02-10',
    issuing_office: 'CFSAN',
    risk_level: 'Low'
  }
])

// 迷你图表数据
const chartBars = [60, 75, 85, 70, 95, 100]

function getRiskBadgeClass(riskLevel) {
  const classes = {
    'High': 'badge-danger',
    'Medium': 'badge-warning',
    'Low': 'badge-success'
  }
  return classes[riskLevel] || 'badge-info'
}
</script>

<style scoped>
/* ═══════════════════════════════════════════════════════════════
   Header
═══════════════════════════════════════════════════════════════ */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-default);
  transition: all var(--duration-normal) var(--ease-default);
}

.dark .header {
  background: rgba(15, 23, 42, 0.8);
}

.header.scrolled {
  box-shadow: var(--shadow-md);
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--header-height);
  gap: var(--space-4);
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  text-decoration: none;
}

.logo-icon svg {
  width: 36px;
  height: 36px;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: var(--text-lg);
  font-weight: var(--font-extrabold);
  color: var(--text-primary);
  line-height: 1;
  letter-spacing: var(--tracking-tight);
}

.logo-subtitle {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  font-weight: var(--font-medium);
}

/* Desktop Nav */
.desktop-nav {
  display: none;
  align-items: center;
  gap: var(--space-1);
}

@media (min-width: 1024px) {
  .desktop-nav {
    display: flex;
  }
}

.nav-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--radius-lg);
  transition: all var(--duration-fast) var(--ease-default);
}

.nav-link:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
}

.nav-link.router-link-active {
  color: var(--color-primary-600);
  background: var(--color-primary-50);
}

.dark .nav-link.router-link-active {
  background: rgba(59, 130, 246, 0.1);
}

.nav-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 6px;
  font-size: 10px;
  font-weight: var(--font-bold);
  color: var(--color-primary-600);
  background: var(--color-primary-100);
  border-radius: var(--radius-full);
}

/* Nav Actions */
.nav-actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  color: var(--text-secondary);
  border-radius: var(--radius-lg);
  transition: all var(--duration-fast) var(--ease-default);
}

.action-btn:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
}

.favorites-btn {
  position: relative;
}

.favorites-count {
  position: absolute;
  top: 2px;
  right: 2px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  font-size: 10px;
  font-weight: var(--font-bold);
  color: white;
  background: var(--color-danger-500);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cta-btn {
  display: none;
}

@media (min-width: 768px) {
  .cta-btn {
    display: inline-flex;
  }
}

/* Mobile Menu Button */
.mobile-menu-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  color: var(--text-secondary);
  border-radius: var(--radius-lg);
}

@media (min-width: 1024px) {
  .mobile-menu-btn {
    display: none;
  }
}

/* Mobile Menu */
.mobile-menu {
  display: none;
  background: var(--bg-primary);
  border-top: 1px solid var(--border-default);
}

.mobile-menu.open {
  display: block;
}

@media (min-width: 1024px) {
  .mobile-menu {
    display: none !important;
  }
}

.mobile-menu-content {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--radius-lg);
  transition: all var(--duration-fast);
}

.mobile-nav-link:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.mobile-favorites-count {
  margin-left: auto;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  font-size: 11px;
  font-weight: var(--font-bold);
  color: white;
  background: var(--color-danger-500);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ═══════════════════════════════════════════════════════════════
   Hero Section
═══════════════════════════════════════════════════════════════ */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding-top: var(--header-height);
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #dbeafe 100%);
}

.dark .hero-bg {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at top right, rgba(59, 130, 246, 0.15), transparent 50%);
}

.hero-pattern {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(rgba(0, 0, 0, 0.03) 1px, transparent 1px);
  background-size: 20px 20px;
}

.dark .hero-pattern {
  background-image: radial-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px);
}

.hero-content {
  position: relative;
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-12);
  padding: var(--space-12) 0;
}

@media (min-width: 1024px) {
  .hero-content {
    grid-template-columns: 1fr 1fr;
    gap: var(--space-16);
    padding: var(--space-16) 0;
  }
}

.hero-text {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1-5) var(--space-3);
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary-600);
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  border-radius: var(--radius-full);
  width: fit-content;
  margin-bottom: var(--space-6);
}

.hero-title {
  font-size: var(--text-4xl);
  font-weight: var(--font-extrabold);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tighter);
  margin-bottom: var(--space-6);
}

@media (min-width: 768px) {
  .hero-title {
    font-size: var(--text-5xl);
  }
}

@media (min-width: 1024px) {
  .hero-title {
    font-size: var(--text-6xl);
  }
}

.gradient-text {
  background: linear-gradient(135deg, var(--color-primary-600) 0%, var(--color-secondary-500) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-description {
  font-size: var(--text-lg);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-8);
  max-width: 540px;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  margin-bottom: var(--space-10);
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: var(--space-6);
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.stat-number {
  font-size: var(--text-2xl);
  font-weight: var(--font-extrabold);
  color: var(--text-primary);
}

.stat-label {
  font-size: var(--text-sm);
  color: var(--text-tertiary);
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: var(--border-default);
}

/* Hero Visual */
.hero-visual {
  display: none;
  align-items: center;
  justify-content: center;
}

@media (min-width: 1024px) {
  .hero-visual {
    display: flex;
  }
}

.hero-card-stack {
  position: relative;
  width: 100%;
  max-width: 400px;
}

.hero-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  box-shadow: var(--shadow-lg);
  transition: all var(--duration-normal) var(--ease-default);
}

.hero-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
}

.hero-card.card-1 {
  position: relative;
  z-index: 3;
}

.hero-card.card-2 {
  position: absolute;
  top: 20px;
  left: 20px;
  right: -10px;
  z-index: 2;
  opacity: 0.9;
}

.hero-card.card-3 {
  position: absolute;
  top: 40px;
  left: 40px;
  right: -20px;
  z-index: 1;
  opacity: 0.8;
}

.hero-card .card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.card-id {
  font-size: var(--text-xs);
  font-family: var(--font-mono);
  color: var(--text-tertiary);
}

.hero-card h4 {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.hero-card p {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-4);
}

.hero-card .card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  padding-top: var(--space-3);
  border-top: 1px solid var(--border-default);
}

/* ═══════════════════════════════════════════════════════════════
   Sections Common
═══════════════════════════════════════════════════════════════ */
.section-header {
  text-align: center;
  margin-bottom: var(--space-12);
}

.section-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1) var(--space-3);
  background: var(--color-primary-50);
  color: var(--color-primary-600);
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  border-radius: var(--radius-full);
  margin-bottom: var(--space-4);
}

.dark .section-badge {
  background: rgba(59, 130, 246, 0.1);
}

.section-title {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--text-primary);
  margin-bottom: var(--space-4);
}

@media (min-width: 768px) {
  .section-title {
    font-size: var(--text-4xl);
  }
}

.section-description {
  font-size: var(--text-lg);
  color: var(--text-secondary);
  max-width: 600px;
  margin-inline: auto;
}

.section-footer {
  text-align: center;
  margin-top: var(--space-10);
}

/* ═══════════════════════════════════════════════════════════════
   Features Section
═══════════════════════════════════════════════════════════════ */
.features-section {
  padding: var(--space-20) 0;
  background: var(--bg-primary);
}

.features-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-6);
}

@media (min-width: 640px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.feature-card {
  padding: var(--space-6);
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  transition: all var(--duration-normal) var(--ease-default);
}

.feature-card:hover {
  border-color: var(--color-primary-200);
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}

.feature-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: var(--space-4);
}

.feature-card h3 {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.feature-card p {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-4);
}

.feature-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-primary-600);
  text-decoration: none;
  transition: gap var(--duration-fast);
}

.feature-link:hover {
  gap: var(--space-2);
}

/* ═══════════════════════════════════════════════════════════════
   Stats Section
═══════════════════════════════════════════════════════════════ */
.stats-section {
  padding: var(--space-20) 0;
  background: var(--bg-secondary);
}

.stats-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-12);
  align-items: center;
}

@media (min-width: 1024px) {
  .stats-content {
    grid-template-columns: 1fr 1fr;
  }
}

.stats-text h2 {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--text-primary);
  margin-bottom: var(--space-4);
}

@media (min-width: 768px) {
  .stats-text h2 {
    font-size: var(--text-4xl);
  }
}

.stats-text > p {
  font-size: var(--text-lg);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-8);
}

.stats-highlights {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  margin-bottom: var(--space-8);
}

.highlight-item {
  display: flex;
  gap: var(--space-4);
}

.highlight-icon {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-50);
  color: var(--color-primary-600);
  border-radius: var(--radius-lg);
}

.dark .highlight-icon {
  background: rgba(59, 130, 246, 0.1);
}

.highlight-item h4 {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.highlight-item p {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

/* Stats Visual */
.stats-visual {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
}

.stats-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: var(--space-4);
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  transition: all var(--duration-normal);
}

.stats-card:hover {
  box-shadow: var(--shadow-md);
}

.stats-card-icon {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-lg);
}

.stats-card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stats-card-number {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--text-primary);
  line-height: 1;
}

.stats-card-label {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
}

.stats-card-trend {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  padding: 2px 6px;
  border-radius: var(--radius-full);
}

.stats-card-trend.up {
  color: var(--color-success-600);
  background: rgba(34, 197, 94, 0.1);
}

.stats-card-trend.down {
  color: var(--color-danger-600);
  background: rgba(239, 68, 68, 0.1);
}

/* Mini Chart */
.mini-chart {
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
}

.mini-chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
}

.mini-chart-header span {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
}

.trend-indicator {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  padding: 2px 8px;
  border-radius: var(--radius-full);
}

.trend-indicator.up {
  color: var(--color-success-600);
  background: rgba(34, 197, 94, 0.1);
}

.mini-chart-bars {
  display: flex;
  align-items: flex-end;
  gap: var(--space-2);
  height: 100px;
  margin-bottom: var(--space-3);
}

.chart-bar {
  flex: 1;
  background: linear-gradient(180deg, var(--color-primary-400), var(--color-primary-600));
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  animation: fadeInUp var(--duration-slow) var(--ease-out) both;
}

.mini-chart-labels {
  display: flex;
  justify-content: space-between;
  font-size: var(--text-xs);
  color: var(--text-tertiary);
}

/* ═══════════════════════════════════════════════════════════════
   Workflow Section
═══════════════════════════════════════════════════════════════ */
.workflow-section {
  padding: var(--space-20) 0;
  background: var(--bg-primary);
}

.workflow-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-8);
}

@media (min-width: 768px) {
  .workflow-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.workflow-card {
  text-align: center;
  padding: var(--space-8);
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  transition: all var(--duration-normal);
  position: relative;
}

.workflow-card:hover {
  border-color: var(--color-primary-200);
  box-shadow: var(--shadow-lg);
}

.workflow-number {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  font-size: var(--text-4xl);
  font-weight: var(--font-extrabold);
  color: var(--text-primary);
  opacity: 0.05;
}

.workflow-icon {
  width: 72px;
  height: 72px;
  border-radius: var(--radius-2xl);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-inline: auto;
  margin-bottom: var(--space-5);
}

.workflow-card h3 {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-3);
}

.workflow-card p {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
}

/* ═══════════════════════════════════════════════════════════════
   Latest Section
═══════════════════════════════════════════════════════════════ */
.latest-section {
  padding: var(--space-20) 0;
  background: var(--bg-secondary);
}

.latest-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-6);
}

@media (min-width: 640px) {
  .latest-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .latest-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.letter-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  cursor: pointer;
  transition: all var(--duration-normal) var(--ease-default);
}

.letter-card:hover {
  border-color: var(--color-primary-300);
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}

.letter-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.letter-id {
  font-size: var(--text-xs);
  font-family: var(--font-mono);
  color: var(--text-tertiary);
}

.letter-company {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.letter-subject {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-4);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.letter-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: var(--space-3);
  border-top: 1px solid var(--border-default);
}

.letter-meta {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-xs);
  color: var(--text-tertiary);
}

.letter-office {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  color: var(--text-secondary);
  padding: 2px 8px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-full);
}

/* ═══════════════════════════════════════════════════════════════
   CTA Section
═══════════════════════════════════════════════════════════════ */
.cta-section {
  padding: var(--space-20) 0;
  background: linear-gradient(135deg, var(--color-primary-600) 0%, var(--color-primary-800) 100%);
}

.cta-content {
  text-align: center;
  max-width: 600px;
  margin-inline: auto;
}

.cta-content h2 {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: white;
  margin-bottom: var(--space-4);
}

@media (min-width: 768px) {
  .cta-content h2 {
    font-size: var(--text-4xl);
  }
}

.cta-content p {
  font-size: var(--text-lg);
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: var(--space-8);
}

.cta-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  justify-content: center;
}

.cta-section .btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-color: rgba(255, 255, 255, 0.3);
}

.cta-section .btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
}

/* ═══════════════════════════════════════════════════════════════
   Footer
═══════════════════════════════════════════════════════════════ */
.footer {
  background: var(--color-gray-900);
  color: var(--color-gray-300);
  padding: var(--space-16) 0 var(--space-8);
}

.footer-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-10);
  margin-bottom: var(--space-10);
}

@media (min-width: 768px) {
  .footer-content {
    grid-template-columns: 1.5fr 1fr;
  }
}

.footer-brand {
  max-width: 360px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.footer-logo span {
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  color: white;
}

.footer-brand p {
  font-size: var(--text-sm);
  color: var(--color-gray-400);
  line-height: var(--leading-relaxed);
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-8);
}

.footer-column h4 {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: white;
  margin-bottom: var(--space-4);
}

.footer-column a {
  display: block;
  font-size: var(--text-sm);
  color: var(--color-gray-400);
  text-decoration: none;
  padding: var(--space-1-5) 0;
  transition: color var(--duration-fast);
}

.footer-column a:hover {
  color: white;
}

.footer-bottom {
  padding-top: var(--space-8);
  border-top: 1px solid var(--color-gray-800);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--color-gray-500);
}

@media (min-width: 640px) {
  .footer-bottom {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

.footer-bottom a {
  color: var(--color-gray-400);
  text-decoration: none;
}

.footer-bottom a:hover {
  color: white;
}
</style>
