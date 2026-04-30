#!/bin/bash
# FDA警告信数据库备份脚本
# 用途：备份 /root/data/fda_warning.db 数据库
# 保留最近30天的备份文件

set -e

# 配置
DB_PATH="/root/data/fda_warning.db"
BACKUP_DIR="/root/backups/fda"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/fda_warning_$DATE.db"
RETENTION_DAYS=30

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 检查数据库是否存在
if [ ! -f "$DB_PATH" ]; then
    log "错误: 数据库文件 $DB_PATH 不存在"
    exit 1
fi

# 创建备份目录（如果不存在）
mkdir -p "$BACKUP_DIR"

# 执行备份
log "开始备份数据库: $DB_PATH"
log "备份目标: $BACKUP_FILE"

sqlite3 "$DB_PATH" ".backup '$BACKUP_FILE'"

if [ $? -eq 0 ] && [ -f "$BACKUP_FILE" ]; then
    FILE_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log "备份成功: $BACKUP_FILE (大小: $FILE_SIZE)"
else
    log "错误: 数据库备份失败"
    exit 1
fi

# 删除超过保留天数的备份文件
log "清理超过 $RETENTION_DAYS 天的旧备份..."
find "$BACKUP_DIR" -name "fda_warning_*.db" -type f -mtime +$RETENTION_DAYS -delete

# 统计剩余备份文件数量
BACKUP_COUNT=$(find "$BACKUP_DIR" -name "fda_warning_*.db" -type f | wc -l)
log "清理完成，当前保留 $BACKUP_COUNT 个备份文件"

# 显示最近5个备份文件
log "最近5个备份文件:"
ls -lth "$BACKUP_DIR"/fda_warning_*.db 2>/dev/null | head -5 | while read line; do
    log "  $line"
done

exit 0
