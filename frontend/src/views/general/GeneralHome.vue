<template>
  <div class="general-home">
    <section class="gen-hero">
      <div class="gen-container">
        <span class="gen-badge">General</span>
        <h1>综合知识库</h1>
        <p>跨行业的横向知识平台，整合 GMP 体系、药典对照、FDA 警告信、法规库等通用内容</p>
      </div>
    </section>

    <section class="gen-section">
      <div class="gen-container">
        <div class="gen-grid">
          <router-link to="/general/gmp-panorama" class="gen-card">
            <div class="gen-card-icon" style="background: #0000C9">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>
            </div>
            <h3>GMP 全景</h3>
            <p>中国 GMP、FDA cGMP、EU GMP 跨行业体系对照，检查要点与常见缺陷分析</p>
          </router-link>

          <router-link to="/general/pharma-compare" class="gen-card">
            <div class="gen-card-icon" style="background: #2563eb">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
            </div>
            <h3>药典对照</h3>
            <p>中国药典、USP、EP、JP 方法差异对比，药典更新追踪与解读</p>
          </router-link>

          <router-link to="/letters" class="gen-card">
            <div class="gen-card-icon" style="background: #dc2626">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
            </div>
            <h3>FDA 警告信数据库</h3>
            <p>986+ 封警告信，AI 智能翻译与分析，支持全文检索和数据可视化</p>
          </router-link>

          <router-link to="/general/regulation-library" class="gen-card">
            <div class="gen-card-icon" style="background: #7c3aed">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"/></svg>
            </div>
            <h3>法规库</h3>
            <p>按行业、地区、主题分类的法规原文与解读，法规对比工具</p>
          </router-link>

          <router-link to="/general/white-papers" class="gen-card">
            <div class="gen-card-icon" style="background: #059669">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            </div>
            <h3>行业白皮书</h3>
            <p>定期发布的行业研究报告，深度分析行业趋势与合规实践</p>
          </router-link>

          <router-link to="/dashboard" class="gen-card">
            <div class="gen-card-icon" style="background: #ea580c">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M3 3v18h18M9 17V9m4 8V5m4 12v-4"/></svg>
            </div>
            <h3>数据看板</h3>
            <p>FDA 警告信数据可视化，年度趋势、办公室排名、状态分布</p>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.gen-container { max-width: 1400px; margin: 0 auto; padding: 0 32px; }

.gen-hero {
  padding: 160px 0 80px;
  background: linear-gradient(135deg, #1a1a2e 0%, #000049 100%);
  color: #fff;
}

.gen-badge {
  display: inline-block;
  padding: 4px 16px;
  background: rgba(255,255,255,0.1);
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 20px;
}

.gen-hero h1 { font-size: 48px; font-weight: 800; margin: 0 0 16px; }
.gen-hero p { font-size: 18px; opacity: 0.9; margin: 0; max-width: 600px; line-height: 1.7; }

.gen-section { padding: 80px 0; }

.gen-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.gen-card {
  padding: 32px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.2s;
}

.gen-card:hover {
  border-color: #0000C9;
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  transform: translateY(-4px);
}

.gen-card-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.gen-card h3 { font-size: 18px; font-weight: 600; color: #000; margin: 0 0 10px; }
.gen-card p { font-size: 14px; color: #666; line-height: 1.7; margin: 0; }

@media (max-width: 1024px) {
  .gen-container { padding: 0 16px; }
  .gen-grid { grid-template-columns: repeat(2, 1fr); }
  .gen-hero { padding: 120px 0 60px; }
  .gen-hero h1 { font-size: 36px; }
}

@media (max-width: 640px) {
  .gen-grid { grid-template-columns: 1fr; }
  .gen-hero h1 { font-size: 28px; }
}
</style>
