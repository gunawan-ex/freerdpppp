import os
import json
import sys
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SESSION_ID = "hermes_main_session" # ID unik untuk agen kamu

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def pull_memory():
    """Mengambil memori terbaru dari Supabase ke lokal VM"""
    response = supabase.table("hermes_memory").select("*").eq("session_id", SESSION_ID).execute()
    if response.data:
        memory_data = response.data[0]["context_data"]
        os.makedirs("memory", exist_ok=True)
        with open("memory/context.json", "w") as f:
            json.dump(memory_data, f, indent=2)
        print("Memori Hermes Agent berhasil ditarik dari Supabase.")
    else:
        print("Belum ada memori terdaftar. Memulai dari awal.")

def push_memory():
    """Menyimpan memori lokal VM kembali ke Supabase"""
    if os.path.exists("memory/context.json"):
        with open("memory/context.json", "r") as f:
            memory_data = json.load(f)
        
        # Upsert: Update jika session_id ada, Insert jika belum
        data = {
            "session_id": SESSION_ID,
            "context_data": memory_data
        }
        supabase.table("hermes_memory").upsert(data, on_conflict="session_id").execute()
        print("Memori Hermes Agent berhasil disimpan ke Supabase.")

if __name__ == "__main__":
    action = sys.argv[1]
    if action == "pull":
        pull_memory()
    elif action == "push":
        push_memory()
