#!/bin/bash
# 资讯门户更新打包脚本
# 使用方法：bash package_portal_update.sh

set -e

echo "📦 开始打包资讯门户更新..."

# 创建临时目录
TEMP_DIR="/tmp/portal_update_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$TEMP_DIR"

# 复制修改过的文件
echo "📄 复制后端文件..."
cp backend/app/routers/portal.py "$TEMP_DIR/"
cp backend/app/models_new.py "$TEMP_DIR/"
cp backend/app/main.py "$TEMP_DIR/"

echo "📄 复制前端文件..."
mkdir -p "$TEMP_DIR/frontend/src/views"
mkdir -p "$TEMP_DIR/frontend/src/components"
mkdir -p "$TEMP_DIR/frontend/src/router"
cp frontend/src/views/PortalHome.vue "$TEMP_DIR/frontend/src/views/"
cp frontend/src/components/Navbar.vue "$TEMP_DIR/frontend/src/components/"
cp frontend/src/router/index.js "$TEMP_DIR/frontend/src/router/"

echo "📄 复制数据库迁移脚本..."
mkdir -p "$TEMP_DIR/scripts"
cp scripts/portal_migration.sql "$TEMP_DIR/scripts/"

echo "📄 复制文档..."
cp PORTAL_IMPLEMENTATION_PLAN.md "$TEMP_DIR/"
cp PORTAL_DEPLOYMENT_GUIDE.md "$TEMP_DIR/"
cp DEPLOYMENT_CHECKLIST_FOR_HERMES.md "$TEMP_DIR/"

# 创建压缩包
OUTPUT_FILE="portal_update_$(date +%Y%m%d).tar.gz"
tar -czf "$OUTPUT_FILE" -C /tmp "$(basename $TEMP_DIR)"

# 清理
rm -rf "$TEMP_DIR"

# 计算文件大小
FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)

echo ""
echo "✅ 打包完成！"
echo ""
echo "📦 文件信息："
echo "  - 文件名：$OUTPUT_FILE"
echo "  - 大小：$FILE_SIZE"
echo "  - 位置：$(pwd)/$OUTPUT_FILE"
echo ""
echo "📋 包含的文件："
echo "  后端："
echo "    - backend/app/routers/portal.py"
echo "    - backend/app/models_new.py"
echo "    - backend/app/main.py"
echo ""
echo "  前端："
echo "    - frontend/src/views/PortalHome.vue"
echo "    - frontend/src/components/Navbar.vue"
echo "    - frontend/src/router/index.js"
echo ""
echo "  数据库："
echo "    - scripts/portal_migration.sql"
echo ""
echo "  文档："
echo "    - PORTAL_IMPLEMENTATION_PLAN.md"
echo "    - PORTAL_DEPLOYMENT_GUIDE.md"
echo "    - DEPLOYMENT_CHECKLIST_FOR_HERMES.md"
echo ""
echo "🚀 下一步："
echo "  1. 上传到VPS：scp $OUTPUT_FILE root@你的VPS_IP:/root/"
echo "  2. 在VPS解压：cd /root/fda-warning-system && tar -xzf /root/$OUTPUT_FILE"
echo "  3. 执行部署清单：cat DEPLOYMENT_CHECKLIST_FOR_HERMES.md"
echo ""
