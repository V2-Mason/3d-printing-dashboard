# GitHub + Streamlit Cloud 部署步骤

## 🎯 目标
将您的Streamlit仪表板部署到云端，获得一个24/7在线的公开URL。

---

## 📋 前提条件

- ✅ GitHub账号（如果没有，访问 https://github.com/signup 注册）
- ✅ Streamlit Cloud账号（您已有）
- ✅ Git已安装（检查：`git --version`）

---

## 🚀 部署步骤

### 第1步：在GitHub创建新仓库

#### 1.1 登录GitHub
访问: https://github.com/

#### 1.2 创建新仓库
1. 点击右上角 **"+"** → **"New repository"**
2. 填写仓库信息：
   - **Repository name**: `3d-printing-dashboard`（或您喜欢的名字）
   - **Description**: `3D打印市场情报仪表板 - Streamlit Dashboard`
   - **Public** 或 **Private**（Streamlit Cloud免费版只支持Public）
   - **不要**勾选 "Add a README file"（我们已经有了）
3. 点击 **"Create repository"**

#### 1.3 记录仓库URL
例如: `https://github.com/您的用户名/3d-printing-dashboard.git`

---

### 第2步：初始化本地Git仓库

#### 2.1 进入项目目录
```bash
cd /home/ubuntu/market_intelligence
```

#### 2.2 初始化Git
```bash
git init
```

#### 2.3 配置Git用户信息（如果还没配置）
```bash
git config --global user.name "您的名字"
git config --global user.email "您的邮箱"
```

---

### 第3步：添加文件到Git

#### 3.1 查看要提交的文件
```bash
git status
```

#### 3.2 添加核心文件
```bash
# 添加仪表板文件
git add dashboard.py
git add start_dashboard.sh
git add requirements.txt
git add .streamlit/config.toml
git add .gitignore

# 添加文档
git add README_DASHBOARD.md
git add STREAMLIT_DEPLOYMENT_GUIDE.md
git add GITHUB_DEPLOYMENT_STEPS.md

# 添加示例数据（重要：Streamlit Cloud需要数据文件）
git add reports/All_Data_Week_04.csv
git add reports/Top_Products_Week_04.csv
git add reports/Watch_Products_Week_04.csv
git add reports/Summary_Week_04.csv
```

#### 3.3 提交
```bash
git commit -m "Initial commit: Add Streamlit dashboard for 3D printing market intelligence"
```

---

### 第4步：推送到GitHub

#### 4.1 添加远程仓库
```bash
git remote add origin https://github.com/您的用户名/3d-printing-dashboard.git
```

#### 4.2 推送代码
```bash
git branch -M main
git push -u origin main
```

**如果提示输入用户名和密码**：
- 用户名：您的GitHub用户名
- 密码：使用 **Personal Access Token**（不是GitHub密码）
  - 创建Token: https://github.com/settings/tokens
  - 勾选 `repo` 权限
  - 复制Token并粘贴

---

### 第5步：在Streamlit Cloud部署

#### 5.1 登录Streamlit Cloud
访问: https://share.streamlit.io/

使用GitHub账号登录（会自动授权）

#### 5.2 创建新应用
1. 点击 **"New app"** 按钮
2. 填写应用信息：
   - **Repository**: 选择 `您的用户名/3d-printing-dashboard`
   - **Branch**: `main`
   - **Main file path**: `dashboard.py`
   - **App URL** (可选): 自定义URL前缀
3. 点击 **"Deploy!"**

#### 5.3 等待部署
- 部署通常需要2-5分钟
- 可以查看实时日志
- 部署成功后会显示 "Your app is live!" ✅

#### 5.4 获得公开URL
例如: `https://3d-printing-dashboard.streamlit.app`

---

### 第6步：测试和验证

#### 6.1 访问URL
在浏览器中打开您的Streamlit Cloud URL

#### 6.2 检查功能
- ✅ 周次选择器工作正常
- ✅ KPI卡片显示数据
- ✅ 产品表格可以搜索和排序
- ✅ 图表正常显示
- ✅ AI分析内容完整

#### 6.3 分享给团队
复制URL分享给团队成员

---

## 🔄 后续更新流程

### 更新数据

#### 1. 本地收集新数据
```bash
cd /home/ubuntu/market_intelligence
python3 run_weekly_report_v3.py
```

#### 2. 提交并推送
```bash
git add reports/
git commit -m "Update week XX data"
git push
```

#### 3. 自动部署
Streamlit Cloud会自动检测到更新并重新部署（约1-2分钟）

### 更新代码

#### 1. 修改代码
```bash
# 编辑 dashboard.py
nano dashboard.py
```

#### 2. 提交并推送
```bash
git add dashboard.py
git commit -m "Update dashboard features"
git push
```

#### 3. 自动部署
Streamlit Cloud会自动重新部署

---

## 🔒 安全设置（可选）

### 添加密码保护

#### 1. 在Streamlit Cloud应用设置中
1. 进入您的应用页面
2. 点击右上角 **"Settings"**
3. 找到 **"Sharing"** 部分
4. 启用 **"Require viewers to log in"**
5. 添加允许访问的邮箱地址

### 使用私有仓库

如果您的数据敏感：
1. 将GitHub仓库设为Private
2. 升级到Streamlit Cloud Pro（$20/月）
3. 或者不上传数据文件，使用API读取

---

## 🎨 自定义域名（可选）

### Streamlit Cloud Pro功能

如果您想使用自定义域名（例如：`dashboard.your-company.com`）：

1. 升级到Streamlit Cloud Pro
2. 在应用设置中添加自定义域名
3. 在域名DNS设置中添加CNAME记录

---

## 🆘 常见问题

### Q1: 推送到GitHub时报错 "Permission denied"
**A**: 使用Personal Access Token而不是密码：
```bash
# 创建Token: https://github.com/settings/tokens
# 勾选 repo 权限
# 使用Token作为密码
```

### Q2: Streamlit Cloud部署失败
**A**: 检查：
1. `requirements.txt` 是否包含所有依赖
2. `dashboard.py` 文件路径是否正确
3. 查看部署日志中的错误信息

### Q3: 仪表板显示"未找到数据文件"
**A**: 确保已将示例数据文件推送到GitHub：
```bash
git add reports/*.csv
git commit -m "Add sample data"
git push
```

### Q4: 如何删除旧的周次数据？
**A**: 
```bash
# 删除旧文件
rm reports/All_Data_Week_01.csv

# 提交删除
git add reports/
git commit -m "Remove old data"
git push
```

### Q5: 如何回滚到之前的版本？
**A**: 
```bash
# 查看提交历史
git log

# 回滚到特定提交
git revert <commit_hash>
git push
```

### Q6: Streamlit Cloud应用太慢？
**A**: 
- 升级到Streamlit Cloud Pro（更多资源）
- 优化数据加载（使用缓存）
- 减少历史数据量

---

## 📊 部署检查清单

部署前请确认：

- [ ] ✅ GitHub仓库已创建
- [ ] ✅ 本地Git仓库已初始化
- [ ] ✅ 核心文件已添加到Git
- [ ] ✅ 示例数据文件已添加
- [ ] ✅ 代码已推送到GitHub
- [ ] ✅ Streamlit Cloud应用已创建
- [ ] ✅ 部署成功，应用可访问
- [ ] ✅ 所有功能测试通过
- [ ] ✅ URL已分享给团队

---

## 🎯 完整命令速查

### 初始部署
```bash
# 1. 初始化Git
cd /home/ubuntu/market_intelligence
git init
git config --global user.name "您的名字"
git config --global user.email "您的邮箱"

# 2. 添加文件
git add dashboard.py start_dashboard.sh requirements.txt .streamlit/ .gitignore
git add README_DASHBOARD.md STREAMLIT_DEPLOYMENT_GUIDE.md
git add reports/*.csv

# 3. 提交
git commit -m "Initial commit: Add Streamlit dashboard"

# 4. 推送到GitHub
git remote add origin https://github.com/您的用户名/3d-printing-dashboard.git
git branch -M main
git push -u origin main
```

### 后续更新
```bash
# 1. 更新数据
python3 run_weekly_report_v3.py

# 2. 提交并推送
git add reports/
git commit -m "Update week XX data"
git push
```

---

## 🎉 完成！

恭喜！您的Streamlit仪表板已成功部署到云端！

**下一步**：
1. 访问您的Streamlit Cloud URL
2. 测试所有功能
3. 分享URL给团队成员
4. 设置密码保护（可选）
5. 每周更新数据

---

**创建日期**: 2026-01-20  
**版本**: v1.0  
**维护者**: Manus AI Agent

祝您使用愉快！🚀
