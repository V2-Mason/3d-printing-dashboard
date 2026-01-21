# 🔐 Google Drive API 配置指南

## 第一步：创建Google Cloud项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 点击顶部的项目下拉菜单
3. 点击 "新建项目"
4. 项目名称：`3d-printing-data-collection`
5. 点击 "创建"

## 第二步：启用Google Drive API

1. 在左侧菜单中，选择 "API和服务" > "库"
2. 搜索 "Google Drive API"
3. 点击 "Google Drive API"
4. 点击 "启用"

## 第三步：创建服务账号

1. 在左侧菜单中，选择 "API和服务" > "凭据"
2. 点击 "+ 创建凭据" > "服务账号"
3. 服务账号名称：`streamlit-dashboard`
4. 服务账号ID：自动生成
5. 点击 "创建并继续"
6. 角色：选择 "基本" > "编辑者"
7. 点击 "继续"
8. 点击 "完成"

## 第四步：创建密钥

1. 在凭据页面，找到刚创建的服务账号
2. 点击服务账号邮箱（例如：streamlit-dashboard@xxx.iam.gserviceaccount.com）
3. 切换到 "密钥" 标签
4. 点击 "添加密钥" > "创建新密钥"
5. 密钥类型：选择 "JSON"
6. 点击 "创建"
7. JSON文件会自动下载到您的电脑

## 第五步：共享Google Drive文件夹

1. 打开 [Google Drive](https://drive.google.com)
2. 找到 `3d-printing-data` 文件夹
3. 右键点击 > "共享"
4. 在 "添加用户和群组" 中，粘贴服务账号邮箱
   （例如：`streamlit-dashboard@xxx.iam.gserviceaccount.com`）
5. 权限设置为 "编辑者"
6. 取消勾选 "通知用户"
7. 点击 "共享"

## 第六步：获取文件夹ID

1. 在Google Drive中打开 `3d-printing-data` 文件夹
2. 查看浏览器地址栏，URL格式为：
   ```
   https://drive.google.com/drive/folders/FOLDER_ID_HERE
   ```
3. 复制 `FOLDER_ID_HERE` 部分（例如：`1a2b3c4d5e6f7g8h9i0j`）

## 第七步：准备配置信息

您需要以下信息：

1. **JSON密钥文件内容**（第四步下载的文件）
2. **文件夹ID**（第六步获取的ID）

---

## ✅ 完成后告诉我

当您完成以上步骤后，请告诉我：
1. JSON密钥文件已准备好（不要在消息中发送，我会指导您如何安全配置）
2. 文件夹ID：`您的文件夹ID`

然后我会帮您配置Streamlit Cloud！
