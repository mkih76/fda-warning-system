<template>
  <div class="about-home">
    <section class="about-hero">
      <div class="about-container">
        <span class="about-badge">About</span>
        <h1>关于我们</h1>
        <p>中国制药·化妆品·食品从业者的国际化行业知识平台</p>
      </div>
    </section>
    <section class="about-section">
      <div class="about-container">
        <div class="about-content">
          <h2>平台愿景</h2>
          <p>PharmaCos Insight 致力于成为中国制药、化妆品、食品行业从业者获取国际行业知识、政策法规、合规实践的首选平台。我们通过 AI 技术与专业内容相结合，提供高质量的行业知识输出。</p>
          <h2>核心价值</h2>
          <ul>
            <li><strong>知识输出</strong> — 有深度、有体系的行业专业知识</li>
            <li><strong>政策解读</strong> — 第一时间解读中美欧最新监管政策</li>
            <li><strong>行业资讯</strong> — 覆盖制药、化妆品、食品三大行业</li>
            <li><strong>合规工具</strong> — FDA 警告信、GMP 清单、法规检索等</li>
          </ul>
          <h2>联系我们</h2>
          <p>如有合作意向或建议，请通过以下方式联系我们：</p>
          <p>邮箱：<a href="mailto:contact@example.com">contact@example.com</a></p>
          <p>GitHub：<a href="https://github.com/mkih76/fda-warning-system" target="_blank">github.com/mkih76/fda-warning-system</a></p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about-container { max-width: 800px; margin: 0 auto; padding: 0 32px; }
.about-hero { padding: 160px 0 80px; background: linear-gradient(135deg, #0000C9 0%, #000049 100%); color: #fff; text-align: center; }
.about-badge { display: inline-block; padding: 4px 16px; background: rgba(255,255,255,0.1); border-radius: 4px; font-size: 12px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 20px; }
.about-hero h1 { font-size: 48px; font-weight: 800; margin: 0 0 16px; }
.about-hero p { font-size: 18px; opacity: 0.9; margin: 0; }
.about-section { padding: 60px 0 80px; }
.about-content h2 { font-size: 24px; font-weight: 700; color: #000; margin: 40px 0 16px; padding-bottom: 8px; border-bottom: 2px solid #0000C9; }
.about-content h2:first-child { margin-top: 0; }
.about-content p { font-size: 16px; color: #333; line-height: 1.8; margin: 0 0 16px; }
.about-content ul { margin: 0 0 16px 24px; }
.about-content li { font-size: 16px; color: #333; line-height: 1.8; margin-bottom: 8px; }
.about-content a { color: #0000C9; }
@media (max-width: 1024px) { .about-container { padding: 0 16px; } .about-hero { padding: 120px 0 60px; } }
</style>
