import os
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

def download_file(service, file_id, folder_target):
    file_info = service.files().get(fileId=file_id).execute()

    if 'application/vnd.google-apps.folder' not in file_info['mimeType']:
        request = service.files().get_media(fileId=file_id)

        if not os.path.exists(folder_target):
            with open(folder_target, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f"Progresso do download: {int(status.progress() * 100)}%")
        else:
            print(f"O arquivo {folder_target} já existe. Pulando o download.")
    else:
        print(f'O item {folder_target} é um diretório. Pulando o download.')


def upload_file(service, local_file_path, folder_id):
    file_name = os.path.basename(local_file_path)
    file_exists = file_exists_in_folder(service, folder_id, file_name)

    if not file_exists:
        media = MediaFileUpload(local_file_path, resumable=True)
        request = service.files().create(
            media_body=media,
            body={
                'name': file_name,
                'parents': [folder_id],
            }
        )
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Progresso do upload: {int(status.progress() * 100)}%")
        print(f"Upload concluído para: {file_name}")
    else:
        print(f"Arquivo '{file_name}' já existe no diretório. Upload ignorado.")


def delete_file(service, folder_id, file_name):
    file_in_folder_to_delete = list_file_in_folder(service, folder_id)
    
    for file in file_in_folder_to_delete:
        if file.get("name") == file_name:
            file_id = file['id']
            if folder_id:
                body_value = {'trashed': True}
                service.files().update(fileId=file_id, body=body_value).execute()
            print(f"Arquivo '{file_name}' excluído do Google Drive.")


def get_id_folder(service, folder_name):
    response = service.files().list(
        q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'",
        spaces="drive",
        fields="files(id, name)"
    ).execute()

    folders = response.get("files", [])
    if folders:
        return folders[0]["id"]
    else:
        return None


def list_file_in_folder(service, id_folder):
    response = service.files().list(
        q=f"'{id_folder}' in parents",
        spaces="drive",
        fields="nextPageToken, files(id, name)"
    ).execute()

    files = response.get("files", [])
    return files


def file_exists_in_folder(service, folder_id, file_name):
    results = service.files().list(
        q=f"'{folder_id}' in parents and name='{file_name}'",
        fields="files(id, name)"
    ).execute()
    files = results.get('files', [])
    return len(files) > 0