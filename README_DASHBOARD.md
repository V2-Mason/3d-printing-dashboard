# 🖨️ 3D打印市场情报仪表板

基于Streamlit的交互式数据可视化仪表板，用于分析TikTok上的3D打印产品趋势。

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

---

## 📊 功能特性

### 核心功能
- ✅ **周次选择器** - 查看不同周次的数据
- ✅ **KPI指标卡片** - 总产品数、平均分、浏览量、点赞数、互动率
- ✅ **产品排名表格** - 支持搜索、排序、高亮显示
- ✅ **数据可视化** - 分数分布、类别占比、散点图、柱状图
- ✅ **AI深度分析** - 市场定位、目标受众、定价策略、风险评估
- ✅ **历史趋势分析** - 周次趋势、浏览量趋势、互动率趋势

### 高级功能
- 🔍 **智能筛选** - 按类别、分数范围筛选
- 📥 **数据导出** - 下载CSV格式数据
- 🎨 **自定义主题** - 科技蓝配色方案
- 📱 **响应式设计** - 支持桌面和移动端

---

## 🚀 快速开始

### 本地运行

#### 1. 安装依赖
```bash
pip install -r requirements.txt
```

#### 2. 启动仪表板
```bash
streamlit run dashboard.py
```

或使用快捷脚本：
```bash
./start_dashboard.sh
```

#### 3. 访问仪表板
浏览器会自动打开，或访问：
- **本地**: http://localhost:8501
- **局域网**: http://您的IP:8501

---

## 🌐 云端部署

### 部署到Streamlit Cloud

1. **Fork此仓库**到您的GitHub账号

2. **登录Streamlit Cloud**
   - 访问: https://share.streamlit.io/
   - 使用GitHub账号登录

3. **创建新应用**
   - 点击 "New app"
   - 选择您的仓库
   - 主文件: `dashboard.py`
   - 点击 "Deploy"

4. **获得公开URL**
   - 例如: `https://your-app.streamlit.app`

详细部署指南请参考: [STREAMLIT_DEPLOYMENT_GUIDE.md](STREAMLIT_DEPLOYMENT_GUIDE.md)

---

## 📁 项目结构

```
market_intelligence/
├── dashboard.py                      # 主仪表板应用
├── start_dashboard.sh                # 快速启动脚本
├── requirements.txt                  # Python依赖
├── .streamlit/
│   └── config.toml                   # Streamlit配置
├── reports/                          # 数据文件目录
│   ├── All_Data_Week_04.csv
│   ├── Top_Products_Week_04.csv
│   └── ...
├── run_weekly_report_v3.py           # 数据收集脚本
└── STREAMLIT_DEPLOYMENT_GUIDE.md     # 完整部署指南
```

---

## 🔄 数据更新

### 每周更新流程

#### 1. 收集数据
```bash
python3 run_weekly_report_v3.py
```

#### 2. 查看仪表板

**本地运行**：
```bash
streamlit run dashboard.py
```

**云端部署**：
```bash
git add reports/
git commit -m "Update week XX data"
git push
```

Streamlit Cloud会自动检测更新并刷新仪表板。

---

## 📊 数据来源

- **TikTok视频数据** - 通过TikTok API收集
- **AI分析** - 使用OpenAI GPT-4进行深度分析
- **趋势分析** - 周环比变化分析

### 数据字段说明

| 字段 | 说明 |
|------|------|
| week_number | 周次编号 |
| product_name | 产品名称 |
| product_category | 产品类别 (Top Product / Watch Product) |
| total_score | 综合评分 (0-100) |
| views | 浏览量 |
| likes | 点赞数 |
| engagement_rate | 互动率 (%) |
| ai_market_positioning | AI分析: 市场定位 |
| ai_target_audience | AI分析: 目标受众 |
| ai_pricing_strategy | AI分析: 定价策略 |
| ai_risks | AI分析: 风险评估 |

---

## 🎨 自定义配置

### 修改主题
编辑 `.streamlit/config.toml`：
```toml
[theme]
primaryColor = "#2196F3"      # 主色调
backgroundColor = "#FFFFFF"    # 背景色
textColor = "#2C3E50"         # 文字颜色
```

### 添加密码保护
在Streamlit Cloud设置中启用 "Require viewers to log in"

---

## 🆘 常见问题

### Q: 显示"未找到数据文件"？
**A**: 运行数据收集脚本：
```bash
python3 run_weekly_report_v3.py
```

### Q: 如何更新云端数据？
**A**: 推送更新到GitHub：
```bash
git add reports/
git commit -m "Update data"
git push
```

### Q: 如何分享给团队？
**A**: 
- **本地**: 分享局域网URL
- **云端**: 分享Streamlit Cloud URL

更多问题请参考: [STREAMLIT_DEPLOYMENT_GUIDE.md](STREAMLIT_DEPLOYMENT_GUIDE.md)

---

## 📚 技术栈

- **Python 3.11+**
- **Streamlit** - Web应用框架
- **Pandas** - 数据处理
- **Plotly** - 交互式图表
- **OpenAI GPT-4** - AI分析

---

## 📄 许可证

本项目为内部使用，仅供3D打印市场情报分析。

---

## 📞 支持

如有问题或建议，请查看：
- [完整部署指南](STREAMLIT_DEPLOYMENT_GUIDE.md)
- [Streamlit官方文档](https://docs.streamlit.io/)

---

**创建日期**: 2026-01-20  
**版本**: v1.0  
**维护者**: Manus AI Agent

---

## 🎉 开始使用

```bash
# 克隆仓库
git clone https://github.com/your-username/3d-printing-dashboard.git
cd 3d-printing-dashboard

# 安装依赖
pip install -r requirements.txt

# 启动仪表板
streamlit run dashboard.py
```

祝您使用愉快！🚀
