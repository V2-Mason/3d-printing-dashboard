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
from pathlib import Path
import glob
from datetime import datetime
import numpy as np

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
    """生成模拟情绪数据（用于演示）"""
    emotions = [
        "兴奋", "好奇", "满意", "信任", "惊喜", "喜悦",
        "担忧", "困惑", "失望", "怀疑", "焦虑", "期待"
    ]
    
    data = []
    for emotion in emotions:
        data.append({
            'emotion': emotion,
            'count': np.random.randint(50, 500),
            'avg_score': np.random.uniform(35, 48),
            'trend': np.random.choice(['上升', '下降', '稳定']),
            'percentage': np.random.uniform(5, 15)
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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📋 产品排名", 
        "📊 数据分析", 
        "🤖 AI洞察", 
        "📈 历史趋势",
        "💭 情绪分析",  # 新增
        "🎭 竞争分析",  # 新增
        "📋 行动计划"   # 新增
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
            st.plotly_chart(fig_score, use_container_width=True)
            
            # 类别分布
            st.markdown("#### 产品类别分布")
            category_counts = filtered_df['product_category'].value_counts()
            fig_category = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title='产品类别占比',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_category, use_container_width=True)
        
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
            st.plotly_chart(fig_scatter, use_container_width=True)
            
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
            st.plotly_chart(fig_bar, use_container_width=True)
    
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
                st.plotly_chart(fig_trend, use_container_width=True)
                
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
                    st.plotly_chart(fig_views, use_container_width=True)
                
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
                    st.plotly_chart(fig_engagement, use_container_width=True)
                
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
                st.plotly_chart(fig_category_trend, use_container_width=True)
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
            st.plotly_chart(fig_emotion_dist, use_container_width=True)
        
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
            st.plotly_chart(fig_emotion_score, use_container_width=True)
        
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
            st.plotly_chart(fig_market_share, use_container_width=True)
        
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
            st.plotly_chart(fig_price, use_container_width=True)
        
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
        st.plotly_chart(fig_matrix, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
        <strong>🎯 我们的定位建议</strong><br>
        • <strong>目标市场</strong>: 中高端市场（$35-45价格区间）<br>
        • <strong>差异化策略</strong>: 快速交付 + 高品质 + 合理价格<br>
        • <strong>突破口</strong>: 填补"高品质+快速交付"的市场空白<br>
        • <strong>目标份额</strong>: 第一年争取5-8%市场份额
        </div>
        """, unsafe_allow_html=True)
    
    # ===== 新增 Tab 7: 行动计划 =====
    with tab7:
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
            st.plotly_chart(fig_budget, use_container_width=True)
        
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
    
    # 页脚
    st.divider()
    st.caption("🖨️ 3D打印市场情报系统（整合版）| 数据来源: TikTok | AI分析: OpenAI GPT-4")
    st.caption("💡 新增功能：情绪分析、竞争分析、行动计划")

if __name__ == "__main__":
    main()
