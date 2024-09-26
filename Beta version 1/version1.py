import os
import fnmatch

def search_files(root_dir):
    # List of patterns for files/directories to exclude
    exclude_patterns = [
        'Windows', 'Program Files', 'Program Files (x86)', 
        'ProgramData', '$Recycle.Bin', 'System Volume Information'
    ]

    for root, dirs, files in os.walk(root_dir):
        # Remove excluded directories from the list to be searched
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pat) for pat in exclude_patterns)]

        for file in files:
            # Construct full file path
            file_path = os.path.join(root, file)
            # Print the file path
            print(file_path)

# Specify the root directory to search
root_directory = r"C:\Users\ketan\Downloads"

# Run the search
search_files(root_directory)