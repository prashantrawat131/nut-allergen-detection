import os

def rename_images(folder_path):
    # Get all files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]
    
    # Sort the files to maintain order
    files.sort()

    # Rename each file
    for index, file in enumerate(files, start=1):
        old_path = os.path.join(folder_path, file)
        new_name = f"{index}.jpg"
        new_path = os.path.join(folder_path, new_name)
        
        os.rename(old_path, new_path)
        print(f"Renamed: {file} -> {new_name}")

# Specify the folder containing the images
folder_path = "./RGB_samples"

# Call the function
rename_images(folder_path)