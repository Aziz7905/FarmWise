
import tkinter as tk
from tkinter import ttk

class SidebarButton:
    def __init__(self, parent, text, icon, command):
        self.frame = ttk.Frame(parent, style='Sidebar.TFrame')
        self.frame.pack(fill=tk.X, pady=2)
        
        self.button = ttk.Button(
            self.frame,
            text=f"  {icon}  {text}",
            style='Sidebar.TButton',
            command=command
        )
        self.button.pack(fill=tk.X, anchor='w')
        
        # Bind hover effects
        self.button.bind("<Enter>", self._on_enter)
        self.button.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        self.button.configure(style='Sidebar.TButton')
    
    def _on_leave(self, event):
        self.button.configure(style='Sidebar.TButton')