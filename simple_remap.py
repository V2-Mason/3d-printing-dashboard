#!/usr/bin/env python3
"""
Simple script to remap tabs by changing tab variable names
"""

with open('dashboard_working.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Strategy: Rename tab variables in the content
# Old: tab1=产品排名, tab2=数据分析, tab3=AI洞察, tab4=历史趋势, tab5=情绪分析, tab6=产品分析, tab7=竞争分析, tab8=行动计划, tab9=执行摘要
# New: tab1=执行摘要, tab2=产品排名, tab3=数据分析, tab4=AI洞察, tab5=历史趋势, tab6=情绪分析, tab7=产品分析, tab8=竞争分析, tab9=行动计划

# First, replace all tab variables with temporary placeholders
replacements = [
    ('with tab1:', 'with TEMP_TAB_PRODUCT_RANKING:'),  # 产品排名 -> temp
    ('with tab2:', 'with TEMP_TAB_DATA_ANALYSIS:'),     # 数据分析 -> temp
    ('with tab3:', 'with TEMP_TAB_AI_INSIGHTS:'),       # AI洞察 -> temp
    ('with tab4:', 'with TEMP_TAB_HISTORICAL:'),        # 历史趋势 -> temp
    ('with tab5:', 'with TEMP_TAB_EMOTION:'),           # 情绪分析 -> temp
    ('with tab6:', 'with TEMP_TAB_PRODUCT_ANALYSIS:'),  # 产品分析 -> temp (will have duplicates)
    ('with tab7:', 'with TEMP_TAB_COMPETITOR:'),        # 竞争分析 -> temp
    ('with tab8:', 'with TEMP_TAB_ACTION_PLAN:'),       # 行动计划 -> temp
    ('with tab9:', 'with TEMP_TAB_EXECUTIVE:'),         # 执行摘要 -> temp
]

for old, new in replacements:
    content = content.replace(old, new)

# Now map temp placeholders to new tab variables
final_replacements = [
    ('with TEMP_TAB_EXECUTIVE:', 'with tab1:'),         # 执行摘要 -> tab1
    ('with TEMP_TAB_PRODUCT_RANKING:', 'with tab2:'),   # 产品排名 -> tab2
    ('with TEMP_TAB_DATA_ANALYSIS:', 'with tab3:'),     # 数据分析 -> tab3
    ('with TEMP_TAB_AI_INSIGHTS:', 'with tab4:'),       # AI洞察 -> tab4
    ('with TEMP_TAB_HISTORICAL:', 'with tab5:'),        # 历史趋势 -> tab5
    ('with TEMP_TAB_EMOTION:', 'with tab6:'),           # 情绪分析 -> tab6
    ('with TEMP_TAB_PRODUCT_ANALYSIS:', 'with tab7:'),  # 产品分析 -> tab7
    ('with TEMP_TAB_COMPETITOR:', 'with tab8:'),        # 竞争分析 -> tab8
    ('with TEMP_TAB_ACTION_PLAN:', 'with tab9:'),       # 行动计划 -> tab9
]

for old, new in final_replacements:
    content = content.replace(old, new)

# Write to new file
with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Tab remapping complete!")
print("   Output: dashboard.py")

# Verify the mapping
import re
tab_lines = []
for i, line in enumerate(content.split('\n'), 1):
    if re.match(r'^    with tab\d+:', line):
        tab_lines.append((i, line.strip()))

print(f"\n📋 Tab sections in new file:")
for line_num, line in tab_lines:
    print(f"   Line {line_num}: {line}")
