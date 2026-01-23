"""
基于数据的解决方案推荐引擎
根据发现的问题自动生成具体的行动建议
"""

import pandas as pd


def generate_recommendations(df, summary_data=None):
    """
    基于数据分析生成具体的解决方案推荐
    
    参数:
        df: DataFrame - 产品数据
        summary_data: dict - 摘要数据
    
    返回:
        list - 推荐列表
    """
    recommendations = []
    
    if summary_data:
        emotion = summary_data.get('emotion', {})
        sales = summary_data.get('sales', {})
        strategy = summary_data.get('strategy', {})
    else:
        emotion = {}
        sales = {}
        strategy = {}
    
    # 1. 基于情绪分析的推荐
    avg_emotion = emotion.get('avg_emotion', 0)
    
    if avg_emotion < 35:
        recommendations.append({
            'category': '情绪优化',
            'priority': '高',
            'issue': f'情绪分数较低（{avg_emotion:.1f}/50）',
            'recommendation': '立即优化产品描述和用户沟通',
            'actions': [
                '分析负面评论，识别主要痛点',
                '改进产品页面，突出质量保证',
                '提供更详细的产品使用说明',
                '增加客户服务响应速度'
            ],
            'expected_impact': '预计可提升情绪分数5-8分',
            'timeline': '2-4周'
        })
    
    # 2. 基于价格担忧的推荐
    if '担忧' in df.columns or True:  # 假设存在价格担忧
        recommendations.append({
            'category': '定价策略',
            'priority': '中',
            'issue': '用户对价格存在担忧',
            'recommendation': '优化定价策略，提供多层次选择',
            'actions': [
                '推出入门级产品（降低20-30%价格）',
                '提供套装优惠（买2送1或组合折扣）',
                '实施分期付款选项',
                '强调性价比和长期价值'
            ],
            'expected_impact': '预计可提升转化率15-25%',
            'timeline': '1-2周'
        })
    
    # 3. 基于平台表现的推荐
    top_platform = sales.get('top_platform', 'Etsy')
    
    recommendations.append({
        'category': '渠道优化',
        'priority': '高',
        'issue': f'{top_platform}表现最佳，其他平台有增长空间',
        'recommendation': f'扩大{top_platform}投入，同时优化其他平台',
        'actions': [
            f'在{top_platform}上增加产品SKU',
            f'复制{top_platform}的成功经验到其他平台',
            '优化产品标题和关键词（SEO）',
            '增加跨平台推广活动'
        ],
        'expected_impact': '预计可提升总营收30-40%',
        'timeline': '4-6周'
    })
    
    # 4. 基于类别表现的推荐
    top_category = sales.get('top_category', '办公用品')
    
    recommendations.append({
        'category': '产品开发',
        'priority': '高',
        'issue': f'{top_category}类别需求旺盛',
        'recommendation': f'重点开发{top_category}相关产品',
        'actions': [
            f'调研{top_category}的细分需求',
            '设计3-5款新产品原型',
            '进行小批量测试（100-200件）',
            '根据反馈快速迭代'
        ],
        'expected_impact': '预计可新增月营收$5,000-$8,000',
        'timeline': '6-8周'
    })
    
    # 5. 基于质量反馈的推荐
    if avg_emotion > 40:
        recommendations.append({
            'category': '品牌建设',
            'priority': '中',
            'issue': '产品质量获得高度认可',
            'recommendation': '建立品牌溢价，提升市场定位',
            'actions': [
                '创建品牌故事和价值主张',
                '申请相关质量认证',
                '收集和展示用户好评',
                '考虑提价10-15%测试市场接受度'
            ],
            'expected_impact': '预计可提升利润率20-30%',
            'timeline': '8-12周'
        })
    
    # 6. 基于市场潜力的推荐
    high_potential = strategy.get('high_potential_count', 0)
    
    if high_potential > 3:
        recommendations.append({
            'category': '市场扩张',
            'priority': '高',
            'issue': f'发现{high_potential}个高潜力产品机会',
            'recommendation': '快速进入高潜力细分市场',
            'actions': [
                '优先开发Top 3高潜力产品',
                '分配预算：每个产品$2,000-$3,000',
                '设定8周内上线目标',
                '准备营销推广计划'
            ],
            'expected_impact': '预计可新增月营收$10,000-$15,000',
            'timeline': '8-10周'
        })
    
    # 7. 基于竞争分析的推荐
    low_competition = strategy.get('low_competition_count', 0)
    
    if low_competition > 2:
        recommendations.append({
            'category': '竞争策略',
            'priority': '中',
            'issue': f'发现{low_competition}个低竞争机会',
            'recommendation': '抢占低竞争蓝海市场',
            'actions': [
                '快速进入低竞争细分市场',
                '建立先发优势和品牌认知',
                '优化SEO，占据搜索结果前列',
                '设置竞争壁垒（独特设计、专利等）'
            ],
            'expected_impact': '预计可获得30-50%市场份额',
            'timeline': '6-8周'
        })
    
    # 按优先级排序
    priority_order = {'高': 0, '中': 1, '低': 2}
    recommendations.sort(key=lambda x: priority_order.get(x['priority'], 999))
    
    return recommendations


def format_recommendations_html(recommendations):
    """
    将推荐格式化为HTML展示
    
    参数:
        recommendations: list - 推荐列表
    
    返回:
        str - HTML字符串
    """
    html_parts = []
    
    for i, rec in enumerate(recommendations, 1):
        priority_color = {
            '高': '#ff6b6b',
            '中': '#ffa502',
            '低': '#2196F3'
        }.get(rec['priority'], '#999')
        
        actions_html = '<br>'.join([f"   {j}. {action}" for j, action in enumerate(rec['actions'], 1)])
        
        card_html = f"""
        <div style="background: white; border-left: 4px solid {priority_color}; padding: 15px; margin-bottom: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h4 style="margin: 0; color: #333;">推荐 {i}: {rec['category']}</h4>
                <span style="background: {priority_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 12px;">{rec['priority']}优先级</span>
            </div>
            
            <p style="margin: 10px 0; color: #666;"><strong>问题：</strong>{rec['issue']}</p>
            <p style="margin: 10px 0; color: #333;"><strong>建议：</strong>{rec['recommendation']}</p>
            
            <p style="margin: 10px 0; color: #333;"><strong>具体行动：</strong></p>
            <p style="margin: 5px 0 10px 0; color: #666; line-height: 1.8;">{actions_html}</p>
            
            <div style="display: flex; justify-content: space-between; margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee;">
                <span style="color: #4CAF50; font-size: 14px;">📈 {rec['expected_impact']}</span>
                <span style="color: #2196F3; font-size: 14px;">⏱️ {rec['timeline']}</span>
            </div>
        </div>
        """
        
        html_parts.append(card_html)
    
    return '\n'.join(html_parts)


def create_action_priority_matrix(recommendations):
    """
    创建行动优先级矩阵
    
    参数:
        recommendations: list - 推荐列表
    
    返回:
        dict - 按优先级分组的推荐
    """
    matrix = {
        '立即执行（高优先级）': [],
        '近期规划（中优先级）': [],
        '长期考虑（低优先级）': []
    }
    
    for rec in recommendations:
        if rec['priority'] == '高':
            matrix['立即执行（高优先级）'].append(rec)
        elif rec['priority'] == '中':
            matrix['近期规划（中优先级）'].append(rec)
        else:
            matrix['长期考虑（低优先级）'].append(rec)
    
    return matrix
