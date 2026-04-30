<template>
  <div class="tools-home">
    <section class="tools-hero">
      <div class="tools-container">
        <span class="tools-badge">Tools</span>
        <h1>实用工具</h1>
        <p>合规辅助工具集，提升工作效率</p>
      </div>
    </section>
    <section class="tools-section">
      <div class="tools-container">
        <div class="tools-grid">
          <router-link to="/letters" class="tool-card">
            <h3>FDA 警告信查询</h3>
            <p>搜索、筛选、分析 FDA 警告信数据库</p>
            <span class="tool-status available">可用</span>
          </router-link>
          <div class="tool-card disabled">
            <h3>法规检索</h3>
            <p>跨行业、跨地区的法规全文搜索</p>
            <span class="tool-status coming">即将上线</span>
          </div>
          <div class="tool-card disabled">
            <h3>GMP 自查清单</h3>
            <p>交互式 GMP 合规自查工具</p>
            <span class="tool-status coming">即将上线</span>
          </div>
          <div class="tool-card disabled">
            <h3>术语词典</h3>
            <p>中英对照行业专业术语查询</p>
            <span class="tool-status coming">即将上线</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.tools-container { max-width: 1400px; margin: 0 auto; padding: 0 32px; }
.tools-hero { padding: 160px 0 80px; background: linear-gradient(135deg, #374151 0%, #111827 100%); color: #fff; }
.tools-badge { display: inline-block; padding: 4px 16px; background: rgba(255,255,255,0.1); border-radius: 4px; font-size: 12px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 20px; }
.tools-hero h1 { font-size: 48px; font-weight: 800; margin: 0 0 16px; }
.tools-hero p { font-size: 18px; opacity: 0.9; margin: 0; }
.tools-section { padding: 80px 0; }
.tools-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }
.tool-card { padding: 32px; background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; text-decoration: none; transition: all 0.2s; position: relative; }
.tool-card:not(.disabled):hover { border-color: #0000C9; box-shadow: 0 8px 24px rgba(0,0,0,0.08); transform: translateY(-4px); }
.tool-card.disabled { opacity: 0.6; cursor: default; }
.tool-card h3 { font-size: 18px; font-weight: 600; color: #000; margin: 0 0 10px; }
.tool-card p { font-size: 14px; color: #666; line-height: 1.7; margin: 0 0 16px; }
.tool-status { font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 4px; }
.tool-status.available { background: rgba(22,163,74,0.1); color: #16a34a; }
.tool-status.coming { background: rgba(245,158,11,0.1); color: #d97706; }
@media (max-width: 1024px) { .tools-container { padding: 0 16px; } .tools-grid { grid-template-columns: 1fr; } .tools-hero { padding: 120px 0 60px; } }
</style>
