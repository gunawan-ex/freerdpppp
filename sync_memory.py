import os
import sys
import shutil
import urllib.request

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
BUCKET_NAME = "hermes-data"
FILE_NAME = "hermes_backup.zip"

# Lokasi $HERMES_HOME di Windows VM
HERMES_DIR = r"C:\Users\runneradmin\AppData\Local\hermes"
TEMP_ZIP = r"C:\Users\runneradmin\hermes_backup"  # shutil.make_archive akan menambah .zip otomatis

def pull_memory():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Credentials Supabase belum di-set.")
        return

    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{FILE_NAME}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        zip_path = f"{TEMP_ZIP}.zip"
        print("Mengunduh backup memori dari Supabase Storage...")
        with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
            out_file.write(response.read())

        # Ekstrak zip ke folder HERMES_DIR
        os.makedirs(HERMES_DIR, exist_ok=True)
        shutil.unpack_archive(zip_path, HERMES_DIR)
        print("Memori Hermes Agent berhasil di-restore ke $HERMES_HOME!")
    except Exception as e:
        print(f"Belum ada backup memori di Supabase / Gagal restore: {e}")

def push_memory():
    if not os.path.exists(HERMES_DIR):
        print("Folder $HERMES_HOME tidak ditemukan, skip backup.")
        return

    print("Mengompres folder $HERMES_HOME...")
    # Kompres folder hermes jadi zip
    zip_path = shutil.make_archive(TEMP_ZIP, 'zip', HERMES_DIR)

    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{FILE_NAME}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/zip",
        "x-upsert": "true"  # Timpa file lama jika sudah ada
    }

    with open(zip_path, 'rb') as f:
        payload = f.read()

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            print("Seluruh memori Hermes Agent ($HERMES_HOME) berhasil disimpan ke Supabase Storage!")
    except Exception as e:
        print(f"Gagal upload backup memori ke Supabase: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "pull":
            pull_memory()
        elif action == "push":
            push_memory()
