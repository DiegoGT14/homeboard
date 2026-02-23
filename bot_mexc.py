import os
from dotenv import load_dotenv
load_dotenv()

# Y cambia las variables de configuración por estas:
TOKEN_TELEGRAM = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
import requests
import time
from datetime import datetime

# === CONFIGURACIÓN ===
# Sustituye con tus datos reales entre las comillas
TOKEN_TELEGRAM = "8116527942:AAE1Rw-0zjIwTmKiwcdrvvvk7U-BXuxv0_I"
CHAT_ID = "8269708346"

class MEXCObserver:
    def __init__(self):
        self.url = "https://api.mexc.com"
        self.known_symbols = set()
        self.first_run = True
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.tele_url = f"https://api.telegram.org{TOKEN_TELEGRAM}/sendMessage"

    def send_telegram_msg(self, message):
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        try:
            requests.post(self.tele_url, json=payload, timeout=10)
        except:
            pass

    def get_all_symbols(self):
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Escaneando MEXC...")
            res = requests.get(self.url, headers=self.headers, timeout=15)
            if res.status_code == 200:
                data = res.json()
                return {item['symbol'] for item in data['symbols'] if item['symbol'].endswith('USDT')}
            return set()
        except Exception as e:
            print(f"Error de red: {e}")
            return set()

    def run(self):
        print("--- MONITOR MEXC INICIADO ---")
        while True:
            current_symbols = self.get_all_symbols()
            if not current_symbols:
                time.sleep(30)
                continue

            if self.first_run:
                self.known_symbols = current_symbols
                self.first_run = False
                print(f"✅ Vigilando {len(self.known_symbols)} pares.")
            else:
                new_listings = current_symbols - self.known_symbols
                if new_listings:
                    for token in new_listings:
                        msg = f"🔔 *NUEVO LISTADO MEXC*\nToken: `{token}`"
                        print(f"🚀 {token}")
                        self.send_telegram_msg(msg)
                    self.known_symbols.update(new_listings)
            time.sleep(30)

if __name__ == "__main__":
    observer = MEXCObserver()
    observer.run()

