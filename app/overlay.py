"""The original compact map overlay, hosted by the graphical app."""
import ctypes
from ctypes import wintypes
import tkinter as tk
from PIL import Image, ImageTk
from engine import resources

MAP = {'1': ('A',282,158), '2': ('F',166,360), '3': ('D',239,362),
       '4': ('C',383,389), '5': ('E',556,363), '6': ('G',607,258), '7': ('B',531,177)}
COLORS = ['#48e5a2','#55c9ff','#ffc857','#ff6b81','#c99bff','#f7f7f2']
BG = '#101722'


class Overlay:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.withdraw()
        self.window.title('Oracles overlay')
        self.window.configure(bg=BG, borderwidth=0, highlightthickness=0)
        self.window.overrideredirect(True)
        self.window.attributes('-alpha', 0.5)
        self.window.attributes('-topmost', True)
        self.window.geometry('600x330+40+40')
        self.canvas = tk.Canvas(self.window, bg=BG, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)
        panel = tk.Frame(self.window, bg=BG, width=170, borderwidth=0, highlightthickness=0)
        panel.pack(side='left', fill='y')
        panel.pack_propagate(False)
        def label(text, color, size, bold=False):
            widget = tk.Label(panel, text=text, fg=color, bg=BG,
                              font=('Segoe UI',size,'bold' if bold else 'normal'),
                              wraplength=155, justify='left', anchor='nw')
            widget.pack(anchor='w', fill='x')
            return widget
        label('VAULT OF GLASS','#9aaec4',8,True)
        self.title = label('Templar','white',17,True)
        tk.Frame(panel,bg='#2a3949',height=1).pack(fill='x',pady=9)
        label('ORACLE ORDER','#9aaec4',8,True)
        self.order = label('','white',11,True)
        self.status = label('Waiting for oracle sequence…','#d9e2ec',9)
        self.encounter = 'templar'
        self.sequence = []
        self.canvas.bind('<Configure>', lambda _: self.paint(self.encounter,self.sequence))
        self.window.update_idletasks()
        self.apply_click_through()
        self.window.deiconify()
        self.window.after(100,self.apply_click_through)

    def apply_click_through(self):
        user32 = ctypes.windll.user32
        user32.GetWindowLongW.argtypes = [wintypes.HWND,ctypes.c_int]
        user32.GetWindowLongW.restype = ctypes.c_long
        user32.SetWindowLongW.argtypes = [wintypes.HWND,ctypes.c_int,ctypes.c_long]
        user32.SetWindowPos.argtypes = [wintypes.HWND,wintypes.HWND,ctypes.c_int,ctypes.c_int,
                                       ctypes.c_int,ctypes.c_int,wintypes.UINT]
        hwnd = int(self.window.wm_frame(),0)
        # Strip native frame/edge styles as well as Tk's decorations.
        native_style = user32.GetWindowLongW(hwnd,-16)
        user32.SetWindowLongW(hwnd,-16,native_style & ~(0x00C00000 | 0x00040000 | 0x00800000))
        style = user32.GetWindowLongW(hwnd,-20)
        # Transparent hit-testing, layered alpha, and no activation on click.
        user32.SetWindowLongW(hwnd,-20,(style & ~(0x1 | 0x100 | 0x200 | 0x20000)) | 0x20 | 0x80000 | 0x08000000)
        # Windows 11 can otherwise add a compositor border around borderless windows.
        dwm = ctypes.windll.dwmapi
        dwm.DwmSetWindowAttribute.argtypes = [wintypes.HWND,wintypes.DWORD,ctypes.c_void_p,wintypes.DWORD]
        for attribute,value in ((34,0xFFFFFFFE),(33,1),(2,1)):
            setting = wintypes.DWORD(value)
            dwm.DwmSetWindowAttribute(hwnd,attribute,ctypes.byref(setting),ctypes.sizeof(setting))
        user32.SetWindowPos(hwnd,wintypes.HWND(-1),40,40,600,330,0x10 | 0x20 | 0x40)

    def destroy(self):
        self.window.destroy()

    def paint(self, encounter, sequence):
        self.encounter, self.sequence = encounter,list(sequence)
        self.title.config(text=encounter.title())
        filename = 'VaultOfGlass_Templar.png' if encounter == 'templar' else 'VaultOfGlass_Atheon.png'
        image = Image.open(resources()/filename).convert('RGB')
        width,height = image.size
        image.thumbnail((max(1,self.canvas.winfo_width()),max(1,self.canvas.winfo_height())))
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.delete('all')
        self.canvas.create_image(0,0,anchor='nw',image=self.photo)
        points = [(MAP[n][1]*image.width/width,MAP[n][2]*image.height/height) for n in sequence] if encounter=='templar' else []
        for a,b in zip(points,points[1:]):
            self.canvas.create_line(*a,*b,fill='white',width=2,arrow=tk.LAST)
        scale=image.width/width
        for i,(x,y) in enumerate(points):
            color=COLORS[i%len(COLORS)]
            r=max(10,int(23*scale))
            self.canvas.create_oval(x-r,y-r,x+r,y+r,fill=BG,outline=color,width=2)
            self.canvas.create_text(x,y-2*scale,text=sequence[i],fill='white',font=('Segoe UI',max(8,int(17*scale)),'bold'))
            badge=max(11,int(22*scale));offset=max(6,int(12*scale))
            self.canvas.create_oval(x+offset,y+offset,x+offset+badge,y+offset+badge,fill=color,outline=BG)
            self.canvas.create_text(x+offset+badge/2,y+offset+badge/2,text=str(i+1),fill=BG,font=('Segoe UI',max(6,int(9*scale)),'bold'))
        self.order.config(text='  →  '.join(f'{i+1}. {n} {MAP[n][0]}' if encounter=='templar' else f'{i+1}. {n}' for i,n in enumerate(sequence)))
        self.status.config(text=f'Detected {len(sequence)} oracle'+('s' if len(sequence)!=1 else '.') if sequence else 'Waiting for oracle sequence…')
