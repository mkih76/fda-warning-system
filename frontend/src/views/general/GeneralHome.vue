<template>
  <div class="general-home">
    <!-- Hero Section with Background Image -->
    <section class="gen-hero">
      <div class="hero-content">
        <div class="gen-container">
          <span class="gen-badge">General Knowledge Base</span>
          <h1>综合知识库</h1>
          <p>跨行业的横向知识平台，整合 GMP 体系、药典对照、FDA 警告信、法规库等通用内容</p>
        </div>
      </div>
    </section>

    <!-- Feature Cards Grid -->
    <section class="gen-section">
      <div class="gen-container">
        <div class="gen-grid">
          <router-link to="/general/gmp-panorama" class="gen-card">
            <div class="card-image">
              <img src="https://images.unsplash.com/photo-1582719471384-894fbb16e074?w=600&q=75" alt="GMP Panorama" loading="lazy">
              <div class="card-overlay"></div>
            </div>
            <div class="card-content">
              <div class="gen-card-icon" style="background: #0000C9">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
                </svg>
              </div>
              <h3>GMP 全景</h3>
              <p>中国 GMP、FDA cGMP、EU GMP 跨行业体系对照，检查要点与常见缺陷分析</p>
            </div>
          </router-link>

          <router-link to="/general/pharma-compare" class="gen-card">
            <div class="card-image">
              <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=75" alt="Pharmacopoeia Comparison" loading="lazy">
              <div class="card-overlay"></div>
            </div>
            <div class="card-content">
              <div class="gen-card-icon" style="background: #2563eb">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                </svg>
              </div>
              <h3>药典对照</h3>
              <p>中国药典、USP、EP、JP 方法差异对比，药典更新追踪与解读</p>
            </div>
          </router-link>

          <router-link to="/letters" class="gen-card">
            <div class="card-image">
              <img src="https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600&q=75" alt="FDA Warning Letters" loading="lazy">
              <div class="card-overlay"></div>
            </div>
            <div class="card-content">
              <div class="gen-card-icon" style="background: #dc2626">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
              </div>
              <h3>FDA 警告信数据库</h3>
              <p>986+ 封警告信，AI 智能翻译与分析，支持全文检索和数据可视化</p>
            </div>
          </router-link>

          <router-link to="/general/regulation-library" class="gen-card">
            <div class="card-image">
              <img src="https://images.unsplash.com/photo-1589994965851-a8f479c573a9?w=600&q=75" alt="Regulation Library" loading="lazy">
              <div class="card-overlay"></div>
            </div>
            <div class="card-content">
              <div class="gen-card-icon" style="background: #7c3aed">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <path d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"/>
                </svg>
              </div>
              <h3>法规库</h3>
              <p>按行业、地区、主题分类的法规原文与解读，法规对比工具</p>
            </div>
          </router-link>

          <router-link to="/general/white-papers" class="gen-card">
            <div class="card-image">
              <img src="https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=600&q=75" alt="White Papers" loading="lazy">
              <div class="card-overlay"></div>
            </div>
            <div class="card-content">
              <div class="gen-card-icon" style="background: #059669">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
              </div>
              <h3>行业白皮书</h3>
              <p>定期发布的行业研究报告，深度分析行业趋势与合规实践</p>
            </div>
          </router-link>

          <router-link to="/dashboard" class="gen-card">
            <div class="card-image">
              <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=75" alt="Dashboard" loading="lazy">
              <div class="card-overlay"></div>
            </div>
            <div class="card-content">
              <div class="gen-card-icon" style="background: #ea580c">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                  <path d="M3 3v18h18M9 17V9m4 8V5m4 12v-4"/>
                </svg>
              </div>
              <h3>数据看板</h3>
              <p>FDA 警告信数据可视化，年度趋势、办公室排名、状态分布</p>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="gen-stats">
      <div class="gen-container">
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-number">986+</div>
            <div class="stat-label">FDA 警告信</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">50+</div>
            <div class="stat-label">法规条目</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">100%</div>
            <div class="stat-label">AI 智能翻译</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">24/7</div>
            <div class="stat-label">实时更新</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Container */
.gen-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
}

/* Hero Section */
.gen-hero {
  position: relative;
  padding: 160px 0 100px;
  background-image: linear-gradient(135deg, rgba(0,0,0,0.75) 0%, rgba(0,0,73,0.85) 100%), url('https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1600&q=80');
  background-size: cover;
  background-position: center 30%;
  background-repeat: no-repeat;
  color: #fff;
  margin-bottom: 0;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.gen-badge {
  display: inline-block;
  padding: 6px 20px;
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(8px);
  border-radius: 40px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 24px;
  font-family: system-ui, -apple-system, 'Noto Sans', Arial, sans-serif;
}

.gen-hero h1 {
  font-size: 56px;
  font-weight: 800;
  margin: 0 0 20px;
  line-height: 1.2;
  letter-spacing: -0.02em;
  font-family: system-ui, -apple-system, 'Noto Sans', Arial, sans-serif;
}

.gen-hero p {
  font-size: 18px;
  opacity: 0.92;
  margin: 0;
  max-width: 600px;
  line-height: 1.6;
  font-weight: 400;
}

/* Cards Section */
.gen-section {
  padding: 80px 0;
  background: #f8f9fc;
}

.gen-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}

.gen-card {
  background: #fff;
  border-radius: 20px;
  overflow: hidden;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.2, 0, 0, 1);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
}

.gen-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0,0,201,0.12);
  border-color: transparent;
}

.card-image {
  position: relative;
  height: 180px;
  overflow: hidden;
  background: #e5e7eb;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.gen-card:hover .card-image img {
  transform: scale(1.05);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent 60%, rgba(0,0,0,0.1));
}

.card-content {
  padding: 24px 28px 32px;
  flex: 1;
}

.gen-card-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  transition: transform 0.2s;
}

.gen-card:hover .gen-card-icon {
  transform: scale(1.05);
}

.gen-card h3 {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 12px;
  letter-spacing: -0.01em;
  font-family: system-ui, -apple-system, 'Noto Sans', Arial, sans-serif;
}

.gen-card p {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
  margin: 0;
}

/* Stats Section */
.gen-stats {
  background: linear-gradient(135deg, #0000C9 0%, #00008f 100%);
  color: #fff;
  padding: 70px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
  text-align: center;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 42px;
  font-weight: 800;
  margin-bottom: 12px;
  letter-spacing: -0.02em;
  font-family: system-ui, -apple-system, 'Noto Sans', Arial, sans-serif;
}

.stat-label {
  font-size: 15px;
  opacity: 0.85;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Responsive */
@media (max-width: 1200px) {
  .gen-container {
    padding: 0 24px;
  }
}

@media (max-width: 1024px) {
  .gen-hero {
    padding: 120px 0 80px;
  }
  .gen-hero h1 {
    font-size: 42px;
  }
  .gen-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
  .stats-grid {
    gap: 30px;
  }
  .stat-number {
    font-size: 36px;
  }
}

@media (max-width: 768px) {
  .gen-section {
    padding: 60px 0;
  }
  .gen-hero {
    padding: 100px 0 60px;
  }
  .gen-hero h1 {
    font-size: 34px;
  }
  .gen-hero p {
    font-size: 16px;
  }
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 32px;
  }
}

@media (max-width: 640px) {
  .gen-container {
    padding: 0 20px;
  }
  .gen-grid {
    grid-template-columns: 1fr;
  }
  .gen-hero h1 {
    font-size: 28px;
  }
  .card-content {
    padding: 20px 24px 28px;
  }
  .stat-number {
    font-size: 32px;
  }
  .stat-label {
    font-size: 13px;
  }
  .gen-stats {
    padding: 50px 0;
  }
}

/* Typography enhancements */
* {
  font-family: system-ui, -apple-system, 'Noto Sans', Arial, sans-serif;
}

h1, h2, h3, h4, .stat-number, .gen-badge {
  font-weight: 600;
}
</style>
