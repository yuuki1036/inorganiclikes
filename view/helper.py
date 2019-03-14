import tkinter as tk
from tkinter import ttk


class Scrollable(ttk.Frame):
    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=600, height=270)
        bar = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.canvas.yview)
        bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas['yscrollcommand'] = bar.set
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH)
        ttk.Frame.__init__(self, master)
        self.inner = self.canvas.create_window(0, 0, window=self, width=self.canvas.cget('width'), anchor=tk.NW)

    def update(self):
        self.update_idletasks()
        self.canvas['scrollregion'] = self.canvas.bbox(self.inner)
