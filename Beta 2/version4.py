import os
import hashlib
from collections import defaultdict
import time
from plyer import notification

def get_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as file:
        buf = file.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(65536)
    return hasher.hexdigest()

def get_file_category(filename):
    extension = os.path.splitext(filename)[1].lower()
    if extension in ['.pdf']:
        return 'PDF'
    elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        return 'Image'
    elif extension in ['.exe', '.msi']:
        return 'Executable'
    elif extension in ['.mp4', '.avi', '.mov', '.wmv', '.flv']:
        return 'Video'
    elif extension in ['.html', '.htm']:
        return 'HTML'
    elif extension in ['.url', '.lnk']:
        return 'Link'
    elif extension in ['.mp3', '.wav', '.ogg', '.flac']:
        return 'Audio'
    elif extension in ['.doc', '.docx', '.txt', '.rtf']:
        return 'Document'
    elif extension in ['.xls', '.xlsx', '.csv']:
        return 'Spreadsheet'
    elif extension in ['.ppt', '.pptx']:
        return 'Presentation'
    else:
        return 'Other'

def find_duplicates(root_dir):
    hash_dict = defaultdict(list)
    duplicate_files = defaultdict(list)
    file_categories = defaultdict(int)
    total_files = 0
    start_time = time.time()

    print("Searching for duplicate files... Please wait.")

    for root, _, files in os.walk(root_dir):
        for filename in files:
            total_files += 1
            filepath = os.path.join(root, filename)
            try:
                file_hash = get_file_hash(filepath)
                hash_dict[file_hash].append(filepath)
                category = get_file_category(filename)
                file_categories[category] += 1
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

    for file_hash, file_list in hash_dict.items():
        if len(file_list) > 1:
            duplicate_files[file_hash] = file_list

    end_time = time.time()
    return duplicate_files, file_categories, total_files, end_time - start_time

def notify_duplicates(duplicate_files):
    for file_hash, file_list in duplicate_files.items():
        duplicate_count = len(file_list)
        notification_title = f"Duplicate Files Detected"
        notification_message = f"Found {duplicate_count} duplicate files:\n" + "\n".join(file_list[:2])
        if duplicate_count > 2:
            notification_message += f"\n...and {duplicate_count - 2} more"
        
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_name="Duplicate File Detector",
            timeout=10
        )
        time.sleep(1)  # Wait a bit between notifications to avoid overwhelming the user

def print_analysis(duplicate_files, file_categories, total_files, search_time):
    print("\nDuplicate File Analysis:")
    print(f"Total files scanned: {total_files}")
    print(f"Analysis completed in {search_time:.2f} seconds")
    print(f"\nFile Format Distribution:")
    for category, count in sorted(file_categories.items(), key=lambda x: x[1], reverse=True):
        print(f"{category}: {count} files")

    print(f"\nDuplicate Files Found: {sum(len(files) for files in duplicate_files.values())}")
    for file_hash, file_list in duplicate_files.items():
        print(f"\nDuplicate set (MD5: {file_hash}):")
        for file_path in file_list:
            print(f"  {file_path}")

# Specify the root directory to search
root_directory = r"C:\Users\ketan\Downloads"

# Find duplicates
duplicate_files, file_categories, total_files, search_time = find_duplicates(root_directory)

# Print analysis
print_analysis(duplicate_files, file_categories, total_files, search_time)

# Notify user of duplicates
if duplicate_files:
    print("\nSending notifications for duplicate files...")
    notify_duplicates(duplicate_files)
else:
    notification.notify(
        title="No Duplicates Found",
        message="Your system is free from duplicate data in the scanned directory.",
        app_name="Duplicate File Detector",
        timeout=10
    )
    print("\nYour system is free from duplicate data in the scanned directory.")

print("\nDuplicate file analysis complete.")