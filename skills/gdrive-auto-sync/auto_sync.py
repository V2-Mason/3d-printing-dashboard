#!/usr/bin/env python3
"""
Google Drive Auto-Sync Script
Automatically detects and uploads missing week data to Google Drive
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import argparse

# Configuration
GDRIVE_CONFIG = {
    "shared_drive_id": "0AFBJflVvo6P2Uk9PVA",
    "rclone_config": "/home/ubuntu/.gdrive-rclone.ini",
    "remote_name": "manus_google_drive",
}

def get_current_week():
    """Get current ISO week number"""
    return int(datetime.now().strftime("%V"))

def get_local_weeks():
    """Get list of weeks with local data"""
    weeks = []
    for path in Path("/home/ubuntu").glob("week_*_data"):
        week_str = path.name.split("_")[1]
        try:
            week_num = int(week_str)
            weeks.append(week_num)
        except ValueError:
            continue
    return sorted(weeks)

def get_remote_weeks():
    """Get list of weeks already in Google Drive"""
    remote_path = f"{GDRIVE_CONFIG['remote_name']},drive_id={GDRIVE_CONFIG['shared_drive_id']}:"
    
    cmd = [
        "rclone", "ls",
        remote_path,
        "--config", GDRIVE_CONFIG["rclone_config"],
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    weeks = set()
    if result.returncode == 0:
        for line in result.stdout.split("\n"):
            if "Week_" in line:
                # Extract week number from filename like "All_Data_Week_06.csv"
                parts = line.split("Week_")
                if len(parts) > 1:
                    week_str = parts[1].split(".")[0]
                    try:
                        weeks.add(int(week_str))
                    except ValueError:
                        continue
    
    return sorted(list(weeks))

def upload_week(week_num):
    """Upload a specific week's data to Google Drive"""
    week_dir = f"/home/ubuntu/week_{week_num:02d}_data"
    
    if not Path(week_dir).exists():
        print(f"   ❌ Week {week_num:02d} data not found locally: {week_dir}")
        return False
    
    # Check if directory has CSV files
    csv_files = list(Path(week_dir).glob("*.csv"))
    if not csv_files:
        print(f"   ❌ No CSV files found in {week_dir}")
        return False
    
    remote_path = f"{GDRIVE_CONFIG['remote_name']},drive_id={GDRIVE_CONFIG['shared_drive_id']}:"
    
    cmd = [
        "rclone", "copy",
        week_dir + "/",
        remote_path,
        "--config", GDRIVE_CONFIG["rclone_config"],
        "-v"
    ]
    
    print(f"   📤 Uploading Week {week_num:02d}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"   ✅ Week {week_num:02d} uploaded successfully")
        return True
    else:
        print(f"   ❌ Week {week_num:02d} upload failed: {result.stderr}")
        return False

def verify_upload(week_num):
    """Verify that all files for a week are in Google Drive"""
    expected_files = [
        f"All_Data_Week_{week_num:02d}.csv",
        f"Platform_Comparison_Week_{week_num:02d}.csv",
        f"Top_Products_Week_{week_num:02d}.csv",
        f"Summary_Week_{week_num:02d}.csv",
    ]
    
    remote_path = f"{GDRIVE_CONFIG['remote_name']},drive_id={GDRIVE_CONFIG['shared_drive_id']}:"
    
    cmd = [
        "rclone", "ls",
        remote_path,
        "--config", GDRIVE_CONFIG["rclone_config"],
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        return False
    
    remote_files = result.stdout
    missing_files = [f for f in expected_files if f not in remote_files]
    
    if missing_files:
        print(f"   ⚠️  Week {week_num:02d} missing files: {', '.join(missing_files)}")
        return False
    
    return True

def sync_all():
    """Sync all local weeks to Google Drive"""
    print("🔍 Scanning for local and remote data...")
    
    local_weeks = get_local_weeks()
    remote_weeks = get_remote_weeks()
    
    print(f"   Local weeks found: {local_weeks}")
    print(f"   Remote weeks found: {remote_weeks}")
    print()
    
    if not local_weeks:
        print("❌ No local week data found")
        return
    
    # Find weeks that need uploading
    missing_weeks = [w for w in local_weeks if w not in remote_weeks]
    
    if not missing_weeks:
        print("✅ All local weeks are already in Google Drive")
        return
    
    print(f"📤 Uploading {len(missing_weeks)} missing weeks: {missing_weeks}")
    print()
    
    success_count = 0
    for week in missing_weeks:
        if upload_week(week):
            if verify_upload(week):
                success_count += 1
            else:
                print(f"   ⚠️  Week {week:02d} uploaded but verification failed")
    
    print()
    print(f"✅ Upload complete: {success_count}/{len(missing_weeks)} weeks successfully uploaded")

def fill_gaps():
    """Fill gaps in week sequence by generating and uploading missing data"""
    print("🔍 Checking for gaps in week sequence...")
    
    remote_weeks = get_remote_weeks()
    
    if not remote_weeks:
        print("❌ No remote data found")
        return
    
    current_week = get_current_week()
    min_week = min(remote_weeks)
    max_week = max(remote_weeks)
    
    # Find gaps between min and current week
    expected_weeks = set(range(min_week, current_week + 1))
    existing_weeks = set(remote_weeks)
    missing_weeks = sorted(expected_weeks - existing_weeks)
    
    if not missing_weeks:
        print(f"✅ No gaps found (Week {min_week} to Week {current_week})")
        return
    
    print(f"⚠️  Found {len(missing_weeks)} missing weeks: {missing_weeks}")
    print()
    
    # Check which missing weeks have local data
    local_weeks = get_local_weeks()
    can_upload = [w for w in missing_weeks if w in local_weeks]
    need_collection = [w for w in missing_weeks if w not in local_weeks]
    
    if can_upload:
        print(f"📤 Can upload from local: {can_upload}")
        for week in can_upload:
            upload_week(week)
    
    if need_collection:
        print(f"⚠️  Need to collect data first: {need_collection}")
        print(f"   Run: cd /home/ubuntu/skills/market-intelligence && python3 collector.py <week_num>")

def main():
    parser = argparse.ArgumentParser(description="Google Drive Auto-Sync for Market Intelligence Data")
    parser.add_argument("--week", type=int, help="Upload specific week number")
    parser.add_argument("--fill-gaps", action="store_true", help="Detect and fill gaps in week sequence")
    parser.add_argument("--verify", action="store_true", help="Verify all uploads without uploading")
    
    args = parser.parse_args()
    
    print("🚀 Google Drive Auto-Sync")
    print(f"📅 Current week: {get_current_week()}")
    print()
    
    if args.week:
        # Upload specific week
        success = upload_week(args.week)
        if success:
            verify_upload(args.week)
    elif args.fill_gaps:
        # Fill gaps in sequence
        fill_gaps()
    elif args.verify:
        # Verify only
        local_weeks = get_local_weeks()
        remote_weeks = get_remote_weeks()
        print(f"Local weeks: {local_weeks}")
        print(f"Remote weeks: {remote_weeks}")
        missing = [w for w in local_weeks if w not in remote_weeks]
        if missing:
            print(f"⚠️  Missing in remote: {missing}")
        else:
            print("✅ All local weeks are in remote")
    else:
        # Default: sync all
        sync_all()

if __name__ == "__main__":
    main()
