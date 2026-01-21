# 数据结构分析 - 基于现有TikTok数据

## 📊 一、现有数据结构

### 1.1 数据来源
**平台**：TikTok（抖音国际版）
**数据类型**：3D打印产品视频数据
**当前周次**：第04周（2026-01-20）
**产品数量**：10个产品（5个Top Product + 5个Watch Product）

### 1.2 数据字段清单（21个字段）

#### 基础信息字段
| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `week_number` | 整数 | 周次编号 | 4 |
| `year` | 整数 | 年份 | 2026 |
| `report_date` | 日期 | 报告日期 | 2026-01-20 |
| `product_rank` | 整数 | 产品排名 | 1, 2, 3... |
| `product_category` | 文本 | 产品类别 | "Top Product" / "Watch Product" |
| `product_name` | 文本 | 产品名称/描述 | "3D printed Shoes..." |
| `tiktok_url` | URL | TikTok视频链接 | https://www.tiktok.com/@... |

#### 评分字段（5个维度）
| 字段名 | 类型 | 说明 | 范围 |
|--------|------|------|------|
| `total_score` | 浮点数 | 总分 | 0-100 |
| `views_score` | 浮点数 | 浏览量得分 | 0-100 |
| `engagement_score` | 浮点数 | 互动得分 | 0-100 |
| `trend_score` | 浮点数 | 趋势得分 | 0-100 |
| `demand_score` | 浮点数 | 需求得分 | 0-100 |

#### 互动数据字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `views` | 整数 | 浏览量 |
| `likes` | 整数 | 点赞数 |
| `comments` | 整数 | 评论数 |
| `shares` | 整数 | 分享数 |
| `engagement_rate` | 浮点数 | 互动率(%) |

#### AI分析字段（4个维度）
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `ai_market_positioning` | 长文本 | AI市场定位分析 |
| `ai_target_audience` | 长文本 | AI目标受众分析 |
| `ai_pricing_strategy` | 长文本 | AI定价策略建议 |
| `ai_risks` | 长文本 | AI风险评估 |

**注意**：Watch Product类别的产品没有AI分析字段（为空）

---

## 🗂️ 二、现有文件结构

```
reports/
├── All_Data_Week_04.csv           # 完整数据（10行，21列）
├── Summary_Week_04.csv            # 摘要统计
├── Top_Products_Week_04.csv       # Top产品（5行）
└── Watch_Products_Week_04.csv     # Watch产品（5行）
```

### 文件说明

**1. All_Data_Week_04.csv**
- 包含所有产品的完整数据
- 21个字段全部包含
- 既有Top Product也有Watch Product

**2. Top_Products_Week_04.csv**
- 只包含Top Product（前5名）
- 包含完整的AI分析字段
- 字段名格式略有不同（首字母大写，空格分隔）

**3. Watch_Products_Week_04.csv**
- 只包含Watch Product（观察产品）
- 不包含AI分析字段
- 字段较少（9个字段）

**4. Summary_Week_04.csv**
- 汇总统计数据
- Key-Value格式

---

## 📋 三、数据收集标准模板

### 3.1 标准CSV格式（基于All_Data格式）

```csv
week_number,year,report_date,product_rank,product_category,product_name,total_score,views_score,engagement_score,trend_score,demand_score,views,likes,comments,shares,engagement_rate,tiktok_url,ai_market_positioning,ai_target_audience,ai_pricing_strategy,ai_risks
```

### 3.2 数据收集规范

#### 必填字段（所有产品）
- `week_number`: 周次编号（递增）
- `year`: 年份
- `report_date`: 收集日期（YYYY-MM-DD）
- `product_rank`: 排名（1-N）
- `product_category`: "Top Product" 或 "Watch Product"
- `product_name`: 产品描述
- `total_score`: 总分（0-100）
- `tiktok_url`: 视频链接

#### 评分字段（必填，0-100）
- `views_score`
- `engagement_score`
- `trend_score`
- `demand_score`

#### 互动数据（必填，整数）
- `views`
- `likes`
- `comments`
- `shares`
- `engagement_rate`（计算得出）

#### AI分析字段（Top Product必填，Watch Product可选）
- `ai_market_positioning`
- `ai_target_audience`
- `ai_pricing_strategy`
- `ai_risks`

---

## 🎯 四、数据收集工作流程

### 当前流程（手动）
```
1. 在TikTok上搜索3D打印相关视频
   ↓
2. 筛选热门视频（浏览量、互动率高）
   ↓
3. 记录视频数据（浏览、点赞、评论、分享）
   ↓
4. 计算各项得分（views_score, engagement_score等）
   ↓
5. 使用AI分析产品（市场定位、目标受众、定价、风险）
   ↓
6. 整理成CSV文件
   ↓
7. 保存到reports/文件夹
   ↓
8. 上传到Dashboard
```

### 建议优化流程（半自动）
```
1. 手动收集TikTok视频链接（10-20个）
   ↓
2. 使用脚本批量抓取视频数据
   ↓
3. 自动计算评分
   ↓
4. 批量调用AI API进行分析
   ↓
5. 自动生成CSV文件
   ↓
6. 一键上传到Google Drive
   ↓
7. Dashboard自动加载新周次数据
```

---

## 💾 五、Google Drive存储结构设计

```
Google Drive: 3d-printing-data/
├── week_01/
│   ├── All_Data_Week_01.csv
│   ├── Top_Products_Week_01.csv
│   ├── Watch_Products_Week_01.csv
│   ├── Summary_Week_01.csv
│   └── metadata.json              # 收集时间、数据源等
├── week_02/
│   └── ...
├── week_03/
│   └── ...
├── week_04/                        # 当前周次
│   ├── All_Data_Week_04.csv
│   ├── Top_Products_Week_04.csv
│   ├── Watch_Products_Week_04.csv
│   ├── Summary_Week_04.csv
│   └── metadata.json
└── config/
    ├── data_schema.json            # 数据字段定义
    └── collection_log.json         # 收集历史记录
```

### metadata.json 示例
```json
{
  "week_number": 4,
  "year": 2026,
  "collection_date": "2026-01-20",
  "collector": "manual",
  "data_source": "TikTok",
  "total_products": 10,
  "top_products": 5,
  "watch_products": 5,
  "keywords_used": [
    "3d printing",
    "3d printed",
    "3d printer"
  ],
  "notes": "手动收集，重点关注鞋类和定制产品"
}
```

---

## 🔧 六、Dashboard集成方案

### 6.1 周次选择器改造

**当前**：硬编码 `["第 01 周", "第 02 周", "第 03 周", "第 04 周"]`

**改造后**：动态加载Google Drive中的周次
```python
def get_available_weeks():
    """从Google Drive获取所有可用周次"""
    weeks = []
    result = subprocess.run(
        ['rclone', 'lsf', 'manus_google_drive:3d-printing-data/', 
         '--config', '/home/ubuntu/.gdrive-rclone.ini'],
        capture_output=True, text=True
    )
    for line in result.stdout.strip().split('\n'):
        if line.startswith('week_'):
            week_num = int(line.split('_')[1].rstrip('/'))
            weeks.append(f"第 {week_num:02d} 周")
    return sorted(weeks)
```

### 6.2 数据加载函数

```python
def load_week_data(week_number):
    """从Google Drive加载指定周次的数据"""
    # 1. 从Google Drive下载CSV到临时目录
    temp_dir = f"/tmp/week_{week_number:02d}"
    os.makedirs(temp_dir, exist_ok=True)
    
    # 2. 使用rclone下载
    subprocess.run([
        'rclone', 'copy',
        f'manus_google_drive:3d-printing-data/week_{week_number:02d}/',
        temp_dir,
        '--config', '/home/ubuntu/.gdrive-rclone.ini'
    ])
    
    # 3. 读取CSV
    df = pd.read_csv(f"{temp_dir}/All_Data_Week_{week_number:02d}.csv")
    return df
```

### 6.3 数据上传界面

在侧边栏添加：
```python
st.sidebar.markdown("---")
st.sidebar.subheader("📤 数据管理")

# 文件上传
uploaded_file = st.sidebar.file_uploader(
    "上传新周次数据",
    type=['csv'],
    help="上传All_Data_Week_XX.csv文件"
)

if uploaded_file:
    # 解析周次
    week_number = extract_week_number(uploaded_file.name)
    
    if st.sidebar.button("💾 保存到Google Drive"):
        with st.spinner("正在上传..."):
            upload_to_gdrive(uploaded_file, week_number)
        st.success(f"✅ 第 {week_number:02d} 周数据已保存！")
        st.experimental_rerun()
```

---

## 📝 七、数据收集操作手册

### 7.1 每周数据收集步骤

**第1步：准备CSV模板**
- 复制上周的CSV文件
- 修改week_number和report_date
- 清空所有产品数据行

**第2步：收集TikTok数据**
- 搜索关键词："3d printing", "3d printed"
- 筛选过去7天内的热门视频
- 记录视频链接和基础数据

**第3步：填写数据**
- 按排名填写product_rank（1-10）
- 前5个标记为"Top Product"
- 后5个标记为"Watch Product"
- 填写所有互动数据

**第4步：AI分析**
- 对Top Product进行AI分析
- 生成市场定位、目标受众、定价策略、风险评估

**第5步：上传到Dashboard**
- 打开Dashboard侧边栏
- 点击"上传新周次数据"
- 选择CSV文件
- 点击"保存到Google Drive"

**第6步：验证**
- 在周次选择器中选择新周次
- 检查所有数据是否正确显示

---

## 🚀 八、下一步实施计划

### Phase 1: 基础功能（立即实施）
- ✅ 创建Google Drive文件夹结构
- ✅ 修改Dashboard周次选择器为动态加载
- ✅ 实现数据上传功能
- ✅ 测试数据加载和显示

### Phase 2: 半自动化（1-2周后）
- 🔄 创建数据收集辅助脚本
- 🔄 批量AI分析工具
- 🔄 数据验证和质量检查

### Phase 3: 全自动化（等Etsy API）
- ⏳ 集成Etsy API
- ⏳ 自动数据收集
- ⏳ 定时任务和通知

---

**准备好开始实施了吗？** 🎯
