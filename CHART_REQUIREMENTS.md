# 用户提供的图表设计要求

基于用户上传的图片文件，需要实现以下图表：

## 1. 12种情绪强度分布 (Emotion Intensity Distribution)
**文件**: pasted_file_MOf02E_image.png (01:27)
**图表类型**: 雷达图 (Radar Chart)
**特点**:
- 12个情绪维度：Trust(信任), Surprise(惊喜), Joy(喜悦), Excitement(兴奋), Pride(自豪), Envy(嫉妒), Disgust(厌恶), Fear(恐惧), Anger(愤怒), Disappointment(失望), Anxiety(焦虑), Nostalgia(怀旧)
- 对比两周数据 (Week 3 vs Week 4)
- 深色背景
- 青色/蓝色渐变填充

## 2. 情绪趋势 (Emotion Trend)
**文件**: 2_emotion_trend.png (01:22)
**图表类型**: 折线图
**特点**:
- X轴: 时间
- Y轴: 强度 (0-10分)
- 多条情绪线对比

## 3. 情绪分布 (Emotion Distribution)
**文件**: 3_emotion_distribution.png (01:22)
**图表类型**: 柱状图或饼图
**特点**:
- 显示各情绪的占比或频次

## 4. 情绪机会矩阵 (Emotion Opportunity Matrix)
**文件**: 4_emotion_opportunity_matrix.png (01:22)
**图表类型**: 散点图矩阵
**特点**:
- X轴: 情绪强度
- Y轴: 商业机会
- 四象限分析

## 5. 评分分解 (Scoring Breakdown)
**文件**: 5_scoring_breakdown.png (01:22)
**图表类型**: 瀑布图或堆叠柱状图
**特点**:
- 展示总分的构成要素
- 各部分贡献度

## 6. 情绪关键词热力图 (Emotion Keyword Heatmap)
**文件**: 6_emotion_keyword_heatmap.png (01:22)
**图表类型**: 热力图
**特点**:
- X轴: 时间或关键词
- Y轴: 情绪类型
- 颜色: 强度

## 7. 情绪组合桑基图 (Emotion Combination Sankey)
**文件**: 7_emotion_combination_sankey.png (01:22)
**图表类型**: 桑基图 (Sankey Diagram)
**特点**:
- 展示情绪之间的流转关系
- 情绪组合模式

## 其他图表
**文件**: pasted_file_yQ0uRe_image.png, pasted_file_PflgOW_image.png, pasted_file_4GI87N_image.png (01:27)
需要查看这些图片了解具体要求

---

## 实现优先级

### 高优先级（立即实现）
1. ✅ 12种情绪强度分布雷达图 - 最重要的可视化
2. ✅ 情绪机会矩阵 - 四象限分析
3. ✅ 情绪关键词热力图 - 展示趋势

### 中优先级（本周完成）
4. ✅ 情绪组合桑基图 - 复杂但有价值
5. ✅ 评分分解图 - 清晰展示构成
6. ✅ 情绪趋势折线图 - 基础但必要

### 低优先级（后续优化）
7. ✅ 情绪分布图 - 相对简单

---

## 技术实现

### 雷达图 (Plotly)
```python
import plotly.graph_objects as go

fig = go.Figure()

# Week 3 data
fig.add_trace(go.Scatterpolar(
    r=[6, 7, 8, 7, 5, 3, 2, 3, 4, 5, 4, 6],
    theta=['Trust', 'Surprise', 'Joy', 'Excitement', 'Pride', 'Envy',
           'Disgust', 'Fear', 'Anger', 'Disappointment', 'Anxiety', 'Nostalgia'],
    fill='toself',
    name='Week 3',
    line_color='cyan'
))

# Week 4 data
fig.add_trace(go.Scatterpolar(
    r=[7, 8, 9, 8, 6, 2, 1, 2, 3, 4, 3, 7],
    theta=['Trust', 'Surprise', 'Joy', 'Excitement', 'Pride', 'Envy',
           'Disgust', 'Fear', 'Anger', 'Disappointment', 'Anxiety', 'Nostalgia'],
    fill='toself',
    name='Week 4',
    line_color='lightblue'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 10]
        )
    ),
    showlegend=True,
    title="12种情绪强度分布 (Emotion Intensity Distribution)",
    template="plotly_dark"
)
```

### 桑基图 (Plotly)
```python
import plotly.graph_objects as go

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=["Joy", "Excitement", "Trust", "Pride", "Product A", "Product B", "Product C"],
        color=["cyan", "lightblue", "blue", "green", "orange", "red", "purple"]
    ),
    link=dict(
        source=[0, 0, 1, 1, 2, 2, 3],
        target=[4, 5, 4, 6, 5, 6, 4],
        value=[8, 4, 6, 2, 5, 3, 7]
    )
)])

fig.update_layout(
    title="情绪组合与产品机会流向",
    font_size=12
)
```

### 热力图 (Plotly)
```python
import plotly.express as px

fig = px.imshow(
    heatmap_data,
    labels=dict(x="Week", y="Emotion", color="Intensity"),
    x=['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    y=['Joy', 'Excitement', 'Trust', 'Pride', 'Fear', 'Anger'],
    color_continuous_scale='Blues',
    title="情绪关键词热力图"
)
```

---

## 下一步行动

1. 查看剩余的3张图片，了解完整需求
2. 在dashboard.py中实现这些图表
3. 确保所有图表使用统一的蓝色配色方案
4. 添加交互功能（悬停提示、点击筛选等）
