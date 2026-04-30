<template>
  <div class="gmp-page">
    <div class="gmp-hero">
      <div class="gmp-container">
        <nav class="breadcrumb">
          <router-link to="/">首页</router-link><span>/</span>
          <router-link to="/general">综合</router-link><span>/</span>
          <span class="current">GMP 全景</span>
        </nav>
        <h1>GMP 全景</h1>
        <p>中国 GMP、FDA cGMP、EU GMP 跨行业体系对照与检查要点</p>
      </div>
    </div>

    <div class="gmp-container">
      <!-- GMP 体系对比表 -->
      <section class="gmp-section">
        <h2>三大 GMP 体系对比</h2>
        <div class="comparison-table-wrapper">
          <table class="comparison-table">
            <thead>
              <tr>
                <th>对比维度</th>
                <th>中国 GMP<br/><small>（NMPA）</small></th>
                <th>FDA cGMP<br/><small>（21 CFR 210/211）</small></th>
                <th>EU GMP<br/><small>（EudraLex Vol.4）</small></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>法规框架</strong></td>
                <td>《药品管理法》+ GMP 附录</td>
                <td>21 CFR Part 210/211 + Guidance</td>
                <td>EudraLex Volume 4 + Annexes</td>
              </tr>
              <tr>
                <td><strong>质量体系</strong></td>
                <td>质量保证 + 质量控制 + GMP</td>
                <td>CGMP 强调质量体系六大系统</td>
                <td>药品质量体系 (PQS) ICH Q10</td>
              </tr>
              <tr>
                <td><strong>验证要求</strong></td>
                <td>工艺验证附录 (2012)</td>
                <td>FDA PV Guide (2011) 三阶段</td>
                <td>Annex 15 确认与验证</td>
              </tr>
              <tr>
                <td><strong>数据完整性</strong></td>
                <td>2020年数据管理指南</td>
                <td>Data Integrity Guidance</td>
                <td>Annex 11 计算机化系统</td>
              </tr>
              <tr>
                <td><strong>检查频率</strong></td>
                <td>每 3-5 年（常规）</td>
                <td>每 2 年（风险分级）</td>
                <td>每 3 年（GMP 证书）</td>
              </tr>
              <tr>
                <td><strong>检查方式</strong></td>
                <td>GMP 认证检查</td>
                <td>Pre-approval / Surveillance</td>
                <td>Routine / For cause</td>
              </tr>
              <tr>
                <td><strong>缺陷分类</strong></td>
                <td>严重缺陷 / 一般缺陷</td>
                <td>483 Observations / Warning Letter</td>
                <td>Critical / Major / Other</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- CGMP 六大系统 -->
      <section class="gmp-section">
        <h2>FDA CGMP 六大系统</h2>
        <div class="systems-grid">
          <div v-for="system in cgmSystems" :key="system.name" class="system-card">
            <div class="system-header" :style="{ borderLeftColor: system.color }">
              <h4>{{ system.name }}</h4>
              <span class="system-en">{{ system.nameEn }}</span>
            </div>
            <ul>
              <li v-for="point in system.points" :key="point">{{ point }}</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- 常见 483 观察项 -->
      <section class="gmp-section">
        <h2>FDA 483 常见观察项 Top 10</h2>
        <p class="section-desc">以下为近年来 FDA 检查中最常出现的 483 观察项类型</p>
        <div class="top10-list">
          <div v-for="(item, i) in top483Items" :key="i" class="top10-item">
            <span class="top10-rank" :class="{ 'top-3': i < 3 }">{{ i + 1 }}</span>
            <div class="top10-content">
              <h4>{{ item.title }}</h4>
              <p>{{ item.desc }}</p>
            </div>
            <span class="top10-freq">{{ item.freq }}</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
const cgmSystems = [
  {
    name: '质量体系', nameEn: 'Quality System', color: '#0000C9',
    points: ['质量方针与目标', '管理评审', '质量风险管理', 'CAPA 系统', '年度产品质量回顾']
  },
  {
    name: '生产体系', nameEn: 'Production System', color: '#2563eb',
    points: ['工艺规程与批记录', '过程控制', '物料平衡', '中间体控制', '返工/重新加工']
  },
  {
    name: '设施设备体系', nameEn: 'Facilities & Equipment', color: '#7c3aed',
    points: ['厂房设计与洁净度', '设备确认与维护', '公用系统验证', '环境监测', '设备清洁']
  },
  {
    name: '物料体系', nameEn: 'Materials System', color: '#059669',
    points: ['供应商审计与管理', '物料取样与检验', '仓储条件控制', '物料追溯性', '标签管理']
  },
  {
    name: '实验室体系', nameEn: 'Laboratory System', color: '#ea580c',
    points: ['OOS/OOT 调查', '方法验证与转移', '稳定性考察', '标准品管理', '数据完整性']
  },
  {
    name: '包装标签体系', nameEn: 'Packaging & Labeling', color: '#dc2626',
    points: ['标签控制与防混', '包装验证', '标签样张审批', '发运记录', '召回机制']
  },
]

const top483Items = [
  { title: '数据完整性', desc: '审计追踪缺失、共享账号、原始数据与报告不一致', freq: '高频' },
  { title: '偏差调查不充分', desc: '未找到根本原因、CAPA 有效性未验证', freq: '高频' },
  { title: '设备清洁验证不足', desc: '清洁验证方案不完整、清洁剂残留未设定限度', freq: '高频' },
  { title: '稳定性考察缺陷', desc: '考察方案不完善、数据趋势未分析', freq: '中高频' },
  { title: '实验室控制不足', desc: 'OOS 调查不彻底、方法验证缺失', freq: '中高频' },
  { title: '变更控制不规范', desc: '变更未评估对已验证状态的影响', freq: '中频' },
  { title: '供应商管理缺陷', desc: '供应商审计缺失、质量协议不完善', freq: '中频' },
  { title: '人员培训不完整', desc: '培训记录缺失、岗位资质未确认', freq: '中频' },
  { title: '生产记录不准确', desc: '批记录填写不规范、关键参数未记录', freq: '中频' },
  { title: '质量部门职责未有效履行', desc: 'QA 放行流程不完善、职责不清', freq: '中频' },
]
</script>

<style scoped>
.gmp-container { max-width: 1200px; margin: 0 auto; padding: 0 32px; }

.gmp-hero {
  background: linear-gradient(135deg, #1a1a2e 0%, #000049 100%);
  color: #fff;
  padding: 160px 0 60px;
}

.breadcrumb { display: flex; gap: 8px; font-size: 13px; color: rgba(255,255,255,0.5); margin-bottom: 20px; }
.breadcrumb a { color: rgba(255,255,255,0.7); text-decoration: none; }
.breadcrumb a:hover { color: #fff; }

.gmp-hero h1 { font-size: 42px; font-weight: 800; margin: 0 0 12px; }
.gmp-hero p { font-size: 17px; opacity: 0.85; margin: 0; }

.gmp-section { padding: 60px 0; }
.gmp-section h2 { font-size: 26px; font-weight: 700; color: #000; margin: 0 0 24px; padding-bottom: 12px; border-bottom: 3px solid #0000C9; }
.section-desc { font-size: 15px; color: #666; margin: -16px 0 24px; }

/* Comparison Table */
.comparison-table-wrapper { overflow-x: auto; }
.comparison-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.comparison-table th { background: #0000C9; color: #fff; padding: 14px 16px; text-align: left; font-weight: 600; white-space: nowrap; }
.comparison-table th small { font-weight: 400; opacity: 0.8; }
.comparison-table td { padding: 12px 16px; border-bottom: 1px solid #e5e7eb; vertical-align: top; }
.comparison-table tr:nth-child(even) td { background: #F2F9FC; }
.comparison-table td:first-child { background: #f5f5f5; font-weight: 500; white-space: nowrap; }

/* Systems Grid */
.systems-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.system-card { border: 1px solid #e5e7eb; border-radius: 8px; padding: 24px; background: #fff; }
.system-header { border-left: 4px solid #0000C9; padding-left: 12px; margin-bottom: 16px; }
.system-header h4 { font-size: 16px; font-weight: 600; color: #000; margin: 0 0 2px; }
.system-en { font-size: 12px; color: #999; }
.system-card ul { margin: 0; padding-left: 20px; }
.system-card li { font-size: 13px; color: #444; margin-bottom: 6px; line-height: 1.5; }

/* Top 10 List */
.top10-list { display: flex; flex-direction: column; gap: 12px; }
.top10-item { display: flex; align-items: center; gap: 16px; padding: 16px 20px; background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; transition: all 0.2s; }
.top10-item:hover { border-color: #0000C9; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
.top10-rank { flex-shrink: 0; width: 36px; height: 36px; border-radius: 50%; background: #f5f5f5; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 700; color: #666; }
.top10-rank.top-3 { background: #0000C9; color: #fff; }
.top10-content { flex: 1; }
.top10-content h4 { font-size: 15px; font-weight: 600; color: #000; margin: 0 0 4px; }
.top10-content p { font-size: 13px; color: #666; margin: 0; }
.top10-freq { font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 4px; background: rgba(0,0,201,0.06); color: #0000C9; white-space: nowrap; }

@media (max-width: 1024px) {
  .gmp-container { padding: 0 16px; }
  .systems-grid { grid-template-columns: 1fr 1fr; }
  .gmp-hero h1 { font-size: 32px; }
}
@media (max-width: 640px) {
  .systems-grid { grid-template-columns: 1fr; }
  .top10-item { flex-wrap: wrap; }
}
</style>
