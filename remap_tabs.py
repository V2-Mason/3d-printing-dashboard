#!/usr/bin/env python3
"""
Script to remap tab contents in dashboard.py to match tab names correctly
"""

def extract_tab_content(lines, start_line, end_line):
    """Extract content between start and end lines"""
    return lines[start_line-1:end_line]

def main():
    # Read the current dashboard
    with open('dashboard.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Extract each tab's content (line numbers are 1-indexed)
    # Current mapping (WRONG):
    # tab1 (line 367-426): Product Ranking Table
    # tab2 (line 427-497): Action Plan  
    # tab3 (line 498-548): Product Analysis
    # tab4 (line 549-619): Emotion Analysis
    # tab5 (line 620-836): Competitor Analysis Part 1
    # tab6 (line 837-942): Data Analysis
    # tab6 again (line 943-1189): Competitor Analysis Part 2
    # tab7 (line 1190-1295): AI Insights
    # tab8 (line 1296-1461): Historical Trends
    # tab9 (line 1462-1667): Executive Summary
    
    # Extract content sections
    header = lines[:366]  # Everything before tabs
    
    tab1_content_old = extract_tab_content(lines, 367, 426)  # Product Ranking
    tab2_content_old = extract_tab_content(lines, 427, 497)  # Action Plan
    tab3_content_old = extract_tab_content(lines, 498, 548)  # Product Analysis
    tab4_content_old = extract_tab_content(lines, 549, 619)  # Emotion Analysis
    tab5_content_old = extract_tab_content(lines, 620, 836)  # Competitor Part 1
    tab6_content_old = extract_tab_content(lines, 837, 942)  # Data Analysis
    tab6_content_old2 = extract_tab_content(lines, 943, 1189)  # Competitor Part 2
    tab7_content_old = extract_tab_content(lines, 1190, 1295)  # AI Insights
    tab8_content_old = extract_tab_content(lines, 1296, 1461)  # Historical Trends
    tab9_content_old = extract_tab_content(lines, 1462, len(lines))  # Executive Summary
    
    # Correct mapping (NEW):
    # tab1 should be: Executive Summary (currently tab9)
    # tab2 should be: Product Ranking (currently tab1)
    # tab3 should be: Product Analysis (currently tab3) ✓
    # tab4 should be: Emotion Analysis (currently tab4) ✓
    # tab5 should be: Competitor Analysis (currently tab5+tab6_part2)
    # tab6 should be: Data Analysis (currently tab6) ✓
    # tab7 should be: AI Insights (currently tab7) ✓
    # tab8 should be: Historical Trends (currently tab8) ✓
    # tab9 should be: Action Plan (currently tab2)
    
    # Build new file
    new_lines = []
    new_lines.extend(header)
    
    # Tab 1: Executive Summary (from old tab9)
    new_lines.append("    # Tab 1: 执行摘要\n")
    new_lines.extend(tab9_content_old)
    new_lines.append("\n")
    
    # Tab 2: Product Ranking (from old tab1)
    new_lines.append("    # Tab 2: 产品排名\n")
    new_lines.extend(tab1_content_old)
    new_lines.append("\n")
    
    # Tab 3: Product Analysis (from old tab3) - already correct
    new_lines.append("    # Tab 3: 产品分析\n")
    new_lines.extend(tab3_content_old)
    new_lines.append("\n")
    
    # Tab 4: Emotion Analysis (from old tab4) - already correct
    new_lines.append("    # Tab 4: 情绪分析\n")
    new_lines.extend(tab4_content_old)
    new_lines.append("\n")
    
    # Tab 5: Competitor Analysis (from old tab5 + tab6_part2)
    new_lines.append("    # Tab 5: 竞争分析\n")
    new_lines.extend(tab5_content_old)
    new_lines.extend(tab6_content_old2)
    new_lines.append("\n")
    
    # Tab 6: Data Analysis (from old tab6) - already correct
    new_lines.append("    # Tab 6: 数据分析\n")
    new_lines.extend(tab6_content_old)
    new_lines.append("\n")
    
    # Tab 7: AI Insights (from old tab7) - already correct
    new_lines.append("    # Tab 7: AI洞察\n")
    new_lines.extend(tab7_content_old)
    new_lines.append("\n")
    
    # Tab 8: Historical Trends (from old tab8) - already correct
    new_lines.append("    # Tab 8: 历史趋势\n")
    new_lines.extend(tab8_content_old)
    new_lines.append("\n")
    
    # Tab 9: Action Plan (from old tab2)
    new_lines.append("    # Tab 9: 行动计划\n")
    new_lines.extend(tab2_content_old)
    
    # Write new file
    with open('dashboard_remapped.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("✅ Tab remapping complete!")
    print(f"   Original file: {len(lines)} lines")
    print(f"   New file: {len(new_lines)} lines")
    print("   Output: dashboard_remapped.py")

if __name__ == "__main__":
    main()
