import os
import os.path
from plyer import notification

# To store paths of previously found files
found_files = []

def search_file(directory, filename):
    try:
        with os.scandir(directory) as entries:
            for entry in entries:
                try:
                    file_path = os.path.join(directory, entry.name)
                    
                    if entry.is_dir(follow_symlinks=False):
                        # Recursively search subdirectories
                        search_file(file_path, filename)
                    
                    elif entry.name == filename:
                        # If a file with the same name is found, check if it's a duplicate
                        if file_path not in found_files:
                            found_files.append(file_path)
                            print(f"File found at: {file_path}")
                            
                            # Send a notification to the user
                            notification.notify(
                                title='File Found',
                                message=f'The file "{filename}" was found at: {file_path}\nDon\'t download it again.',
                                app_name='File Searcher',
                                timeout=8
                            )
                        else:
                            print(f"Duplicate file found at: {file_path}")
                            notification.notify(
                                title='Duplicate File Alert',
                                message=f'A duplicate of "{filename}" was found at: {file_path}\nDon\'t download it again.',
                                app_name='File Searcher',
                                timeout=8
                            )
                except PermissionError:
                    print(f"Permission denied: {file_path}")
    except PermissionError:
        print(f"Permission denied: {directory}")
    except Exception as e:
        print(f"Error reading directory {directory}: {e}")

# Function to simulate checking before downloading
def check_before_download(filename):
    print(f"Checking for existing instances of {filename}...")
    search_file('C:\\', filename)
    
    if found_files:
        notification.notify(
            title='File Already Exists',
            message=f'The file "{filename}" already exists in the following locations:\n' + '\n'.join(found_files),
            app_name='File Searcher',
            timeout=10
        )
        print(f"Alert: The file '{filename}' already exists at: {found_files}")
    else:
        print(f"No duplicate found. You can proceed with downloading '{filename}'.")

# Check if the file already exists before "downloading"
check_before_download('AnyDesk.exe')
