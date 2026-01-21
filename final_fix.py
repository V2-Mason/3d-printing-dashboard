#!/usr/bin/env python3
"""
Final fix: Manually extract and reorder all tabs correctly
"""

with open('dashboard_clean.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Manual extraction based on line numbers from grep output
# Original structure:
# 352: tab1 (产品排名)
# 412: tab2 (数据分析)
# 483: tab3 (AI洞察)
# 534: tab4 (历史趋势)
# 605: tab5 (情绪分析)
# 822: tab6 (竞争分析 - first occurrence, WRONG)
# 928: tab6 (产品分析 - second occurrence, WRONG)
# 1175: tab7 (竞争分析 - duplicate)
# 1281: tab8 (行动计划)
# 1447: tab9 (执行摘要)

# Target structure:
# tab1: 执行摘要 (from line 1447)
# tab2: 产品排名 (from line 352)
# tab3: 数据分析 (from line 412)
# tab4: AI洞察 (from line 483)
# tab5: 历史趋势 (from line 534)
# tab6: 情绪分析 (from line 605)
# tab7: 产品分析 (from line 928)
# tab8: 竞争分析 (from line 822, skip line 1175 duplicate)
# tab9: 行动计划 (from line 1281)

# Extract header (everything before first tab)
header = lines[:351]  # Up to line 351 (before tab1 at 352)

# Update tab names in header
for i, line in enumerate(header):
    if 'tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([' in line:
        # Replace the tab names
        header[i] = '    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([\n'
        header[i+1] = '        "📊 执行摘要",   # 移到第一位\n'
        header[i+2] = '        "📋 产品排名",\n'
        header[i+3] = '        "📊 数据分析",\n'
        header[i+4] = '        "🤖 AI洞察",\n'
        header[i+5] = '        "📈 历史趋势",\n'
        header[i+6] = '        "💭 情绪分析",\n'
        header[i+7] = '        "🎯 产品分析",\n'
        header[i+8] = '        "🎭 竞争分析",\n'
        header[i+9] = '        "📋 行动计划"\n'
        break

# Extract tab contents
tab1_old = lines[351:411]   # 产品排名 (352-411)
tab2_old = lines[411:482]   # 数据分析 (412-482)
tab3_old = lines[482:533]   # AI洞察 (483-533)
tab4_old = lines[533:604]   # 历史趋势 (534-604)
tab5_old = lines[604:821]   # 情绪分析 (605-821)
tab6_old_first = lines[821:927]   # 竞争分析 (822-927) - will become tab8
tab6_old_second = lines[927:1174]  # 产品分析 (928-1174) - will become tab7
# Skip tab7 at 1175 (duplicate of competitor analysis)
tab8_old = lines[1280:1446]  # 行动计划 (1281-1446)
tab9_old = lines[1446:1661]  # 执行摘要 (1447-1661)

# Build new content
new_content = []
new_content.extend(header)
new_content.append('\n')

# Tab 1: 执行摘要 (from old tab9)
new_content.append('    # Tab 1: 执行摘要\n')
# Change "with tab9:" to "with tab1:"
for line in tab9_old:
    if line.strip() == 'with tab9:':
        new_content.append('    with tab1:\n')
    else:
        new_content.append(line)
new_content.append('\n')

# Tab 2: 产品排名 (from old tab1)
new_content.append('    # Tab 2: 产品排名\n')
for line in tab1_old:
    if line.strip() == 'with tab1:':
        new_content.append('    with tab2:\n')
    else:
        new_content.append(line)
new_content.append('\n')

# Tab 3: 数据分析 (from old tab2)
new_content.append('    # Tab 3: 数据分析\n')
for line in tab2_old:
    if line.strip() == 'with tab2:':
        new_content.append('    with tab3:\n')
    else:
        new_content.append(line)
new_content.append('\n')

# Tab 4: AI洞察 (from old tab3)
new_content.append('    # Tab 4: AI洞察\n')
for line in tab3_old:
    if line.strip() == 'with tab3:':
        new_content.append('    with tab4:\n')
    else:
        new_content.append(line)
new_content.append('\n')

# Tab 5: 历史趋势 (from old tab4)
new_content.append('    # Tab 5: 历史趋势\n')
for line in tab4_old:
    if line.strip() == 'with tab4:':
        new_content.append('    with tab5:\n')
    else:
        new_content.append(line)
new_content.append('\n')

# Tab 6: 情绪分析 (from old tab5)
new_content.append('    # Tab 6: 情绪分析\n')
for line in tab5_old:
    if line.strip() == 'with tab5:':
        new_content.append('    with tab6:\n')
    else:
        new_content.append(line)
new_content.append('\n')

# Tab 7: 产品分析 (from old tab6 second occurrence)
new_content.append('    # Tab 7: 产品分析\n')
for line in tab6_old_second:
    if line.strip() == 'with tab6:':
        new_content.append('    with tab7:\n')
    else:
        new_content.append(line)
new_content.append('\n')

# Tab 8: 竞争分析 (from old tab6 first occurrence)
new_content.append('    # Tab 8: 竞争分析\n')
for line in tab6_old_first:
    if line.strip() == 'with tab6:':
        new_content.append('    with tab8:\n')
    else:
        new_content.append(line)
new_content.append('\n')

# Tab 9: 行动计划 (from old tab8)
new_content.append('    # Tab 9: 行动计划\n')
for line in tab8_old:
    if line.strip() == 'with tab8:':
        new_content.append('    with tab9:\n')
    else:
        new_content.append(line)
new_content.append('\n')

# Add footer
new_content.extend([
    '    # 页脚\n',
    '    st.divider()\n',
    '    st.caption("🖨️ 3D打印市场情报系统（完整增强版）| 数据来源: TikTok | AI分析: OpenAI GPT-4")\n',
    '    st.caption("💡 新增功能：情绪分析、产品分析、竞争分析、行动计划、执行摘要")\n',
    '\n',
    'if __name__ == "__main__":\n',
    '    main()\n'
])

# Write to dashboard.py
with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.writelines(new_content)

print("✅ Final fix complete!")
print(f"   Output: dashboard.py ({len(new_content)} lines)")

# Verify tab order
import re
tab_lines = []
for i, line in enumerate(new_content, 1):
    if re.match(r'^    with tab\d+:', line):
        tab_lines.append((i, line.strip()))

print(f"\n📋 Tab sections in correct order:")
for line_num, line in tab_lines:
    print(f"   Line {line_num}: {line}")
