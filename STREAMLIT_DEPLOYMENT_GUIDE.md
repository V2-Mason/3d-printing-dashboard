# Streamlit仪表板部署指南

## 🎉 恭喜！您的Streamlit仪表板已经准备就绪

---

## 📦 已创建的文件

### 1. `dashboard.py` - 主仪表板应用
**功能包括**：
- ✅ 周次选择器（自动检测所有周次数据）
- ✅ 5个KPI指标卡片（产品数、平均分、浏览量、点赞数、互动率）
- ✅ 产品排名表格（支持搜索、排序、高亮显示）
- ✅ 数据可视化分析（分数分布、类别占比、散点图、柱状图）
- ✅ AI深度分析展示（市场定位、目标受众、定价策略、风险评估）
- ✅ 历史趋势分析（周次趋势、浏览量趋势、互动率趋势）
- ✅ 数据筛选（类别、分数范围）
- ✅ 数据下载（CSV导出）
- ✅ 自定义主题（科技蓝配色）

### 2. `requirements.txt` - Python依赖
已添加Streamlit相关依赖：
- streamlit>=1.31.0
- plotly>=5.18.0

### 3. `.streamlit/config.toml` - 配置文件
包含主题和服务器配置

---

## 🚀 部署方式

您有**两种部署方式**可选：

---

## 方式1：本地运行（立即可用）⭐

### 步骤1：安装依赖
```bash
cd /home/ubuntu/market_intelligence
pip install streamlit plotly
```

### 步骤2：启动仪表板
```bash
streamlit run dashboard.py
```

### 步骤3：访问仪表板
浏览器会自动打开，或访问：
- **本地**: http://localhost:8501
- **局域网**: http://您的IP:8501

### 优势
- ✅ 立即可用，无需注册
- ✅ 数据完全在本地，安全
- ✅ 修改代码立即生效

### 适合场景
- 个人使用
- 内网团队访问
- 快速测试和迭代

---

## 方式2：部署到Streamlit Cloud（24/7在线）🌐

### 前提条件
- ✅ GitHub账号
- ✅ Streamlit Cloud账号（您已有）

### 步骤1：创建GitHub仓库

#### 1.1 初始化Git仓库
```bash
cd /home/ubuntu/market_intelligence
git init
```

#### 1.2 创建.gitignore文件
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/

# Data files (可选：如果数据敏感，不上传)
# reports/*.csv
# reports/*.xlsx
# reports/*.pdf

# Secrets
.env
*.key
*.pem

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
```

#### 1.3 添加文件并提交
```bash
git add dashboard.py
git add requirements.txt
git add .streamlit/config.toml
git add reports/  # 包含示例数据
git commit -m "Add Streamlit dashboard for 3D printing market intelligence"
```

#### 1.4 推送到GitHub
```bash
# 在GitHub上创建新仓库（例如：3d-printing-dashboard）
# 然后执行：
git remote add origin https://github.com/您的用户名/3d-printing-dashboard.git
git branch -M main
git push -u origin main
```

### 步骤2：在Streamlit Cloud部署

#### 2.1 登录Streamlit Cloud
访问：https://share.streamlit.io/

#### 2.2 创建新应用
1. 点击 **"New app"** 按钮
2. 选择您的GitHub仓库：`您的用户名/3d-printing-dashboard`
3. 选择分支：`main`
4. 主文件路径：`dashboard.py`
5. 点击 **"Deploy!"**

#### 2.3 等待部署完成
- 通常需要2-5分钟
- 部署成功后会自动分配一个URL

#### 2.4 获得公开URL
例如：`https://3d-printing-dashboard.streamlit.app`

### 步骤3：配置数据更新（可选）

#### 选项A：使用GitHub Actions自动更新
创建 `.github/workflows/update_data.yml`：
```yaml
name: Update Data

on:
  schedule:
    - cron: '0 8 * * 1'  # 每周一早上8点
  workflow_dispatch:  # 手动触发

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run data collection
        run: python3 run_weekly_report_v3.py
      - name: Commit and push
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add reports/
          git commit -m "Update weekly data" || exit 0
          git push
```

#### 选项B：手动更新
```bash
# 本地运行数据收集
python3 run_weekly_report_v3.py

# 提交并推送
git add reports/
git commit -m "Update week XX data"
git push
```

Streamlit Cloud会自动检测到更新并重新部署。

### 优势
- ✅ 24/7在线访问
- ✅ 任何人都可以访问（通过URL）
- ✅ 自动更新（推送代码即可）
- ✅ 免费托管

### 适合场景
- 团队协作
- 远程访问
- 分享给客户/合作伙伴

---

## 📊 仪表板功能说明

### 主要功能

#### 1. **侧边栏配置**
- 周次选择（自动检测所有周次数据）
- 产品类别筛选（全部/Top Product/Watch Product）
- 总分范围筛选（滑块）
- 显示选项（AI分析、历史趋势）

#### 2. **KPI指标卡片**
- 总产品数
- 平均总分
- 总浏览量（自动格式化：K/M）
- 总点赞数
- 平均互动率

#### 3. **Tab 1: 产品排名**
- 搜索产品名称
- 排序选项（排名、总分、浏览量、互动率）
- 高亮显示（高分绿色、低分红色）
- 下载CSV功能

#### 4. **Tab 2: 数据分析**
- 总分分布直方图
- 产品类别占比饼图
- 浏览量vs互动率散点图
- Top 5产品对比柱状图

#### 5. **Tab 3: AI洞察**
- 选择产品查看详细分析
- 显示产品基本信息（排名、总分、类别）
- AI分析内容：
  - 🎯 市场定位
  - 👥 目标受众
  - 💰 定价策略
  - ⚠️ 风险评估
- TikTok视频链接

#### 6. **Tab 4: 历史趋势**
- 平均总分趋势（折线图）
- 总浏览量趋势（面积图）
- 平均互动率趋势（面积图）
- 产品类别趋势（多线图）

---

## 🔄 数据更新流程

### 每周工作流程

#### 第1步：收集数据
```bash
cd /home/ubuntu/market_intelligence
python3 run_weekly_report_v3.py
```

#### 第2步：查看仪表板

**本地运行**：
```bash
streamlit run dashboard.py
```

**云端部署**：
```bash
# 提交并推送
git add reports/
git commit -m "Update week XX data"
git push
```

Streamlit Cloud会自动检测更新并刷新仪表板（约1-2分钟）。

---

## 🎨 自定义配置

### 修改主题颜色
编辑 `.streamlit/config.toml`：
```toml
[theme]
primaryColor = "#2196F3"      # 主色调
backgroundColor = "#FFFFFF"    # 背景色
secondaryBackgroundColor = "#F5F7FA"  # 次要背景
textColor = "#2C3E50"         # 文字颜色
```

### 添加密码保护（Streamlit Cloud）
在Streamlit Cloud设置中：
1. 进入应用设置
2. 启用 "Require viewers to log in"
3. 添加允许访问的邮箱地址

### 自定义域名（付费功能）
Streamlit Cloud Pro支持自定义域名：
- 例如：`dashboard.your-company.com`

---

## 🆘 常见问题

### Q1: 本地运行报错 "ModuleNotFoundError: No module named 'streamlit'"
**A**: 安装依赖：
```bash
pip install streamlit plotly
```

### Q2: 仪表板显示"未找到数据文件"
**A**: 确保已运行数据收集脚本：
```bash
python3 run_weekly_report_v3.py
```

### Q3: Streamlit Cloud部署失败
**A**: 检查：
1. `requirements.txt` 是否包含所有依赖
2. GitHub仓库是否包含 `reports/` 目录和示例数据
3. 文件路径是否正确

### Q4: 如何更新云端数据？
**A**: 
```bash
# 本地更新数据
python3 run_weekly_report_v3.py

# 推送到GitHub
git add reports/
git commit -m "Update data"
git push
```

### Q5: 仪表板加载慢？
**A**: 
- 使用 `@st.cache_data` 装饰器（已添加）
- 减少数据量（筛选历史周次）
- 升级到Streamlit Cloud Pro（更多资源）

### Q6: 如何分享给团队？
**A**: 
- **本地运行**: 分享局域网URL（http://您的IP:8501）
- **云端部署**: 分享Streamlit Cloud URL

### Q7: 数据安全吗？
**A**: 
- **本地运行**: 数据完全在本地，不上传
- **云端部署**: 
  - 可以设置密码保护
  - 可以设置私有仓库（GitHub Pro）
  - 敏感数据可以不上传（使用API读取）

---

## 📚 进阶功能

### 1. 连接Google Drive数据
修改 `dashboard.py`：
```python
import subprocess

def load_data_from_gdrive(week_number):
    # 使用rclone下载最新数据
    subprocess.run([
        'rclone', 'copy',
        f'manus_google_drive:Market_Intelligence_Reports/2026/Sheets/All_Data_Week_{week_number:02d}.csv',
        'reports/',
        '--config', '/home/ubuntu/.gdrive-rclone.ini'
    ])
    return pd.read_csv(f'reports/All_Data_Week_{week_number:02d}.csv')
```

### 2. 添加实时刷新
```python
import time

# 添加自动刷新按钮
if st.button('🔄 刷新数据'):
    st.cache_data.clear()
    st.rerun()

# 或者自动刷新（每5分钟）
time.sleep(300)
st.rerun()
```

### 3. 添加用户认证
使用 `streamlit-authenticator` 库：
```bash
pip install streamlit-authenticator
```

### 4. 导出PDF报告
使用 `reportlab` 或 `weasyprint`：
```python
if st.button('📄 导出PDF报告'):
    # 生成PDF逻辑
    pass
```

---

## 🎯 最佳实践

### 1. 数据缓存
使用 `@st.cache_data` 装饰器缓存数据加载：
```python
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)
```

### 2. 性能优化
- 限制历史数据加载范围
- 使用数据采样（大数据集）
- 延迟加载（按需加载）

### 3. 用户体验
- 添加加载动画：`st.spinner('加载中...')`
- 提供清晰的错误提示
- 添加帮助文档

### 4. 安全性
- 不要在代码中硬编码密钥
- 使用环境变量或Streamlit Secrets
- 设置访问控制

---

## 📞 获取帮助

### 官方资源
- [Streamlit文档](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery) - 示例应用
- [Streamlit Forum](https://discuss.streamlit.io/) - 社区支持

### 视频教程
- YouTube搜索: "Streamlit tutorial"
- [Streamlit官方YouTube频道](https://www.youtube.com/c/Streamlit)

---

## ✅ 快速开始清单

- [ ] 1. 安装Streamlit: `pip install streamlit plotly`
- [ ] 2. 测试本地运行: `streamlit run dashboard.py`
- [ ] 3. 创建GitHub仓库
- [ ] 4. 推送代码到GitHub
- [ ] 5. 在Streamlit Cloud创建应用
- [ ] 6. 等待部署完成
- [ ] 7. 获得公开URL
- [ ] 8. 分享给团队
- [ ] 9. 设置数据自动更新（可选）
- [ ] 10. 配置密码保护（可选）

---

## 🎉 完成！

您的Streamlit仪表板已经准备就绪！

**下一步**：
1. 先本地测试：`streamlit run dashboard.py`
2. 确认功能正常后，部署到Streamlit Cloud
3. 分享URL给团队成员

祝您使用愉快！🚀

---

**创建日期**: 2026-01-20  
**版本**: v1.0  
**维护者**: Manus AI Agent
