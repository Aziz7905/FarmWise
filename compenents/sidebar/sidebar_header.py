import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class SidebarHeader:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, style='Sidebar.TFrame')
        self.frame.pack(fill=tk.X, pady=(20, 30), padx=10)
        
        try:
            logo_img = Image.open("logo.png").resize((40, 40), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(logo_img)
            ttk.Label(self.frame, image=self.logo_img, style='Sidebar.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        except:
            pass

        ttk.Label(self.frame, text="FarmWise", style='Sidebar.TLabel', 
                 font=('Montserrat', 14, 'bold')).pack(side=tk.LEFT)