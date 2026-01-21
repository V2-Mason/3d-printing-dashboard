"""
Enhanced Emotion Analysis Charts
Based on user's provided designs with dark theme and cyan/blue/purple colors
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Dark theme template
DARK_TEMPLATE = "plotly_dark"
COLOR_SCHEME = {
    'cyan': '#00CED1',
    'lightblue': '#87CEEB',
    'purple': '#9370DB',
    'pink': '#FF69B4',
    'yellow': '#FFD700',
    'green': '#00FF7F',
    'red': '#FF6B6B',
    'orange': '#FFA500'
}

def create_emotion_radar_chart(week3_data, week4_data):
    """
    创建12种情绪强度分布雷达图
    Emotion Intensity Distribution Radar Chart
    """
    emotions = ['Trust', 'Surprise', 'Joy', 'Excitement', 'Pride', 'Envy',
                'Disgust', 'Fear', 'Anger', 'Disappointment', 'Anxiety', 'Nostalgia']
    
    emotions_cn = ['信任', '惊喜', '喜悦', '兴奋', '自豪', '嫉妒',
                   '厌恶', '恐惧', '愤怒', '失望', '焦虑', '怀旧']
    
    fig = go.Figure()
    
    # Week 3 trace
    fig.add_trace(go.Scatterpolar(
        r=week3_data,
        theta=emotions_cn,
        fill='toself',
        name='本周 (Week 4)',
        line_color=COLOR_SCHEME['cyan'],
        fillcolor='rgba(0, 206, 209, 0.3)'
    ))
    
    # Week 4 trace
    fig.add_trace(go.Scatterpolar(
        r=week4_data,
        theta=emotions_cn,
        fill='toself',
        name='上周 (Week 3)',
        line_color=COLOR_SCHEME['lightblue'],
        line_dash='dash',
        fillcolor='rgba(135, 206, 235, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(size=10, color='white'),
                gridcolor='rgba(255, 255, 255, 0.2)'
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='white'),
                gridcolor='rgba(255, 255, 255, 0.2)'
            ),
            bgcolor='rgba(0, 0, 0, 0.5)'
        ),
        showlegend=True,
        title=dict(
            text="12种情绪强度分布 (Emotion Intensity Distribution)",
            font=dict(size=18, color='white'),
            x=0.5,
            xanchor='center'
        ),
        template=DARK_TEMPLATE,
        height=600,
        legend=dict(
            font=dict(color='white'),
            bgcolor='rgba(0, 0, 0, 0.5)'
        ),
        paper_bgcolor='#1e1e2e',
        plot_bgcolor='#1e1e2e'
    )
    
    return fig


def create_emotion_frequency_bar(emotion_data):
    """
    创建情绪提及频次横向柱状图
    Emotion Mention Frequency Bar Chart
    """
    emotions_cn = ['兴奋', '喜悦', '惊喜', '怀旧', '信任', '自豪', '嫉妒', 
                   '愤怒', '失望', '焦虑', '恐惧', '厌恶']
    
    # Create color list - positive emotions in cyan/purple, negative in red
    colors = [COLOR_SCHEME['cyan'], COLOR_SCHEME['cyan'], COLOR_SCHEME['purple'],
              COLOR_SCHEME['purple'], COLOR_SCHEME['lightblue'], COLOR_SCHEME['lightblue'],
              COLOR_SCHEME['yellow'], COLOR_SCHEME['red'], COLOR_SCHEME['red'],
              COLOR_SCHEME['orange'], COLOR_SCHEME['orange'], COLOR_SCHEME['red']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=emotions_cn,
        x=emotion_data['mentions'],
        orientation='h',
        text=[f"{m} ({p:.1f}%)" for m, p in zip(emotion_data['mentions'], emotion_data['percentage'])],
        textposition='outside',
        marker=dict(
            color=colors,
            line=dict(color='white', width=1)
        ),
        hovertemplate='<b>%{y}</b><br>提及次数: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="情绪提及频次分布 (Emotion Mention Frequency)",
            font=dict(size=18, color='white'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="提及次数 (Mentions)",
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='rgba(255, 255, 255, 0.1)'
        ),
        yaxis=dict(
            titlefont=dict(color='white'),
            tickfont=dict(size=12, color='white'),
            gridcolor='rgba(255, 255, 255, 0.1)'
        ),
        template=DARK_TEMPLATE,
        height=500,
        paper_bgcolor='#1e1e2e',
        plot_bgcolor='#1e1e2e',
        showlegend=False
    )
    
    return fig


def create_emotion_opportunity_matrix(emotion_data):
    """
    创建情绪强度 vs 商业潜力矩阵 (气泡图)
    Emotion Intensity vs Commercial Potential Matrix
    """
    fig = go.Figure()
    
    # Add scatter points with different colors based on quadrant
    for idx, row in emotion_data.iterrows():
        # Determine quadrant and color
        if row['intensity'] >= 5 and row['potential'] >= 5:
            color = COLOR_SCHEME['pink']  # High priority
            quadrant = '高优先级 (High Priority)'
        elif row['intensity'] < 5 and row['potential'] >= 5:
            color = COLOR_SCHEME['yellow']  # Potential
            quadrant = '潜力区 (Potential)'
        elif row['intensity'] >= 5 and row['potential'] < 5:
            color = COLOR_SCHEME['cyan']  # Watch
            quadrant = '观察区 (Watch)'
        else:
            color = COLOR_SCHEME['red']  # Low priority
            quadrant = '低优先级 (Low Priority)'
        
        fig.add_trace(go.Scatter(
            x=[row['intensity']],
            y=[row['potential']],
            mode='markers+text',
            name=row['emotion'],
            text=[row['emotion']],
            textposition='top center',
            textfont=dict(size=10, color='white'),
            marker=dict(
                size=row['size'],
                color=color,
                line=dict(width=2, color='white'),
                opacity=0.8
            ),
            hovertemplate=f"<b>{row['emotion']}</b><br>" +
                         f"情绪强度: {row['intensity']}<br>" +
                         f"商业潜力: {row['potential']}<br>" +
                         f"象限: {quadrant}<extra></extra>"
        ))
    
    # Add quadrant lines
    fig.add_hline(y=5, line_dash="dash", line_color="rgba(255, 255, 255, 0.3)", line_width=2)
    fig.add_vline(x=5, line_dash="dash", line_color="rgba(255, 255, 255, 0.3)", line_width=2)
    
    # Add quadrant labels
    fig.add_annotation(x=7.5, y=7.5, text="⭐ 高优先级<br>(High Priority)",
                      showarrow=False, font=dict(size=12, color=COLOR_SCHEME['pink']),
                      bgcolor="rgba(255, 105, 180, 0.2)", bordercolor=COLOR_SCHEME['pink'], borderwidth=2)
    
    fig.add_annotation(x=2.5, y=7.5, text="💡 潜力区<br>(Potential)",
                      showarrow=False, font=dict(size=12, color=COLOR_SCHEME['yellow']),
                      bgcolor="rgba(255, 215, 0, 0.2)", bordercolor=COLOR_SCHEME['yellow'], borderwidth=2)
    
    fig.add_annotation(x=7.5, y=2.5, text="⚠️ 观察区<br>(Watch)",
                      showarrow=False, font=dict(size=12, color=COLOR_SCHEME['cyan']),
                      bgcolor="rgba(0, 206, 209, 0.2)", bordercolor=COLOR_SCHEME['cyan'], borderwidth=2)
    
    fig.add_annotation(x=2.5, y=2.5, text="❌ 低优先级<br>(Low Priority)",
                      showarrow=False, font=dict(size=12, color=COLOR_SCHEME['red']),
                      bgcolor="rgba(255, 107, 107, 0.2)", bordercolor=COLOR_SCHEME['red'], borderwidth=2)
    
    fig.update_layout(
        title=dict(
            text="情绪强度 vs 商业潜力矩阵 (Emotion Intensity vs Commercial Potential)",
            font=dict(size=18, color='white'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="情绪强度 (Emotion Intensity)",
            range=[0, 10],
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='rgba(255, 255, 255, 0.1)'
        ),
        yaxis=dict(
            title="商业潜力 (Commercial Potential)",
            range=[0, 10],
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='rgba(255, 255, 255, 0.1)'
        ),
        template=DARK_TEMPLATE,
        height=600,
        showlegend=False,
        paper_bgcolor='#1e1e2e',
        plot_bgcolor='#1e1e2e'
    )
    
    return fig


def create_emotion_score_waterfall(product_name="3D打印制鞋"):
    """
    创建情绪需求分数分解瀑布图
    Emotional Demand Score Breakdown Waterfall Chart
    """
    categories = ['情绪强度\n(40%)', '提及频率\n(30%)', '传播力度\n(20%)', '时间趋势\n(10%)', '总分']
    values = [32.8, 30.0, 17.0, 8.0, 87.8]
    
    # Create colors: cyan for components, green for total
    colors = [COLOR_SCHEME['cyan'], COLOR_SCHEME['cyan'], 
              COLOR_SCHEME['cyan'], COLOR_SCHEME['cyan'], 
              COLOR_SCHEME['green']]
    
    fig = go.Figure()
    
    # Add waterfall bars
    fig.add_trace(go.Waterfall(
        name="Score",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=categories,
        textposition="outside",
        text=[f"+{v}" if i < 4 else f"{v}" for i, v in enumerate(values)],
        y=values,
        connector={"line": {"color": "rgba(255, 255, 255, 0.3)"}},
        increasing={"marker": {"color": COLOR_SCHEME['cyan']}},
        totals={"marker": {"color": COLOR_SCHEME['green']}},
        textfont=dict(size=14, color='white')
    ))
    
    fig.update_layout(
        title=dict(
            text=f"情绪需求分数计算详情 (Emotional Demand Score Breakdown)<br>产品: {product_name}",
            font=dict(size=18, color='white'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            titlefont=dict(color='white'),
            tickfont=dict(size=12, color='white'),
            gridcolor='rgba(255, 255, 255, 0.1)'
        ),
        yaxis=dict(
            title="分数 (Score)",
            range=[0, 100],
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='rgba(255, 255, 255, 0.1)'
        ),
        template=DARK_TEMPLATE,
        height=500,
        showlegend=False,
        paper_bgcolor='#1e1e2e',
        plot_bgcolor='#1e1e2e'
    )
    
    return fig


# Sample data generators for testing
def generate_sample_emotion_data():
    """Generate sample data for testing"""
    
    # Radar chart data
    week3_radar = [6, 7, 8, 7, 5, 3, 2, 3, 4, 5, 4, 6]
    week4_radar = [7, 8, 9, 8, 6, 2, 1, 2, 3, 4, 3, 7]
    
    # Frequency bar data
    frequency_data = pd.DataFrame({
        'emotion': ['兴奋', '喜悦', '惊喜', '怀旧', '信任', '自豪', '嫉妒', 
                   '愤怒', '失望', '焦虑', '恐惧', '厌恶'],
        'mentions': [1200, 1000, 750, 650, 580, 450, 320, 186, 145, 98, 56, 42],
        'percentage': [22.0, 18.3, 13.7, 11.9, 10.6, 8.2, 5.9, 3.4, 2.7, 1.8, 1.0, 0.8]
    })
    
    # Opportunity matrix data
    matrix_data = pd.DataFrame({
        'emotion': ['喜悦', '信任', '兴奋', '惊喜', '怀旧', '自豪', '失望', '焦虑', '恐惧', '愤怒'],
        'intensity': [8.5, 7.5, 9.0, 7.0, 6.5, 6.0, 3.5, 4.0, 2.5, 3.0],
        'potential': [9.0, 8.5, 9.5, 7.5, 5.0, 6.5, 3.0, 2.5, 1.5, 2.0],
        'size': [50, 45, 55, 40, 35, 38, 25, 22, 18, 20]
    })
    
    return {
        'radar': (week3_radar, week4_radar),
        'frequency': frequency_data,
        'matrix': matrix_data
    }


if __name__ == "__main__":
    print("✅ Emotion charts module created successfully")
    print("Available functions:")
    print("  - create_emotion_radar_chart()")
    print("  - create_emotion_frequency_bar()")
    print("  - create_emotion_opportunity_matrix()")
    print("  - create_emotion_score_waterfall()")
