#!/bin/bash
# Quick start script for Streamlit dashboard

echo "🖨️  启动3D打印市场情报仪表板..."
echo ""

# 检查数据文件
if [ ! -f "reports/All_Data_Week_04.csv" ]; then
    echo "⚠️  警告: 未找到数据文件"
    echo "请先运行: python3 run_weekly_report_v3.py"
    echo ""
    read -p "是否现在运行数据收集? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 run_weekly_report_v3.py
    else
        exit 1
    fi
fi

echo "✅ 数据文件检查完成"
echo ""
echo "🚀 启动Streamlit仪表板..."
echo "   本地访问: http://localhost:8501"
echo "   局域网访问: http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

streamlit run dashboard.py
