"""
数据管理模块 - Google Drive集成
用于管理周次数据的上传、下载和列表
"""

import subprocess
import os
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional

GDRIVE_CONFIG = "/home/ubuntu/.gdrive-rclone.ini"
GDRIVE_BASE_PATH = "manus_google_drive:3d-printing-data"


def get_available_weeks() -> List[int]:
    """
    从Google Drive获取所有可用的周次
    
    Returns:
        List[int]: 周次编号列表，例如 [1, 2, 3, 4]
    """
    try:
        result = subprocess.run(
            ['rclone', 'lsf', f'{GDRIVE_BASE_PATH}/', 
             '--config', GDRIVE_CONFIG],
            capture_output=True, 
            text=True,
            timeout=10
        )
        
        weeks = []
        for line in result.stdout.strip().split('\n'):
            if line.startswith('week_'):
                try:
                    week_num = int(line.split('_')[1].rstrip('/'))
                    weeks.append(week_num)
                except (IndexError, ValueError):
                    continue
        
        return sorted(weeks)
    except Exception as e:
        print(f"Error getting available weeks: {e}")
        return [4]  # 默认返回第4周


def load_week_data(week_number: int) -> Optional[pd.DataFrame]:
    """
    从Google Drive加载指定周次的完整数据
    
    Args:
        week_number: 周次编号
        
    Returns:
        pd.DataFrame: 产品数据，如果失败则返回None
    """
    try:
        # 创建临时目录
        temp_dir = f"/tmp/week_{week_number:02d}"
        os.makedirs(temp_dir, exist_ok=True)
        
        # 从Google Drive下载CSV文件
        csv_filename = f"All_Data_Week_{week_number:02d}.csv"
        local_path = os.path.join(temp_dir, csv_filename)
        remote_path = f"{GDRIVE_BASE_PATH}/week_{week_number:02d}/{csv_filename}"
        
        result = subprocess.run(
            ['rclone', 'copyto', remote_path, local_path,
             '--config', GDRIVE_CONFIG],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"Error downloading data: {result.stderr}")
            return None
        
        # 读取CSV
        if os.path.exists(local_path):
            df = pd.read_csv(local_path)
            return df
        else:
            return None
            
    except Exception as e:
        print(f"Error loading week {week_number} data: {e}")
        return None


def load_week_metadata(week_number: int) -> Optional[Dict]:
    """
    从Google Drive加载指定周次的元数据
    
    Args:
        week_number: 周次编号
        
    Returns:
        Dict: 元数据字典，如果失败则返回None
    """
    try:
        temp_file = f"/tmp/metadata_week_{week_number:02d}.json"
        remote_path = f"{GDRIVE_BASE_PATH}/week_{week_number:02d}/metadata.json"
        
        result = subprocess.run(
            ['rclone', 'copyto', remote_path, temp_file,
             '--config', GDRIVE_CONFIG],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and os.path.exists(temp_file):
            with open(temp_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
        
    except Exception as e:
        print(f"Error loading metadata: {e}")
        return None


def upload_week_data(csv_file, week_number: int, notes: str = "") -> bool:
    """
    上传新周次数据到Google Drive
    
    Args:
        csv_file: Streamlit UploadedFile对象
        week_number: 周次编号
        notes: 备注信息
        
    Returns:
        bool: 上传是否成功
    """
    try:
        # 创建周次文件夹
        week_folder = f"week_{week_number:02d}"
        subprocess.run(
            ['rclone', 'mkdir', f'{GDRIVE_BASE_PATH}/{week_folder}',
             '--config', GDRIVE_CONFIG],
            capture_output=True,
            timeout=10
        )
        
        # 保存上传的CSV到临时文件
        temp_csv = f"/tmp/All_Data_Week_{week_number:02d}.csv"
        with open(temp_csv, 'wb') as f:
            f.write(csv_file.getbuffer())
        
        # 上传CSV到Google Drive
        remote_csv = f"{GDRIVE_BASE_PATH}/{week_folder}/All_Data_Week_{week_number:02d}.csv"
        result = subprocess.run(
            ['rclone', 'copyto', temp_csv, remote_csv,
             '--config', GDRIVE_CONFIG],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"Error uploading CSV: {result.stderr}")
            return False
        
        # 读取CSV获取统计信息
        df = pd.read_csv(temp_csv)
        top_products = len(df[df['product_category'] == 'Top Product'])
        watch_products = len(df[df['product_category'] == 'Watch Product'])
        
        # 创建元数据
        metadata = {
            "week_number": week_number,
            "year": datetime.now().year,
            "collection_date": datetime.now().strftime("%Y-%m-%d"),
            "collector": "manual",
            "data_source": "TikTok",
            "total_products": len(df),
            "top_products": top_products,
            "watch_products": watch_products,
            "keywords_used": ["3d printing", "3d printed", "3d printer"],
            "notes": notes
        }
        
        # 保存并上传元数据
        temp_meta = f"/tmp/metadata_week_{week_number:02d}.json"
        with open(temp_meta, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        remote_meta = f"{GDRIVE_BASE_PATH}/{week_folder}/metadata.json"
        subprocess.run(
            ['rclone', 'copyto', temp_meta, remote_meta,
             '--config', GDRIVE_CONFIG],
            capture_output=True,
            timeout=10
        )
        
        return True
        
    except Exception as e:
        print(f"Error uploading week data: {e}")
        return False


def get_week_summary(week_number: int) -> Dict:
    """
    获取指定周次的数据摘要
    
    Args:
        week_number: 周次编号
        
    Returns:
        Dict: 包含统计信息的字典
    """
    df = load_week_data(week_number)
    if df is None:
        return {}
    
    metadata = load_week_metadata(week_number)
    
    summary = {
        "week_number": week_number,
        "total_products": len(df),
        "top_products": len(df[df['product_category'] == 'Top Product']),
        "watch_products": len(df[df['product_category'] == 'Watch Product']),
        "avg_total_score": df['total_score'].mean(),
        "avg_engagement_rate": df['engagement_rate'].mean(),
        "collection_date": metadata.get('collection_date', 'Unknown') if metadata else 'Unknown'
    }
    
    return summary


def extract_week_number_from_filename(filename: str) -> Optional[int]:
    """
    从文件名中提取周次编号
    
    Args:
        filename: 文件名，例如 "All_Data_Week_05.csv"
        
    Returns:
        int: 周次编号，如果无法提取则返回None
    """
    try:
        # 匹配 Week_XX 格式
        import re
        match = re.search(r'Week_(\d+)', filename)
        if match:
            return int(match.group(1))
        return None
    except:
        return None


if __name__ == "__main__":
    # 测试功能
    print("Testing data_manager module...")
    
    weeks = get_available_weeks()
    print(f"Available weeks: {weeks}")
    
    if weeks:
        week = weeks[-1]
        print(f"\nLoading week {week} data...")
        df = load_week_data(week)
        if df is not None:
            print(f"Loaded {len(df)} products")
            print(df.head())
        
        print(f"\nWeek {week} summary:")
        summary = get_week_summary(week)
        for key, value in summary.items():
            print(f"  {key}: {value}")
