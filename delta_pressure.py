import os
import sys
import re
import time
import tkinter as tk
from PIL import ImageGrab, Image
import pytesseract

__author__ = "Lucas Albuquerque"
__version__ = "1.0"

# =====================================================================================
# TESSERACT CONFIG
# =====================================================================================

if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

tesseract_path = os.path.join(base_path, "tesseract", "tesseract.exe")

if not os.path.exists(tesseract_path):
    raise FileNotFoundError("Tesseract executable not found.")

pytesseract.pytesseract.tesseract_cmd = tesseract_path

# =====================================================================================
# CONSTANTS
# =====================================================================================

NUMBER_REGEX = re.compile(r"\d+[,\.]\d+")

BLOCKED_VALUES = {
    "5000,0", "5000.0",
    "4000,0", "4000.0",
    "0,0", "0.0"
}

# =====================================================================================
# COLORS
# =====================================================================================

BG_MAIN = "#E9EDF2"
BG_PANEL = "#D9DEE5"
BORDER_DARK = "#5A6A7A"
BORDER_LIGHT = "#FFFFFF"
TEXT_BLUE = "#003A8F"
TEXT_GREEN = "#008A2E"
TRANSPARENT = "#FF00FF"

# =====================================================================================
# SETTINGS
# =====================================================================================

UPDATE_INTERVAL = 3000
CM_TO_PX = 37.8

WINDOW_WIDTH = int(5.0 * CM_TO_PX)
WINDOW_HEIGHT = int(5.6 * CM_TO_PX)

READ_WIDTH = int(2.5 * CM_TO_PX)
READ_HEIGHT = int(0.8 * CM_TO_PX)

pressure_history = []
start_time = time.time()

# =====================================================================================
# OCR FUNCTION
# =====================================================================================
# This application captures only a small region of the screen to perform OCR on the 
# pressure value displayed by the instrument software.
# No screenshots are saved, and no data is stored, logged, or transmitted externally.

def capture_pressure():

    wx = root.winfo_x()
    wy = root.winfo_y()

    rx = wx + (WINDOW_WIDTH - READ_WIDTH) // 2
    ry = wy + (WINDOW_HEIGHT - READ_HEIGHT) // 2

    bbox = (rx, ry, rx + READ_WIDTH, ry + READ_HEIGHT)

    img = ImageGrab.grab(bbox)
    img = img.convert("L")
    img = img.point(lambda p: 255 if p > 150 else 0)

    try:
        text = pytesseract.image_to_string(
            img,
            config="--psm 6 -c tessedit_char_whitelist=0123456789,."
        )
    except Exception:
        return None

    numbers = NUMBER_REGEX.findall(text)

    filtered_numbers = [
        n for n in numbers
        if n not in BLOCKED_VALUES
    ]

    if filtered_numbers:
        return float(filtered_numbers[0].replace(",", "."))

    return None

# =====================================================================================
# LOOP UPDATE
# =====================================================================================

def update():

    now = time.time()
    value = capture_pressure()

    if value is not None:

        pressure_history.append((now, value))

        limite_60 = now - 60
        while pressure_history and pressure_history[0][0] < limite_60:
            pressure_history.pop(0)

        values_30 = [v for t, v in pressure_history if t >= now - 30]
        values_60 = [v for t, v in pressure_history if t >= now - 60]

        delta_30 = max(values_30) - min(values_30) if values_30 else 0.0
        delta_60 = max(values_60) - min(values_60) if values_60 else 0.0

        label_psi.config(text=f"{value:.1f} psi")
        label_delta_30.config(text=f"Δ30s {delta_30:.1f}")
        label_delta_60.config(text=f"Δ60s {delta_60:.1f}")

    root.attributes("-topmost", True)
    root.after(UPDATE_INTERVAL, update)

# =====================================================================================
# SPLASH SCREEN
# =====================================================================================

def show_splash():

    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg=BG_MAIN)

    width = 260
    height = 120

    x = (splash.winfo_screenwidth() // 2) - (width // 2)
    y = (splash.winfo_screenheight() // 2) - (height // 2)

    splash.geometry(f"{width}x{height}+{x}+{y}")

    frame = tk.Frame(splash, bg=BG_MAIN, bd=2, relief="ridge")
    frame.pack(expand=True, fill="both", padx=5, pady=5)

    tk.Label(
        frame,
        text="Alliance Delta Monitor",
        font=("Segoe UI", 12, "bold"),
        bg=BG_MAIN
    ).pack(pady=(20, 5))

    tk.Label(
        frame,
        text=f"Developed by: {__author__}\nVersion {__version__}",
        font=("Segoe UI", 9),
        bg=BG_MAIN
    ).pack()

    splash.after(2000, splash.destroy)
    splash.mainloop()


show_splash()

# =====================================================================================
# MAIN WINDOW
# =====================================================================================

root = tk.Tk()
root.title("Alliance Delta Monitor")

icon_path = os.path.join(base_path, "delta.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

root.overrideredirect(True)
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg=BG_MAIN)
root.attributes("-topmost", True)

root.wm_attributes("-transparentcolor", TRANSPARENT)

canvas = tk.Canvas(
    root,
    bg=BG_MAIN,
    bd=0,
    highlightthickness=0,
    relief="flat"
)

canvas.place(x=0, y=0, relwidth=1, relheight=1)

# =====================================================================================
# BORDER
# =====================================================================================

canvas.create_rectangle(
    0, 0,
    WINDOW_WIDTH - 1,
    WINDOW_HEIGHT - 1,
    outline=BORDER_DARK,
    width=1
)

canvas.create_line(1, 1, WINDOW_WIDTH - 2, 1, fill=BORDER_LIGHT)
canvas.create_line(1, 1, 1, WINDOW_HEIGHT - 2, fill=BORDER_LIGHT)

canvas.create_line(
    1, WINDOW_HEIGHT - 2,
    WINDOW_WIDTH - 2, WINDOW_HEIGHT - 2,
    fill=BORDER_DARK
)

canvas.create_line(
    WINDOW_WIDTH - 2, 1,
    WINDOW_WIDTH - 2, WINDOW_HEIGHT - 2,
    fill=BORDER_DARK
)

# =====================================================================================
# PSI
# =====================================================================================

label_psi = tk.Label(
    root,
    text="-- psi",
    fg=TEXT_BLUE,
    bg=BG_MAIN,
    font=("Segoe UI", 16, "bold")
)
label_psi.place(relx=0.5, rely=0.2, anchor="center")

# =====================================================================================
# READ AREA
# =====================================================================================

x1 = (WINDOW_WIDTH - READ_WIDTH) // 2
y1 = (WINDOW_HEIGHT - READ_HEIGHT) // 2
x2 = x1 + READ_WIDTH
y2 = y1 + READ_HEIGHT

canvas.create_rectangle(
    x1 - 6, y1 - 6, x2 + 6, y2 + 6,
    fill=BG_MAIN,
    outline="#9AA7B4",
    width=1
)

canvas.create_line(x1 - 1, y1 - 1, x2 + 1, y1 - 1, fill=BORDER_DARK)
canvas.create_line(x1 - 1, y1 - 1, x1 - 1, y2 + 1, fill=BORDER_DARK)

canvas.create_line(x1 - 1, y2 + 1, x2 + 1, y2 + 1, fill=BORDER_LIGHT)
canvas.create_line(x2 + 1, y1 - 1, x2 + 1, y2 + 1, fill=BORDER_LIGHT)

canvas.create_rectangle(
    x1 - 1, y1 - 1, x2 + 1, y2 + 1,
    fill=TRANSPARENT,
    outline="#9AA7B4",
    width=1
)

# =====================================================================================
# TIMER
# =====================================================================================

def format_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def reset_timer():

    global start_time
    global pressure_history

    start_time = time.time()
    pressure_history.clear()

    label_psi.config(text="-- psi")
    label_delta_30.config(text="Δ30s --")
    label_delta_60.config(text="Δ60s --")

def update_timer():

    run_time = int(time.time() - start_time)
    label_timer.config(text=format_time(run_time))

    root.after(200, update_timer)

label_timer = tk.Label(
    root,
    text="00:00:00",
    fg="#404040",
    bg=BG_MAIN,
    font=("Segoe UI", 8, "bold")
)
label_timer.place(relx=0.45, rely=0.70, anchor="center")

btn_reset = tk.Button(
    root,
    text="↺",
    command=reset_timer,
    font=("Segoe UI", 8),
    width=2,
    height=1,
    relief="flat",
    bd=0,
    bg=BG_PANEL,
    activebackground=BG_MAIN,
    highlightthickness=0
)
btn_reset.place(relx=0.68, rely=0.70, anchor="center")

# =====================================================================================
# DELTA
# =====================================================================================

label_delta_30 = tk.Label(
    root,
    text="Δ30s --",
    fg=TEXT_GREEN,
    bg=BG_MAIN,
    font=("Consolas", 11, "bold")
)
label_delta_30.place(relx=0.5, rely=0.82, anchor="center")

label_delta_60 = tk.Label(
    root,
    text="Δ60s --",
    fg=TEXT_GREEN,
    bg=BG_MAIN,
    font=("Consolas", 12, "bold")
)
label_delta_60.place(relx=0.5, rely=0.92, anchor="center")

# =====================================================================================
# CLOSE BUTTON
# =====================================================================================

btn_close = tk.Label(
    root,
    text="X",
    fg="#C00000",
    bg=BG_MAIN,
    cursor="hand2",
    font=("Segoe UI", 9, "bold")
)
btn_close.place(relx=0.98, rely=0.02, anchor="ne")
btn_close.bind("<Button-1>", lambda e: root.destroy())

# =====================================================================================
# DRAG WINDOW
# =====================================================================================

def start_drag(event):
    root.x = event.x
    root.y = event.y

def drag(event):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    root.geometry(f"+{x}+{y}")

root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", drag)

# =====================================================================================
# START
# =====================================================================================

root.after(1000, update)
root.after(200, update_timer)

root.mainloop()