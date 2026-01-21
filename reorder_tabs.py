#!/usr/bin/env python3
"""
Reorder tab sections in dashboard.py to match the correct sequence
"""

with open('dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find tab section boundaries
tab_sections = {}
for i, line in enumerate(lines):
    if line.strip().startswith('with tab') and ':' in line:
        tab_num = int(line.strip().split('tab')[1].split(':')[0])
        tab_sections[tab_num] = i

print("Tab sections found:")
for tab, line_num in sorted(tab_sections.items()):
    print(f"  tab{tab}: line {line_num+1}")

# Extract each tab's content
tab_contents = {}
sorted_tabs = sorted(tab_sections.keys())

for idx, tab_num in enumerate(sorted_tabs):
    start = tab_sections[tab_num]
    # Find where this tab section ends
    if idx < len(sorted_tabs) - 1:
        # Next tab starts
        next_tab = sorted_tabs[idx + 1]
        end = tab_sections[next_tab]
    else:
        # Last tab - goes until footer
        for j in range(start, len(lines)):
            if '# 页脚' in lines[j] or 'if __name__' in lines[j]:
                end = j
                break
        else:
            end = len(lines)
    
    # Also look backwards for the comment line
    comment_start = start
    for j in range(start-1, max(0, start-5), -1):
        if '# =====' in lines[j] or '# Tab' in lines[j]:
            comment_start = j
            break
    
    tab_contents[tab_num] = lines[comment_start:end]
    print(f"  tab{tab_num}: lines {comment_start+1}-{end} ({len(tab_contents[tab_num])} lines)")

# Build new file
# Everything before first tab
first_tab_line = min(tab_sections.values())
# Find the comment before first tab
header_end = first_tab_line
for j in range(first_tab_line-1, max(0, first_tab_line-10), -1):
    if '# =====' in lines[j] or '# Tab' in lines[j]:
        header_end = j
        break

header = lines[:header_end]

# Add tabs in correct order: 1, 2, 3, 4, 5, 6, 7, 8, 9
new_content = header
for tab_num in range(1, 10):
    if tab_num in tab_contents:
        new_content.extend(tab_contents[tab_num])
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

# Write new file
with open('dashboard_reordered.py', 'w', encoding='utf-8') as f:
    f.writelines(new_content)

print(f"\n✅ Reordering complete!")
print(f"   Original: {len(lines)} lines")
print(f"   New: {len(new_content)} lines")
print(f"   Output: dashboard_reordered.py")
