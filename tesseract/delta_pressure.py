import os
import sys
import re
import tkinter as tk
from PIL import ImageGrab, Image
import pytesseract

# ==============================
# CONFIG TESSERACT LOCAL
# ==============================

base_path = os.path.dirname(sys.executable)
tesseract_path = os.path.join(base_path, "tesseract", "tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# ==============================
# CONFIGURAÇÕES
# ==============================

UPDATE_INTERVAL = 3000
CM_TO_PX = 37.8

WINDOW_WIDTH = int(6.0 * CM_TO_PX)
WINDOW_HEIGHT = int(4.0 * CM_TO_PX)

READ_WIDTH = int(2.5 * CM_TO_PX)
READ_HEIGHT = int(2.7 * CM_TO_PX)

pressao_anterior = None

# ==============================
# FUNÇÃO OCR
# ==============================

def capturar_pressao():
    wx = root.winfo_x()
    wy = root.winfo_y()

    rx = wx + (WINDOW_WIDTH - READ_WIDTH) // 2
    ry = wy + (WINDOW_HEIGHT - READ_HEIGHT) // 2

    bbox = (rx, ry, rx + READ_WIDTH, ry + READ_HEIGHT)

    img = ImageGrab.grab(bbox)
    img = img.convert("L")
    img = img.point(lambda p: 255 if p > 150 else 0)

    texto = pytesseract.image_to_string(
        img,
        config="--psm 6 -c tessedit_char_whitelist=0123456789,."
    )

    numeros = re.findall(r"\d+[,\.]\d+", texto)

    valores_bloqueados = {
        "5000,0", "5000.0",
        "4000,0", "4000.0",
        "0,0", "0.0"
    }

    numeros_filtrados = [
        n for n in numeros
        if n not in valores_bloqueados
    ]

    if numeros_filtrados:
        return numeros_filtrados[0]

    return None


# ==============================
# LOOP ATUALIZAÇÃO
# ==============================

def atualizar():
    global pressao_anterior

    valor = capturar_pressao()

    if valor:
        valor_float = float(valor.replace(",", "."))

        if pressao_anterior is not None:
            delta = valor_float - pressao_anterior
        else:
            delta = 0.0

        pressao_anterior = valor_float

        texto = f"{valor_float:.1f} psi   Δ {delta:+.1f}"
    else:
        texto = "-- psi"

    label_valor.config(text=texto)

    # garante sobreposição contínua
    root.attributes("-topmost", True)

    root.after(UPDATE_INTERVAL, atualizar)


# ==============================
# JANELA
# ==============================

root = tk.Tk()
root.overrideredirect(True)
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg="black")
root.attributes("-topmost", True)

root.wm_attributes("-transparentcolor", "white")

canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black", highlightthickness=0)
canvas.pack()

# Área vazada
x1 = (WINDOW_WIDTH - READ_WIDTH) // 2
y1 = (WINDOW_HEIGHT - READ_HEIGHT) // 2
x2 = x1 + READ_WIDTH
y2 = y1 + READ_HEIGHT

canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="red", width=2)

# ==============================
# LABEL VALOR
# ==============================

label_valor = tk.Label(
    root,
    text="-- psi",
    fg="lime",
    bg="black",
    font=("Arial", 16, "bold")
)
label_valor.place(relx=0.5, rely=0.9, anchor="center")

# ==============================
# BOTÃO X
# ==============================

btn_close = tk.Label(root, text="X", fg="red", bg="black", cursor="hand2")
btn_close.place(relx=0.98, rely=0.02, anchor="ne")
btn_close.bind("<Button-1>", lambda e: root.destroy())

# ==============================
# ARRASTAR JANELA
# ==============================

def iniciar_arrasto(event):
    root.x = event.x
    root.y = event.y

def arrastar(event):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    root.geometry(f"+{x}+{y}")

root.bind("<Button-1>", iniciar_arrasto)
root.bind("<B1-Motion>", arrastar)

# ==============================
# INICIAR
# ==============================

root.after(1000, atualizar)
root.mainloop()