import os
import sys 
import time
from datetime import datetime, timedelta
from pathlib import Path

# Set the threshold for "old" files (60 days ago)
TIME_THRESHOLD = datetime.now() - timedelta(days=60)

def find_old_files(directory_path: str):
    """
    Scans the given directory and identifies files older than the TIME_THRESHOLD.
    """
    old_files = []
    
    scan_path = Path(directory_path)
    
    if not scan_path.is_dir():
        print(f"🚨 Error: Path '{directory_path}' is not a valid directory.")
        return old_files

    print(f"\n🔍 Scanning: {directory_path}")
    print(f"✨ Vibe Check: Looking for files older than {TIME_THRESHOLD.strftime('%Y-%m-%d')}")
    
    for file_path in scan_path.rglob('*'):
        if file_path.is_file():
            # Get the file's last modification time (mtime)
            mtime_timestamp = os.path.getmtime(file_path)
            
            # Convert the timestamp to a readable datetime object
            mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
            
            # This is the core logic: Is the file older than our threshold?
            if mtime_datetime < TIME_THRESHOLD:
                old_files.append(file_path)
                
    return old_files

def quarantine_files(files_list, base_path):
    """
    Moves identified files into a timestamped Quarantine folder 
    to maintain system order and data integrity.
    """
    if not files_list:
        return

    # Create a unique, timestamped Quarantine folder
    timestamp = datetime.now().strftime("%Y%m%d")
    quarantine_folder_name = f"_Quarantine_{timestamp}"
    
    quarantine_path = Path(base_path) / quarantine_folder_name
    quarantine_path.mkdir(exist_ok=True) # Create the folder if it doesn't exist

    print(f"\n📦 Initiating Quarantine Protocol: Moving {len(files_list)} files to:")
    print(f"   {quarantine_path}")

    moved_count = 0
    for file_path in files_list:
        try:
            # Define the new file location
            new_location = quarantine_path / file_path.name
            
            # The Critical Fix: Ensure robust move with absolute path
            file_path.resolve().rename(new_location) 
            moved_count += 1
        except Exception as e:
            # Handle files that can't be moved (permission issues, etc.)
            print(f"   ⚠️ Failed to move {file_path.name}: {e}")

    print(f"\n✅ Quarantine Complete! Successfully moved {moved_count} files.")
    print("✨ Digital Zen Achieved. Your system is now cleaner and more orderly.")

# --- Main Logic: Accepting Arguments ---
if __name__ == "__main__":
    
    # 1. Check for Command Line Input 
    if len(sys.argv) < 2:
        print("\n🚨 Vibe Check Failed: Please provide a directory path to scan.")
        print("   Usage: python sL_system_scanner.py [path/to/folder]")
        scan_directory = Path.cwd()
        print(f"   (Defaulting to current directory: {scan_directory})")
    else:
        # Get the path from the first argument
        scan_directory = Path(sys.argv[1])

    # 2. Execute the Scan
    files_to_quarantine = find_old_files(str(scan_directory))

    # 3. Execute the Quarantine Protocol
    if files_to_quarantine:
        print(f"\n✅ Found {len(files_to_quarantine)} files older than 60 days.")
        
        # --- EXECUTE THE QUARANTINE ---
        quarantine_files(files_to_quarantine, scan_directory) 
    else:
        print("\n🎉 Vibe Coding Success! No old files detected. Digital Zen!")