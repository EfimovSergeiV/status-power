import time, os, requests


SERVER = os.getenv("SERVER_URL", "http://your_vps_ip:8000/ping")
PING_INTERVAL = int(os.getenv("PING_INTERVAL", "30"))

while True:
    try:
        requests.get(SERVER, timeout=5)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error pinging server: {e}")

    time.sleep(PING_INTERVAL)