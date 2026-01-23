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
        
        # 直接从Shared Drive根目录查找CSV文件
        files = list_files_in_folder(service, GDRIVE_FOLDER_ID)
        csv_filename = f"All_Data_Week_{week_number:02d}.csv"
        
        for file in files:
            if file['name'] == csv_filename:
                # 下载文件
                content = download_file(service, file['id'])
                if content:
                    df = pd.read_csv(io.BytesIO(content))
                    return df
        
        print(f"CSV file not found for week {week_number}")
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
        Dict: 元数据字典
    """
    try:
        service = get_drive_service()
        if not service:
            return None
        
        # 查找周次文件夹
        folders = list_files_in_folder(service, GDRIVE_FOLDER_ID)
        week_folder_name = f"week_{week_number:02d}"
        week_folder_id = None
        
        for folder in folders:
            if folder['name'] == week_folder_name and \
               folder['mimeType'] == 'application/vnd.google-apps.folder':
                week_folder_id = folder['id']
                break
        
        if not week_folder_id:
            return None
        
        # 查找metadata.json文件
        files = list_files_in_folder(service, week_folder_id)
        
        for file in files:
            if file['name'] == 'metadata.json':
                # 下载并解析JSON
                content = download_file(service, file['id'])
                if content:
                    return json.loads(content.decode('utf-8'))
        
        return None
        
    except Exception as e:
        print(f"Error loading metadata: {e}")
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
        
        # 创建周次文件夹
        week_folder_name = f"week_{week_number:02d}"
        
        # 检查文件夹是否已存在
        folders = list_files_in_folder(service, GDRIVE_FOLDER_ID)
        week_folder_id = None
        
        for folder in folders:
            if folder['name'] == week_folder_name and \
               folder['mimeType'] == 'application/vnd.google-apps.folder':
                week_folder_id = folder['id']
                break
        
        # 如果不存在则创建
        if not week_folder_id:
            folder_metadata = {
                'name': week_folder_name,
                'parents': [GDRIVE_FOLDER_ID],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = service.files().create(body=folder_metadata, fields='id', supportsAllDrives=True).execute()
            week_folder_id = folder.get('id')
        
        # 保存CSV到临时文件
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.csv') as tmp:
            tmp.write(csv_file.getbuffer())
            tmp_path = tmp.name
        
        # 读取CSV获取统计信息
        df = pd.read_csv(tmp_path)
        top_products = len(df[df['product_category'] == 'Top Product'])
        watch_products = len(df[df['product_category'] == 'Watch Product'])
        
        # 上传CSV文件
        csv_filename = f"All_Data_Week_{week_number:02d}.csv"
        upload_file(service, tmp_path, csv_filename, week_folder_id)
        
        # 删除临时文件
        os.unlink(tmp_path)
        
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
        
        # 上传元数据
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            json.dump(metadata, tmp, indent=2, ensure_ascii=False)
            tmp_path = tmp.name
        
        upload_file(service, tmp_path, 'metadata.json', week_folder_id)
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
