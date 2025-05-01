import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class SidebarFooter:
    def __init__(self, parent, controller):
        self.frame = ttk.Frame(parent, style='Sidebar.TFrame')
        self.frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=5)
        
        # Help button
        self.help_button = ttk.Button(
            self.frame,
            text="  ℹ️  Help",
            style='Sidebar.TButton',
            command=self.show_help
        )
        self.help_button.pack(fill=tk.X, anchor='w', pady=5)
        
        # Contact button
        self.contact_button = ttk.Button(
            self.frame,
            text="  ✉️  Contact",
            style='Sidebar.TButton',
            command=self.show_contact
        )
        self.contact_button.pack(fill=tk.X, anchor='w', pady=5)
        
        self.controller = controller
    
    def show_help(self):
        messagebox.showinfo("Help", "Contact support@farmwise.com for assistance.")
    
    def show_contact(self):
        messagebox.showinfo("Contact Us", "Email: contact@farmwise.com\nPhone: +1 (555) 123-4567")