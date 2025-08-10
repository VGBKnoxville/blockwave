import time
import requests
from collections import deque
import statistics
import sys

# Пары для мониторинга
PAIRS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]

# Длина окна в минутах
WINDOW = 10
API_URL = "https://api.binance.com/api/v3/klines"

def get_volume(pair, interval="1m", limit=1):
    try:
        resp = requests.get(API_URL, params={"symbol": pair, "interval": interval, "limit": limit}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return float(data[-1][5])  # 5-й индекс — объем
    except Exception as e:
        print(f"[ERROR] Не удалось получить данные для {pair}: {e}")
        return None

def monitor():
    history = {pair: deque(maxlen=WINDOW) for pair in PAIRS}
    
    print(f"🌊 BlockWave запущен. Мониторим пары: {', '.join(PAIRS)}")
    while True:
        for pair in PAIRS:
            vol = get_volume(pair)
            if vol is None:
                continue

            history[pair].append(vol)

            if len(history[pair]) == WINDOW:
                avg = statistics.mean(history[pair])
                stdev = statistics.pstdev(history[pair])
                
                if stdev > 0 and vol > avg + 3 * stdev:
                    print(f"🚨 Всплеск объёма {pair}: {vol:.2f} (среднее {avg:.2f}, σ={stdev:.2f})")
        
        time.sleep(60)

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print("\n🛑 Завершено пользователем.")
        sys.exit(0)
