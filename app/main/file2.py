import subprocess, os
import firebase_admin
from firebase_admin import credentials, storage
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label

# Initialize Firebase
cred = credentials.Certificate("C:/Users/ketan/Downloads/service-account-file.json")

firebase_admin.initialize_app(cred, {
    'apiKey': "AIzaSyCMqGqsB1g583KrToDJmeyG9JQAlmh-Ps4",
    'authDomain': "coding-crafters-6af4a.firebaseapp.com",
    'databaseURL': "https://coding-crafters-6af4a-default-rtdb.firebaseio.com",
    'projectId': "coding-crafters-6af4a",
    'storageBucket': "coding-crafters-6af4a.appspot.com",
    'messagingSenderId': "571618682184",
    'appId': "1:571618682184:web:5a0d80d4ec8c23db8d7f7d",
    'measurementId': "G-700JFMKQ60"
})

def show_loading_screen():
    global loading_screen
    loading_screen = Toplevel()
    loading_screen.title("Loading")
    loading_screen.geometry("300x100")
    loading_screen.attributes('-topmost', True)
    Label(loading_screen, text="Processing... Please wait.").pack(pady=20)
    loading_screen.update()

def close_loading_screen():
    loading_screen.destroy()

def download_file_from_firebase(filename, bucket, blob_name):
    download_path = os.path.join("C:/Users/ketan/Downloads", filename)  # Set download to Downloads folder
    blob = bucket.blob(blob_name)
    blob.download_to_filename(download_path)
    print(f"File downloaded: {download_path}")
    return download_path

def show_popup(message):
    root = tk.Tk()
    root.title("Download File")
    root.withdraw()  
    root.attributes('-topmost', True)
    result = messagebox.askyesno("Download File", message)
    root.quit()  
    return result

def show_notification(message):
    root = tk.Tk()
    root.withdraw()  
    messagebox.showinfo("Notification", message)
    root.quit()

def get_filename_from_gui():
    root = tk.Tk()
    root.withdraw()  
    filename_input = simpledialog.askstring("Input", "Enter the filename you want to search for:")
    root.quit()
    return filename_input

def main():
    # Display loading screen
    
    filename_input = get_filename_from_gui()
    if not filename_input:
        show_notification("No filename entered.")
        close_loading_screen()
        return

    bucket = storage.bucket()
    blob = bucket.blob(f'Images/{filename_input}')
    show_loading_screen()
    
    try:
        if not blob.exists():
            close_loading_screen()
            show_notification(f"File '{filename_input}' does not exist in Firebase.")
            return
        
        blob.reload()
        firebase_metadata = {
            "Name": blob.name.split('/')[-1], 
            "Size": blob.size
        }

        print("Firebase File Metadata:")
        for key, value in firebase_metadata.items():
            print(f"{key}: {value}")

        command = f'Get-ChildItem -Path "C:\\" -Filter "{filename_input}" -Recurse -ErrorAction SilentlyContinue'
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()

        if len(lines) > 2:
            directory_path = lines[0].replace('Directory: ', '').strip()
            file_details_line = lines[-1].strip()
            file_details = file_details_line.split()

            local_file_size = int(file_details[-2])
            local_file_name = file_details[-1]

            print(f'\nFile found at: {directory_path}')
            print(f'File Name: {local_file_name}')
            print(f'File Size: {local_file_size} bytes')
            close_loading_screen()

            if firebase_metadata["Name"] == local_file_name and firebase_metadata["Size"] == local_file_size:
                print("\nThe file's name and size match between Firebase and the local system.")
                
                download_choice = show_popup("\nDo you want to download the file from Firebase?")
                if download_choice:
                    downloaded_file = download_file_from_firebase(local_file_name, bucket, f'Images/{local_file_name}')
                    show_notification(f"File downloaded: {downloaded_file}")
                else:
                    show_notification("Download canceled.")
            else:
                print("\nThe file's name and/or size do not match between Firebase and the local system.")
                download_choice = show_popup("\nDo you want to download the file from Firebase?")
                if download_choice:
                    downloaded_file = download_file_from_firebase(local_file_name, bucket, f'Images/{local_file_name}')
                    show_notification(f"File downloaded: {downloaded_file}")
                else:
                    show_notification("Download canceled.")
        else:
            print("\nFile not found locally.")
            download_file_from_firebase(filename_input, bucket, f'Images/{filename_input}')
            show_notification(f"File downloaded: C:/Users/ketan/Downloads/{filename_input}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Close loading screen
    close_loading_screen()

if __name__ == "__main__":
    main()
