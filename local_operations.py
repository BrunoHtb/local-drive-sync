import os

def verify_new_file_local(local_folder_path):
    local_files = [os.path.join(local_folder_path, file) for file in os.listdir(local_folder_path) if os.path.isfile(os.path.join(local_folder_path, file))]
    return local_files
