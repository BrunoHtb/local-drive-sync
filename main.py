import os.path
import configparser
from googleapiclient.errors import HttpError

import credentials as credential
import drive_operations as drive_operation
import local_operations as local_operation


config = configparser.ConfigParser()
with open('config.ini', 'r', encoding='utf-8') as f:
    config.read_file(f)

drive_folder_name_ok = config['paths']['drive_folder_ok_path']
drive_folder_name_main = config['paths']['drive_folder_path']
local_folder_path_ok = config['paths']['local_folder_ok_path']
local_folder_path  = config['paths']['local_folder_path']

downloaded_files_txt = 'downloaded_files.txt'


def upload_folder_user(service, id_folder_search, local_full_path_user):
  local_files = local_operation.verify_new_file_local(local_full_path_user)
  for local_file in local_files:
      drive_operation.upload_file(service, local_file, id_folder_search)


def download_folder_ok(service, id_folder_search, local_full_path, drive_folder_name):
    drive_folder_ok = drive_operation.list_folder(service, id_folder_search)

    if not drive_folder_ok:
        print(f"No folders found in the directory with ID {id_folder_search}")
        return

    if drive_folder_ok[0]['name'] == "OK":
        file_in_folder = drive_operation.list_file_in_folder(service, drive_folder_ok[0]['id'])
        if file_in_folder:
            local_full_path = local_operation.verify_folder_exist(local_full_path, "OK")
            downloaded_files = local_operation.load_downloaded_files(downloaded_files_txt)
            for file in file_in_folder:
                folder_target = os.path.join(local_full_path, file.get("name"))
                drive_operation.download_file(service, file.get("id"), folder_target, drive_folder_name, downloaded_files, downloaded_files_txt)



def run_folders_children(service, list_id_folder_in_parent):
  for id_folder in list_id_folder_in_parent:
    folder_name = drive_operation.get_name_folder(service, id_folder)
    local_full_path_user = local_operation.verify_folder_exist(local_folder_path, folder_name)
    id_folder_search = drive_operation.get_id_folder(service, folder_name)
    print(f"Nome do diretorio: {folder_name}")

    download_folder_ok(service, id_folder_search, local_full_path_user, folder_name)
    #upload_folder_user(service, id_folder_search, local_full_path_user)


def main():
  try:
    service = credential.check_credentials()

    id_folder_parent = drive_operation.get_id_folder(service, drive_folder_name_main)
    list_id_folder_in_parent = drive_operation.list_folder_parent(service, id_folder_parent)   
    run_folders_children(service, list_id_folder_in_parent)

    input("PAROU AQUI")

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()
