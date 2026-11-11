import time
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from engine import Engine, input_devices, resources


class App:
    def __init__(self, root):
        self.root = root
        self.engine = Engine()
        self.started = 0
        self.overlay = None
        self.devices = []
        root.title('Oracles')
        root.geometry('760x650')
        root.minsize(600, 520)
        root.configure(bg='#211e35')
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#211e35')
        style.configure('TLabel', background='#211e35', foreground='#eee9f4', font=('Segoe UI', 11))
        style.configure('TButton', font=('Segoe UI', 11), padding=8)
        frame = ttk.Frame(root, padding=24)
        frame.pack(fill='both', expand=True)
        ttk.Label(frame, text='Oracles', font=('Segoe UI', 25, 'bold')).pack(anchor='w')
        ttk.Label(frame, text='Vault of Glass · Prophet audio detector').pack(anchor='w', pady=(0, 18))
        ttk.Label(frame, text='Encounter').pack(anchor='w')
        self.encounter = ttk.Combobox(frame, state='readonly', values=['Templar', 'Atheon'])
        self.encounter.set('Templar')
        self.encounter.pack(fill='x', pady=(4, 12))
        self.encounter.bind('<<ComboboxSelected>>', self.change_encounter)
        ttk.Label(frame, text='Game audio input').pack(anchor='w')
        row = ttk.Frame(frame)
        row.pack(fill='x', pady=(4, 8))
        self.device = ttk.Combobox(row, state='readonly')
        self.device.pack(side='left', fill='x', expand=True)
        self.refresh_button = ttk.Button(row, text='Refresh', command=self.refresh)
        self.refresh_button.pack(side='left', padx=(8, 0))
        ttk.Label(frame, text='Route game audio to a virtual input, then select it here.', wraplength=660).pack(anchor='w')
        actions = ttk.Frame(frame)
        actions.pack(fill='x', pady=16)
        self.start_button = ttk.Button(actions, text='Start listening', command=self.start)
        self.start_button.pack(side='left')
        self.stop_button = ttk.Button(actions, text='Stop', command=self.stop, state='disabled')
        self.stop_button.pack(side='left', padx=8)
        ttk.Button(actions, text='Show overlay', command=self.show_overlay).pack(side='left')
        self.status = tk.StringVar(value='Choose an encounter and audio input to begin.')
        ttk.Label(frame, textvariable=self.status, wraplength=660).pack(anchor='w')
        self.order = tk.StringVar(value='Waiting for oracle sequence')
        ttk.Label(frame, textvariable=self.order, font=('Segoe UI', 20, 'bold')).pack(anchor='w', pady=14)
        self.canvas = tk.Canvas(frame, bg='#171524', highlightthickness=0, height=240)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Configure>', lambda _: self.paint())
        self.sequence = []
        self.refresh()
        root.protocol('WM_DELETE_WINDOW', self.close)
        root.after(250, self.poll)

    def refresh(self):
        previous = self.device.get()
        try:
            self.devices = input_devices()
            names = [f'{name}  [{i}]' for i, name in self.devices]
            self.device['values'] = names
            if names:
                selected = names.index(previous) if previous in names else next((i for i, s in enumerate(names) if 'CABLE Output' in s), 0)
                self.device.current(selected)
            else:
                self.device.set('')
                self.status.set('No audio inputs found. Connect one, then select Refresh.')
        except Exception as exc:
            self.devices = []
            self.status.set(f'Could not list audio inputs: {exc}')

    def change_encounter(self, _event=None):
        self.sequence = []
        self.order.set('Waiting for oracle sequence')
        self.paint()

    def start(self):
        index = self.device.current()
        if not 0 <= index < len(self.devices):
            messagebox.showerror('Select audio input', 'Choose an available game audio input first.')
            return
        try:
            self.engine.start(self.encounter.get().lower(), self.devices[index][0])
        except Exception as exc:
            messagebox.showerror('Could not start', str(exc))
            return
        self.started = time.monotonic()
        self.sequence = []
        self.order.set('Waiting for oracle sequence')
        self.status.set('Starting detector…')
        self.start_button['state'] = 'disabled'
        self.stop_button['state'] = 'normal'
        self.encounter['state'] = 'disabled'
        self.device['state'] = 'disabled'
        self.refresh_button['state'] = 'disabled'
        self.paint()

    def stop(self):
        self.engine.stop()
        self.start_button['state'] = 'normal'
        self.stop_button['state'] = 'disabled'
        self.encounter['state'] = 'readonly'
        self.device['state'] = 'readonly'
        self.refresh_button['state'] = 'normal'
        self.status.set('Stopped. Choose settings or start again.')

    def poll(self):
        process = self.engine.process
        if process:
            if process.poll() is not None:
                details = self.engine.error()
                self.stop()
                self.status.set('Detector stopped unexpectedly. Check the selected audio input.')
                messagebox.showerror('Detector stopped', 'Try another audio input.\n\n' + details)
            else:
                sequence = self.engine.sequence()
                if sequence != self.sequence:
                    self.sequence = sequence
                    self.order.set(' → '.join(sequence) if sequence else 'Waiting for oracle sequence')
                    self.paint()
                if time.monotonic() - self.started > 20:
                    self.status.set('Detector running. Waiting for game audio.' if not sequence else 'Oracle sequence received.')
        self.root.after(250, self.poll)

    def show_overlay(self):
        if self.overlay and self.overlay.winfo_exists():
            self.overlay.lift()
            return
        self.overlay = tk.Toplevel(self.root)
        self.overlay.title('Oracles · sequence')
        self.overlay.geometry('620x490')
        self.overlay.minsize(420, 340)
        self.overlay.attributes('-topmost', True)
        self.overlay.configure(bg='#211e35')
        ttk.Label(self.overlay, textvariable=self.order, font=('Segoe UI', 24, 'bold'), padding=18).pack()
        ttk.Label(self.overlay, text='Move or resize this window normally. Close it to hide.', padding=8).pack()
        self.overlay_canvas = tk.Canvas(self.overlay, bg='#171524', highlightthickness=0)
        self.overlay_canvas.pack(fill='both', expand=True)
        self.overlay_canvas.bind('<Configure>', lambda _: self.paint())
        self.paint()

    def paint(self):
        encounter = self.encounter.get().lower()
        filename = 'VaultOfGlass_Templar.png' if encounter == 'templar' else 'VaultOfGlass_Atheon.png'
        canvases = [self.canvas]
        if self.overlay and self.overlay.winfo_exists():
            canvases.append(self.overlay_canvas)
        for canvas in canvases:
            image = Image.open(resources() / filename).convert('RGB')
            width, height = image.size
            image.thumbnail((max(1, canvas.winfo_width()), max(1, canvas.winfo_height())))
            canvas.photo = ImageTk.PhotoImage(image)
            canvas.delete('all')
            left = (canvas.winfo_width() - image.width) / 2
            top = (canvas.winfo_height() - image.height) / 2
            canvas.create_image(left, top, anchor='nw', image=canvas.photo)
            if encounter == 'templar':
                # Same coordinates and callout mapping as the supplied overlay.
                locations = {'1': (282,158), '2': (166,360), '3': (239,362),
                             '4': (383,389), '5': (556,363), '6': (607,258), '7': (531,177)}
                points = [(left + locations[n][0]*image.width/width,
                           top + locations[n][1]*image.height/height) for n in self.sequence]
                for a,b in zip(points,points[1:]):
                    canvas.create_line(*a,*b,fill='white',width=2,arrow=tk.LAST)
                for i,(x,y) in enumerate(points):
                    canvas.create_oval(x-12,y-12,x+12,y+12,fill='#211e35',outline='#c5b9e5',width=2)
                    canvas.create_text(x,y,text=str(i+1),fill='white',font=('Segoe UI',10,'bold'))

    def close(self):
        self.engine.stop()
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    App(root)
    root.mainloop()
