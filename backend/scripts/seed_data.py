#!/usr/bin/env python3
"""
PharmaCos Insight - Seed Data Script
Populates categories and sample articles into the database.
Run this ONCE after deploying the new code.

Usage:
  python -m backend.scripts.seed_data
  OR on VPS: docker exec fda-warning-backend python -m backend.scripts.seed_data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import SessionLocal, engine, Base
from app.models_new import Category, Article, User
from datetime import datetime

# Ensure tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ═══ Categories ═══
categories_data = [
    # Pharma
    {"name": "行业动态", "name_en": "Industry News", "slug": "industry-news", "sector": "pharma", "sort_order": 1},
    {"name": "政策法规", "name_en": "Regulations", "slug": "regulations", "sector": "pharma", "sort_order": 2},
    {"name": "GMP 实务", "name_en": "GMP Practice", "slug": "gmp-practice", "sector": "pharma", "sort_order": 3},
    {"name": "药典解读", "name_en": "Pharmacopoeia", "slug": "pharmacopoeia", "sector": "pharma", "sort_order": 4},
    {"name": "注册申报", "name_en": "Registration", "slug": "registration", "sector": "pharma", "sort_order": 5},
    {"name": "质量控制", "name_en": "Quality Control", "slug": "quality-control", "sector": "pharma", "sort_order": 6},
    {"name": "工艺验证", "name_en": "Process Validation", "slug": "process-validation", "sector": "pharma", "sort_order": 7},
    {"name": "案例研究", "name_en": "Case Studies", "slug": "pharma-case-studies", "sector": "pharma", "sort_order": 8},

    # Cosmetics
    {"name": "行业动态", "name_en": "Industry News", "slug": "cosmetics-industry", "sector": "cosmetics", "sort_order": 1},
    {"name": "政策法规", "name_en": "Regulations", "slug": "cosmetics-regulations", "sector": "cosmetics", "sort_order": 2},
    {"name": "配方与安全", "name_en": "Formulation & Safety", "slug": "formulation-safety", "sector": "cosmetics", "sort_order": 3},
    {"name": "功效评价", "name_en": "Efficacy Testing", "slug": "efficacy-testing", "sector": "cosmetics", "sort_order": 4},
    {"name": "原料合规", "name_en": "Ingredient Compliance", "slug": "ingredient-compliance", "sector": "cosmetics", "sort_order": 5},
    {"name": "标签与宣称", "name_en": "Labeling & Claims", "slug": "labeling-claims", "sector": "cosmetics", "sort_order": 6},
    {"name": "生产质量管理", "name_en": "Manufacturing QM", "slug": "manufacturing-qm", "sector": "cosmetics", "sort_order": 7},
    {"name": "市场趋势", "name_en": "Market Trends", "slug": "cosmetics-trends", "sector": "cosmetics", "sort_order": 8},

    # Food
    {"name": "行业动态", "name_en": "Industry News", "slug": "food-industry", "sector": "food", "sort_order": 1},
    {"name": "政策法规", "name_en": "Regulations", "slug": "food-regulations", "sector": "food", "sort_order": 2},
    {"name": "食品安全管理体系", "name_en": "Food Safety Mgmt", "slug": "food-safety-mgmt", "sector": "food", "sort_order": 3},
    {"name": "添加剂与新原料", "name_en": "Additives", "slug": "food-additives", "sector": "food", "sort_order": 4},
    {"name": "标签标识", "name_en": "Labeling", "slug": "food-labeling", "sector": "food", "sort_order": 5},
    {"name": "进出口合规", "name_en": "Import/Export", "slug": "food-import-export", "sector": "food", "sort_order": 6},
    {"name": "营养与健康声称", "name_en": "Nutrition Claims", "slug": "nutrition-claims", "sector": "food", "sort_order": 7},
    {"name": "市场趋势", "name_en": "Market Trends", "slug": "food-trends", "sector": "food", "sort_order": 8},

    # General
    {"name": "GMP 全景", "name_en": "GMP Panorama", "slug": "gmp-panorama", "sector": "general", "sort_order": 1},
    {"name": "药典对照", "name_en": "Pharma Compare", "slug": "pharma-compare", "sector": "general", "sort_order": 2},
    {"name": "法规库", "name_en": "Regulation Library", "slug": "regulation-library", "sector": "general", "sort_order": 3},
    {"name": "行业白皮书", "name_en": "White Papers", "slug": "white-papers", "sector": "general", "sort_order": 4},
]

print("═══ Seeding Categories ═══")
for cat_data in categories_data:
    existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
    if not existing:
        cat = Category(**cat_data)
        db.add(cat)
        print(f"  + {cat_data['sector']}/{cat_data['name']}")
    else:
        print(f"  = {cat_data['sector']}/{cat_data['name']} (exists)")

db.commit()

# ═══ Sample Articles ═══
print("\n═══ Seeding Sample Articles ═══")

# Get first category IDs for each sector
def get_cat_id(slug):
    cat = db.query(Category).filter(Category.slug == slug).first()
    return cat.id if cat else None

articles_data = [
    {
        "title": "FDA 483 观察项 Top 10 及企业应对策略",
        "slug": "fda-483-top-10-应对策略",
        "sector": "pharma",
        "category_slug": "gmp-practice",
        "summary": "本文梳理了近年来 FDA 483 观察项中最常见的十大缺陷类型，并为企业提供了切实可行的应对策略和预防措施。",
        "content": """# FDA 483 观察项 Top 10 及企业应对策略

## 引言

FDA Form 483 是 FDA 检查员在检查过程中发现的观察项（Observations）的记录文件。了解最常见的 483 观察项类型，有助于企业有针对性地完善质量体系。

## Top 10 观察项

### 1. 数据完整性问题 (Data Integrity)
数据完整性一直是 FDA 检查的重点。常见问题包括：
- 审计追踪功能未开启或被禁用
- 共享登录账号
- 原始数据与报告数据不一致
- 删除或覆盖原始数据

**应对策略：** 确保所有 GxP 系统启用审计追踪，实施唯一的用户账号管理，建立数据治理政策。

### 2. 偏差调查不充分 (Inadequate Deviation Investigation)
- 偏差调查未找到根本原因
- CAPA 有效性未验证
- 趋势分析缺失

**应对策略：** 采用结构化调查方法（如鱼骨图、5 Why），确保根本原因分析到位，CAPA 可追溯。

### 3. 设备清洁验证不足
- 清洁验证方案不完整
- 目视检查标准不明确
- 清洁剂残留限度未设定

### 4. 稳定性考察缺陷
### 5. 实验室控制不足
### 6. 变更控制不规范
### 7. 供应商管理缺陷
### 8. 人员培训记录不完整
### 9. 生产记录不准确
### 10. 质量部门职责未有效履行

## 结论

企业应定期进行内部审计，对照 483 观察项类型自查自纠，防患于未然。
""",
        "access_level": "free",
    },
    {
        "title": "2025 版中国药典重大变化总览",
        "slug": "2025-chp-major-changes",
        "sector": "pharma",
        "category_slug": "pharmacopoeia",
        "summary": "全面梳理 2025 版中国药典相较于 2020 版的重大变化，包括新增各论、方法更新和通用章节修订。",
        "content": """# 2025 版中国药典重大变化总览

## 概述

2025 版《中华人民共和国药典》（ChP 2025）是继 2020 版之后的又一次重大修订。本次修订在品种收载、检测方法、通用技术要求等方面均有显著变化。

## 主要变化

### 一、品种收载变化
- 新增中药各论 XX 个
- 新增化学药各论 XX 个
- 新增生物制品各论 XX 个
- 删除/合并部分不再适用的品种

### 二、检测方法更新
- 新增多种现代分析方法
- 更新杂质检查方法
- 强化元素杂质控制要求（通则 2321）

### 三、通用技术要求
- 无菌检查法修订
- 微生物限度检查法更新
- 稳定性试验指导原则完善

## 对企业的影响

企业需要：
1. 评估现有产品是否需要因药典变化而调整质量标准
2. 更新内部检验 SOP
3. 完成必要的方法验证/确认
4. 更新供应商质量协议中的药典引用
""",
        "access_level": "pro",
    },
    {
        "title": "化妆品安全评估报告全流程指南",
        "slug": "cosmetics-safety-assessment-guide",
        "sector": "cosmetics",
        "category_slug": "formulation-safety",
        "summary": "从法规要求到实操步骤，手把手教你完成化妆品安全评估报告的编写。",
        "content": """# 化妆品安全评估报告全流程指南

## 法规背景

根据《化妆品监督管理条例》及《化妆品安全评估技术导则（2021年版）》，所有普通化妆品在注册/备案时需提交安全评估报告。

## 评估流程

### 第一步：产品信息收集
- 配方信息（全部成分及用量）
- 产品使用方法和频率
- 目标人群
- 包装材料信息

### 第二步：各成分评估
- 查询《已使用化妆品原料目录》
- 收集各成分的毒理学数据
- 计算安全边际值（MoS）

### 第三步：产品整体评估
- 评估各成分间的相互作用
- 评估产品稳定性
- 评估微生物安全性

### 第四步：撰写评估报告
- 按照规定格式撰写
- 附上所有参考文献

## 常见问题

**Q: 哪些成分需要特别关注？**
A: 防腐剂、着色剂、防晒剂等有限量要求的成分，以及新原料。

**Q: MoS 值多少算安全？**
A: 一般要求 MoS ≥ 100。
""",
        "access_level": "free",
    },
    {
        "title": "HACCP 七大原理实操指南",
        "slug": "haccp-seven-principles-guide",
        "sector": "food",
        "category_slug": "food-safety-mgmt",
        "summary": "从原理到实践，详解 HACCP 七大原理的实施要点和常见误区。",
        "content": """# HACCP 七大原理实操指南

## 什么是 HACCP

HACCP（Hazard Analysis and Critical Control Points，危害分析与关键控制点）是一套系统性的食品安全管理方法，通过识别、评估和控制食品安全危害来保障食品的安全性。

## 七大原理

### 原理一：危害分析 (Hazard Analysis)
识别食品生产过程中可能存在的所有危害：
- 生物性危害（病原菌、病毒、寄生虫）
- 化学性危害（农药残留、重金属、添加剂超标）
- 物理性危害（金属碎片、玻璃、异物）

### 原理二：确定关键控制点 (CCP)
使用 CCP 决策树确定哪些步骤是关键控制点。

### 原理三：建立关键限值 (Critical Limits)
每个 CCP 必须有可测量的关键限值，如温度、时间、pH 值等。

### 原理四：建立监控程序
### 原理五：建立纠偏措施
### 原理六：建立验证程序
### 原理七：建立记录保持程序

## 实施建议
1. 组建跨部门 HACCP 团队
2. 完整描述产品和预期用途
3. 绘制详细的工艺流程图
4. 现场验证流程图的准确性
""",
        "access_level": "free",
    },
    {
        "title": "化妆品新原料备案全流程指南",
        "slug": "cosmetics-new-ingredient-filing",
        "sector": "cosmetics",
        "category_slug": "ingredient-compliance",
        "summary": "详解中国化妆品新原料注册/备案的完整流程、所需资料和注意事项。",
        "content": """# 化妆品新原料备案全流程指南

## 概述

根据《化妆品监督管理条例》，具有防腐、防晒、着色、染发、祛斑美白功能的新原料需注册，其他新原料实行备案管理。

## 备案流程

### 1. 前期准备
- 确认原料是否属于新原料（查询《已使用化妆品原料目录》）
- 确定注册/备案路径
- 准备安全性评估数据

### 2. 安全性评估
- 毒理学评估
- 稳定性评估
- 微生物学评估

### 3. 提交备案
- 通过 NMPA 化妆品注册备案信息服务平台提交
- 所需资料：配方/组成、制备工艺、质量控制标准、安全评估报告等

### 4. 备案后管理
- 3 年安全监测期
- 每年度报告

## 注意事项
- 新原料使用量不得超过安全评估的最大使用量
- 需建立完善的质量标准
""",
        "access_level": "pro",
    },
]

for art_data in articles_data:
    slug = art_data["slug"]
    existing = db.query(Article).filter(Article.slug == slug).first()
    if existing:
        print(f"  = {art_data['title']} (exists)")
        continue

    cat_id = get_cat_id(art_data["category_slug"])
    article = Article(
        title=art_data["title"],
        slug=slug,
        content=art_data["content"],
        summary=art_data["summary"],
        sector=art_data["sector"],
        category_id=cat_id,
        access_level=art_data.get("access_level", "free"),
        status="published",
        published_at=datetime.utcnow(),
        view_count=0,
        like_count=0,
    )
    db.add(article)
    print(f"  + {art_data['title']}")

db.commit()
db.close()

print("\n✅ Seed data complete!")
print(f"   Categories: {len(categories_data)}")
print(f"   Articles: {len(articles_data)}")
