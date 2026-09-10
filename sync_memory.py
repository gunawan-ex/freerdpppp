import os
import json
import sys
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SESSION_ID = "hermes_main_session"

# Folder penyimpan memori di Windows VM
MEMORY_DIR = r"C:\Users\runneradmin\HermesMemory"
MEMORY_FILE = os.path.join(MEMORY_DIR, "context.json")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def pull_memory():
    response = supabase.table("hermes_memory").select("*").eq("session_id", SESSION_ID).execute()
    if response.data:
        memory_data = response.data[0]["context_data"]
        os.makedirs(MEMORY_DIR, exist_ok=True)
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory_data, f, indent=2)
        print("Memori Hermes Agent berhasil ditarik ke VM.")
    else:
        print("Belum ada memori. Memulai dari awal.")

def push_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            memory_data = json.load(f)
        
        data = {
            "session_id": SESSION_ID,
            "context_data": memory_data
        }
        supabase.table("hermes_memory").upsert(data, on_conflict="session_id").execute()
        print("Memori Hermes Agent berhasil disimpan ke Supabase.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "pull":
            pull_memory()
        elif action == "push":
            push_memory()
