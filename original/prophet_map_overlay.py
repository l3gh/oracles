import ctypes
import os
import queue
import sys
import threading
import tkinter as tk
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "VaultOfGlass_Templar.png"
SEQUENCE = HERE / "sequence.txt"
MAP = {
    "1": ("A", 282, 158),
    "2": ("F", 166, 360),
    "3": ("D", 239, 362),
    "4": ("C", 383, 389),
    "5": ("E", 556, 363),
    "6": ("G", 607, 258),
    "7": ("B", 531, 177),
}
COLORS = ["#48e5a2", "#55c9ff", "#ffc857", "#ff6b81", "#c99bff", "#f7f7f2"]

root = tk.Tk()
root.title("Prophet — Templar Oracle Map")
root.configure(bg="#101722")
root.attributes("-topmost", True)
root.attributes("-alpha", 0.5)
root.overrideredirect(True)

source_image = tk.PhotoImage(file=str(IMAGE))
display_image = source_image
map_scale = 1.0
current_sequence = []
resize_job = None

map_canvas = tk.Canvas(root, width=source_image.width(), height=source_image.height(),
                       bg="#101722", highlightthickness=0)
map_canvas.pack(side="left", fill="both", expand=True, padx=(8, 3), pady=8)
image_item = map_canvas.create_image(0, 0, image=display_image, anchor="nw")

panel = tk.Frame(root, bg="#101722", width=170)
panel.pack(side="left", fill="y", padx=(8, 10), pady=12)
panel.pack_propagate(False)

tk.Label(panel, text="VAULT OF GLASS", fg="#9aaec4", bg="#101722",
         font=("Segoe UI", 8, "bold")).pack(anchor="w")
tk.Label(panel, text="Templar", fg="white", bg="#101722",
         font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(0, 8))
tk.Frame(panel, bg="#2a3949", height=1).pack(fill="x", pady=(0, 9))
tk.Label(panel, text="ORACLE ORDER", fg="#9aaec4", bg="#101722",
         font=("Segoe UI", 8, "bold")).pack(anchor="w")
order = tk.Label(panel, text="", fg="white", bg="#101722", font=("Segoe UI", 11, "bold"),
                 wraplength=155, justify="left", anchor="nw")
order.pack(fill="x", pady=(7, 5))
status = tk.Label(panel, text="Waiting for oracle sequence…", fg="#d9e2ec",
                  bg="#101722", font=("Segoe UI", 9), wraplength=155,
                  justify="left", anchor="nw")
status.pack(fill="x", anchor="w", pady=(4, 0))
tk.Label(panel, text="Ctrl+Shift+←/→ move\nCtrl+Shift+↑/↓ resize\nCtrl+Shift+F12 close",
         fg="#8494a7", bg="#101722", font=("Segoe UI", 8),
         justify="left").pack(side="bottom", anchor="w", pady=(0, 2))


def paint(sequence):
    global current_sequence
    current_sequence = [number for number in sequence if number in MAP]
    map_canvas.delete("dynamic")
    for i in range(len(current_sequence) - 1):
        _, x1, y1 = MAP[current_sequence[i]]
        _, x2, y2 = MAP[current_sequence[i + 1]]
        map_canvas.create_line(x1*map_scale, y1*map_scale, x2*map_scale, y2*map_scale,
                               fill="#ffffff", width=max(2, int(4*map_scale)),
                               arrow=tk.LAST, arrowshape=(8, 10, 4), tags="dynamic")
    for i, number in enumerate(current_sequence):
        letter, x, y = MAP[number]
        x, y = x*map_scale, y*map_scale
        radius = max(10, int(23*map_scale))
        color = COLORS[i % len(COLORS)]
        map_canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="#101722",
                               outline=color, width=max(2, int(4*map_scale)), tags="dynamic")
        map_canvas.create_text(x, y-2*map_scale, text=number, fill="white",
                               font=("Segoe UI", max(8, int(17*map_scale)), "bold"), tags="dynamic")
        badge = max(11, int(22*map_scale))
        offset = max(6, int(12*map_scale))
        map_canvas.create_oval(x+offset, y+offset, x+offset+badge, y+offset+badge,
                               fill=color, outline="#101722", width=1, tags="dynamic")
        map_canvas.create_text(x+offset+badge/2, y+offset+badge/2, text=str(i+1),
                               fill="#101722", font=("Segoe UI", max(6, int(9*map_scale)), "bold"),
                               tags="dynamic")
    if not current_sequence:
        order.config(text="")
        status.config(text="Waiting for oracle sequence…")
        return
    order.config(text="  →  ".join(f"{i+1}. {n} {MAP[n][0]}" for i, n in enumerate(current_sequence)))
    status.config(text=f"Detected {len(current_sequence)} oracle" +
                  ("s" if len(current_sequence) != 1 else "."))


def apply_resize():
    global display_image, map_scale
    canvas_width = max(1, map_canvas.winfo_width())
    canvas_height = max(1, map_canvas.winfo_height())
    requested_scale = min(canvas_width / source_image.width(),
                          canvas_height / source_image.height())
    fraction = Fraction(max(0.2, min(2.0, requested_scale))).limit_denominator(12)
    display_image = source_image.zoom(fraction.numerator).subsample(fraction.denominator)
    map_scale = display_image.width() / source_image.width()
    map_canvas.itemconfigure(image_item, image=display_image)
    map_canvas.configure(scrollregion=(0, 0, display_image.width(), display_image.height()))
    paint(current_sequence)


def schedule_resize(_event=None):
    global resize_job
    if resize_job is not None:
        root.after_cancel(resize_job)
    resize_job = root.after(100, apply_resize)


def apply_click_through():
    """Make this layered window visible but transparent to all mouse hit-testing."""
    try:
        user32 = ctypes.windll.user32
        hwnd_text = root.wm_frame()
        hwnd = int(hwnd_text, 0)
        get_style = user32.GetWindowLongW
        set_style = user32.SetWindowLongW
        get_style.restype = ctypes.c_long
        set_style.restype = ctypes.c_long
        current = get_style(hwnd, -20)  # GWL_EXSTYLE
        click_through_styles = 0x00000020 | 0x00080000 | 0x08000000
        set_style(hwnd, -20, current | click_through_styles)  # transparent, layered, no-activate
        user32.SetWindowPos(hwnd, None, 0, 0, 0, 0,
                            0x0001 | 0x0002 | 0x0004 | 0x0010 | 0x0020)
    except (AttributeError, OSError, ValueError):
        pass


# Global shortcuts keep a click-through overlay manageable without taking focus.
def poll_shortcuts():
    try:
        user32 = ctypes.windll.user32
        ctrl = bool(user32.GetAsyncKeyState(0x11) & 0x8000)
        shift = bool(user32.GetAsyncKeyState(0x10) & 0x8000)
        down = {vk for vk in (0x25, 0x26, 0x27, 0x28, 0x7B)
                if user32.GetAsyncKeyState(vk) & 0x8000}
        if ctrl and shift:
            pressed = down - getattr(root, "_shortcut_keys", set())
            x, y = root.winfo_x(), root.winfo_y()
            width, height = root.winfo_width(), root.winfo_height()
            if 0x7B in pressed:
                root.destroy()
                return
            if 0x25 in pressed:
                root.geometry(f"+{x-20}+{y}")
            if 0x27 in pressed:
                root.geometry(f"+{x+20}+{y}")
            if 0x26 in pressed:
                root.geometry(f"{width+25}x{height+19}+{x}+{y}")
            if 0x28 in pressed:
                root.geometry(f"{max(430,width-25)}x{max(260,height-19)}+{x}+{y}")
            root._shortcut_keys = down
        else:
            root._shortcut_keys = set()
    except (AttributeError, OSError):
        pass
    root.after(80, poll_shortcuts)


# Start at about half the previous window size; keyboard shortcuts can adjust it later.
root.geometry(f"600x330+40+40")
root.bind("<Configure>", schedule_resize)
root.after(400, apply_click_through)
root.after(100, poll_shortcuts)


def poll_sequence():
    try:
        raw = SEQUENCE.read_text(encoding="utf-8").strip()
        paint([part.strip() for part in raw.split("-") if part.strip()])
    except (OSError, UnicodeError):
        pass
    root.after(250, poll_sequence)

command_queue = queue.Queue()


def read_commands():
    for line in sys.stdin:
        command = line.strip().lower()
        if command in {"hide", "show", "clear", "c"}:
            command_queue.put(command)


def poll_commands():
    while True:
        try:
            command = command_queue.get_nowait()
        except queue.Empty:
            break
        if command == "hide":
            root.withdraw()
        elif command == "show":
            root.deiconify()
            root.attributes("-topmost", True)
            root.attributes("-alpha", 0.5)
            root.after(350, apply_click_through)
        elif command in {"clear", "c"}:
            os.system("cls")
            print(INTRO, flush=True)
    root.after(100, poll_commands)


INTRO = "Prophet overlay console: type hide/show, clear or c, then press Enter."
print(INTRO, flush=True)
threading.Thread(target=read_commands, daemon=True).start()
poll_commands()
poll_sequence()
root.mainloop()