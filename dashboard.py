"""
3D打印市场情报仪表板
优化版本 - 移除emoji,增强数据可追溯性
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

# Import custom modules
import data_manager_gdrive as dm
import components as comp
import analytics as ana

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
    .stApp {
        background-color: #F8F9FA;
    }
    
    h1, h2, h3 {
        color: #2C3E50;
        font-weight: 600;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 600;
        color: #3498DB;
    }
    
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #3498DB;
    }
    
    .streamlit-expanderHeader {
        background-color: #ECF0F1;
        border-radius: 6px;
        font-weight: 500;
    }
    
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    .stButton>button {
        border-radius: 6px;
        border: none;
        background-color: #3498DB;
        color: white;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #2980B9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E0E0E0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """主函数"""
    
    # 侧边栏 - 配置选项
    with st.sidebar:
        st.title("配置选项")
        
        # 选择周次
        available_weeks = dm.get_available_weeks()
        if not available_weeks:
            st.error("无法加载周次数据")
            return
        
        selected_week_num = st.selectbox(
            "选择周次",
            options=available_weeks,
            format_func=lambda x: f"第 {x:02d} 周",
            key="week_selector"
        )
        
        st.markdown("---")
        
        # 数据筛选
        st.subheader("数据筛选")
        
        # 加载数据
        df = dm.load_week_data(selected_week_num)
        
        if df is None or df.empty:
            st.error(f"无法加载第{selected_week_num}周数据")
            return
        
        # 类别筛选
        categories = ['全部'] + sorted(df['product_category'].unique().tolist())
        selected_category = st.selectbox("产品类别", categories)
        
        # 轨道类型筛选
        track_types = ['全部'] + sorted(df['track_type'].unique().tolist())
        selected_track = st.selectbox("轨道类型", track_types)
        
        # 应用筛选
        filtered_df = df.copy()
        if selected_category != '全部':
            filtered_df = filtered_df[filtered_df['product_category'] == selected_category]
        if selected_track != '全部':
            filtered_df = filtered_df[filtered_df['track_type'] == selected_track]
        
        st.markdown("---")
        st.caption(f"数据更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # 主标题
    st.title("3D打印市场情报仪表板")
    st.markdown(f"**当前查看**: 第 {selected_week_num:02d} 周数据")
    
    # 标签页
    tabs = st.tabs([
        "执行摘要",
        "产品排名",
        "数据分析",
        "AI洞察",
        "历史趋势",
        "情绪分析",
        "产品分析",
        "竞争分析",
        "行动计划"
    ])
    
    # ==================== 标签页1: 执行摘要 ====================
    with tabs[0]:
        render_executive_summary(filtered_df, selected_week_num)
    
    # ==================== 标签页2: 产品排名 ====================
    with tabs[1]:
        render_product_ranking(filtered_df)
    
    # ==================== 标签页3: 数据分析 ====================
    with tabs[2]:
        render_data_analysis(filtered_df, selected_week_num)
    
    # ==================== 标签页4: AI洞察 ====================
    with tabs[3]:
        render_ai_insights(filtered_df, selected_week_num)
    
    # ==================== 标签页5: 历史趋势 ====================
    with tabs[4]:
        render_historical_trends(selected_week_num)
    
    # ==================== 标签页6: 情绪分析 ====================
    with tabs[5]:
        render_emotion_analysis(filtered_df, selected_week_num)
    
    # ==================== 标签页7: 产品分析 ====================
    with tabs[6]:
        render_product_analysis(filtered_df)
    
    # ==================== 标签页8: 竞争分析 ====================
    with tabs[7]:
        render_competitor_analysis(filtered_df, selected_week_num)
    
    # ==================== 标签页9: 行动计划 ====================
    with tabs[8]:
        render_action_plan(filtered_df, selected_week_num)


def render_executive_summary(df: pd.DataFrame, week_num: int):
    """渲染执行摘要页面"""
    st.header("执行摘要")
    
    # 加载摘要数据
    summary_data = dm.load_summary_data(week_num)
    
    # 生成动态摘要
    summary = ana.generate_executive_summary(df, summary_data)
    
    # 关键指标
    st.subheader("关键指标")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        comp.kpi_card(
            "总产品数",
            len(df),
            help_text="本周分析的产品总数"
        )
    
    with col2:
        comp.kpi_card(
            "平均总分",
            f"{df['total_score'].mean():.2f}",
            help_text="所有产品的平均综合评分"
        )
    
    with col3:
        comp.kpi_card(
            "总浏览量",
            ana.format_number(df['views'].sum()),
            help_text="所有产品的总浏览量"
        )
    
    with col4:
        comp.kpi_card(
            "总点赞数",
            ana.format_number(df['likes'].sum()),
            help_text="所有产品的总点赞数"
        )
    
    st.markdown("---")
    
    # 核心目标
    st.subheader("核心目标")
    st.info(summary['core_goal'])
    
    st.markdown("---")
    
    # 三大核心洞察
    st.subheader("三大核心洞察")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"#### {summary['insight_1_title']}")
        st.markdown(summary['insight_1_content'])
    
    with col2:
        st.markdown(f"#### {summary['insight_2_title']}")
        st.markdown(summary['insight_2_content'])
    
    with col3:
        st.markdown(f"#### {summary['insight_3_title']}")
        st.markdown(summary['insight_3_content'])
    
    st.markdown("---")
    
    # Top 3 产品推荐
    st.subheader("Top 3 产品推荐")
    
    recommendations = ana.generate_product_recommendations(df, top_n=3)
    
    for i, product in enumerate(recommendations, 1):
        comp.recommendation_card(product, i)


def render_product_ranking(df: pd.DataFrame):
    """渲染产品排名页面"""
    st.header("产品排名")
    
    # 排序选项
    sort_options = {
        "总分": "total_score",
        "情绪分": "emotion_score",
        "增长率": "growth_rate",
        "浏览量": "views",
        "互动率": "engagement_rate",
        "ROI估算": "roi_estimate"
    }
    
    col1, col2 = st.columns([3, 1])
    with col1:
        sort_by = st.selectbox("排序依据", list(sort_options.keys()))
    with col2:
        sort_order = st.radio("排序", ["降序", "升序"], horizontal=True)
    
    # 排序
    sorted_df = df.sort_values(
        by=sort_options[sort_by],
        ascending=(sort_order == "升序")
    )
    
    # 显示产品列表
    for idx, row in sorted_df.iterrows():
        with st.expander(f"#{idx+1} {row['product_name']} - {sort_by}: {row[sort_options[sort_by]]:.2f}"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("总分", f"{row['total_score']:.1f}")
                st.metric("情绪分", f"{row['emotion_score']:.1f}/50")
            
            with col2:
                st.metric("增长率", f"{row['growth_rate']:.1f}%")
                st.metric("浏览量", ana.format_number(row['views']))
            
            with col3:
                st.metric("互动率", f"{row['engagement_rate']:.2f}%")
                st.metric("转化率", f"{row['conversion_rate']:.2f}%")
            
            with col4:
                st.metric("预估月营收", f"${row['revenue_estimate']:,.0f}")
                st.metric("ROI估算", f"{row['roi_estimate']:.1f}%")
            
            st.markdown(f"**类别**: {row['product_category']} > {row['product_subcategory']}")
            st.markdown(f"**轨道类型**: {row['track_type']}")
            st.markdown(f"**目标受众**: {row['target_audience']}")


def render_data_analysis(df: pd.DataFrame, week_num: int):
    """渲染数据分析页面"""
    st.header("数据分析")
    
    # 加载平台对比数据
    platform_data = dm.load_platform_comparison(week_num)
    
    if platform_data is not None and not platform_data.empty:
        st.subheader("平台对比")
        comp.data_source_table(platform_data)
        
        # 平台增长率对比
        comp.comparison_chart(
            platform_data,
            x_col='platform',
            y_col='growth_rate',
            color_col='platform_type',
            title="各平台增长率对比"
        )
        
        st.markdown("---")
    
    # 类别分析
    st.subheader("类别分析")
    
    category_stats = df.groupby('product_category').agg({
        'total_score': 'mean',
        'growth_rate': 'mean',
        'revenue_estimate': 'sum',
        'product_id': 'count'
    }).reset_index()
    
    category_stats.columns = ['类别', '平均总分', '平均增长率', '总预估营收', '产品数']
    
    comp.comparison_chart(
        category_stats,
        x_col='类别',
        y_col='平均总分',
        title="各类别平均总分对比"
    )
    
    st.dataframe(category_stats, use_container_width=True, hide_index=True)


def render_ai_insights(df: pd.DataFrame, week_num: int):
    """渲染AI洞察页面"""
    st.header("AI洞察")
    
    # 加载主题分析数据
    topic_data = dm.load_topic_analysis(week_num)
    
    if topic_data is not None and not topic_data.empty:
        # 提取洞察
        insights = ana.extract_emotion_topic_insights(topic_data)
        
        st.subheader("关键发现")
        
        for insight in insights:
            comp.solution_panel(
                problem=insight['title'],
                data_evidence=f"数据来源:\n" + "\n".join([f"- {k}: {v}" for k, v in insight['data'].items()]),
                solution=insight['solution'],
                action_items=[]
            )
        
        st.markdown("---")
        
        # 主题-情绪热力图
        st.subheader("主题-情绪关联分析")
        comp.topic_emotion_heatmap(topic_data)
    
    # 价格敏感度分析
    if topic_data is not None:
        st.markdown("---")
        st.subheader("价格敏感度分析")
        
        price_analysis = ana.analyze_price_sensitivity(df, topic_data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "价格相关担忧占比",
                f"{price_analysis['price_worry_pct']:.1f}%",
                help_text="担忧情绪中与价格相关的比例"
            )
        
        with col2:
            st.metric(
                "平均价格",
                f"${price_analysis['avg_price']:.2f}",
                help_text="所有产品的平均价格"
            )
        
        with col3:
            st.metric(
                "最佳价格区间",
                price_analysis['best_price_range'],
                help_text="用户接受度最高的价格区间"
            )
        
        st.info(f"{price_analysis['recommendation']}")


def render_historical_trends(week_num: int):
    """渲染历史趋势页面"""
    st.header("历史趋势")
    
    # 获取所有可用周次
    available_weeks = dm.get_available_weeks()
    
    if len(available_weeks) < 2:
        st.info("历史数据不足，需要至少2周数据才能显示趋势")
        return
    
    # 加载多周数据
    trend_data = []
    for week in available_weeks:
        df = dm.load_week_data(week)
        if df is not None:
            trend_data.append({
                'week': week,
                'avg_score': df['total_score'].mean(),
                'avg_emotion': df['emotion_score'].mean(),
                'avg_growth': df['growth_rate'].mean(),
                'total_products': len(df)
            })
    
    if trend_data:
        trend_df = pd.DataFrame(trend_data)
        
        # 趋势图
        comp.trend_line_chart(
            trend_df,
            x_col='week',
            y_cols=['avg_score', 'avg_emotion', 'avg_growth'],
            title="关键指标趋势"
        )
        
        st.dataframe(trend_df, use_container_width=True, hide_index=True)


def render_emotion_analysis(df: pd.DataFrame, week_num: int):
    """渲染情绪分析页面"""
    st.header("情绪分析")
    
    # 加载情绪分析数据
    emotion_data = dm.load_emotion_analysis(week_num)
    
    if emotion_data is None or emotion_data.empty:
        st.warning("暂无情绪分析数据")
        return
    
    # 情绪健康度仪表盘
    st.subheader("情绪健康度")
    emotion_score, status, analysis = ana.analyze_emotion_health(emotion_data)
    comp.emotion_health_gauge(emotion_score)
    
    # 健康度解读
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("正面情绪占比", f"{analysis['positive_pct']:.1f}%")
    
    with col2:
        st.metric("负面情绪占比", f"{analysis['negative_pct']:.1f}%")
    
    with col3:
        st.metric("市场建议", analysis['recommendation'])
    
    st.markdown("---")
    
    # 情绪分布
    st.subheader("情绪分布详解")
    comp.emotion_distribution_chart(emotion_data)
    
    st.markdown("---")
    
    # 各情绪详细分析
    st.subheader("情绪-行为映射")
    
    for _, row in emotion_data.iterrows():
        emotion_dict = row.to_dict()
        comp.emotion_behavior_mapping(row['emotion'], emotion_dict)
        st.markdown("---")
    
    # 情绪解读指南
    with st.expander("情绪解读指南"):
        st.markdown("""
        ### 情绪定义与业务价值
        
        **兴奋**
        - 定义: 用户表现出强烈的购买意愿和积极评价
        - 关键词: 太棒了、想买、立即下单、惊艳
        - 行为映射: 高互动率(>8%)、高转化率(>10%)、低退货率(<5%)
        - 业务价值: 主轨道产品首选，预期ROI>80%
        
        **满意**
        - 定义: 用户对产品质量和功能表示认可
        - 关键词: 不错、满意、值得、推荐
        - 行为映射: 中等互动率(5-8%)、稳定转化率(6-10%)、高复购率(>15%)
        - 业务价值: 稳定盈利产品，适合长期运营
        
        **好奇**
        - 定义: 用户对产品感兴趣但尚未决定购买
        - 关键词: 有意思、想了解、怎么样、试试
        - 行为映射: 高点击率(>12%)、低转化率(3-5%)、高咨询率(>20%)
        - 业务价值: 潜在市场，需要教育和引导
        
        **中性**
        - 定义: 用户态度不明确，观望状态
        - 关键词: 一般、还行、看看、考虑
        - 行为映射: 中等点击率(5-8%)、低转化率(<3%)
        - 业务价值: 需要优化产品或营销策略
        
        **担忧**
        - 定义: 用户对产品某些方面存在顾虑
        - 关键词: 担心、不确定、会不会、怕
        - 行为映射: 高跳出率(>45%)、低转化率(<2%)、高咨询率(>25%)
        - 业务价值: 需要解决用户痛点，提供保障
        
        **困惑**
        - 定义: 用户不理解产品用途或使用方法
        - 关键词: 不知道、怎么用、什么意思、不明白
        - 行为映射: 高跳出率(>50%)、极低转化率(<1%)
        - 业务价值: 需要优化产品说明和用户教育
        """)


def render_product_analysis(df: pd.DataFrame):
    """渲染产品分析页面"""
    st.header("产品分析")
    
    # 产品详情搜索
    product_names = df['product_name'].tolist()
    selected_product = st.selectbox("选择产品", product_names)
    
    product_data = df[df['product_name'] == selected_product].iloc[0]
    
    # 产品概览
    st.subheader(f"{product_data['product_name']}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总分", f"{product_data['total_score']:.1f}")
        st.metric("情绪分", f"{product_data['emotion_score']:.1f}/50")
    
    with col2:
        st.metric("增长率", f"{product_data['growth_rate']:.1f}%")
        st.metric("浏览量", ana.format_number(product_data['views']))
    
    with col3:
        st.metric("互动率", f"{product_data['engagement_rate']:.2f}%")
        st.metric("转化率", f"{product_data['conversion_rate']:.2f}%")
    
    with col4:
        st.metric("预估月营收", f"${product_data['revenue_estimate']:,.0f}")
        st.metric("ROI估算", f"{product_data['roi_estimate']:.1f}%")
    
    st.markdown("---")
    
    # 产品详情
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 基本信息")
        st.markdown(f"**类别**: {product_data['product_category']}")
        st.markdown(f"**子类别**: {product_data['product_subcategory']}")
        st.markdown(f"**轨道类型**: {product_data['track_type']}")
        st.markdown(f"**目标受众**: {product_data['target_audience']}")
    
    with col2:
        st.markdown("### 价格与销量")
        st.markdown(f"**平均价格**: ${product_data['price_avg']:.2f}")
        st.markdown(f"**价格区间**: ${product_data['price_min']:.2f} - ${product_data['price_max']:.2f}")
        st.markdown(f"**月销量**: {product_data['sales_volume']:,} 件")
        st.markdown(f"**利润率**: {product_data['profit_margin']:.1f}%")
    
    # 情绪分布
    if 'emotion_distribution' in product_data and product_data['emotion_distribution']:
        st.markdown("---")
        st.subheader("情绪分布")
        
        emotion_dist = product_data['emotion_distribution']
        if isinstance(emotion_dist, dict):
            emotion_df = pd.DataFrame([
                {'emotion': k, 'percentage': v}
                for k, v in emotion_dist.items()
            ])
            
            fig = px.bar(emotion_df, x='emotion', y='percentage', title='情绪分布')
            st.plotly_chart(fig, use_container_width=True)


def render_competitor_analysis(df: pd.DataFrame, week_num: int):
    """渲染竞争分析页面"""
    st.header("竞争分析")
    
    # 按类别分组
    categories = df['product_category'].unique()
    selected_cat = st.selectbox("选择类别进行对比", categories)
    
    cat_df = df[df['product_category'] == selected_cat]
    
    # 类别内产品对比
    st.subheader(f"{selected_cat} 类别产品对比")
    
    # 创建对比图表
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='总分',
        x=cat_df['product_name'],
        y=cat_df['total_score']
    ))
    
    fig.add_trace(go.Bar(
        name='情绪分',
        x=cat_df['product_name'],
        y=cat_df['emotion_score']
    ))
    
    fig.update_layout(
        title=f"{selected_cat} 产品评分对比",
        barmode='group',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 详细对比表
    comparison_df = cat_df[[
        'product_name',
        'total_score',
        'emotion_score',
        'growth_rate',
        'revenue_estimate',
        'roi_estimate'
    ]].copy()
    
    comparison_df.columns = ['产品名称', '总分', '情绪分', '增长率', '预估营收', 'ROI估算']
    
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)


def render_action_plan(df: pd.DataFrame, week_num: int):
    """渲染行动计划页面"""
    st.header("行动计划")
    
    # 生成推荐产品
    recommendations = ana.generate_product_recommendations(df, top_n=3)
    
    # 生成行动计划
    action_plans = ana.generate_action_plan(df, recommendations)
    
    for plan in action_plans:
        st.subheader(f"优先级 {plan['priority']}: {plan['product_name']}")
        st.markdown(f"**轨道类型**: {plan['track_type']}")
        
        for action in plan['actions']:
            with st.expander(action['phase']):
                st.markdown("**任务清单**:")
                for task in action['tasks']:
                    st.markdown(f"- {task}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("预算", action['budget'])
                with col2:
                    st.info(f"**预期成果**: {action['expected_outcome']}")
        
        st.markdown("---")


if __name__ == "__main__":
    main()
