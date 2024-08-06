import os

def verify_folder_exist(local_folder_path, local_folder_children):
    local_full_path = os.path.join(local_folder_path, local_folder_children)
    if not os.path.exists(local_full_path):
        os.makedirs(local_full_path)
    return local_full_path

def verify_new_file_local(local_folder_path):
    local_files = [os.path.join(local_folder_path, file) for file in os.listdir(local_folder_path) if os.path.isfile(os.path.join(local_folder_path, file))]
    return local_files

def load_downloaded_files(txt_path):
    if not os.path.exists(txt_path):
        return set()
    with open(txt_path, 'r') as f:
        return set(line.strip() for line in f)

def add_downloaded_file(txt_path, file_name):
    with open(txt_path, 'a') as f:
        f.write(f"{file_name}\n")