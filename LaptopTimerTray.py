import time
import threading
import os
from plyer import notification
import pystray
from PIL import Image, ImageDraw

# --- Fungsi buat ikon tray ---
def create_image():
    img = Image.new('RGB', (64, 64), color="white")
    d = ImageDraw.Draw(img)
    d.ellipse((8, 8, 56, 56), fill="black")
    return img

# --- Fungsi sleep Windows ---
def sleep_windows():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

# --- Timer ---
timer_thread = None
remaining = 0
running = False

def start_timer(hours):
    global timer_thread, remaining, running
    if running:
        notification.notify(title="Timer sudah jalan",
                            message="Stop dulu sebelum set ulang.",
                            timeout=5)
        return
    remaining = hours * 3600
    running = True

    def run():
        global remaining, running
        while running and remaining > 0:
            time.sleep(1)
            remaining -= 1
            if remaining == 300:  # 5 menit lagi
                notification.notify(title="Peringatan",
                                    message="Waktu tinggal 5 menit!",
                                    timeout=10)
        if running and remaining <= 0:
            notification.notify(title="Waktu Habis",
                                message="Laptop akan sleep sekarang.",
                                timeout=5)
            sleep_windows()
        running = False

    timer_thread = threading.Thread(target=run, daemon=True)
    timer_thread.start()

def stop_timer(icon, item):
    global running
    running = False
    notification.notify(title="Timer Dihentikan",
                        message="Hitungan waktu dihentikan.",
                        timeout=5)

def quit_app(icon, item):
    global running
    running = False
    icon.stop()

# --- Menu Tray ---
def setup(icon):
    icon.visible = True

menu = pystray.Menu(
    pystray.MenuItem("1 Jam", lambda icon, item: start_timer(1)),
    pystray.MenuItem("2 Jam", lambda icon, item: start_timer(2)),
    pystray.MenuItem("3 Jam", lambda icon, item: start_timer(3)),
    pystray.MenuItem("Stop Timer", stop_timer),
    pystray.MenuItem("Keluar", quit_app)
)

icon = pystray.Icon("Laptop Timer", create_image(), "Laptop Usage Timer", menu)
icon.run(setup)
