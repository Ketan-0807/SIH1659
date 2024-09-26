import os
import fnmatch
from collections import defaultdict
import time
import hashlib
from datetime import datetime

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

def get_file_metadata(file_path):
    try:
        stat = os.stat(file_path)
        return {
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'accessed': datetime.fromtimestamp(stat.st_atime),
        }
    except Exception as e:
        print(f"Error getting metadata for {file_path}: {e}")
        return None

def generate_file_id(file_path):
    return hashlib.md5(file_path.encode()).hexdigest()

def search_and_categorize_files(root_dir):
    exclude_patterns = [
        'Windows', 'Program Files', 'Program Files (x86)', 
        'ProgramData', '$Recycle.Bin', 'System Volume Information'
    ]
    
    file_categories = defaultdict(list)
    total_files = 0
    start_time = time.time()

    print("Searching and analyzing files... Please wait.")

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pat) for pat in exclude_patterns)]
        
        for file in files:
            total_files += 1
            file_path = os.path.join(root, file)
            category = get_file_category(file)
            metadata = get_file_metadata(file_path)
            if metadata:
                file_info = {
                    'path': file_path,
                    'id': generate_file_id(file_path),
                    'metadata': metadata
                }
                file_categories[category].append(file_info)

    end_time = time.time()
    
    return file_categories, total_files, end_time - start_time

def print_file_analysis(file_categories, total_files, search_time):
    print("\nFile's Data and Metadata sorting algorithm successfully worked!")
    print(f"\nAnalysis completed in {search_time:.2f} seconds")
    print(f"Total files analyzed: {total_files}")
    print("\nFile Format Analysis:")
    
    for category, files in file_categories.items():
        print(f"\n{category}: {len(files)} files")
        # Sort files by creation time (assumed to be download time)
        sorted_files = sorted(files, key=lambda x: x['metadata']['created'], reverse=True)
        for file in sorted_files[:5]:  # Show top 5 most recently downloaded files
            print(f"  ID: {file['id'][:8]}... | Size: {file['metadata']['size']} bytes | "
                  f"Downloaded: {file['metadata']['created'].strftime('%Y-%m-%d %H:%M:%S')}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more")

# Specify the root directory to search
root_directory = r"C:\Users\ketan\Downloads"

# Run the search and categorization
file_categories, total_files, search_time = search_and_categorize_files(root_directory)

# Print the analysis
print_file_analysis(file_categories, total_files, search_time)

print("\nAll files' metadata has been sorted and analyzed successfully.")