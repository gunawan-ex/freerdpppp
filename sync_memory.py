import os
import json
import sys
import urllib.request

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SESSION_ID = "hermes_main_session"

MEMORY_DIR = r"C:\Users\runneradmin\HermesMemory"
MEMORY_FILE = os.path.join(MEMORY_DIR, "context.json")

def pull_memory():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Credentials Supabase belum di-set.")
        return

    url = f"{SUPABASE_URL}/rest/v1/hermes_memory?session_id=eq.{SESSION_ID}&select=*"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data:
                memory_data = data[0]["context_data"]
                os.makedirs(MEMORY_DIR, exist_ok=True)
                with open(MEMORY_FILE, "w") as f:
                    json.dump(memory_data, f, indent=2)
                print("Memori Hermes Agent berhasil ditarik ke VM.")
            else:
                print("Belum ada memori terdaftar di Supabase.")
    except Exception as e:
        print(f"Gagal pull memory: {e}")

def push_memory():
    if not os.path.exists(MEMORY_FILE):
        print("File memori lokal tidak ditemukan.")
        return

    with open(MEMORY_FILE, "r") as f:
        memory_data = json.load(f)

    url = f"{SUPABASE_URL}/rest/v1/hermes_memory"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates" # Otomatis Upsert
    }
    
    payload = json.dumps({
        "session_id": SESSION_ID,
        "context_data": memory_data
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            print("Memori Hermes Agent berhasil disimpan ke Supabase.")
    except Exception as e:
        print(f"Gagal push memory: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "pull":
            pull_memory()
        elif action == "push":
            push_memory()
