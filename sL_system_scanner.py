import os
import time
from datetime import datetime, timedelta
from pathlib import Path

# Set the threshold for "old" files (60 days ago)
# timedelta is a clean way to define a time duration.
TIME_THRESHOLD = datetime.now() - timedelta(days=60)

def find_old_files(directory_path: str):
    """
    Scans the given directory and identifies files older than the TIME_THRESHOLD.
    
    Args:
        directory_path: The full path to the directory to scan.
    
    Returns:
        A list of Path objects for the old files found.
    """
    old_files = []
    
    # Use Path to handle the directory; it's clean and platform-independent
    scan_path = Path(directory_path)
    
    if not scan_path.is_dir():
        print(f"🚨 Error: Path '{directory_path}' is not a valid directory.")
        return old_files

    print(f"\n🔍 Scanning: {directory_path}")
    print(f"✨ Vibe Check: Looking for files older than {TIME_THRESHOLD.strftime('%Y-%m-%d')}")
    
    # Use rglob to recursively find all files in subdirectories
    for file_path in scan_path.rglob('*'):
        if file_path.is_file():
            # Get the file's last modification time (mtime)
            # os.path.getmtime returns a timestamp (seconds since epoch)
            mtime_timestamp = os.path.getmtime(file_path)
            
            # Convert the timestamp to a readable datetime object
            mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
            
            # This is the core logic: Is the file older than our threshold?
            if mtime_datetime < TIME_THRESHOLD:
                old_files.append(file_path)
                
    return old_files

# --- Example Usage ---
# NOTE: Replace the path below with a safe test directory on your system!
if __name__ == "__main__":
    # Create a safe test directory for this project if you need one!
    # TEST_DIR = Path("./test_files") 
    # TEST_DIR.mkdir(exist_ok=True)
    
    # For a real run, you might use your Downloads folder:
    # EXAMPLE_PATH = r"C:\Users\YourUser\Downloads" 
    
    # Start with your current project directory for a safe first test:
    EXAMPLE_PATH = Path.cwd() 
    
    files_to_quarantine = find_old_files(str(EXAMPLE_PATH))

    if files_to_quarantine:
        print(f"\n✅ Found {len(files_to_quarantine)} files to quarantine:")
        for f in files_to_quarantine:
            print(f" - {f.name} (Modified: {datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d')})")
    else:
        print("\n🎉 Vibe Coding Success! No files older than 60 days found. Digital Zen!")