# Drive Sync Downloader (Google Drive → Local)

Automated downloader that mirrors files from a Google Drive folder structure into a local directory,
focusing on files placed inside an **OK** subfolder.

---

## 🇧🇷 Drive Sync Downloader (Google Drive → Local)

Baixador automático que espelha arquivos de uma estrutura de pastas no Google Drive para um diretório local,
com foco nos arquivos colocados dentro de uma subpasta **OK**.

---

## What it does

- Authenticates with Google Drive (OAuth)
- Finds a main Drive folder (by name)
- Iterates through its child folders
- Looks for an **OK** folder inside each child folder
- Downloads files from **OK** to `local/<child>/OK/`
- Skips previously downloaded files using `downloaded_files.txt`
- Runs periodically (every 2 hours)

## Folder structure (example)

### Google Drive

NUVEM_DE_PONTOS/
    Project_A/
        OK/
            file1.las
            file2.tif
    Project_B/
        OK/
            file3.las

shell
Copy code

### Local

E:/_TESTE_SYNC/
    Project_A/
        OK/
            file1.las
            file2.tif
    Project_B/
        OK/
            file3.las
            downloaded_files.txt


## Setup

### 1) Credentials

Place your `client_secret.json` (OAuth credentials from Google Cloud) in the project root.

### 2) Configuration

Copy `config.example.ini` to `config.ini` and edit the paths:

```ini
[paths]
local_folder_path = E:/_TESTE_SYNC/
local_folder_ok_path = OK
drive_folder_path = NUVEM_DE_PONTOS
drive_folder_ok_path = OK

3) Install dependencies
```bash
pip install -r requirements.txt