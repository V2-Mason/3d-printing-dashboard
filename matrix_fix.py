# Enhanced Matrix Visualization with Four Quadrants

import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_quadrant_matrix(df, x_col='avg_price', y_col='market_share', name_col='name', title='市场定位矩阵（四象限分析）'):
    """
    创建真正的四象限矩阵图
    
    参数:
        df: DataFrame with competitor data
        x_col: column name for x-axis (price)
        y_col: column name for y-axis (market share)
        name_col: column name for labels
        title: chart title
    """
    
    # Calculate medians for quadrant lines
    median_x = df[x_col].median()
    median_y = df[y_col].median()
    
    # Create figure
    fig = go.Figure()
    
    # Add quadrant background shapes
    # Quadrant 1: High price, High share (Top Right) - Leaders
    fig.add_shape(
        type="rect",
        x0=median_x, x1=df[x_col].max() * 1.1,
        y0=median_y, y1=df[y_col].max() * 1.1,
        fillcolor="rgba(144,238,144,0.2)",  # Light green
        line=dict(width=0),
        layer="below"
    )
    
    # Quadrant 2: Low price, High share (Top Left) - Challengers
    fig.add_shape(
        type="rect",
        x0=df[x_col].min() * 0.9, x1=median_x,
        y0=median_y, y1=df[y_col].max() * 1.1,
        fillcolor="rgba(173,216,230,0.2)",  # Light blue
        line=dict(width=0),
        layer="below"
    )
    
    # Quadrant 3: Low price, Low share (Bottom Left) - Followers
    fig.add_shape(
        type="rect",
        x0=df[x_col].min() * 0.9, x1=median_x,
        y0=df[y_col].min() * 0.9, y1=median_y,
        fillcolor="rgba(255,182,193,0.2)",  # Light pink/red
        line=dict(width=0),
        layer="below"
    )
    
    # Quadrant 4: High price, Low share (Bottom Right) - Niche
    fig.add_shape(
        type="rect",
        x0=median_x, x1=df[x_col].max() * 1.1,
        y0=df[y_col].min() * 0.9, y1=median_y,
        fillcolor="rgba(255,218,185,0.2)",  # Light orange
        line=dict(width=0),
        layer="below"
    )
    
    # Add scatter points
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='markers+text',
        text=df[name_col],
        textposition='top center',
        marker=dict(
            size=15,
            color='#2196F3',
            line=dict(width=2, color='white')
        ),
        hovertemplate='<b>%{text}</b><br>' +
                      f'{x_col}: %{{x:.2f}}<br>' +
                      f'{y_col}: %{{y:.2f}}<extra></extra>'
    ))
    
    # Add quadrant dividing lines
    fig.add_hline(
        y=median_y,
        line_dash="dash",
        line_color="gray",
        line_width=2,
        annotation_text=f"市场份额中位数: {median_y:.1f}%",
        annotation_position="right"
    )
    fig.add_vline(
        x=median_x,
        line_dash="dash",
        line_color="gray",
        line_width=2,
        annotation_text=f"价格中位数: ${median_x:.2f}",
        annotation_position="top"
    )
    
    # Add quadrant labels
    # Calculate positions for labels
    x_high = median_x + (df[x_col].max() - median_x) * 0.5
    x_low = df[x_col].min() + (median_x - df[x_col].min()) * 0.5
    y_high = median_y + (df[y_col].max() - median_y) * 0.5
    y_low = df[y_col].min() + (median_y - df[y_col].min()) * 0.5
    
    # Quadrant 1: Leaders (Top Right)
    fig.add_annotation(
        x=x_high, y=y_high,
        text="<b>领导者</b><br>高价高份额<br>品牌溢价强",
        showarrow=False,
        font=dict(size=14, color="darkgreen"),
        bgcolor="rgba(144,238,144,0.5)",
        bordercolor="darkgreen",
        borderwidth=2,
        borderpad=8
    )
    
    # Quadrant 2: Challengers (Top Left)
    fig.add_annotation(
        x=x_low, y=y_high,
        text="<b>挑战者</b><br>低价高份额<br>性价比优势",
        showarrow=False,
        font=dict(size=14, color="darkblue"),
        bgcolor="rgba(173,216,230,0.5)",
        bordercolor="darkblue",
        borderwidth=2,
        borderpad=8
    )
    
    # Quadrant 3: Followers (Bottom Left)
    fig.add_annotation(
        x=x_low, y=y_low,
        text="<b>追随者</b><br>低价低份额<br>需要突破",
        showarrow=False,
        font=dict(size=14, color="darkred"),
        bgcolor="rgba(255,182,193,0.5)",
        bordercolor="darkred",
        borderwidth=2,
        borderpad=8
    )
    
    # Quadrant 4: Niche (Bottom Right)
    fig.add_annotation(
        x=x_high, y=y_low,
        text="<b>利基市场</b><br>高价低份额<br>专业定位",
        showarrow=False,
        font=dict(size=14, color="darkorange"),
        bgcolor="rgba(255,218,185,0.5)",
        bordercolor="darkorange",
        borderwidth=2,
        borderpad=8
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color='#2196F3')
        ),
        xaxis_title=f'{x_col.replace("_", " ").title()} ($)',
        yaxis_title=f'{y_col.replace("_", " ").title()} (%)',
        showlegend=False,
        height=600,
        hovermode='closest',
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            zeroline=False
        )
    )
    
    return fig


# Code to insert into dashboard.py at line 902:
MATRIX_REPLACEMENT = '''
        # 使用增强的四象限矩阵
        from matrix_fix import create_quadrant_matrix
        fig_matrix = create_quadrant_matrix(
            competitor_df,
            x_col='avg_price',
            y_col='market_share',
            name_col='name',
            title='竞争对手市场定位矩阵（四象限战略分析）'
        )
'''

print("✅ Enhanced matrix visualization function created")
print("This creates a proper four-quadrant matrix with:")
print("  - Quadrant dividing lines")
print("  - Colored background for each quadrant")
print("  - Strategic labels (Leaders, Challengers, Followers, Niche)")
print("  - Clear positioning guidance")
