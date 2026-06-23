"""
自动启动 TradingView 调试模式，等待 CDP 就绪后退出。
供 agent 在拉取 K 线数据前调用。
"""

import subprocess
import sys
import time
import urllib.request
import urllib.error


CDP_URL = "http://localhost:9222/json/version"
TV_EXE = r"C:\Program Files\WindowsApps\TradingView.Desktop_3.2.0.7916_x64__n534cwy3pjxzj\TradingView.exe"
WAIT_SECONDS = 30


def cdp_ready(timeout=2):
    try:
        urllib.request.urlopen(CDP_URL, timeout=timeout)
        return True
    except Exception:
        return False


def main():
    if cdp_ready():
        print("[OK] TradingView CDP already available on port 9222")
        return

    print("[INFO] TradingView not running, starting with debug port 9222...")

    # Kill existing instances
    subprocess.run(["taskkill", "/F", "/IM", "TradingView.exe"],
                   capture_output=True)
    time.sleep(2)

    # Launch TradingView with CDP
    subprocess.Popen(
        [TV_EXE, "--remote-debugging-port=9222", "--remote-allow-origins=*"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait for CDP to become available
    print(f"[INFO] Waiting for TradingView to load (up to {WAIT_SECONDS}s)...")
    for i in range(WAIT_SECONDS):
        time.sleep(1)
        if cdp_ready():
            print(f"[OK] TradingView CDP ready after {i+1}s")
            return
        if i % 5 == 4:
            print(f"[INFO] Still waiting... ({i+1}s)")

    print("[ERROR] TradingView did not become ready in time. Check if it's installed.")
    sys.exit(1)


if __name__ == "__main__":
    main()
