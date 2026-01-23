"""
可重用的UI组件
包含可展开面板、数据解释面板、图表等
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Any


def expandable_insight(title: str, content: str, data_source: Dict = None, solution: str = None):
    """
    可展开的洞察卡片
    
    Args:
        title: 标题
        content: 简要内容
        data_source: 数据来源详情
        solution: 解决方案建议
    """
    with st.expander(f"📊 {title}", expanded=False):
        st.markdown(content)
        
        if data_source:
            st.markdown("---")
            st.markdown("**数据来源**")
            
            if isinstance(data_source, dict):
                # 显示为表格
                df = pd.DataFrame([data_source])
                st.dataframe(df, use_container_width=True)
            elif isinstance(data_source, pd.DataFrame):
                st.dataframe(data_source, use_container_width=True)
            else:
                st.write(data_source)
        
        if solution:
            st.markdown("---")
            st.markdown("**💡 解决方案**")
            st.info(solution)


def emotion_health_gauge(emotion_score: float, title: str = "本周市场情绪健康度"):
    """
    情绪健康度仪表盘
    
    Args:
        emotion_score: 情绪分数 (0-100)
        title: 标题
    """
    # 确定健康状态
    if emotion_score >= 60:
        status = "热烈"
        status_color = "#FF6B6B"
        zone = "积极偏热烈"
    elif emotion_score >= 50:
        status = "积极"
        status_color = "#4ECDC4"
        zone = "积极"
    elif emotion_score >= 40:
        status = "中立偏积极"
        status_color = "#95E1D3"
        zone = "中立偏积极"
    elif emotion_score >= 30:
        status = "中立"
        status_color = "#F3A683"
        zone = "中立"
    else:
        status = "消极"
        status_color = "#A8A8A8"
        zone = "消极"
    
    # 创建仪表盘
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=emotion_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        number={'suffix': "", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': status_color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 20], 'color': '#E8E8E8', 'name': '消极'},
                {'range': [20, 30], 'color': '#F0F0F0', 'name': '中立'},
                {'range': [30, 40], 'color': '#F8F8F8', 'name': '积极'},
                {'range': [40, 50], 'color': '#FAFAFA', 'name': '热烈'},
                {'range': [50, 60], 'color': '#FCFCFC', 'name': '狂热'},
                {'range': [60, 100], 'color': '#FFFFFF', 'name': '狂热'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        font={'color': "darkgray", 'family': "Arial"}
    )
    
    # 添加刻度标签
    fig.add_annotation(
        x=0.15, y=0.15,
        text="消极",
        showarrow=False,
        font=dict(size=10, color="gray")
    )
    fig.add_annotation(
        x=0.35, y=0.05,
        text="中立",
        showarrow=False,
        font=dict(size=10, color="gray")
    )
    fig.add_annotation(
        x=0.5, y=0,
        text="积极",
        showarrow=False,
        font=dict(size=10, color="gray")
    )
    fig.add_annotation(
        x=0.65, y=0.05,
        text="热烈",
        showarrow=False,
        font=dict(size=10, color="gray")
    )
    fig.add_annotation(
        x=0.85, y=0.15,
        text="狂热",
        showarrow=False,
        font=dict(size=10, color="gray")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 显示状态说明
    st.markdown(f"**健康状态**: {status} （适合入市）" if emotion_score >= 40 else f"**健康状态**: {status} （建议观察）")
    
    return status, zone


def emotion_distribution_chart(emotion_data: pd.DataFrame):
    """
    情绪分布图表
    
    Args:
        emotion_data: 情绪数据DataFrame，包含emotion, count, percentage列
    """
    # 创建饼图
    fig = px.pie(
        emotion_data,
        values='count',
        names='emotion',
        title='情绪分布',
        hole=0.4,
        color='emotion',
        color_discrete_map={
            '兴奋': '#FF6B6B',
            '满意': '#4ECDC4',
            '好奇': '#95E1D3',
            '中性': '#F3A683',
            '担忧': '#FFA07A',
            '困惑': '#A8A8A8'
        }
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>数量: %{value}<br>占比: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def emotion_behavior_mapping(emotion: str, emotion_data: Dict):
    """
    情绪-行为映射展示
    
    Args:
        emotion: 情绪名称
        emotion_data: 情绪数据字典
    """
    st.markdown(f"### {emotion}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "样本量",
            f"{emotion_data.get('count', 0)}条",
            f"{emotion_data.get('percentage', 0)}%"
        )
    
    with col2:
        engagement = emotion_data.get('avg_engagement', 0)
        st.metric(
            "互动率",
            f"{engagement}%",
            delta=f"+{engagement - 5:.1f}%" if engagement > 5 else None
        )
    
    with col3:
        conversion = emotion_data.get('conversion_rate', 0)
        st.metric(
            "转化率",
            f"{conversion}%",
            delta=f"+{conversion - 4.5:.1f}%" if conversion > 4.5 else None
        )
    
    # 关键词
    if 'top_keywords' in emotion_data:
        keywords = emotion_data['top_keywords']
        if isinstance(keywords, list):
            st.markdown(f"**关键词**: {', '.join(keywords)}")
    
    # 示例评论
    if 'sample_comments' in emotion_data:
        comments = emotion_data['sample_comments']
        if isinstance(comments, list) and len(comments) > 0:
            with st.expander("查看示例评论"):
                for comment in comments[:5]:
                    st.markdown(f"- {comment}")


def data_source_table(platform_data: pd.DataFrame):
    """
    数据来源详细表格
    
    Args:
        platform_data: 平台数据DataFrame
    """
    st.markdown("### 数据来源详情")
    
    # 格式化数据
    display_df = platform_data.copy()
    
    if 'growth_rate' in display_df.columns:
        display_df['growth_rate'] = display_df['growth_rate'].apply(lambda x: f"+{x:.1f}%")
    
    if 'avg_engagement_rate' in display_df.columns:
        display_df['avg_engagement_rate'] = display_df['avg_engagement_rate'].apply(lambda x: f"{x:.1f}%")
    
    # 重命名列
    column_mapping = {
        'platform': '平台',
        'platform_type': '类型',
        'total_views': '总浏览量',
        'total_engagement': '总互动数',
        'growth_rate': '增长率',
        'avg_engagement_rate': '平均互动率',
        'product_count': '产品数',
        'top_category': '热门类别'
    }
    
    display_df = display_df.rename(columns=column_mapping)
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def topic_emotion_heatmap(topic_data: pd.DataFrame):
    """
    主题-情绪热力图
    
    Args:
        topic_data: 主题分析数据
    """
    # 创建透视表
    pivot_data = topic_data.pivot_table(
        index='topic',
        columns='emotion',
        values='percentage',
        fill_value=0
    )
    
    # 创建热力图
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='RdYlGn',
        text=pivot_data.values,
        texttemplate='%{text:.0f}%',
        textfont={"size": 12},
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>%{x}: %{z:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title='主题-情绪关联热力图',
        xaxis_title='情绪',
        yaxis_title='主题',
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def recommendation_card(product: Dict, rank: int):
    """
    产品推荐卡片
    
    Args:
        product: 产品数据字典
        rank: 排名
    """
    with st.container():
        st.markdown(f"### #{rank} {product.get('product_name', 'Unknown')}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("情绪分", f"{product.get('emotion_score', 0):.1f}/50")
        
        with col2:
            st.metric("增长率", f"{product.get('growth_rate', 0):.1f}%")
        
        with col3:
            st.metric("预估月营收", f"${product.get('revenue_estimate', 0):,.0f}")
        
        with col4:
            st.metric("ROI", f"{product.get('roi_estimate', 0):.1f}%")
        
        # 推荐理由
        reason = product.get('recommendation_reason', '情绪分数高，办公类需求旺盛，适合快速进入市场')
        st.info(f"**推荐理由**: {reason}")
        
        # 可展开的详细数据
        with st.expander("查看详细数据"):
            st.markdown(f"**类别**: {product.get('product_category', 'N/A')}")
            st.markdown(f"**轨道类型**: {product.get('track_type', 'N/A')}")
            st.markdown(f"**平均价格**: ${product.get('price_avg', 0):.2f}")
            st.markdown(f"**销量**: {product.get('sales_volume', 0):,} 件/月")
            st.markdown(f"**转化率**: {product.get('conversion_rate', 0):.1f}%")
            st.markdown(f"**目标受众**: {product.get('target_audience', 'N/A')}")
        
        st.markdown("---")


def solution_panel(problem: str, data_evidence: str, solution: str, action_items: List[str]):
    """
    问题-数据-解决方案面板
    
    Args:
        problem: 问题描述
        data_evidence: 数据证据
        solution: 解决方案
        action_items: 行动项列表
    """
    with st.container():
        # 问题
        st.markdown(f"**问题识别**: {problem}")
        
        # 数据证据（可展开）
        with st.expander("📊 查看数据支撑"):
            st.markdown(data_evidence)
        
        # 解决方案
        st.success(f"**💡 解决方案**: {solution}")
        
        # 行动项
        if action_items:
            st.markdown("**行动清单**:")
            for i, item in enumerate(action_items, 1):
                st.markdown(f"{i}. {item}")
        
        st.markdown("---")


def kpi_card(label: str, value: Any, delta: Any = None, help_text: str = None):
    """
    KPI指标卡片
    
    Args:
        label: 指标名称
        value: 指标值
        delta: 变化值
        help_text: 帮助文本
    """
    st.metric(
        label=label,
        value=value,
        delta=delta,
        help=help_text
    )


def comparison_chart(data: pd.DataFrame, x_col: str, y_col: str, color_col: str = None, title: str = "对比图"):
    """
    对比柱状图
    
    Args:
        data: 数据DataFrame
        x_col: X轴列名
        y_col: Y轴列名
        color_col: 颜色分组列名
        title: 图表标题
    """
    fig = px.bar(
        data,
        x=x_col,
        y=y_col,
        color=color_col if color_col else None,
        title=title,
        text=y_col
    )
    
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=True if color_col else False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def trend_line_chart(data: pd.DataFrame, x_col: str, y_cols: List[str], title: str = "趋势图"):
    """
    趋势折线图
    
    Args:
        data: 数据DataFrame
        x_col: X轴列名
        y_cols: Y轴列名列表
        title: 图表标题
    """
    fig = go.Figure()
    
    for y_col in y_cols:
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y_col],
            mode='lines+markers',
            name=y_col,
            line=dict(width=2),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title="值",
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
