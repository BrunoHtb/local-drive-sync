import os.path
import time
import configparser
from googleapiclient.errors import HttpError

import credentials as credential
import drive_operations as drive_operation
import local_operations as local_operation

config = configparser.ConfigParser()
with open('config.ini', 'r', encoding='utf-8') as f:
    config.read_file(f)


def main():
    while True:
        try:
            service = credential.check_credentials()

            drive_folder_name_ok = config['paths']['drive_folder_ok_path']
            drive_folder_name_main = config['paths']['drive_folder_path']
            local_root = config['paths']['local_folder_path']
            downloaded_files_txt = os.path.join(local_root, "downloaded_files.txt")

            parent_id = drive_operation.get_id_folder(service, drive_folder_name_main)
            if not parent_id:
                raise RuntimeError(f"Pasta '{drive_folder_name_main}' não encontrada no Drive. Verifique o nome exato e acentos.")

            children_ids = drive_operation.list_folder_parent(service, parent_id)

            for child_id in children_ids:
                child_name = drive_operation.get_name_folder(service, child_id)
                local_full_path = local_operation.verify_folder_exist(local_root, child_name)

                ok_id = drive_operation.get_id_folder(service, drive_folder_name_ok, parent_id=child_id)
                if not ok_id:
                    continue 

                files = drive_operation.list_file_in_folder(service, ok_id)
                if not files:
                    continue

                local_ok = local_operation.verify_folder_exist(local_full_path, drive_folder_name_ok)
                downloaded = local_operation.load_downloaded_files(downloaded_files_txt)

                for f in files:
                    target_path = os.path.join(local_ok, f["name"])
                    drive_operation.download_file(service, f["id"], target_path, drive_folder_name_main, downloaded, downloaded_files_txt)

            time.sleep(7200)

        except HttpError as e:
            print(f"Google API error: {e}")
            time.sleep(15)
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(15)


if __name__ == "__main__":
    main()
