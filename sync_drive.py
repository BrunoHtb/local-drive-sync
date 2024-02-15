import os.path
from googleapiclient.errors import HttpError

import credentials as credential
import drive_operations as drive_operation
import local_operations as local_operation

drive_folder_name_ok = "OK"
drive_folder_name_main = "Bruno"
local_folder_path_ok = "D:/_TESTE_SYNC/OK"
local_folder_path  = "D:/_TESTE_SYNC"

def main():
  try:
    service = credential.check_credentials()

    id_folder_search = drive_operation.get_id_folder(service, drive_folder_name_main)
    id_folder_ok = drive_operation.get_id_folder(service, drive_folder_name_ok)

    if id_folder_search:
        file_in_folder = drive_operation.list_file_in_folder(service, id_folder_search)
        
        for file in file_in_folder:
            folder_target = os.path.join(local_folder_path, file.get("name"))
            drive_operation.download_file(service, file.get("id"), folder_target)

        
        local_files = local_operation.verify_new_file_local(local_folder_path_ok)

        for local_file in local_files:
            file_name = os.path.basename(local_file)
            drive_operation.upload_file(service, local_file, id_folder_ok)
            #delete_file(service, id_folder_search, file_name)
    else:
        print(f'Diretório {drive_folder_name_main} não encontrado no Google Drive.')

  except HttpError as error:
    print(f"An error occurred: {error}")
   
if __name__ == "__main__":
  main()
