#!/usr/bin/env python3
"""
Sync data from Google Drive to local reports directory
This script runs automatically when the dashboard starts
"""

import os
import subprocess
import sys
from pathlib import Path

def sync_from_google_drive():
    """Download all data files from Google Drive to local reports directory"""
    
    print("🔄 Syncing data from Google Drive...")
    
    # Create reports directory if it doesn't exist
    reports_dir = Path('reports')
    reports_dir.mkdir(exist_ok=True)
    
    # Check if rclone config exists
    rclone_config = Path.home() / '.gdrive-rclone.ini'
    
    if not rclone_config.exists():
        print("⚠️  Google Drive not configured. Using local data only.")
        return False
    
    try:
        # Sync all CSV files from Google Drive
        cmd = [
            'rclone', 'copy',
            'manus_google_drive:Market Intelligence Data/',
            str(reports_dir),
            '--config', str(rclone_config),
            '--include', '*.csv',
            '-v'
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            # Count synced files
            csv_files = list(reports_dir.glob('*.csv'))
            week_files = [f for f in csv_files if 'All_Data_Week_' in f.name]
            
            print(f"✅ Sync complete! {len(week_files)} week data files available.")
            return True
        else:
            print(f"❌ Sync failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️  Sync timeout. Using cached data.")
        return False
    except Exception as e:
        print(f"❌ Sync error: {e}")
        return False

def main():
    """Main entry point"""
    success = sync_from_google_drive()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
