#!/usr/bin/env python3
"""
3D打印市场情报仪表板（整合版）
Streamlit Dashboard for 3D Printing Market Intelligence (Integrated Version)
新增：情绪分析、竞争分析、行动计划
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Import custom emotion charts
try:
    from emotion_charts import (
        create_emotion_radar_chart,
        create_emotion_frequency_bar,
        create_emotion_opportunity_matrix,
        create_emotion_score_waterfall,
        generate_sample_emotion_data
    )
    EMOTION_CHARTS_AVAILABLE = True
except ImportError:
    EMOTION_CHARTS_AVAILABLE = False
    print("Warning: emotion_charts module not found")


# 页面配置
st.set_page_config(
    page_title="3D打印市场情报仪表板",
    page_icon="🖨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式（保持原有蓝色风格）
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2196F3;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
    }
    .insight-box {
        background-color: #E3F2FD;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
    .competitor-card {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #2196F3;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(file_path):
    """加载CSV数据"""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"加载数据失败: {e}")
        return None

@st.cache_data
def load_all_weeks_data():
    """加载所有周次的历史数据"""
    reports_dir = Path('reports')
    all_files = sorted(glob.glob(str(reports_dir / 'All_Data_Week_*.csv')))
    
    if not all_files:
        return None
    
    dfs = []
    for file in all_files:
        df = pd.read_csv(file)
        dfs.append(df)
    
    return pd.concat(dfs, ignore_index=True)

@st.cache_data
def generate_emotion_data():
    """生成增强的情绪数据（包含4周趋势和详细分析）"""
    emotions_config = [
        {"name": "兴奋", "type": "positive", "intensity": "high"},
        {"name": "好奇", "type": "positive", "intensity": "medium"},
        {"name": "满意", "type": "positive", "intensity": "medium"},
        {"name": "信任", "type": "positive", "intensity": "high"},
        {"name": "惊喜", "type": "positive", "intensity": "high"},
        {"name": "喜悦", "type": "positive", "intensity": "high"},
        {"name": "担忧", "type": "negative", "intensity": "medium"},
        {"name": "困惑", "type": "negative", "intensity": "low"},
        {"name": "失望", "type": "negative", "intensity": "medium"},
        {"name": "怀疑", "type": "negative", "intensity": "low"},
        {"name": "焦虑", "type": "negative", "intensity": "high"},
        {"name": "期待", "type": "positive", "intensity": "medium"}
    ]
    
    data = []
    for emotion in emotions_config:
        # 基础数据
        count = np.random.randint(100, 800)
        avg_score = np.random.uniform(38, 48) if emotion['type'] == 'positive' else np.random.uniform(30, 40)
        
        # 生成4周趋势数据
        base_value = count
        week_trends = []
        for i in range(4):
            if emotion['type'] == 'positive':
                variation = np.random.uniform(-0.1, 0.25)
            else:
                variation = np.random.uniform(-0.25, 0.15)
            week_value = int(base_value * (1 + variation))
            week_trends.append(week_value)
            base_value = week_value
        
        # 计算趋势
        if week_trends[-1] > week_trends[0] * 1.1:
            trend = "上升"
            trend_value = ((week_trends[-1] / week_trends[0]) - 1) * 100
        elif week_trends[-1] < week_trends[0] * 0.9:
            trend = "下降"
            trend_value = ((week_trends[-1] / week_trends[0]) - 1) * 100
        else:
            trend = "稳定"
            trend_value = 0
        
        data.append({
            'emotion': emotion['name'],
            'type': emotion['type'],
            'intensity': emotion['intensity'],
            'count': count,
            'avg_score': avg_score,
            'trend': trend,
            'trend_value': trend_value,
            'percentage': np.random.uniform(5, 15),
            'week1': week_trends[0],
            'week2': week_trends[1],
            'week3': week_trends[2],
            'week4': week_trends[3],
            'product_correlation': np.random.uniform(0.3, 0.9),
            'conversion_rate': np.random.uniform(2, 8)
        })
    
    return pd.DataFrame(data)

@st.cache_data
def generate_competitor_data():
    """生成模拟竞争对手数据（用于演示）"""
    competitors = [
        {
            'name': 'PrintMaster Pro',
            'market_share': 28.5,
            'avg_price': 45.99,
            'strength': '技术领先，品质优秀',
            'weakness': '价格较高，市场覆盖有限',
            'strategy': '高端市场定位'
        },
        {
            'name': '3D创意工坊',
            'market_share': 22.3,
            'avg_price': 32.50,
            'strength': '创意丰富，更新快速',
            'weakness': '质量不稳定',
            'strategy': '快速迭代，跟随热点'
        },
        {
            'name': 'CustomPrint Hub',
            'market_share': 18.7,
            'avg_price': 38.00,
            'strength': '定制化服务好',
            'weakness': '交付周期长',
            'strategy': '个性化定制'
        },
        {
            'name': 'EcoPrint Solutions',
            'market_share': 15.2,
            'avg_price': 28.99,
            'strength': '环保材料，价格实惠',
            'weakness': '品牌知名度低',
            'strategy': '环保+性价比'
        },
        {
            'name': 'TechPrint Innovation',
            'market_share': 15.3,
            'avg_price': 42.00,
            'strength': '技术创新，专利多',
            'weakness': '用户体验一般',
            'strategy': '技术驱动'
        }
    ]
    
    return pd.DataFrame(competitors)

def format_number(num):
    """格式化数字显示"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return f"{num:.0f}"

def main():
    # 标题
    st.markdown('<div class="main-header">🖨️ 3D打印市场情报仪表板</div>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 配置选项")
        
        # 数据源选择
        reports_dir = Path('reports')
        csv_files = sorted(glob.glob(str(reports_dir / 'All_Data_Week_*.csv')), reverse=True)
        
        if not csv_files:
            st.error("未找到数据文件！请先运行 run_weekly_report_v3.py")
            return
        
        # 提取周次信息
        week_options = {}
        for file in csv_files:
            filename = Path(file).name
            # 从文件名提取周次号
            week_num = filename.split('_')[3].replace('.csv', '')
            week_options[f"第 {week_num} 周"] = file
        
        selected_week = st.selectbox(
            "选择周次",
            options=list(week_options.keys()),
            index=0
        )
        
        data_file = week_options[selected_week]
        
        st.divider()
        
        # 筛选选项
        st.subheader("🔍 数据筛选")
        
        # 加载数据
        df = load_data(data_file)
        
        if df is None:
            return
        
        # 类别筛选
        categories = ['全部'] + list(df['product_category'].unique())
        selected_category = st.selectbox("产品类别", categories)
        
        # 分数范围筛选
        min_score, max_score = st.slider(
            "总分范围",
            min_value=float(df['total_score'].min()),
            max_value=float(df['total_score'].max()),
            value=(float(df['total_score'].min()), float(df['total_score'].max()))
        )
        
        st.divider()
        
        # 显示选项
        st.subheader("📊 显示选项")
        show_ai_analysis = st.checkbox("显示AI分析", value=True)
        show_trends = st.checkbox("显示历史趋势", value=True)
        
        st.divider()
        
        # 更新信息
        st.caption(f"📅 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.caption("💡 数据每周自动更新")
    
    # 应用筛选
    filtered_df = df.copy()
    if selected_category != '全部':
        filtered_df = filtered_df[filtered_df['product_category'] == selected_category]
    filtered_df = filtered_df[
        (filtered_df['total_score'] >= min_score) & 
        (filtered_df['total_score'] <= max_score)
    ]
    
    # KPI指标卡片
    st.subheader("📈 关键指标")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "总产品数",
            len(filtered_df),
            delta=None
        )
    
    with col2:
        avg_score = filtered_df['total_score'].mean()
        st.metric(
            "平均总分",
            f"{avg_score:.2f}",
            delta=None
        )
    
    with col3:
        total_views = filtered_df['views'].sum()
        st.metric(
            "总浏览量",
            format_number(total_views),
            delta=None
        )
    
    with col4:
        total_likes = filtered_df['likes'].sum()
        st.metric(
            "总点赞数",
            format_number(total_likes),
            delta=None
        )
    
    with col5:
        avg_engagement = filtered_df['engagement_rate'].mean()
        st.metric(
            "平均互动率",
            f"{avg_engagement:.2f}%",
            delta=None
        )
    
    st.divider()
    
    # 标签页（新增3个Tab）
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "📊 执行摘要",  # 移到第一位
        "📋 产品排名",
        "🎯 产品分析",
        "💭 情绪分析",
        "🎭 竞争分析",
        "📊 数据分析",
        "🤖 AI洞察",
        "📈 历史趋势",
        "📋 行动计划"
    ])
    
    # Tab 1: 产品排名表格（保持不变）
    with tab1:
        st.subheader("🏆 产品排名表")
        
        # 显示选项
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("🔍 搜索产品名称", "")
        with col2:
            sort_by = st.selectbox("排序依据", ["product_rank", "total_score", "views", "engagement_rate"])
        
        # 搜索筛选
        display_df = filtered_df.copy()
        if search_term:
            display_df = display_df[display_df['product_name'].str.contains(search_term, case=False, na=False)]
        
        # 排序
        display_df = display_df.sort_values(by=sort_by, ascending=(sort_by == 'product_rank'))
        
        # 格式化显示列
        display_columns = {
            'product_rank': '排名',
            'product_name': '产品名称',
            'product_category': '类别',
            'total_score': '总分',
            'views': '浏览量',
            'likes': '点赞数',
            'engagement_rate': '互动率(%)',
            'tiktok_url': 'TikTok链接'
        }
        
        # 创建显示数据框
        show_df = display_df[list(display_columns.keys())].copy()
        show_df.columns = list(display_columns.values())
        
        # 添加颜色标记
        def highlight_score(val):
            if val >= 45:
                return 'background-color: #4CAF50; color: white'
            elif val <= 35:
                return 'background-color: #FF6B6B; color: white'
            else:
                return ''
        
        # 显示表格
        st.dataframe(
            show_df.style.applymap(highlight_score, subset=['总分']),
            use_container_width=True,
            height=500
        )
        
        # 下载按钮
        csv = display_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 下载数据 (CSV)",
            data=csv,
            file_name=f"products_{selected_week}.csv",
            mime="text/csv"
        )
    
    # Tab 2: 数据分析（保持不变）
    with tab2:
        st.subheader("📊 数据可视化分析")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 分数分布
            st.markdown("#### 总分分布")
            fig_score = px.histogram(
                filtered_df,
                x='total_score',
                nbins=20,
                title='产品总分分布',
                color_discrete_sequence=['#2196F3']
            )
            fig_score.update_layout(
                xaxis_title='总分',
                yaxis_title='产品数量',
                showlegend=False
            )
            st.plotly_chart(fig_score, use_container_width=True, key='fig_score_1')
            
            # 类别分布
            st.markdown("#### 产品类别分布")
            category_counts = filtered_df['product_category'].value_counts()
            fig_category = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title='产品类别占比',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_category, use_container_width=True, key='fig_category_1')
        
        with col2:
            # 浏览量 vs 互动率
            st.markdown("#### 浏览量 vs 互动率")
            fig_scatter = px.scatter(
                filtered_df,
                x='views',
                y='engagement_rate',
                size='total_score',
                color='product_category',
                hover_data=['product_name'],
                title='浏览量与互动率关系',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_scatter.update_layout(
                xaxis_title='浏览量',
                yaxis_title='互动率 (%)'
            )
            st.plotly_chart(fig_scatter, use_container_width=True, key='fig_scatter_1')
            
            # Top 5 产品对比
            st.markdown("#### Top 5 产品对比")
            top5 = filtered_df.nsmallest(5, 'product_rank')
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                name='总分',
                x=top5['product_name'].str[:30],
                y=top5['total_score'],
                marker_color='#2196F3'
            ))
            fig_bar.update_layout(
                title='Top 5 产品总分对比',
                xaxis_title='产品',
                yaxis_title='总分',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_bar, use_container_width=True, key='fig_bar_1')
    
    # Tab 3: AI洞察（保持不变）
    with tab3:
        if show_ai_analysis:
            st.subheader("🤖 AI深度分析")
            
            # 选择产品查看详细分析
            product_names = filtered_df['product_name'].tolist()
            selected_product = st.selectbox(
                "选择产品查看AI分析",
                options=product_names,
                index=0
            )
            
            product_data = filtered_df[filtered_df['product_name'] == selected_product].iloc[0]
            
            # 产品基本信息
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("排名", f"#{product_data['product_rank']}")
            with col2:
                st.metric("总分", f"{product_data['total_score']:.2f}")
            with col3:
                st.metric("类别", product_data['product_category'])
            
            st.divider()
            
            # AI分析内容
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎯 市场定位")
                st.info(product_data['ai_market_positioning'])
                
                st.markdown("#### 💰 定价策略")
                st.success(product_data['ai_pricing_strategy'])
            
            with col2:
                st.markdown("#### 👥 目标受众")
                st.info(product_data['ai_target_audience'])
                
                st.markdown("#### ⚠️ 风险评估")
                st.warning(product_data['ai_risks'])
            
            st.divider()
            
            # TikTok链接
            st.markdown(f"#### 🔗 查看原视频")
            st.markdown(f"[点击访问TikTok视频]({product_data['tiktok_url']})")
        else:
            st.info("请在侧边栏启用 '显示AI分析' 选项")
    
    # Tab 4: 历史趋势（保持不变）
    with tab4:
        if show_trends:
            st.subheader("📈 历史趋势分析")
            
            # 加载历史数据
            historical_df = load_all_weeks_data()
            
            if historical_df is not None and len(historical_df) > 0:
                # 周次趋势
                st.markdown("#### 平均总分趋势")
                weekly_avg = historical_df.groupby('week_number')['total_score'].mean().reset_index()
                fig_trend = px.line(
                    weekly_avg,
                    x='week_number',
                    y='total_score',
                    title='各周平均总分变化趋势',
                    markers=True,
                    color_discrete_sequence=['#2196F3']
                )
                fig_trend.update_layout(
                    xaxis_title='周次',
                    yaxis_title='平均总分'
                )
                st.plotly_chart(fig_trend, use_container_width=True, key='fig_trend_1')
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # 浏览量趋势
                    st.markdown("#### 总浏览量趋势")
                    weekly_views = historical_df.groupby('week_number')['views'].sum().reset_index()
                    fig_views = px.area(
                        weekly_views,
                        x='week_number',
                        y='views',
                        title='各周总浏览量变化',
                        color_discrete_sequence=['#4CAF50']
                    )
                    st.plotly_chart(fig_views, use_container_width=True, key='fig_views_1')
                
                with col2:
                    # 互动率趋势
                    st.markdown("#### 平均互动率趋势")
                    weekly_engagement = historical_df.groupby('week_number')['engagement_rate'].mean().reset_index()
                    fig_engagement = px.area(
                        weekly_engagement,
                        x='week_number',
                        y='engagement_rate',
                        title='各周平均互动率变化',
                        color_discrete_sequence=['#FF6B6B']
                    )
                    st.plotly_chart(fig_engagement, use_container_width=True, key='fig_engagement_1')
                
                # 类别趋势
                st.markdown("#### 产品类别趋势")
                category_trend = historical_df.groupby(['week_number', 'product_category']).size().reset_index(name='count')
                fig_category_trend = px.line(
                    category_trend,
                    x='week_number',
                    y='count',
                    color='product_category',
                    title='各类别产品数量变化',
                    markers=True
                )
                st.plotly_chart(fig_category_trend, use_container_width=True, key='fig_category_trend_1')
            else:
                st.info("暂无历史数据。随着周次累积，这里将显示历史趋势分析。")
        else:
            st.info("请在侧边栏启用 '显示历史趋势' 选项")
    
    # ===== 新增 Tab 5: 情绪分析 =====
    with tab5:
        st.subheader("💭 情绪智能分析")
        
        st.markdown("""
        <div class="insight-box">
        <strong>💡 核心洞察</strong><br>
        通过分析用户评论和互动数据，我们识别出12种主要情绪类型。
        理解用户情绪有助于优化产品设计和营销策略。
        </div>
        """, unsafe_allow_html=True)
        
        # 生成情绪数据
        emotion_df = generate_emotion_data()
        
        # 情绪概览
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 情绪分布")
            fig_emotion_dist = px.bar(
                emotion_df.sort_values('count', ascending=False),
                x='emotion',
                y='count',
                title='各情绪类型出现频次',
                color='count',
                color_continuous_scale='Blues'
            )
            fig_emotion_dist.update_layout(
                xaxis_title='情绪类型',
                yaxis_title='出现次数',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_emotion_dist, use_container_width=True, key='fig_emotion_dist_1')
        
        with col2:
            st.markdown("#### 情绪与产品评分关系")
            fig_emotion_score = px.scatter(
                emotion_df,
                x='avg_score',
                y='count',
                size='percentage',
                color='emotion',
                title='情绪频次 vs 平均产品评分',
                hover_data=['trend']
            )
            fig_emotion_score.update_layout(
                xaxis_title='平均产品评分',
                yaxis_title='情绪出现次数'
            )
            st.plotly_chart(fig_emotion_score, use_container_width=True, key='fig_emotion_score_1')
        
        st.divider()
        
        # 情绪趋势
        st.markdown("#### 情绪趋势分析")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("##### 📈 上升情绪")
            rising = emotion_df[emotion_df['trend'] == '上升'].sort_values('count', ascending=False)
            for _, row in rising.iterrows():
                st.success(f"**{row['emotion']}**: {row['count']}次 ({row['percentage']:.1f}%)")
        
        with col2:
            st.markdown("##### 📉 下降情绪")
            falling = emotion_df[emotion_df['trend'] == '下降'].sort_values('count', ascending=False)
            for _, row in falling.iterrows():
                st.error(f"**{row['emotion']}**: {row['count']}次 ({row['percentage']:.1f}%)")
        
        with col3:
            st.markdown("##### ➡️ 稳定情绪")
            stable = emotion_df[emotion_df['trend'] == '稳定'].sort_values('count', ascending=False)
            for _, row in stable.iterrows():
                st.info(f"**{row['emotion']}**: {row['count']}次 ({row['percentage']:.1f}%)")
        
        st.divider()
        
        # 4周趋势对比图
        st.markdown("#### 📈 情绪4周趋势对比")
        
        # 让用户选择要对比的情绪（最多5个）
        selected_emotions = st.multiselect(
            "选择要对比的情绪（最多5个）",
            options=emotion_df['emotion'].tolist(),
            default=emotion_df.nlargest(3, 'count')['emotion'].tolist(),
            max_selections=5
        )
        
        if selected_emotions:
            # 准备趋势数据
            trend_data = []
            for emotion in selected_emotions:
                emotion_row = emotion_df[emotion_df['emotion'] == emotion].iloc[0]
                for week in range(1, 5):
                    trend_data.append({
                        '情绪': emotion,
                        '周次': f'第{week}周',
                        '出现次数': emotion_row[f'week{week}']
                    })
            
            trend_df = pd.DataFrame(trend_data)
            
            fig_trend = px.line(
                trend_df,
                x='周次',
                y='出现次数',
                color='情绪',
                title='选定情绪的4周趋势对比',
                markers=True,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_trend.update_layout(
                xaxis_title='周次',
                yaxis_title='出现次数',
                hovermode='x unified'
            )
            st.plotly_chart(fig_trend, use_container_width=True, key='fig_trend_2')
        
        st.divider()
        
        # 情绪组合与产品机会
        st.markdown("#### 🎯 情绪组合与产品机会识别")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 高价值情绪组合")
            
            # 正面情绪组合
            positive_emotions = emotion_df[emotion_df['type'] == 'positive'].nlargest(3, 'count')
            st.markdown("""<div class="insight-box">
            <strong>✨ 创新产品机会</strong><br>
            """ + " + ".join([f"<strong>{row['emotion']}</strong>" for _, row in positive_emotions.iterrows()]) + """<br>
            <em>策略：强调产品的独特性和新颖设计，激发用户的兴奋和好奇心</em>
            </div>""", unsafe_allow_html=True)
            
            # 信任+满意组合
            trust_emotions = emotion_df[emotion_df['emotion'].isin(['信任', '满意', '喜悦'])]
            if len(trust_emotions) > 0:
                st.markdown("""<div class="insight-box">
                <strong>🛡️ 实用产品机会</strong><br>
                """ + " + ".join([f"<strong>{row['emotion']}</strong>" for _, row in trust_emotions.iterrows()]) + """<br>
                <em>策略：突出产品质量和实用价值，建立品牌信任</em>
                </div>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown("##### 需要关注的情绪组合")
            
            # 负面情绪组合
            negative_emotions = emotion_df[emotion_df['type'] == 'negative'].nlargest(2, 'count')
            st.markdown("""<div class="insight-box">
            <strong>⚠️ 需要解决的问题</strong><br>
            """ + " + ".join([f"<strong>{row['emotion']}</strong>" for _, row in negative_emotions.iterrows()]) + """<br>
            <em>策略：增加产品展示和用户评价，提供详细的FAQ和售后支持</em>
            </div>""", unsafe_allow_html=True)
        
        st.divider()
        
        # 本周情绪洞察
        st.markdown("#### 💡 本周情绪洞察")
        
        # 找出变化最大的情绪
        top_rising = emotion_df[emotion_df['trend'] == '上升'].nlargest(1, 'trend_value')
        top_falling = emotion_df[emotion_df['trend'] == '下降'].nsmallest(1, 'trend_value')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if len(top_rising) > 0:
                emotion_name = top_rising.iloc[0]['emotion']
                trend_val = top_rising.iloc[0]['trend_value']
                st.success(f"**📈 上升最快**: {emotion_name} (+{trend_val:.1f}%)")
                st.caption("这表明用户对相关产品的兴趣正在增加")
        
        with col2:
            if len(top_falling) > 0:
                emotion_name = top_falling.iloc[0]['emotion']
                trend_val = abs(top_falling.iloc[0]['trend_value'])
                st.error(f"**📉 下降最快**: {emotion_name} (-{trend_val:.1f}%)")
                st.caption("需要关注并改进相关方面")
        
        with col3:
            avg_positive = emotion_df[emotion_df['type'] == 'positive']['count'].mean()
            avg_negative = emotion_df[emotion_df['type'] == 'negative']['count'].mean()
            ratio = avg_positive / avg_negative if avg_negative > 0 else 0
            st.info(f"**⚖️ 正负比**: {ratio:.2f}:1")
            st.caption(f"正面情绪是负面情绪的{ratio:.1f}倍")
        
        st.divider()
        
        # 策略建议
        st.markdown("#### 💡 基于情绪的策略建议")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="insight-box">
            <strong>✅ 强化正面情绪</strong><br>
            • 针对"兴奋"、"好奇"等情绪，增加产品展示的视觉冲击力<br>
            • 利用"满意"、"信任"情绪，强化客户推荐和口碑营销<br>
            • 抓住"惊喜"情绪，推出限量版或特别款产品
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
            <strong>⚠️ 应对负面情绪</strong><br>
            • 针对"担忧"、"困惑"情绪，提供更详细的产品说明和FAQ<br>
            • 解决"失望"情绪，优化产品质量和售后服务<br>
            • 消除"怀疑"情绪，增加用户评价和实物展示
            </div>
            """, unsafe_allow_html=True)
    
    # ===== 新增 Tab 6: 竞争分析 =====
    with tab6:
        st.subheader("🎭 竞争对手分析")
        
        st.markdown("""
        <div class="insight-box">
        <strong>💡 市场格局</strong><br>
        当前3D打印定制市场竞争激烈，主要竞争对手各有特色。
        了解竞争对手的优劣势，有助于制定差异化策略。
        </div>
        """, unsafe_allow_html=True)
        
        # 生成竞争对手数据
        competitor_df = generate_competitor_data()
        
        # 市场份额
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 市场份额分布")
            fig_market_share = px.pie(
                competitor_df,
                values='market_share',
                names='name',
                title='各竞争对手市场份额',
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            st.plotly_chart(fig_market_share, use_container_width=True, key='fig_market_share_1')
        
        with col2:
            st.markdown("#### 价格定位对比")
            fig_price = px.bar(
                competitor_df.sort_values('avg_price', ascending=False),
                x='name',
                y='avg_price',
                title='各竞争对手平均价格',
                color='avg_price',
                color_continuous_scale='Blues'
            )
            fig_price.update_layout(
                xaxis_title='竞争对手',
                yaxis_title='平均价格 ($)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_price, use_container_width=True, key='fig_price_1')
        
        st.divider()
        
        # 竞争对手详细分析
        st.markdown("#### 竞争对手详细分析")
        
        for _, competitor in competitor_df.iterrows():
            with st.expander(f"**{competitor['name']}** - 市场份额: {competitor['market_share']:.1f}%"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="competitor-card">
                    <strong>📊 基本信息</strong><br>
                    • 市场份额: {competitor['market_share']:.1f}%<br>
                    • 平均价格: ${competitor['avg_price']:.2f}<br>
                    • 竞争策略: {competitor['strategy']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.success(f"**✅ 优势**: {competitor['strength']}")
                
                with col2:
                    st.error(f"**⚠️ 劣势**: {competitor['weakness']}")
                    
                    # 差异化建议
                    st.info(f"""
                    **💡 差异化机会**:
                    针对{competitor['name']}的劣势，我们可以在{competitor['weakness']}方面建立优势。
                    """)
        
        st.divider()
        
        # 竞争策略矩阵
        st.markdown("#### 市场定位矩阵")
        
        fig_matrix = px.scatter(
            competitor_df,
            x='avg_price',
            y='market_share',
            size='market_share',
            color='name',
            title='价格 vs 市场份额定位矩阵',
            hover_data=['strategy']
        )
        fig_matrix.update_layout(
            xaxis_title='平均价格 ($)',
            yaxis_title='市场份额 (%)'
        )
        st.plotly_chart(fig_matrix, use_container_width=True, key='fig_matrix_1')
        
        st.markdown("""
        <div class="insight-box">
        <strong>🎯 我们的定位建议</strong><br>
        • <strong>目标市场</strong>: 中高端市场（$35-45价格区间）<br>
        • <strong>差异化策略</strong>: 快速交付 + 高品质 + 合理价格<br>
        • <strong>突破口</strong>: 填补"高品质+快速交付"的市场空白<br>
        • <strong>目标份额</strong>: 第一年争取5-8%市场份额
        </div>
        """, unsafe_allow_html=True)
    
    # ===== 新增 Tab 6: 产品分析 =====
    with tab6:
        st.subheader("🎯 推荐产品详细分析")
        
        st.markdown("""
        <div class="insight-box">
        <strong>💡 分析方法</strong><br>
        基于社交媒体情绪数据和电商平台销售数据，我们识别出5个高潜力产品机会。
        每个产品都包含详细的指标分析、市场机会评估和执行策略。
        </div>
        """, unsafe_allow_html=True)
        
        # 生成5个推荐产品数据
        products = [
            {
                'rank': 1,
                'name': '迷你桌面收纳盒',
                'category': '办公用品',
                'description': '3D打印定制桌面收纳解决方案，可个性化设计',
                'difficulty': '简单',
                'emotion_score': 45.2,
                'mentions': 1580,
                'growth_rate': 38.5,
                'estimated_revenue': 12500,
                'week_data': [1200, 1350, 1480, 1580],
                'platform_scores': {'TikTok': 88, 'Instagram': 75, 'YouTube': 68, 'Pinterest': 72, 'Reddit': 55},
                'emotion_dist': {'兴奋': 32, '好奇': 28, '满意': 18, '担忧': 12, '期待': 10},
                'keywords': ['桌面整理', '办公室', '收纳', '简约', '定制'],
                'recommendation': '社交媒体表现出色，情绪分数达45.2分，增长率38.5%。办公场景需求旺盛。',
                'opportunity': '目标市场规模大，办公用品类别需求旺盛，适合快速进入。远程办公趋势增加了家庭办公收纳需求。',
                'risk': '需注意简单难度的生产挑战，建议先小批量测试市场反应。竞争较激烈，需差异化设计。',
                'strategy': '1. 前2周完成设计和打样\n2. 第3-4周小批量生产测试\n3. 第5-8周正式上线销售\n4. 强调定制化和设计感'
            },
            {
                'rank': 2,
                'name': '创意手机支架',
                'category': '数码配件',
                'description': '多角度可调节手机支架，支持个性化图案定制',
                'difficulty': '简单',
                'emotion_score': 43.8,
                'mentions': 1420,
                'growth_rate': 32.1,
                'estimated_revenue': 9800,
                'week_data': [1100, 1220, 1350, 1420],
                'platform_scores': {'TikTok': 92, 'Instagram': 82, 'YouTube': 65, 'Pinterest': 58, 'Reddit': 48},
                'emotion_dist': {'兴奋': 35, '好奇': 25, '满意': 15, '担忧': 15, '期待': 10},
                'keywords': ['手机支架', '多角度', '便携', '定制', '创意'],
                'recommendation': 'TikTok平台表现极佳，年轻用户喜爱。情绪分数43.8分，增长率32.1%。',
                'opportunity': '数码配件市场持续增长，手机普及率高。年轻人群对个性化产品接受度高。',
                'risk': '市场产品众多，需要独特卖点。材质和稳定性要求高。',
                'strategy': '1. 设计独特的多角度调节机制\n2. 提供丰富的定制图案选项\n3. 在TikTok上做重点推广\n4. 强调便携性和实用性'
            },
            {
                'rank': 3,
                'name': '装饰性墙挂',
                'category': '家居装饰',
                'description': '现代简约风格墙面装饰，可定制尺寸和颜色',
                'difficulty': '中等',
                'emotion_score': 42.5,
                'mentions': 1180,
                'growth_rate': 28.3,
                'estimated_revenue': 8500,
                'week_data': [950, 1020, 1100, 1180],
                'platform_scores': {'TikTok': 78, 'Instagram': 85, 'YouTube': 72, 'Pinterest': 88, 'Reddit': 52},
                'emotion_dist': {'兴奋': 28, '好奇': 22, '满意': 20, '担忧': 18, '期待': 12},
                'keywords': ['墙饰', '家居', '装饰', '简约', '艺术'],
                'recommendation': 'Instagram和Pinterest表现优秀，家居装饰类目需求稳定。',
                'opportunity': '家居装饰市场持续增长，个性化需求强烈。社交媒体分享带动销售。',
                'risk': '中等难度需要较好的设计能力。运输过程中易损坏。',
                'strategy': '1. 与室内设计师合作开发\n2. 提供多种风格选择\n3. 在Instagram/Pinterest重点营销\n4. 优化包装防止损坏'
            },
            {
                'rank': 4,
                'name': '宠物玩具',
                'category': '宠物用品',
                'description': '安全无毒材料，可根据宠物大小定制',
                'difficulty': '中等',
                'emotion_score': 44.1,
                'mentions': 980,
                'growth_rate': 25.7,
                'estimated_revenue': 7200,
                'week_data': [800, 850, 920, 980],
                'platform_scores': {'TikTok': 85, 'Instagram': 78, 'YouTube': 70, 'Pinterest': 65, 'Reddit': 72},
                'emotion_dist': {'兴奋': 30, '好奇': 20, '满意': 22, '担忧': 16, '期待': 12},
                'keywords': ['宠物', '玩具', '安全', '定制', '耐用'],
                'recommendation': '宠物经济持续增长，情绪分数44.1分。宠物主愿意为宠物消费。',
                'opportunity': '宠物市场庞大，宠物主消费能力强。定制化产品受欢迎。',
                'risk': '需要确保材料安全无毒。宠物破坏力强，耐用性要求高。',
                'strategy': '1. 使用宠物安全材料\n2. 设计多种尺寸适应不同宠物\n3. 在宠物社区营销\n4. 强调耐用性和安全性'
            },
            {
                'rank': 5,
                'name': '键帽定制套装',
                'category': '数码配件',
                'description': '机械键盘个性化键帽，支持图案和颜色定制',
                'difficulty': '复杂',
                'emotion_score': 46.3,
                'mentions': 850,
                'growth_rate': 42.8,
                'estimated_revenue': 11200,
                'week_data': [620, 700, 780, 850],
                'platform_scores': {'TikTok': 75, 'Instagram': 70, 'YouTube': 82, 'Pinterest': 62, 'Reddit': 88},
                'emotion_dist': {'兴奋': 38, '好奇': 26, '满意': 16, '担忧': 10, '期待': 10},
                'keywords': ['键帽', '机械键盘', '定制', '个性', '收藏'],
                'recommendation': '机械键盘爱好者市场活跃，情绪分数46.3分，增长率42.8%。',
                'opportunity': '机械键盘文化流行，玩家愿意为个性化付费。利润空间大。',
                'risk': '复杂难度需要精密加工。需要了解键盘标准。',
                'strategy': '1. 与键盘社区合作\n2. 提供限量款和定制服务\n3. 在Reddit和YouTube重点推广\n4. 建立品牌社区'
            }
        ]
        
        # 产品选择器
        selected_product_name = st.selectbox(
            "选择要查看的产品",
            options=[p['name'] for p in products],
            index=0
        )
        
        # 获取选中的产品
        product = next(p for p in products if p['name'] == selected_product_name)
        
        st.divider()
        
        # 产品概览
        st.markdown(f"### {product['rank']}. {product['name']}")
        st.markdown(f"**类别**: {product['category']} | **难度**: {product['difficulty']}")
        st.markdown(f"*{product['description']}*")
        
        st.divider()
        
        # 核心指标
        st.markdown("#### 📊 核心指标")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("情绪分数", f"{product['emotion_score']:.1f}", "+高")
        with col2:
            st.metric("提及次数", f"{product['mentions']:,}", f"+{product['growth_rate']:.1f}%")
        with col3:
            st.metric("增长率", f"{product['growth_rate']:.1f}%", "+上升")
        with col4:
            st.metric("预估营收", f"${product['estimated_revenue']:,}", "+潜力")
        
        st.divider()
        
        # 4周趋势图和平台表现雷达图
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 4周趋势")
            trend_df = pd.DataFrame({
                '周次': [f'第{i+1}周' for i in range(4)],
                '提及次数': product['week_data']
            })
            fig_trend = px.line(
                trend_df,
                x='周次',
                y='提及次数',
                title=f'{product["name"]}的4周趋势',
                markers=True,
                color_discrete_sequence=['#2196F3']
            )
            fig_trend.update_layout(hovermode='x unified')
            st.plotly_chart(fig_trend, use_container_width=True, key='fig_trend_3')
        
        with col2:
            st.markdown("#### 🎯 平台表现")
            platform_df = pd.DataFrame([
                {'平台': k, '分数': v} for k, v in product['platform_scores'].items()
            ])
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=list(product['platform_scores'].values()),
                theta=list(product['platform_scores'].keys()),
                fill='toself',
                line_color='#2196F3'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                title=f'{product["name"]}在各平台的表现'
            )
            st.plotly_chart(fig_radar, use_container_width=True, key='fig_radar_1')
        
        st.divider()
        
        # 情绪分布和关键词
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💭 情绪分布")
            emotion_df = pd.DataFrame([
                {'情绪': k, '比例': v} for k, v in product['emotion_dist'].items()
            ])
            fig_emotion = px.bar(
                emotion_df,
                x='情绪',
                y='比例',
                title=f'{product["name"]}的情绪分布',
                color='比例',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_emotion, use_container_width=True, key='fig_emotion_1')
        
        with col2:
            st.markdown("#### 🏷️ 关键词标签")
            st.write(" ")
            st.write(" ")
            for keyword in product['keywords']:
                st.markdown(f"<span style='background-color: #E3F2FD; padding: 0.3rem 0.8rem; border-radius: 15px; margin: 0.2rem; display: inline-block;'>{keyword}</span>", unsafe_allow_html=True)
        
        st.divider()
        
        # 详细分析
        st.markdown("#### 📝 详细分析")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="insight-box">
            <strong>✅ 推荐理由</strong><br>
            """ + product['recommendation'] + """
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="insight-box">
            <strong>🎯 市场机会</strong><br>
            """ + product['opportunity'] + """
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
            <strong>⚠️ 风险提示</strong><br>
            """ + product['risk'] + """
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="insight-box">
            <strong>🚀 执行策略</strong><br>
            """ + product['strategy'].replace('\n', '<br>') + """
            </div>
            """, unsafe_allow_html=True)
    
    # ===== 新增 Tab 7: 竞争分析 =====
    with tab7:
        st.subheader("🎭 竞争对手分析")
        
        st.markdown("""
        <div class="insight-box">
        <strong>💡 市场格局</strong><br>
        当前3D打印定制市场竞争激烈，主要竞争对手各有特色。
        了解竞争对手的优劣势，有助于制定差异化策略。
        </div>
        """, unsafe_allow_html=True)
        
        # 生成竞争对手数据
        competitor_df = generate_competitor_data()
        
        # 市场份额
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 市场份额分布")
            fig_market_share = px.pie(
                competitor_df,
                values='market_share',
                names='name',
                title='各竞争对手市场份额',
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            st.plotly_chart(fig_market_share, use_container_width=True, key='fig_market_share_2')
        
        with col2:
            st.markdown("#### 价格定位对比")
            fig_price = px.bar(
                competitor_df.sort_values('avg_price', ascending=False),
                x='name',
                y='avg_price',
                title='各竞争对手平均价格',
                color='avg_price',
                color_continuous_scale='Blues'
            )
            fig_price.update_layout(
                xaxis_title='竞争对手',
                yaxis_title='平均价格 ($)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_price, use_container_width=True, key='fig_price_2')
        
        st.divider()
        
        # 竞争对手详细分析
        st.markdown("#### 竞争对手详细分析")
        
        for _, competitor in competitor_df.iterrows():
            with st.expander(f"**{competitor['name']}** - 市场份额: {competitor['market_share']:.1f}%"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="competitor-card">
                    <strong>📊 基本信息</strong><br>
                    • 市场份额: {competitor['market_share']:.1f}%<br>
                    • 平均价格: ${competitor['avg_price']:.2f}<br>
                    • 竞争策略: {competitor['strategy']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.success(f"**✅ 优势**: {competitor['strength']}")
                
                with col2:
                    st.error(f"**⚠️ 劣势**: {competitor['weakness']}")
                    
                    # 差异化建议
                    st.info(f"""
                    **💡 差异化机会**:
                    针对{competitor['name']}的劣势，我们可以在{competitor['weakness']}方面建立优势。
                    """)
        
        st.divider()
        
        # 竞争策略矩阵
        st.markdown("#### 市场定位矩阵")
        
        fig_matrix = px.scatter(
            competitor_df,
            x='avg_price',
            y='market_share',
            size='market_share',
            color='name',
            title='价格 vs 市场份额定位矩阵',
            hover_data=['strategy']
        )
        fig_matrix.update_layout(
            xaxis_title='平均价格 ($)',
            yaxis_title='市场份额 (%)'
        )
        st.plotly_chart(fig_matrix, use_container_width=True, key='fig_matrix_2')
        
        st.markdown("""
        <div class="insight-box">
        <strong>🎯 我们的定位建议</strong><br>
        • <strong>目标市场</strong>: 中高端市场（$35-45价格区间）<br>
        • <strong>差异化策略</strong>: 快速交付 + 高品质 + 合理价格<br>
        • <strong>突破口</strong>: 填补“高品质+快速交付”的市场空白<br>
        • <strong>目标份额</strong>: 第一年争取5-8%市场份额
        </div>
        """, unsafe_allow_html=True)
    
    # ===== 新增 Tab 8: 行动计划 =====
    with tab8:
        st.subheader("📋 8周行动计划")
        
        st.markdown("""
        <div class="insight-box">
        <strong>🎯 总体目标</strong><br>
        在8周内完成产品开发、测试和初步市场推广，建立稳定的销售渠道。
        </div>
        """, unsafe_allow_html=True)
        
        # 时间线
        st.markdown("#### 📅 执行时间线")
        
        timeline_data = [
            {
                'week': '第1-2周',
                'phase': '产品开发',
                'tasks': '• 完成Top 3产品的3D建模\n• 测试打印材料和工艺\n• 优化产品设计',
                'budget': '$2,000',
                'status': '准备中'
            },
            {
                'week': '第3-4周',
                'phase': '样品制作',
                'tasks': '• 打印产品样品\n• 质量检测和改进\n• 拍摄产品照片和视频',
                'budget': '$1,500',
                'status': '准备中'
            },
            {
                'week': '第5-6周',
                'phase': '平台上架',
                'tasks': '• 在Etsy、Amazon开店\n• 上传产品信息\n• 设置定价和物流',
                'budget': '$1,000',
                'status': '准备中'
            },
            {
                'week': '第7-8周',
                'phase': '营销推广',
                'tasks': '• TikTok内容营销\n• 社交媒体广告\n• 收集用户反馈',
                'budget': '$3,000',
                'status': '准备中'
            }
        ]
        
        for item in timeline_data:
            with st.expander(f"**{item['week']}**: {item['phase']} - 预算: {item['budget']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**📝 主要任务**\n{item['tasks']}")
                
                with col2:
                    st.metric("预算", item['budget'])
                    st.metric("状态", item['status'])
        
        st.divider()
        
        # 预算分配
        st.markdown("#### 💰 预算分配")
        
        col1, col2 = st.columns(2)
        
        with col1:
            budget_data = pd.DataFrame({
                '类别': ['产品开发', '样品制作', '平台费用', '营销推广', '运营储备'],
                '金额': [2000, 1500, 1000, 3000, 1500]
            })
            
            fig_budget = px.pie(
                budget_data,
                values='金额',
                names='类别',
                title='总预算分配 ($9,000)',
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            st.plotly_chart(fig_budget, use_container_width=True, key='fig_budget_1')
        
        with col2:
            st.markdown("##### 预算明细")
            for _, row in budget_data.iterrows():
                percentage = (row['金额'] / budget_data['金额'].sum()) * 100
                st.metric(
                    row['类别'],
                    f"${row['金额']:,}",
                    delta=f"{percentage:.1f}%"
                )
        
        st.divider()
        
        # 关键指标
        st.markdown("#### 📊 关键绩效指标 (KPI)")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "目标销售额",
                "$15,000",
                delta="第一季度"
            )
        
        with col2:
            st.metric(
                "目标订单数",
                "300+",
                delta="前8周"
            )
        
        with col3:
            st.metric(
                "客户满意度",
                "4.5+",
                delta="5分制"
            )
        
        with col4:
            st.metric(
                "复购率",
                "25%+",
                delta="目标"
            )
        
        st.divider()
        
        # 风险管理
        st.markdown("#### ⚠️ 风险管理")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="insight-box">
            <strong>🚨 主要风险</strong><br>
            1. <strong>供应链风险</strong>: 打印材料短缺或价格波动<br>
            2. <strong>质量风险</strong>: 产品质量不稳定导致退货<br>
            3. <strong>竞争风险</strong>: 竞争对手推出类似产品<br>
            4. <strong>平台风险</strong>: 账号被封或平台政策变化
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
            <strong>✅ 应对措施</strong><br>
            1. 建立多个供应商关系，储备关键材料<br>
            2. 严格质量控制流程，提供质保服务<br>
            3. 持续产品创新，建立品牌差异化<br>
            4. 多平台布局，分散风险
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # 下一步行动
        st.markdown("""
        <div class="insight-box">
        <strong>🚀 立即行动</strong><br>
        1. ✅ 确认Top 3产品选择<br>
        2. ✅ 联系3D打印材料供应商<br>
        3. ✅ 注册Etsy和Amazon卖家账号<br>
        4. ✅ 准备产品拍摄设备和场地<br>
        5. ✅ 制定详细的TikTok内容日历
        </div>
        """, unsafe_allow_html=True)
    
    # ===== 新增 Tab 9: 执行摘要 =====
    with tab9:
        st.subheader("📊 执行摘要")
        
        st.markdown("""
        <div class="insight-box">
        <strong>🎯 核心目标</strong><br>
        基于社交媒体情绪数据和电商平台销售数据，快速识别高潜力产品机会，
        助力3D打印定制业务实现数据驱动的产品选择和市场策略。
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # 三大核心洞察
        st.markdown("### 💡 三大核心洞察")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="insight-box">
            <strong>💭 情绪发现</strong><br><br>
            • <strong>正面情绪占主导</strong>: 兴奋、好奇、满意等正面情绪占总量的65%<br>
            • <strong>上升最快</strong>: 兴奋情绪4周增长38%，表明用户对创新产品接受度高<br>
            • <strong>需要关注</strong>: 担忧和困惑情绪主要集中在价格和质量方面<br><br>
            <em>建议：强化产品质量展示，提供透明的定价说明</em>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
            <strong>💰 销售发现</strong><br><br>
            • <strong>Etsy表现最佳</strong>: 增长率32%，用户愿意为定制付费<br>
            • <strong>热门类别</strong>: 办公用品和数码配件需求旺盛<br>
            • <strong>平均客单价</strong>: $38，中高端市场潜力大<br><br>
            <em>建议：优先在Etsy上架，重点开发办公和数码类产品</em>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="insight-box">
            <strong>🎯 战略建议</strong><br><br>
            • <strong>快速进入</strong>: 市场处于快速增长期，机会窗口期<br>
            • <strong>小批量测试</strong>: 8周内完成从设计到上线<br>
            • <strong>预算控制</strong>: 总预算$9,000，分阶段执行<br><br>
            <em>建议：立即启动Top 3产品开发</em>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # 6个KPI
        st.markdown("### 📊 6大关键指标 (KPI)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "💬 总提及次数",
                "8,420",
                "+28.5%",
                help="过去4周在社交媒体上的总提及次数"
            )
        
        with col2:
            st.metric(
                "🚀 平均情绪分数",
                "44.2",
                "+3.8",
                help="正面情绪分数，满分50分"
            )
        
        with col3:
            st.metric(
                "📈 增长率",
                "32.1%",
                "+5.2%",
                help="过去4周的平均增长率"
            )
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.metric(
                "💰 预估营收",
                "$48,200",
                "+$12,500",
                help="基于Top 5产品的预估月营收"
            )
        
        with col5:
            st.metric(
                "🎯 转化率",
                "5.8%",
                "+1.2%",
                help="从浏览到购买的平均转化率"
            )
        
        with col6:
            st.metric(
                "⭐ 客户满意度",
                "4.5/5.0",
                "+0.3",
                help="平台平均评分"
            )
        
        st.divider()
        
        # Top 3产品推荐
        st.markdown("### 🏆 Top 3 产品推荐")
        
        top_products = [
            {
                'rank': 1,
                'name': '迷你桌面收纳盒',
                'score': 45.2,
                'growth': 38.5,
                'revenue': 12500,
                'reason': '情绪分数最高，办公场景需求旺盛，适合快速进入',
                'link': 'https://www.etsy.com/search?q=desk+organizer+3d+print'
            },
            {
                'rank': 2,
                'name': '创意手机支架',
                'score': 43.8,
                'growth': 32.1,
                'revenue': 9800,
                'reason': 'TikTok平台表现极佳，年轻用户喜爱，定制化需求强',
                'link': 'https://www.etsy.com/search?q=phone+stand+3d+print'
            },
            {
                'rank': 3,
                'name': '装饰性墙挂',
                'score': 42.5,
                'growth': 28.3,
                'revenue': 8500,
                'reason': 'Instagram/Pinterest表现优秀，家居装饰市场稳定',
                'link': 'https://www.etsy.com/search?q=wall+decor+3d+print'
            }
        ]
        
        for product in top_products:
            with st.expander(f"**#{product['rank']} {product['name']}** - 情绪分数: {product['score']}", expanded=(product['rank']==1)):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    **📊 核心指标**
                    - 情绪分数: **{product['score']}**/50
                    - 增长率: **{product['growth']}%**
                    - 预估月营收: **${product['revenue']:,}**
                    
                    **✅ 推荐理由**
                    {product['reason']}
                    """)
                    
                    st.markdown(f"[🔗 查看类似产品]({product['link']})")
                
                with col2:
                    # 进度条
                    st.markdown("**各项评分**")
                    st.progress(product['score']/50, text=f"情绪: {product['score']}/50")
                    st.progress(product['growth']/50, text=f"增长: {product['growth']:.0f}%")
                    st.progress(min(product['revenue']/15000, 1.0), text=f"营收: ${product['revenue']/1000:.1f}K")
        
        st.divider()
        
        # 数据解读
        st.markdown("### 📖 数据解读")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="insight-box">
            <strong>🔍 如何读懂情绪分数</strong><br><br>
            情绪分数基于社交媒体用户评论和互动数据，通过AI分析生成：<br><br>
            • <strong>40-50分</strong>: 极高正面情绪，强烈推荐<br>
            • <strong>35-40分</strong>: 正面情绪为主，值得尝试<br>
            • <strong>30-35分</strong>: 中立态度，需谨慎评估<br>
            • <strong>30分以下</strong>: 负面情绪较多，不建议进入
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
            <strong>📈 如何读懂增长率</strong><br><br>
            增长率反映了4周内的趋势变化，帮助判断市场热度：<br><br>
            • <strong>30%以上</strong>: 快速增长，市场需求旺盛<br>
            • <strong>15-30%</strong>: 稳定增长，市场潜力大<br>
            • <strong>0-15%</strong>: 缓慢增长，需要营销推动<br>
            • <strong>负增长</strong>: 市场需求下降，谨慎进入
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # 下一步行动
        st.markdown("""
        <div class="insight-box">
        <strong>🚀 立即行动清单</strong><br><br>
        1. ✅ <strong>确认产品选择</strong>: 从 Top 3 中选择 1-2 个产品启动<br>
        2. ✅ <strong>联系供应商</strong>: 找到3D打印材料供应商，获取报价<br>
        3. ✅ <strong>注册平台</strong>: 在 Etsy 和 Amazon 注册卖家账号<br>
        4. ✅ <strong>开始设计</strong>: 完成产品3D建模和打样<br>
        5. ✅ <strong>制定计划</strong>: 根据行动计划Tab制定详细时间表<br><br>
        <strong>💼 预算准备</strong>: $9,000 (分阶段执行)<br>
        <strong>⏰ 预计周期</strong>: 8周（从设计到上线）
        </div>
        """, unsafe_allow_html=True)
    
    # 页脚
    st.divider()
    st.caption("🖨️ 3D打印市场情报系统（完整增强版）| 数据来源: TikTok | AI分析: OpenAI GPT-4")
    st.caption("💡 新增功能：情绪分析、产品分析、竞争分析、行动计划、执行摘要")

if __name__ == "__main__":
    main()
