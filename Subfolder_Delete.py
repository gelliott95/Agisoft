import os
import shutil

# Define the source and destination folders
source_folder = r'#Source Folder Path#'
destination_folder = source_folder

# Walk through all subdirectories and move files to the destination folder
for root, _, files in os.walk(source_folder):
    for file in files:
        source_path = os.path.join(root, file)
        destination_path = os.path.join(destination_folder, file)

        try:
            shutil.move(source_path, destination_path)
            print(f'Moved: {source_path} -> {destination_path}')
        except Exception as e:
            print(f'Error moving {source_path}: {str(e)}')

print('All files have been moved to the destination folder.')
