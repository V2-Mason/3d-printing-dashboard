"""
数据管理模块 - Google Drive API v3集成
用于管理周次数据的上传、下载和列表
"""

import os
import json
import pandas as pd
import streamlit as st
from datetime import datetime
from typing import List, Dict, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
import tempfile

# Google Drive Shared Drive ID
GDRIVE_FOLDER_ID = "0AFBJflVvo6P2Uk9PVA"


def get_drive_service():
    """
    创建Google Drive API服务
    
    Returns:
        Resource: Drive API服务对象
    """
    try:
        # 从Streamlit secrets读取服务账号凭证
        if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
            credentials_dict = dict(st.secrets['gcp_service_account'])
        else:
            # 本地开发时从环境变量读取
            credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
            if credentials_json:
                credentials_dict = json.loads(credentials_json)
            else:
                raise Exception("No Google credentials found")
        
        # 创建凭证对象
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        
        # 创建Drive API服务
        service = build('drive', 'v3', credentials=credentials)
        return service
        
    except Exception as e:
        print(f"Failed to create Drive service: {e}")
        return None


def list_files_in_folder(service, folder_id):
    """
    列出文件夹中的所有文件
    
    Args:
        service: Drive API服务对象
        folder_id: 文件夹ID
        
    Returns:
        List: 文件列表
    """
    try:
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        return results.get('files', [])
    except Exception as e:
        print(f"Error listing files: {e}")
        return []


def get_available_weeks() -> List[int]:
    """
    从Google Drive获取所有可用的周次
    
    Returns:
        List[int]: 周次编号列表
    """
    try:
        service = get_drive_service()
        if not service:
            return [4]  # 默认返回第4周
        
        # 直接从Shared Drive根目录列出CSV文件
        files = list_files_in_folder(service, GDRIVE_FOLDER_ID)
        
        weeks = []
        for file in files:
            if file['name'].startswith('All_Data_Week_') and file['name'].endswith('.csv'):
                try:
                    import re
                    match = re.search(r'Week_(\d+)', file['name'])
                    if match:
                        week_num = int(match.group(1))
                        weeks.append(week_num)
                except (IndexError, ValueError):
                    continue
        
        return sorted(weeks) if weeks else [4]
        
    except Exception as e:
        print(f"Error getting available weeks: {e}")
        return [4]


def download_file(service, file_id):
    """
    下载文件内容
    
    Args:
        service: Drive API服务对象
        file_id: 文件ID
        
    Returns:
        bytes: 文件内容
    """
    try:
        request = service.files().get_media(fileId=file_id, supportsAllDrives=True)
        file_content = io.BytesIO()
        downloader = MediaIoBaseDownload(file_content, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        file_content.seek(0)
        return file_content.read()
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None


def load_csv_file(service, folder_id, filename):
    """
    从Shared Drive加载CSV文件
    
    Args:
        service: Drive API服务对象
        folder_id: 文件夹ID
        filename: 文件名
        
    Returns:
        pd.DataFrame: 数据框
    """
    try:
        files = list_files_in_folder(service, folder_id)
        
        for file in files:
            if file['name'] == filename:
                content = download_file(service, file['id'])
                if content:
                    return pd.read_csv(io.BytesIO(content))
        
        print(f"File not found: {filename}")
        return None
        
    except Exception as e:
        print(f"Error loading CSV file {filename}: {e}")
        return None


def load_week_data(week_number: int) -> Optional[pd.DataFrame]:
    """
    从Google Drive加载指定周次的完整数据
    
    Args:
        week_number: 周次编号
        
    Returns:
        pd.DataFrame: 产品数据
    """
    try:
        service = get_drive_service()
        if not service:
            return None
        
        csv_filename = f"All_Data_Week_{week_number:02d}.csv"
        df = load_csv_file(service, GDRIVE_FOLDER_ID, csv_filename)
        
        if df is not None:
            # 解析JSON字段
            if 'platforms_detail' in df.columns:
                df['platforms_detail'] = df['platforms_detail'].apply(
                    lambda x: json.loads(x) if isinstance(x, str) else x
                )
            if 'marketplace_detail' in df.columns:
                df['marketplace_detail'] = df['marketplace_detail'].apply(
                    lambda x: json.loads(x) if isinstance(x, str) else x
                )
            if 'emotion_distribution' in df.columns:
                df['emotion_distribution'] = df['emotion_distribution'].apply(
                    lambda x: json.loads(x) if isinstance(x, str) else x
                )
            if 'emotion_topics' in df.columns:
                df['emotion_topics'] = df['emotion_topics'].apply(
                    lambda x: json.loads(x) if isinstance(x, str) else x
                )
        
        return df
        
    except Exception as e:
        print(f"Error loading week {week_number} data: {e}")
        return None


def load_summary_data(week_number: int) -> Optional[pd.DataFrame]:
    """
    从Google Drive加载指定周次的摘要数据
    
    Args:
        week_number: 周次编号
        
    Returns:
        pd.DataFrame: 摘要数据
    """
    try:
        service = get_drive_service()
        if not service:
            return None
        
        csv_filename = f"Summary_Week_{week_number:02d}.csv"
        return load_csv_file(service, GDRIVE_FOLDER_ID, csv_filename)
        
    except Exception as e:
        print(f"Error loading summary data: {e}")
        return None


def load_platform_comparison(week_number: int) -> Optional[pd.DataFrame]:
    """
    从Google Drive加载指定周次的平台对比数据
    
    Args:
        week_number: 周次编号
        
    Returns:
        pd.DataFrame: 平台对比数据
    """
    try:
        service = get_drive_service()
        if not service:
            return None
        
        csv_filename = f"Platform_Comparison_Week_{week_number:02d}.csv"
        return load_csv_file(service, GDRIVE_FOLDER_ID, csv_filename)
        
    except Exception as e:
        print(f"Error loading platform comparison: {e}")
        return None


def load_emotion_analysis(week_number: int) -> Optional[pd.DataFrame]:
    """
    从Google Drive加载指定周次的情绪分析数据
    
    Args:
        week_number: 周次编号
        
    Returns:
        pd.DataFrame: 情绪分析数据
    """
    try:
        service = get_drive_service()
        if not service:
            return None
        
        csv_filename = f"Emotion_Analysis_Week_{week_number:02d}.csv"
        df = load_csv_file(service, GDRIVE_FOLDER_ID, csv_filename)
        
        if df is not None:
            # 解析JSON字段
            if 'top_keywords' in df.columns:
                df['top_keywords'] = df['top_keywords'].apply(
                    lambda x: json.loads(x) if isinstance(x, str) else x
                )
            if 'sample_comments' in df.columns:
                df['sample_comments'] = df['sample_comments'].apply(
                    lambda x: json.loads(x) if isinstance(x, str) else x
                )
        
        return df
        
    except Exception as e:
        print(f"Error loading emotion analysis: {e}")
        return None


def load_topic_analysis(week_number: int) -> Optional[pd.DataFrame]:
    """
    从Google Drive加载指定周次的主题分析数据
    
    Args:
        week_number: 周次编号
        
    Returns:
        pd.DataFrame: 主题分析数据
    """
    try:
        service = get_drive_service()
        if not service:
            return None
        
        csv_filename = f"Topic_Analysis_Week_{week_number:02d}.csv"
        df = load_csv_file(service, GDRIVE_FOLDER_ID, csv_filename)
        
        if df is not None:
            # 解析JSON字段
            if 'keywords' in df.columns:
                df['keywords'] = df['keywords'].apply(
                    lambda x: json.loads(x) if isinstance(x, str) else x
                )
        
        return df
        
    except Exception as e:
        print(f"Error loading topic analysis: {e}")
        return None


def upload_file(service, file_path, filename, folder_id):
    """
    上传文件到Google Drive
    
    Args:
        service: Drive API服务对象
        file_path: 本地文件路径
        filename: 目标文件名
        folder_id: 目标文件夹ID
        
    Returns:
        str: 上传后的文件ID
    """
    try:
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True
        ).execute()
        return file.get('id')
    except Exception as e:
        print(f"Error uploading file: {e}")
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
        service = get_drive_service()
        if not service:
            return False
        
        # 保存CSV到临时文件
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.csv') as tmp:
            tmp.write(csv_file.getbuffer())
            tmp_path = tmp.name
        
        # 上传CSV文件到Shared Drive根目录
        csv_filename = f"All_Data_Week_{week_number:02d}.csv"
        upload_file(service, tmp_path, csv_filename, GDRIVE_FOLDER_ID)
        
        # 删除临时文件
        os.unlink(tmp_path)
        
        return True
        
    except Exception as e:
        print(f"Error uploading week data: {e}")
        st.error(f"Upload failed: {e}")
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
    
    summary = {
        "week_number": week_number,
        "total_products": len(df),
        "main_track_count": len(df[df['track_type'] == '主轨道']),
        "secondary_track_count": len(df[df['track_type'] == '副轨道']),
        "watch_count": len(df[df['track_type'] == '观察']),
        "avg_total_score": df['total_score'].mean(),
        "avg_emotion_score": df['emotion_score'].mean(),
        "avg_engagement_rate": df['engagement_rate'].mean(),
        "collection_date": df['collection_date'].iloc[0] if 'collection_date' in df.columns else 'Unknown'
    }
    
    return summary


def extract_week_number_from_filename(filename: str) -> Optional[int]:
    """
    从文件名中提取周次编号
    
    Args:
        filename: 文件名
        
    Returns:
        int: 周次编号
    """
    try:
        import re
        match = re.search(r'Week_(\d+)', filename)
        if match:
            return int(match.group(1))
        return None
    except:
        return None


if __name__ == "__main__":
    print("Testing data_manager_gdrive module...")
    print("Note: This requires Google Drive API credentials to be configured")
