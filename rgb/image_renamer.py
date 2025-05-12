import os

def rename_images(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]
    files.sort()
    for index, file in enumerate(files, start=1):
        old_path = os.path.join(folder_path, file)
        new_name = f"{index}.jpg"
        new_path = os.path.join(folder_path, new_name)
        
        os.rename(old_path, new_path)
        print(f"Renamed: {file} -> {new_name}")

folder_path = "./RGB_samples"
rename_images(folder_path)