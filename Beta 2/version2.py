import os
import fnmatch
from collections import defaultdict
import time

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

def search_and_categorize_files(root_dir):
    exclude_patterns = [
        'Windows', 'Program Files', 'Program Files (x86)', 
        'ProgramData', '$Recycle.Bin', 'System Volume Information'
    ]
    
    file_categories = defaultdict(int)
    total_files = 0
    start_time = time.time()

    print("Searching and sorting files... Please wait.")

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pat) for pat in exclude_patterns)]
        
        for file in files:
            total_files += 1
            category = get_file_category(file)
            file_categories[category] += 1

    end_time = time.time()
    
    return file_categories, total_files, end_time - start_time

def print_file_analysis(file_categories, total_files, search_time):
    print("\nFile's Data and Metadata sorting algorithm successfully worked!")
    print(f"\nAnalysis completed in {search_time:.2f} seconds")
    print(f"Total files analyzed: {total_files}")
    print("\nFile Format Analysis:")
    
    sorted_categories = sorted(file_categories.items(), key=lambda x: x[1], reverse=True)
    
    for category, count in sorted_categories:
        percentage = (count / total_files) * 100
        print(f"{category}: {count} files ({percentage:.2f}%)")

# Specified here the root directory to perform searching
root_directory = r"C:\Users\ketan\Downloads"

# Runs a searching  and categorization of the files
file_categories, total_files, search_time = search_and_categorize_files(root_directory)

# Print the analysis of file format 
print_file_analysis(file_categories, total_files, search_time)