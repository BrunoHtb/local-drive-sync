import os.path
from googleapiclient.errors import HttpError

import credentials as credential
import drive_operations as drive_operation
import local_operations as local_operation

drive_folder_name_ok = "OK"
drive_folder_name_main = "81422 - IGC LASER - SÃO PAULO"
local_folder_path_ok = "OK"
local_folder_path  = "E:/_TESTE_SYNC/"

def upload_folder_user(service, id_folder_search, local_full_path_user):
  local_files = local_operation.verify_new_file_local(local_full_path_user)
  for local_file in local_files:
      drive_operation.upload_file(service, local_file, id_folder_search)


def download_folder_ok(service, id_folder_search, local_full_path):
  drive_folder_ok = drive_operation.list_folder(service, id_folder_search)

  if drive_folder_ok[0]['name'] == "OK":
    file_in_folder = drive_operation.list_file_in_folder(service, drive_folder_ok[0]['id'])
    if file_in_folder:
      local_full_path = local_operation.verify_folder_exist(local_full_path, "OK")
      for file in file_in_folder:
        folder_target = os.path.join(local_full_path, file.get("name"))
        drive_operation.download_file(service, file.get("id"), folder_target)


def run_folders_children(service, list_id_folder_in_parent):
  for id_folder in list_id_folder_in_parent:
    folder_name = drive_operation.get_name_folder(service, id_folder)
    local_full_path_user = local_operation.verify_folder_exist(local_folder_path, folder_name)
    id_folder_search = drive_operation.get_id_folder(service, folder_name)
    print(f"Nome do diretorio: {folder_name}")

    download_folder_ok(service, id_folder_search, local_full_path_user)
    upload_folder_user(service, id_folder_search, local_full_path_user)


def main():
  try:
    service = credential.check_credentials()

    id_folder_parent = drive_operation.get_id_folder(service, drive_folder_name_main)
    list_id_folder_in_parent = drive_operation.list_folder_parent(service, id_folder_parent)
    run_folders_children(service, list_id_folder_in_parent)

    input("PAROU AQUI")

    id_folder_search = drive_operation.get_id_folder(service, drive_folder_name_main)
    id_folder_ok = drive_operation.get_id_folder(service, drive_folder_name_ok)


  except HttpError as error:
    print(f"An error occurred: {error}")
   
if __name__ == "__main__":
  main()
