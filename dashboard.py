#!/usr/bin/env python3
"""
3D打印市场情报仪表板
Streamlit Dashboard for 3D Printing Market Intelligence
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import glob
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="3D打印市场情报仪表板",
    page_icon="🖨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
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
    
    # 标签页
    tab1, tab2, tab3, tab4 = st.tabs(["📋 产品排名", "📊 数据分析", "🤖 AI洞察", "📈 历史趋势"])
    
    # Tab 1: 产品排名表格
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
    
    # Tab 2: 数据分析
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
    
    # Tab 3: AI洞察
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
                st.metric("排名", f"#{int(product_data['product_rank'])}")
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
    
    # Tab 4: 历史趋势
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
    
    # 页脚
    st.divider()
    st.caption("🖨️ 3D打印市场情报系统 | 数据来源: TikTok | AI分析: OpenAI GPT-4")

if __name__ == "__main__":
    main()
