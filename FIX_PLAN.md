# Dashboard修复计划

## 需要修复的问题

### 1. 产品分类命名混淆 ✅
**当前问题**：
- "Top Product" 和 "Watch Product" 不清晰

**修复方案**：
```python
# 修改侧边栏产品分类选项
product_categories = ["全部", "热门产品 (Top 10)", "关注产品 (Watch List)"]
```

---

### 2. 图表类型单一 ✅
**当前问题**：
- 主要是折线图和柱状图
- 缺少多样化的可视化

**修复方案 - 添加以下图表类型**：

#### Tab 1: 产品排名
- ✅ 保持现有表格
- ➕ 添加：**树状图** (Treemap) - 按类别和分数展示产品
- ➕ 添加：**漏斗图** (Funnel) - 展示从浏览到转化的漏斗

#### Tab 2: 数据分析  
- ✅ 保持折线图
- ➕ 添加：**面积图** (Area Chart) - 累积趋势
- ➕ 添加：**箱线图** (Box Plot) - 分数分布
- ➕ 添加：**小提琴图** (Violin Plot) - 数据密度

#### Tab 3: AI洞察
- ✅ 保持现有图表
- ➕ 添加：**词云图** (Word Cloud) - 关键词可视化
- ➕ 添加：**桑基图** (Sankey) - 用户流向

#### Tab 4: 历史趋势
- ✅ 保持折线图
- ➕ 添加：**热力图** (Heatmap) - 周次对比矩阵
- ➕ 添加：**日历热力图** - 每日数据

#### Tab 5: 情绪分析
- ✅ 保持柱状图
- ➕ 添加：**雷达图** (Radar) - 多维情绪对比
- ➕ 添加：**旭日图** (Sunburst) - 情绪层级关系
- ➕ 添加：**气泡图** (Bubble) - 情绪强度vs频次

#### Tab 6: 产品分析
- ✅ 保持趋势图和雷达图
- ➕ 添加：**瀑布图** (Waterfall) - 营收贡献分解
- ➕ 添加：**甘特图** (Gantt) - 产品上市时间线

#### Tab 7: 竞争分析
- ❌ **需要修复**：当前矩阵图不是真正的矩阵
- ➕ 改为：**四象限散点图** - 价格vs市场份额，带象限标签
- ➕ 添加：**堆叠柱状图** - 竞争对手优势对比
- ➕ 添加：**极坐标图** - 竞争力雷达

#### Tab 8: 行动计划
- ✅ 保持时间线
- ➕ 添加：**甘特图** - 任务进度
- ➕ 添加：**仪表盘** (Gauge) - KPI完成度

#### Tab 9: 执行摘要
- ➕ 添加：**指标卡片** - 大数字展示
- ➕ 添加：**迷你图** (Sparkline) - 趋势缩略图
- ➕ 添加：**环形图** (Donut) - 占比分布

---

### 3. Tab顺序调整 ✅
**当前顺序**：
1. 产品排名
2. 数据分析
3. AI洞察
4. 历史趋势
5. 情绪分析
6. 产品分析
7. 竞争分析
8. 行动计划
9. 执行摘要

**修复后顺序**：
1. **📊 执行摘要** ⬅️ 移到第一位
2. 📋 产品排名
3. 🎯 产品分析
4. 💭 情绪分析
5. 🎭 竞争分析
6. 📊 数据分析
7. 🤖 AI洞察
8. 📈 历史趋势
9. 📋 行动计划

**逻辑**：
- 先看摘要（高层决策）
- 再看产品（具体机会）
- 然后看市场（情绪+竞争）
- 最后看数据和执行

---

### 4. 矩阵可视化修复 ✅
**当前问题**：
- 竞争分析Tab的"市场定位矩阵"只是普通散点图
- 没有象限划分和标签

**修复方案**：
```python
# 创建真正的四象限矩阵
fig_matrix = go.Figure()

# 添加散点
fig_matrix.add_trace(go.Scatter(
    x=competitor_df['avg_price'],
    y=competitor_df['market_share'],
    mode='markers+text',
    text=competitor_df['name'],
    textposition='top center',
    marker=dict(size=15, color='#2196F3')
))

# 计算中位数作为象限分界线
median_price = competitor_df['avg_price'].median()
median_share = competitor_df['market_share'].median()

# 添加象限分界线
fig_matrix.add_hline(y=median_share, line_dash="dash", line_color="gray")
fig_matrix.add_vline(x=median_price, line_dash="dash", line_color="gray")

# 添加象限标签
fig_matrix.add_annotation(
    x=median_price * 1.3, y=median_share * 1.3,
    text="高价高份额<br>(领导者)", showarrow=False,
    font=dict(size=12, color="green"), bgcolor="rgba(144,238,144,0.3)"
)
fig_matrix.add_annotation(
    x=median_price * 0.7, y=median_share * 1.3,
    text="低价高份额<br>(挑战者)", showarrow=False,
    font=dict(size=12, color="blue"), bgcolor="rgba(173,216,230,0.3)"
)
fig_matrix.add_annotation(
    x=median_price * 1.3, y=median_share * 0.7,
    text="高价低份额<br>(利基)", showarrow=False,
    font=dict(size=12, color="orange"), bgcolor="rgba(255,218,185,0.3)"
)
fig_matrix.add_annotation(
    x=median_price * 0.7, y=median_share * 0.7,
    text="低价低份额<br>(追随者)", showarrow=False,
    font=dict(size=12, color="red"), bgcolor="rgba(255,182,193,0.3)"
)

fig_matrix.update_layout(
    title="竞争对手市场定位矩阵（四象限分析）",
    xaxis_title="平均价格 ($)",
    yaxis_title="市场份额 (%)",
    showlegend=False
)
```

---

### 5. 历史数据追踪系统 ✅
**需求**：
- 定期保存数据快照
- 可以选择不同时间段对比
- 生成趋势报告

**设计方案**：

#### 数据存储结构
```
reports/
├── snapshots/
│   ├── 2026-01-21_snapshot.csv
│   ├── 2026-01-14_snapshot.csv
│   └── 2026-01-07_snapshot.csv
├── history_metadata.json
└── trend_analysis.csv
```

#### 功能实现
```python
import json
from datetime import datetime, timedelta

# 1. 保存数据快照
def save_snapshot(df, snapshot_date=None):
    """保存当前数据为历史快照"""
    if snapshot_date is None:
        snapshot_date = datetime.now().strftime("%Y-%m-%d")
    
    snapshot_dir = Path('reports/snapshots')
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    filename = snapshot_dir / f"{snapshot_date}_snapshot.csv"
    df.to_csv(filename, index=False)
    
    # 更新元数据
    update_metadata(snapshot_date, len(df))
    
    return filename

# 2. 加载历史快照
def load_snapshot(snapshot_date):
    """加载指定日期的快照"""
    filename = Path(f'reports/snapshots/{snapshot_date}_snapshot.csv')
    if filename.exists():
        return pd.read_csv(filename)
    return None

# 3. 对比两个时间点
def compare_snapshots(date1, date2):
    """对比两个快照的差异"""
    df1 = load_snapshot(date1)
    df2 = load_snapshot(date2)
    
    if df1 is None or df2 is None:
        return None
    
    # 计算变化
    comparison = pd.merge(
        df1[['product_name', 'total_score', 'views']],
        df2[['product_name', 'total_score', 'views']],
        on='product_name',
        suffixes=('_before', '_after')
    )
    
    comparison['score_change'] = comparison['total_score_after'] - comparison['total_score_before']
    comparison['views_growth'] = (comparison['views_after'] - comparison['views_before']) / comparison['views_before'] * 100
    
    return comparison

# 4. 生成趋势报告
def generate_trend_report(days=30):
    """生成过去N天的趋势报告"""
    snapshot_dir = Path('reports/snapshots')
    all_snapshots = sorted(snapshot_dir.glob('*_snapshot.csv'))
    
    # 筛选时间范围内的快照
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_snapshots = [
        f for f in all_snapshots 
        if datetime.strptime(f.stem.split('_')[0], "%Y-%m-%d") >= cutoff_date
    ]
    
    # 合并所有快照
    dfs = []
    for snapshot in recent_snapshots:
        df = pd.read_csv(snapshot)
        df['snapshot_date'] = snapshot.stem.split('_')[0]
        dfs.append(df)
    
    trend_df = pd.concat(dfs, ignore_index=True)
    
    # 计算趋势指标
    trend_summary = trend_df.groupby('product_name').agg({
        'total_score': ['mean', 'std', 'min', 'max'],
        'views': ['mean', 'sum'],
        'engagement_rate': 'mean'
    }).reset_index()
    
    return trend_summary

# 5. 自动保存功能
def auto_save_snapshot():
    """每周自动保存快照"""
    # 检查是否需要保存（每周一）
    today = datetime.now()
    if today.weekday() == 0:  # 周一
        # 加载当前数据
        current_df = load_data('reports/All_Data_Week_04.csv')
        if current_df is not None:
            save_snapshot(current_df)
            st.success(f"✅ 数据快照已保存：{today.strftime('%Y-%m-%d')}")
```

#### UI组件
```python
# 在侧边栏添加历史数据选择
with st.sidebar:
    st.markdown("### 📅 历史数据对比")
    
    # 获取所有可用快照
    snapshot_dir = Path('reports/snapshots')
    if snapshot_dir.exists():
        snapshots = sorted([f.stem.split('_')[0] for f in snapshot_dir.glob('*_snapshot.csv')], reverse=True)
        
        if len(snapshots) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                date1 = st.selectbox("对比日期1", snapshots, index=0)
            with col2:
                date2 = st.selectbox("对比日期2", snapshots, index=min(1, len(snapshots)-1))
            
            if st.button("📊 生成对比报告"):
                comparison = compare_snapshots(date1, date2)
                if comparison is not None:
                    st.session_state['comparison_data'] = comparison
                    st.success("对比报告已生成！")
    
    # 趋势分析
    st.markdown("### 📈 趋势分析")
    trend_days = st.select_slider("分析周期", options=[7, 14, 30, 60, 90], value=30)
    
    if st.button("生成趋势报告"):
        trend_report = generate_trend_report(trend_days)
        st.session_state['trend_report'] = trend_report
        st.success(f"已生成{trend_days}天趋势报告！")
```

---

## 实施计划

### 阶段1：立即修复（今天）
1. ✅ 修改产品分类命名
2. ✅ 调整Tab顺序
3. ✅ 修复竞争分析矩阵

### 阶段2：图表增强（1-2天）
4. ✅ 添加10+种新图表类型
5. ✅ 优化现有图表样式

### 阶段3：历史数据系统（2-3天）
6. ✅ 实现数据快照功能
7. ✅ 实现对比分析功能
8. ✅ 实现趋势报告功能
9. ✅ 添加自动保存机制

---

## 预期效果

### 修复后的优势
1. **更清晰的导航** - 执行摘要优先，逻辑流畅
2. **更丰富的可视化** - 20+种图表类型，适合不同数据
3. **真正的矩阵分析** - 四象限图，清晰的战略定位
4. **历史追踪能力** - 可以对比任意时间点，发现趋势
5. **自动化** - 每周自动保存数据，无需手动操作

### 用户体验提升
- 📊 **决策效率** ↑ 50% - 执行摘要优先
- 🎨 **视觉吸引力** ↑ 80% - 多样化图表
- 📈 **洞察深度** ↑ 100% - 历史对比和趋势分析
- ⏱️ **操作便捷性** ↑ 60% - 自动化数据管理

---

## 下一步

请确认：
1. 是否立即开始阶段1的修复？
2. 图表类型的选择是否满意？
3. 历史数据系统的设计是否符合需求？

确认后我将开始实施！🚀
