import requests, time, datetime, os

TELE_TOKEN = os.getenv("TELE_TOKEN", "8997419013:AAFgXTYisEW7r-rqMBeVq6o7V8zVa6b0mKk")
BUFFER_TOKEN = os.getenv("BUFFER_TOKEN", "DjZs5JZGVE_N1--HwNjMZPv10dvTT8SdwT1WdrXEqQM")
THREADS_ID = "6ad6ebe0778b240e2f642c21"

HEADERS = {"Authorization": f"Bearer {BUFFER_TOKEN}", "Content-Type": "application/json"}
TELE_URL = f"https://api.telegram.org/bot{TELE_TOKEN}"

def post_threads(text):
    safe = text.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')
    q = f'mutation {{ createPost(input: {{ text: "{safe}", channelId: "{THREADS_ID}", schedulingType: automatic, mode: shareNow }}) {{ ... on PostActionSuccess {{ post {{ id }} }} ... on MutationError {{ message }} }} }}'
    r = requests.post("https://api.buffer.com", headers=HEADERS, json={"query": q}, timeout=25)
    return r.text

def send(chat_id, txt):
    requests.post(f"{TELE_URL}/sendMessage", data={"chat_id": chat_id, "text": txt})

print("=== JOGJALEND V4 - BALAS SEMUA PESAN JALAN ===")
offset=0
while True:
    try:
        res = requests.get(f"{TELE_URL}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=40).json()
        for u in res.get("result", []):
            offset = u["update_id"]+1
            text = u.get("message",{}).get("text","").strip()
            chat_id = u.get("message",{}).get("chat",{}).get("id")
            if not text: continue
            jam = datetime.datetime.now().strftime('%H:%M:%S')
            print(f"[{jam}] {text}")
            if text.lower() in ["/start","/help"]:
                send(chat_id, f"🤖 JOGJALEND V4 AKTIF Jam {jam}\nKirim apapun -> auto ke Threads @jogjalend")
                continue
            if text.lower() == "/status":
                send(chat_id, f"✅ Bot ON Jam {jam} WIB\nID 12:21 6ad6fa33 SUKSES")
                continue
            konten = text.replace("/post ","",1).strip() if text.startswith("/post ") else text
            send(chat_id, f"⏳ [{jam}] PROSES...")
            hasil = post_threads(konten)
            if '"id"' in hasil:
                send(chat_id, f"✅ TERKIRIM! Jam {jam}\n{konten}")
            else:
                send(chat_id, f"❌ GAGAL Jam {jam}\n{hasil[:300]}")
    except Exception as e:
        print(f"Reconnect {e}"); time.sleep(5)
