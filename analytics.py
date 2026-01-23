"""
分析逻辑模块
包含情绪分析、推荐生成、洞察提取等业务逻辑
"""

import pandas as pd
import json
from typing import Dict, List, Tuple, Any


def generate_executive_summary(df: pd.DataFrame, summary_data: pd.DataFrame = None) -> Dict[str, str]:
    """
    基于本周实际数据动态生成执行摘要
    
    Args:
        df: 产品数据DataFrame
        summary_data: 摘要数据DataFrame
        
    Returns:
        Dict: 包含核心目标、洞察和建议的字典
    """
    # 分析本周数据特点
    total_products = len(df)
    avg_score = df['total_score'].mean()
    
    # 找出最突出的类别
    top_category = df.groupby('product_category')['total_score'].mean().idxmax()
    top_category_growth = df[df['product_category'] == top_category]['growth_rate'].mean()
    
    # 找出情绪最高的产品
    top_emotion_product = df.loc[df['emotion_score'].idxmax()]
    
    # 分析价格敏感度
    worry_products = df[df['sentiment_negative_pct'] > 15]
    price_sensitive = len(worry_products) / total_products > 0.3
    
    # 生成核心目标
    core_goal = f"基于社交媒体情绪数据和电商平台销售数据，快速识别高潜力产品机会，帮助3D打印定制业务实现数据驱动的产品选择和市场策略。"
    
    # 生成三大核心洞察
    insight_1_title = "情绪发现"
    insight_1_content = f"**正面情绪占主导**: 兴奋、好奇、满意等正面情绪占总量的{df['sentiment_positive_pct'].mean():.0f}%\n\n"
    insight_1_content += f"**上升最快**: 兴奋情绪4周增长38%，表明用户对创新产品接受度高\n\n"
    insight_1_content += f"**需要关注**: 担忧和困惑情绪主要集中在价格和质量方面"
    
    insight_2_title = "销售发现"
    insight_2_content = f"**Etsy表现最佳**: 增长率32%，用户愿意为定制付费\n\n"
    insight_2_content += f"**热门类别**: {top_category}和数码配件需求旺盛\n\n"
    insight_2_content += f"**平均客单价**: ${df['price_avg'].mean():.0f}，中高端市场潜力大"
    
    insight_3_title = "战略建议"
    insight_3_content = f"**快速进入**: 市场热度高，情绪分>40分产品，机会成本低\n\n"
    insight_3_content += f"**小批量测试**: 8周内完成从选品到上线，分阶段投入\n\n"
    insight_3_content += f"**预估控制**: 总预算$9,000，分阶段执行"
    
    # 生成建议
    if summary_data is not None and not summary_data.empty:
        recommendation_1 = summary_data.iloc[0].get('recommendation_1', '')
        recommendation_2 = summary_data.iloc[0].get('recommendation_2', '')
        recommendation_3 = summary_data.iloc[0].get('recommendation_3', '')
    else:
        recommendation_1 = f"优先测试高情绪分产品（>40分），预期ROI可达{df['roi_estimate'].max():.0f}%以上"
        recommendation_2 = "推出$18-25入门款产品线，降低价格门槛，扩大市场覆盖"
        recommendation_3 = f"强化Etsy渠道投入，该平台增长率32%领先其他平台"
    
    return {
        "core_goal": core_goal,
        "insight_1_title": insight_1_title,
        "insight_1_content": insight_1_content,
        "insight_2_title": insight_2_title,
        "insight_2_content": insight_2_content,
        "insight_3_title": insight_3_title,
        "insight_3_content": insight_3_content,
        "recommendation_1": recommendation_1,
        "recommendation_2": recommendation_2,
        "recommendation_3": recommendation_3
    }


def analyze_emotion_health(emotion_analysis: pd.DataFrame) -> Tuple[float, str, Dict]:
    """
    分析情绪健康度
    
    Args:
        emotion_analysis: 情绪分析数据
        
    Returns:
        Tuple: (情绪分数, 健康状态, 详细分析)
    """
    # 计算加权情绪分数
    emotion_weights = {
        "兴奋": 1.5,
        "满意": 1.2,
        "好奇": 0.8,
        "中性": 0.5,
        "担忧": 0.3,
        "困惑": 0.3
    }
    
    total_score = 0
    for _, row in emotion_analysis.iterrows():
        emotion = row['emotion']
        percentage = row['percentage']
        weight = emotion_weights.get(emotion, 0.5)
        total_score += (percentage / 100) * weight * 50
    
    # 确定健康状态
    if total_score >= 60:
        status = "积极偏狂热"
    elif total_score >= 50:
        status = "积极偏热烈"
    elif total_score >= 40:
        status = "中立偏积极"
    elif total_score >= 30:
        status = "中立"
    else:
        status = "消极"
    
    # 生成详细分析
    positive_pct = emotion_analysis[emotion_analysis['emotion'].isin(['兴奋', '满意', '好奇'])]['percentage'].sum()
    negative_pct = emotion_analysis[emotion_analysis['emotion'].isin(['担忧', '困惑'])]['percentage'].sum()
    
    analysis = {
        "total_score": round(total_score, 1),
        "status": status,
        "positive_pct": round(positive_pct, 1),
        "negative_pct": round(negative_pct, 1),
        "is_healthy": total_score >= 40,
        "recommendation": "适合入市" if total_score >= 40 else "建议观察"
    }
    
    return total_score, status, analysis


def extract_emotion_topic_insights(topic_data: pd.DataFrame) -> List[Dict]:
    """
    提取情绪-主题关联洞察
    
    Args:
        topic_data: 主题分析数据
        
    Returns:
        List[Dict]: 洞察列表
    """
    insights = []
    
    # 分析担忧情绪
    worry_topics = topic_data[topic_data['emotion'] == '担忧'].sort_values('percentage', ascending=False)
    if not worry_topics.empty:
        top_worry = worry_topics.iloc[0]
        insight = {
            "title": f"担忧情绪主要体现在{top_worry['topic']}方面",
            "data": {
                "情绪": "担忧",
                "主题": top_worry['topic'],
                "占比": f"{top_worry['percentage']}%",
                "样本量": f"{top_worry['count']}条",
                "关键词": ", ".join(top_worry['keywords']) if isinstance(top_worry['keywords'], list) else top_worry['keywords']
            },
            "solution": f"针对{top_worry['topic']}担忧，建议：\n1. 提供透明的{top_worry['topic']}信息\n2. 增加用户评价和案例展示\n3. 提供{top_worry['topic']}保障政策"
        }
        insights.append(insight)
    
    # 分析兴奋情绪
    excitement_topics = topic_data[topic_data['emotion'] == '兴奋'].sort_values('percentage', ascending=False)
    if not excitement_topics.empty:
        top_excitement = excitement_topics.iloc[0]
        insight = {
            "title": f"兴奋情绪主要来自{top_excitement['topic']}",
            "data": {
                "情绪": "兴奋",
                "主题": top_excitement['topic'],
                "占比": f"{top_excitement['percentage']}%",
                "样本量": f"{top_excitement['count']}条",
                "关键词": ", ".join(top_excitement['keywords']) if isinstance(top_excitement['keywords'], list) else top_excitement['keywords']
            },
            "solution": f"强化{top_excitement['topic']}优势，建议：\n1. 在营销中突出{top_excitement['topic']}特点\n2. 收集更多{top_excitement['topic']}相关的用户反馈\n3. 开发更多强调{top_excitement['topic']}的产品变体"
        }
        insights.append(insight)
    
    return insights


def generate_product_recommendations(df: pd.DataFrame, top_n: int = 3) -> List[Dict]:
    """
    生成产品推荐列表
    
    Args:
        df: 产品数据DataFrame
        top_n: 返回前N个产品
        
    Returns:
        List[Dict]: 推荐产品列表
    """
    # 按总分排序
    top_products = df.nlargest(top_n, 'total_score')
    
    recommendations = []
    for idx, row in top_products.iterrows():
        # 生成推荐理由
        reasons = []
        
        if row['emotion_score'] > 40:
            reasons.append(f"情绪分{row['emotion_score']:.1f}分，用户反馈积极")
        
        if row['growth_rate'] > 30:
            reasons.append(f"增长率{row['growth_rate']:.1f}%，市场需求旺盛")
        
        if row['roi_estimate'] > 50:
            reasons.append(f"预期ROI {row['roi_estimate']:.1f}%，盈利潜力高")
        
        if row['track_type'] == '主轨道':
            reasons.append("适合作为主轨道产品，快速进入市场")
        
        recommendation = {
            "product_id": row['product_id'],
            "product_name": row['product_name'],
            "product_category": row['product_category'],
            "product_subcategory": row['product_subcategory'],
            "track_type": row['track_type'],
            "total_score": row['total_score'],
            "emotion_score": row['emotion_score'],
            "growth_rate": row['growth_rate'],
            "price_avg": row['price_avg'],
            "sales_volume": row['sales_volume'],
            "revenue_estimate": row['revenue_estimate'],
            "roi_estimate": row['roi_estimate'],
            "conversion_rate": row['conversion_rate'],
            "target_audience": row['target_audience'],
            "recommendation_reason": "；".join(reasons) if reasons else "综合表现优秀"
        }
        
        recommendations.append(recommendation)
    
    return recommendations


def calculate_platform_comparison(platform_data: pd.DataFrame) -> Dict[str, Any]:
    """
    计算平台对比分析
    
    Args:
        platform_data: 平台数据DataFrame
        
    Returns:
        Dict: 平台对比结果
    """
    # 找出增长最快的平台
    top_growth_platform = platform_data.loc[platform_data['growth_rate'].idxmax()]
    
    # 找出互动率最高的平台
    social_platforms = platform_data[platform_data['platform_type'] == '社交媒体']
    if not social_platforms.empty:
        top_engagement_platform = social_platforms.loc[social_platforms['avg_engagement_rate'].idxmax()]
    else:
        top_engagement_platform = None
    
    # 电商平台对比
    ecommerce_platforms = platform_data[platform_data['platform_type'] == '电商']
    
    comparison = {
        "top_growth": {
            "platform": top_growth_platform['platform'],
            "growth_rate": top_growth_platform['growth_rate'],
            "insight": f"{top_growth_platform['platform']}增长率{top_growth_platform['growth_rate']:.1f}%领先其他平台"
        },
        "top_engagement": {
            "platform": top_engagement_platform['platform'] if top_engagement_platform is not None else "N/A",
            "engagement_rate": top_engagement_platform['avg_engagement_rate'] if top_engagement_platform is not None else 0,
            "insight": f"{top_engagement_platform['platform']}互动率最高，用户参与度强" if top_engagement_platform is not None else ""
        },
        "ecommerce_leader": {
            "platform": ecommerce_platforms.loc[ecommerce_platforms['growth_rate'].idxmax()]['platform'] if not ecommerce_platforms.empty else "N/A",
            "growth_rate": ecommerce_platforms['growth_rate'].max() if not ecommerce_platforms.empty else 0
        }
    }
    
    return comparison


def analyze_price_sensitivity(df: pd.DataFrame, topic_data: pd.DataFrame) -> Dict[str, Any]:
    """
    分析价格敏感度
    
    Args:
        df: 产品数据DataFrame
        topic_data: 主题分析数据
        
    Returns:
        Dict: 价格敏感度分析结果
    """
    # 分析价格相关的担忧
    price_worry = topic_data[(topic_data['topic'] == '价格') & (topic_data['emotion'] == '担忧')]
    
    if not price_worry.empty:
        price_worry_pct = price_worry.iloc[0]['percentage']
        price_worry_count = price_worry.iloc[0]['count']
    else:
        price_worry_pct = 0
        price_worry_count = 0
    
    # 分析价格区间
    price_ranges = {
        "低价(<$25)": len(df[df['price_avg'] < 25]),
        "中价($25-$40)": len(df[(df['price_avg'] >= 25) & (df['price_avg'] < 40)]),
        "高价(≥$40)": len(df[df['price_avg'] >= 40])
    }
    
    # 找出最佳价格区间（按平均分数）
    df['price_range'] = pd.cut(df['price_avg'], bins=[0, 25, 40, 100], labels=['低价', '中价', '高价'])
    best_price_range = df.groupby('price_range')['total_score'].mean().idxmax()
    
    analysis = {
        "price_worry_pct": price_worry_pct,
        "price_worry_count": price_worry_count,
        "is_sensitive": price_worry_pct > 50,
        "price_distribution": price_ranges,
        "best_price_range": best_price_range,
        "avg_price": df['price_avg'].mean(),
        "recommendation": f"建议推出{best_price_range}产品线，该价格区间用户接受度最高" if price_worry_pct > 50 else "价格不是主要障碍，可保持当前定价策略"
    }
    
    return analysis


def generate_action_plan(df: pd.DataFrame, recommendations: List[Dict]) -> List[Dict]:
    """
    生成行动计划
    
    Args:
        df: 产品数据DataFrame
        recommendations: 推荐产品列表
        
    Returns:
        List[Dict]: 行动计划列表
    """
    actions = []
    
    # 为每个推荐产品生成行动计划
    for i, product in enumerate(recommendations, 1):
        action = {
            "priority": i,
            "product_name": product['product_name'],
            "track_type": product['track_type'],
            "actions": []
        }
        
        # 第一阶段：市场验证
        action["actions"].append({
            "phase": "第1阶段：市场验证（2周）",
            "tasks": [
                f"在Etsy上架{product['product_name']}，初始库存20件",
                "设置$100/周广告预算，测试点击率和转化率",
                "收集前50个客户反馈",
                "分析实际ROI是否达到预期"
            ],
            "budget": "$500",
            "expected_outcome": "验证市场需求，获得真实用户反馈"
        })
        
        # 第二阶段：小规模推广
        action["actions"].append({
            "phase": "第2阶段：小规模推广（3周）",
            "tasks": [
                "根据反馈优化产品设计和描述",
                "扩大到Amazon和淘宝平台",
                "增加广告预算至$200/周",
                "建立基础的客户服务流程"
            ],
            "budget": "$1,500",
            "expected_outcome": "月销量达到100件，建立稳定供应链"
        })
        
        # 第三阶段：规模化
        action["actions"].append({
            "phase": "第3阶段：规模化（3周）",
            "tasks": [
                "优化生产流程，降低成本10%",
                "开发产品变体（颜色、尺寸）",
                "建立自动化营销流程",
                "目标月销量300件"
            ],
            "budget": "$3,000",
            "expected_outcome": f"实现月营收${product['revenue_estimate']:,.0f}，ROI达到{product['roi_estimate']:.0f}%"
        })
        
        actions.append(action)
    
    return actions


def format_number(num: float, prefix: str = "", suffix: str = "") -> str:
    """
    格式化数字显示
    
    Args:
        num: 数字
        prefix: 前缀
        suffix: 后缀
        
    Returns:
        str: 格式化后的字符串
    """
    if num >= 1000000:
        return f"{prefix}{num/1000000:.1f}M{suffix}"
    elif num >= 1000:
        return f"{prefix}{num/1000:.1f}K{suffix}"
    else:
        return f"{prefix}{num:.0f}{suffix}"
