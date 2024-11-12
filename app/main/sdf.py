# Original list
data = [
    'Directory: C:\\Users\\solap\\OneDrive\\Pictures\\Wallpaper',
    '',
    '',
    'Mode                 LastWriteTime         Length Name',
    '----                 -------------         ------ ----',
    '                      -a---l        12/29/2022  12:32 AM         411716 155802.jpg'
]

# Extract the last line containing the file details
file_details_line = data[-1].strip()

# Split the line by whitespace
file_details = file_details_line.split()

# Extract the file size and name (last two elements in the list)
file_size = file_details[-2]
file_name = file_details[-1]

# Output the results
print('File Size:', file_size)  # "411716"
print('File Name:', file_name)  # "155802.jpg"
