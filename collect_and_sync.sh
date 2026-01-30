#!/bin/bash
# One-click automated data collection and sync script
# Usage: ./collect_and_sync.sh [week_number]

set -e

echo "========================================"
echo "  自动数据收集与同步系统"
echo "========================================"
echo ""

# Determine next week number
if [ -z "$1" ]; then
    # Auto-detect next week
    LAST_WEEK=$(ls /home/ubuntu/week_*_data/ 2>/dev/null | tail -1 | grep -o '[0-9]\+' || echo "6")
    WEEK_NUMBER=$((LAST_WEEK + 1))
    echo "📅 自动检测：收集第 $WEEK_NUMBER 周数据"
else
    WEEK_NUMBER=$1
    echo "📅 手动指定：收集第 $WEEK_NUMBER 周数据"
fi

echo ""

# Step 1: Collect data
echo "🔄 步骤 1/3: 收集数据..."
cd /home/ubuntu/3d-printing-dashboard
echo "$WEEK_NUMBER" | python3 data_collector.py

if [ $? -ne 0 ]; then
    echo "❌ 数据收集失败"
    exit 1
fi

echo ""

# Step 2: Upload to Google Drive
echo "☁️  步骤 2/3: 上传到 Google Drive..."
WEEK_DIR=$(printf "week_%02d_data" $WEEK_NUMBER)
rclone copy /home/ubuntu/${WEEK_DIR}/ \
    manus_google_drive:"Market Intelligence Data/" \
    --config /home/ubuntu/.gdrive-rclone.ini \
    -v

if [ $? -ne 0 ]; then
    echo "❌ 上传失败"
    exit 1
fi

echo ""

# Step 3: Sync to dashboard
echo "📊 步骤 3/3: 同步到 Dashboard..."
python3 sync_data_from_gdrive.py

if [ $? -ne 0 ]; then
    echo "⚠️  同步警告（Dashboard 会自动同步）"
fi

echo ""
echo "========================================"
echo "  ✅ 完成！"
echo "========================================"
echo ""
echo "📊 第 $WEEK_NUMBER 周数据已准备就绪"
echo "🌐 Dashboard 将在 2-3 分钟后自动更新"
echo "🔗 访问: https://3d-printing-dashboard-afddl4mkziis7paeshgqnt.streamlit.app/"
echo ""
