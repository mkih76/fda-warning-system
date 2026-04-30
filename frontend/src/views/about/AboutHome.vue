<template>
  <div class="about-home">
    <!-- Hero Section with Background Image -->
    <section class="about-hero">
      <div class="hero-overlay"></div>
      <div class="about-container hero-content">
        <span class="about-badge">About</span>
        <h1>关于我们</h1>
        <p>中国制药·化妆品·食品从业者的国际化行业知识平台</p>
      </div>
    </section>

    <!-- Main Content Section -->
    <section class="about-section">
      <div class="about-container">
        <div class="about-content">
          <!-- 平台愿景 -->
          <div class="content-block">
            <div class="block-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#0000C9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="#0000C9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="#0000C9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="block-text">
              <h2>平台愿景</h2>
              <p>PharmaCos Insight 致力于成为中国制药、化妆品、食品行业从业者获取国际行业知识、政策法规、合规实践的首选平台。我们通过 AI 技术与专业内容相结合，提供高质量的行业知识输出。</p>
            </div>
          </div>

          <!-- 核心价值 -->
          <div class="content-block">
            <div class="block-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L15 8.5L22 9.5L17 14L18.5 21L12 17.5L5.5 21L7 14L2 9.5L9 8.5L12 2Z" stroke="#0000C9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 2L15 8.5L22 9.5L17 14L18.5 21L12 17.5L5.5 21L7 14L2 9.5L9 8.5L12 2Z" stroke="#0000C9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="block-text">
              <h2>核心价值</h2>
              <ul class="value-list">
                <li><span class="value-icon">📚</span><strong>知识输出</strong> — 有深度、有体系的行业专业知识</li>
                <li><span class="value-icon">📋</span><strong>政策解读</strong> — 第一时间解读中美欧最新监管政策</li>
                <li><span class="value-icon">📡</span><strong>行业资讯</strong> — 覆盖制药、化妆品、食品三大行业</li>
                <li><span class="value-icon">🔧</span><strong>合规工具</strong> — FDA 警告信、GMP 清单、法规检索等</li>
              </ul>
            </div>
          </div>

          <!-- 图片展示区 -->
          <div class="image-showcase">
            <img src="https://images.unsplash.com/photo-1573164713988-8665fc963095?w=800&q=75" alt="FDA regulatory compliance" loading="lazy">
          </div>

          <!-- 联系我们 -->
          <div class="content-block">
            <div class="block-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22 16.92V19.92C22.0011 20.1985 21.9441 20.4742 21.8325 20.7294C21.7209 20.9845 21.5573 21.2136 21.352 21.402C21.1467 21.5904 20.9046 21.7335 20.6409 21.8217C20.3771 21.91 20.0974 21.9415 19.82 21.914C17.9027 21.6906 16.0552 21.0191 14.44 19.958C12.9579 18.9848 11.7323 17.6852 10.86 16.17C9.78272 14.518 9.13324 12.6498 8.97 10.7C8.94254 10.4231 8.97415 10.1437 9.06273 9.88032C9.15131 9.6169 9.29478 9.3752 9.48375 9.17035C9.67272 8.9655 9.90245 8.80247 10.1587 8.69166C10.4149 8.58086 10.692 8.52488 10.97 8.52702H13.97C14.4087 8.52304 14.8345 8.6719 15.1761 8.94509C15.5177 9.21828 15.7525 9.59675 15.84 10.02C16.015 10.9463 16.3092 11.8463 16.71 12.68C17.0035 13.3057 17.0829 14.0108 16.9367 14.6851C16.7905 15.3595 16.425 15.9658 15.9 16.41L15.49 16.77C16.1003 17.8532 16.9252 18.801 17.9096 19.5467C18.894 20.2924 20.0132 20.8183 21.2 21.09C21.5448 21.1631 21.9044 21.0968 22.2 20.9C22.4783 20.6956 22.6689 20.3945 22.733 20.056C22.7741 19.8298 22.8188 19.559 22.8188 19.559" stroke="#0000C9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="block-text">
              <h2>联系我们</h2>
              <p>如有合作意向或建议，请通过以下方式联系我们：</p>
              <div class="contact-links">
                <a href="mailto:contact@example.com" class="contact-link">
                  <span class="contact-icon">✉️</span>
                  contact@example.com
                </a>
                <a href="https://github.com/mkih76/fda-warning-system" target="_blank" class="contact-link">
                  <span class="contact-icon">🐙</span>
                  github.com/mkih76/fda-warning-system
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about-home {
  background-color: #ffffff;
}

/* Container */
.about-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 32px;
  position: relative;
  z-index: 2;
}

/* Hero Section */
.about-hero {
  position: relative;
  padding: 160px 0 100px;
  background-image: url('https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1600&q=80');
  background-size: cover;
  background-position: center 30%;
  background-repeat: no-repeat;
  color: #ffffff;
  text-align: center;
  overflow: hidden;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0,0,201,0.85) 0%, rgba(0,0,73,0.95) 100%);
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.about-badge {
  display: inline-block;
  padding: 6px 20px;
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(4px);
  border-radius: 40px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 24px;
  border: 1px solid rgba(255,255,255,0.3);
}

.about-hero h1 {
  font-size: 56px;
  font-weight: 800;
  margin: 0 0 20px;
  letter-spacing: -0.02em;
  line-height: 1.2;
  text-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.about-hero p {
  font-size: 20px;
  opacity: 0.95;
  margin: 0;
  font-weight: 400;
  line-height: 1.5;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* Content Section */
.about-section {
  padding: 80px 0 100px;
  background: #ffffff;
}

.about-content {
  display: flex;
  flex-direction: column;
  gap: 56px;
}

.content-block {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.block-icon {
  flex-shrink: 0;
  width: 56px;
  height: 56px;
  background: #f0f4ff;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.block-icon:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,201,0.15);
}

.block-text {
  flex: 1;
}

.block-text h2 {
  font-size: 28px;
  font-weight: 700;
  color: #000000;
  margin: 0 0 16px;
  letter-spacing: -0.01em;
}

.block-text p {
  font-size: 16px;
  color: #4a5568;
  line-height: 1.7;
  margin: 0;
}

/* Value List */
.value-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.value-list li {
  font-size: 16px;
  color: #2d3748;
  line-height: 1.6;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #edf2f7;
}

.value-icon {
  font-size: 22px;
  width: 32px;
  text-align: center;
}

.value-list li strong {
  color: #0000C9;
  font-weight: 700;
  min-width: 90px;
}

/* Image Showcase */
.image-showcase {
  margin: 20px 0 10px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0,0,0,0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.image-showcase:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.12);
}

.image-showcase img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.image-showcase:hover img {
  transform: scale(1.02);
}

/* Contact Links */
.contact-links {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.contact-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  background: #f7fafc;
  border-radius: 12px;
  color: #0000C9;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s ease;
  border: 1px solid #e2e8f0;
}

.contact-link:hover {
  background: #edf2f7;
  border-color: #0000C9;
  transform: translateX(4px);
}

.contact-icon {
  font-size: 20px;
}

/* Responsive */
@media (max-width: 1024px) {
  .about-container {
    padding: 0 24px;
  }
  
  .about-hero {
    padding: 120px 0 80px;
  }
  
  .about-hero h1 {
    font-size: 44px;
  }
  
  .about-hero p {
    font-size: 18px;
  }
  
  .about-section {
    padding: 60px 0 80px;
  }
  
  .content-block {
    gap: 20px;
  }
  
  .block-icon {
    width: 48px;
    height: 48px;
  }
  
  .block-icon svg {
    width: 28px;
    height: 28px;
  }
  
  .block-text h2 {
    font-size: 26px;
  }
}

@media (max-width: 768px) {
  .about-container {
    padding: 0 20px;
  }
  
  .about-hero {
    padding: 100px 0 60px;
  }
  
  .about-hero h1 {
    font-size: 36px;
  }
  
  .about-hero p {
    font-size: 16px;
  }
  
  .about-section {
    padding: 50px 0 60px;
  }
  
  .content-block {
    flex-direction: column;
    gap: 16px;
  }
  
  .block-icon {
    width: 44px;
    height: 44px;
  }
  
  .block-text h2 {
    font-size: 24px;
    margin-bottom: 12px;
  }
  
  .value-list li {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .value-list li strong {
    min-width: auto;
  }
  
  .contact-links {
    flex-direction: column;
    gap: 12px;
  }
  
  .contact-link {
    justify-content: center;
  }
}
</style>