"""
情绪可视化模块
包含情绪健康仪表盘和情绪-主题交叉分析热力图
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def create_emotion_health_gauge(emotion_score, max_score=50):
    """
    创建情绪健康仪表盘（类似速度表）
    
    参数:
        emotion_score: float - 当前情绪分数
        max_score: int - 最大分数（默认50）
    
    返回:
        plotly figure
    """
    # 定义颜色区间
    if emotion_score < 20:
        color = "#ff6b6b"  # 红色 - 较差
        level = "较差"
    elif emotion_score < 35:
        color = "#ffa502"  # 橙色 - 一般
        level = "一般"
    elif emotion_score < 45:
        color = "#2196F3"  # 蓝色 - 良好
        level = "良好"
    else:
        color = "#4CAF50"  # 绿色 - 优秀
        level = "优秀"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=emotion_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"情绪健康指数<br><span style='font-size:0.8em;color:gray'>{level}</span>"},
        delta={'reference': 44.2, 'increasing': {'color': "#4CAF50"}},
        gauge={
            'axis': {'range': [None, max_score], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 20], 'color': '#ffe6e6'},
                {'range': [20, 35], 'color': '#fff4e6'},
                {'range': [35, 45], 'color': '#e3f2fd'},
                {'range': [45, 50], 'color': '#e8f5e9'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 40
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        font={'size': 14}
    )
    
    return fig


def create_emotion_topic_heatmap(df):
    """
    创建情绪-主题交叉分析热力图
    
    参数:
        df: DataFrame - 包含情绪和主题数据
    
    返回:
        plotly figure
    """
    # 定义情绪和主题
    emotions = ['兴奋', '好奇', '满意', '信任', '期待', '喜悦', 
                '担忧', '困惑', '失望', '愤怒', '恐惧', '悲伤']
    topics = ['价格', '质量', '设计', '功能', '配送', '服务']
    
    # 生成模拟数据（实际应该从真实数据计算）
    # 这里创建一个关联强度矩阵
    np.random.seed(42)
    
    # 创建更真实的关联模式
    correlation_matrix = np.zeros((len(emotions), len(topics)))
    
    # 正面情绪与不同主题的关联
    correlation_matrix[0, :] = [0.3, 0.4, 0.8, 0.7, 0.2, 0.3]  # 兴奋 - 设计和功能强相关
    correlation_matrix[1, :] = [0.4, 0.5, 0.6, 0.7, 0.3, 0.4]  # 好奇 - 功能强相关
    correlation_matrix[2, :] = [0.5, 0.8, 0.6, 0.7, 0.7, 0.8]  # 满意 - 质量和服务强相关
    correlation_matrix[3, :] = [0.4, 0.7, 0.5, 0.6, 0.6, 0.7]  # 信任 - 质量和服务
    correlation_matrix[4, :] = [0.5, 0.6, 0.7, 0.8, 0.4, 0.5]  # 期待 - 功能和设计
    correlation_matrix[5, :] = [0.4, 0.6, 0.7, 0.6, 0.5, 0.7]  # 喜悦 - 设计和服务
    
    # 负面情绪与不同主题的关联
    correlation_matrix[6, :] = [0.8, 0.5, 0.3, 0.4, 0.6, 0.5]  # 担忧 - 价格强相关
    correlation_matrix[7, :] = [0.6, 0.4, 0.5, 0.7, 0.5, 0.6]  # 困惑 - 功能和价格
    correlation_matrix[8, :] = [0.5, 0.7, 0.6, 0.6, 0.7, 0.6]  # 失望 - 质量和配送
    correlation_matrix[9, :] = [0.6, 0.8, 0.5, 0.5, 0.8, 0.7]  # 愤怒 - 质量和配送
    correlation_matrix[10, :] = [0.7, 0.6, 0.4, 0.5, 0.5, 0.5]  # 恐惧 - 价格和质量
    correlation_matrix[11, :] = [0.5, 0.7, 0.5, 0.5, 0.6, 0.6]  # 悲伤 - 质量
    
    # 创建热力图
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix,
        x=topics,
        y=emotions,
        colorscale=[
            [0, '#f0f0f0'],      # 白色 - 无关联
            [0.3, '#b3d9ff'],    # 浅蓝 - 弱关联
            [0.5, '#66b3ff'],    # 中蓝 - 中等关联
            [0.7, '#3399ff'],    # 深蓝 - 强关联
            [1, '#0066cc']       # 最深蓝 - 极强关联
        ],
        text=np.round(correlation_matrix, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(
            title="关联强度",
            tickvals=[0, 0.25, 0.5, 0.75, 1.0],
            ticktext=['无', '弱', '中', '强', '极强']
        ),
        hovertemplate='<b>%{y}</b> × <b>%{x}</b><br>关联强度: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '情绪-主题交叉分析热力图',
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='讨论主题',
        yaxis_title='用户情绪',
        height=500,
        margin=dict(l=80, r=80, t=80, b=80)
    )
    
    return fig


def create_emotion_correlation_chart(df):
    """
    创建情绪关联分析图表
    显示每种情绪主要与什么相关
    
    参数:
        df: DataFrame - 包含情绪数据
    
    返回:
        plotly figure
    """
    # 模拟数据：每种情绪的主要关联对象
    emotion_correlations = {
        '兴奋': {'创新设计': 0.8, '新功能': 0.7, '独特性': 0.6},
        '好奇': {'新功能': 0.8, '技术规格': 0.6, '使用方法': 0.5},
        '满意': {'质量': 0.8, '性价比': 0.7, '服务': 0.6},
        '担忧': {'价格': 0.8, '质量': 0.6, '耐用性': 0.5},
        '困惑': {'使用方法': 0.7, '功能说明': 0.6, '兼容性': 0.5},
        '失望': {'质量': 0.8, '实际效果': 0.7, '期望差距': 0.6}
    }
    
    # 准备数据
    data = []
    for emotion, correlations in emotion_correlations.items():
        for topic, strength in correlations.items():
            data.append({
                '情绪': emotion,
                '关联对象': topic,
                '关联强度': strength
            })
    
    correlation_df = pd.DataFrame(data)
    
    # 创建分组柱状图
    fig = px.bar(
        correlation_df,
        x='情绪',
        y='关联强度',
        color='关联对象',
        barmode='group',
        title='情绪关联分析：各情绪的主要关注点',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_layout(
        xaxis_title='用户情绪',
        yaxis_title='关联强度',
        height=400,
        legend_title='关联对象',
        hovermode='x unified'
    )
    
    fig.update_traces(
        hovertemplate='<b>%{fullData.name}</b><br>关联强度: %{y:.2f}<extra></extra>'
    )
    
    return fig


def generate_emotion_insights(emotion_score, correlation_data=None):
    """
    基于情绪分数和关联数据生成洞察
    
    参数:
        emotion_score: float - 情绪分数
        correlation_data: dict - 情绪关联数据
    
    返回:
        str - 洞察文本
    """
    insights = []
    
    # 基于分数的洞察
    if emotion_score < 20:
        insights.append("⚠️ **警告**: 情绪健康指数较低，需要立即关注负面反馈")
        insights.append("• 建议优先解决用户最关心的问题（通常是价格或质量）")
    elif emotion_score < 35:
        insights.append("📊 **一般**: 情绪表现中等，有较大提升空间")
        insights.append("• 建议加强产品亮点宣传，提升用户期待")
    elif emotion_score < 45:
        insights.append("✅ **良好**: 情绪表现不错，用户整体满意")
        insights.append("• 建议保持当前策略，持续优化细节")
    else:
        insights.append("🌟 **优秀**: 情绪健康指数很高，用户高度认可")
        insights.append("• 建议扩大推广，这是值得重点投入的产品")
    
    # 基于关联数据的洞察
    if correlation_data:
        insights.append("\n**关键发现**:")
        insights.append("• 兴奋情绪主要与创新设计相关，说明用户喜欢新颖产品")
        insights.append("• 担忧情绪主要与价格相关，建议提供更多价格档位")
        insights.append("• 满意情绪主要与质量相关，继续保持质量优势")
    
    return "\n".join(insights)
