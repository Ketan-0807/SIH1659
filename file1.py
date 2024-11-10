import subprocess
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase
cred = credentials.Certificate("C:/Users/solap/Downloads/service-account-file.json")
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

# Reference to the file in Firebase Storage
bucket = storage.bucket()
blob = bucket.blob('Images/155802.jpg')

# Fetch Firebase file metadata
blob.reload()  # Ensures metadata is loaded
firebase_metadata = {
    "Name": blob.name.split('/')[-1],  # Extract the file name only
    "Size": blob.size
}

print("Firebase File Metadata:")
for key, value in firebase_metadata.items():
    print(f"{key}: {value}")

# PowerShell command to search for the file locally
filename = "155802.jpg"  # File name to search for
command = f'Get-ChildItem -Path "C:\\" -Filter "{filename}" -Recurse -ErrorAction SilentlyContinue'

# Run the PowerShell command using subprocess
result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)

# Parse the output of the PowerShell command to get the file location and extract size and name
lines = result.stdout.strip().splitlines()
directory_path = lines[0].replace('Directory: ', '').strip()
file_details_line = lines[-1].strip()
file_details = file_details_line.split()

file_size = int(file_details[-2])
file_name = file_details[-1]
print('File Name:', file_name)  # "155802.jpg"
print('File path:', directory_path)  # "155802.jpg"
print('File Size:', file_size)  # "411716"



if firebase_metadata["Name"] == file_name and firebase_metadata["Size"] == file_size:
        print("The file's name and size match between Firebase and the local system.")
else:
        print("The file's name and/or size do not match between Firebase and the local system.")


