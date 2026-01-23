"""
动态执行摘要生成器
基于实际数据生成每周不同的洞察和建议
"""

import pandas as pd
import numpy as np

def generate_dynamic_summary(df):
    """
    基于数据生成动态执行摘要
    
    参数:
        df: DataFrame - 当前周的数据
    
    返回:
        dict - 包含三大洞察和关键指标的字典
    """
    summary = {}
    
    # ===== 情绪发现 =====
    emotion_insight = analyze_emotion_trends(df)
    summary['emotion'] = emotion_insight
    
    # ===== 销售发现 =====
    sales_insight = analyze_sales_trends(df)
    summary['sales'] = sales_insight
    
    # ===== 战略建议 =====
    strategy_insight = generate_strategy_recommendations(df)
    summary['strategy'] = strategy_insight
    
    # ===== 关键指标 =====
    kpis = calculate_kpis(df)
    summary['kpis'] = kpis
    
    return summary


def analyze_emotion_trends(df):
    """分析情绪趋势"""
    insight = {}
    
    # 计算情绪分布
    if 'sentiment_positive_pct' in df.columns:
        positive_pct = df['sentiment_positive_pct'].mean()
        neutral_pct = df['sentiment_neutral_pct'].mean()
        negative_pct = df['sentiment_negative_pct'].mean()
        
        insight['positive_pct'] = positive_pct
        insight['dominant_sentiment'] = '正面' if positive_pct > 50 else '中性'
    
    # 找出最高情绪分数的产品
    if 'emotion_score' in df.columns:
        top_emotion = df.nlargest(1, 'emotion_score')
        if not top_emotion.empty:
            insight['top_product'] = top_emotion.iloc[0]['product_name']
            insight['top_score'] = top_emotion.iloc[0]['emotion_score']
    
    # 分析情绪趋势
    if 'emotion_trend' in df.columns:
        trend_counts = df['emotion_trend'].value_counts()
        if not trend_counts.empty:
            insight['trend_direction'] = trend_counts.index[0]
    
    # 计算平均情绪分
    if 'emotion_score' in df.columns:
        insight['avg_emotion'] = df['emotion_score'].mean()
    
    return insight


def analyze_sales_trends(df):
    """分析销售趋势"""
    insight = {}
    
    # 按平台分析
    if 'platform' in df.columns:
        platform_performance = df.groupby('platform').agg({
            'views': 'sum',
            'sales_volume': 'sum',
            'revenue_estimate': 'sum'
        }).sort_values('revenue_estimate', ascending=False)
        
        if not platform_performance.empty:
            top_platform = platform_performance.index[0]
            insight['top_platform'] = top_platform
            insight['top_platform_revenue'] = platform_performance.iloc[0]['revenue_estimate']
    
    # 按类别分析
    if 'product_category' in df.columns:
        category_performance = df.groupby('product_category').agg({
            'views': 'sum',
            'sales_volume': 'sum'
        }).sort_values('views', ascending=False)
        
        if not category_performance.empty:
            top_category = category_performance.index[0]
            insight['top_category'] = top_category
            insight['top_category_views'] = category_performance.iloc[0]['views']
    
    # 计算平均价格
    if 'price_avg' in df.columns:
        insight['avg_price'] = df['price_avg'].mean()
    
    # 计算增长率
    if 'growth_rate' in df.columns:
        insight['avg_growth'] = df['growth_rate'].mean()
        insight['max_growth'] = df['growth_rate'].max()
    
    return insight


def generate_strategy_recommendations(df):
    """生成战略建议"""
    recommendations = {}
    
    # 分析市场机会
    if 'market_potential' in df.columns:
        high_potential = df[df['market_potential'] == 'high']
        recommendations['high_potential_count'] = len(high_potential)
    
    # 分析竞争水平
    if 'competition_level' in df.columns:
        low_competition = df[df['competition_level'] == 'low']
        recommendations['low_competition_count'] = len(low_competition)
    
    # 推荐优先级
    if 'action_priority' in df.columns:
        high_priority = df[df['action_priority'] == 'high']
        recommendations['high_priority_products'] = high_priority['product_name'].tolist()[:3]
    
    # ROI估算
    if 'roi_estimate' in df.columns:
        recommendations['avg_roi'] = df['roi_estimate'].mean()
        recommendations['max_roi'] = df['roi_estimate'].max()
    
    return recommendations


def calculate_kpis(df):
    """计算关键指标"""
    kpis = {}
    
    # 总提及次数
    if 'views' in df.columns:
        kpis['total_mentions'] = int(df['views'].sum())
    
    # 平均情绪分数
    if 'emotion_score' in df.columns:
        kpis['avg_emotion_score'] = round(df['emotion_score'].mean(), 1)
    
    # 增长率
    if 'growth_rate' in df.columns:
        kpis['avg_growth_rate'] = round(df['growth_rate'].mean(), 1)
    
    # 预估营收
    if 'revenue_estimate' in df.columns:
        kpis['total_revenue'] = int(df['revenue_estimate'].sum())
    
    # 转化率
    if 'conversion_rate' in df.columns:
        kpis['avg_conversion_rate'] = round(df['conversion_rate'].mean(), 2)
    
    # 客户满意度（基于评分）
    if 'rating_avg' in df.columns:
        kpis['avg_rating'] = round(df['rating_avg'].mean(), 2)
    
    return kpis


def format_insight_html(summary):
    """将洞察格式化为HTML"""
    emotion = summary.get('emotion', {})
    sales = summary.get('sales', {})
    strategy = summary.get('strategy', {})
    
    # 情绪洞察
    emotion_html = f"""
    <div class="insight-box">
    <strong>情绪发现</strong><br><br>
    • <strong>情绪主导</strong>: {emotion.get('dominant_sentiment', '正面')}情绪占主导，
    正面情绪占比{emotion.get('positive_pct', 0):.1f}%<br>
    • <strong>最佳表现</strong>: "{emotion.get('top_product', 'N/A')}" 
    情绪分数{emotion.get('top_score', 0):.1f}<br>
    • <strong>平均情绪分</strong>: {emotion.get('avg_emotion', 0):.1f}分，
    整体{emotion.get('trend_direction', '稳定')}<br><br>
    <em>建议：关注高情绪分产品，分析用户喜好特征</em>
    </div>
    """
    
    # 销售洞察
    top_platform = sales.get('top_platform', 'N/A')
    top_category = sales.get('top_category', 'N/A')
    avg_price = sales.get('avg_price', 0)
    avg_growth = sales.get('avg_growth', 0)
    
    sales_html = f"""
    <div class="insight-box">
    <strong>销售发现</strong><br><br>
    • <strong>{top_platform}表现最佳</strong>: 
    预估营收${sales.get('top_platform_revenue', 0):,.0f}<br>
    • <strong>热门类别</strong>: {top_category}需求旺盛<br>
    • <strong>平均客单价</strong>: ${avg_price:.2f}，
    平均增长率{avg_growth:+.1f}%<br><br>
    <em>建议：优先在{top_platform}上架，重点开发{top_category}类产品</em>
    </div>
    """
    
    # 战略建议
    high_priority = strategy.get('high_priority_products', [])
    priority_text = "、".join(high_priority[:3]) if high_priority else "待分析"
    avg_roi = strategy.get('avg_roi', 0)
    
    strategy_html = f"""
    <div class="insight-box">
    <strong>战略建议</strong><br><br>
    • <strong>高潜力产品</strong>: {strategy.get('high_potential_count', 0)}个产品值得关注<br>
    • <strong>低竞争机会</strong>: {strategy.get('low_competition_count', 0)}个细分市场竞争较小<br>
    • <strong>预期ROI</strong>: 平均{avg_roi:.1f}%，最高{strategy.get('max_roi', 0):.1f}%<br><br>
    <em>建议：优先开发 {priority_text}</em>
    </div>
    """
    
    return emotion_html, sales_html, strategy_html
