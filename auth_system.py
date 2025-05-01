import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk, ImageDraw
import sqlite3
from sqlite3 import Error
import hashlib

class DatabaseManager:
    """Handles all database operations"""
    def __init__(self, db_path):
        self.DB_PATH = db_path
        print(f"Using database at: {self.DB_PATH}")
        self.initialize_database()
    
    def create_connection(self):
        """Create database connection with path verification"""
        try:
            # Verify the directory exists
            db_dir = os.path.dirname(self.DB_PATH)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
                
            conn = sqlite3.connect(self.DB_PATH, timeout=30)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=30000")
            return conn
            
        except Exception as e:
            print(f"Failed to connect to database: {str(e)}")
            return None
    
    def initialize_database(self):
        """Initialize database tables and default user"""
        print(f"\nInitializing database at:\n{self.DB_PATH}")
        
        conn = self.create_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT,
                    farm_size TEXT
                )
            ''')
            
            # Add default user if needed
            cursor.execute("SELECT COUNT(*) FROM users WHERE username='farmer'")
            if cursor.fetchone()[0] == 0:
                hashed_pw = self.hash_password('harvest')
                cursor.execute(
                    "INSERT INTO users (username, password, full_name, farm_size) "
                    "VALUES (?, ?, ?, ?)",
                    ('farmer', hashed_pw, 'Default Farmer', '5 acres')
                )
            
            conn.commit()
            print("Database initialized successfully!")
            return True

        except Exception as e:
            print(f"Database initialization failed: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, hashed_password, user_password):
        """Verify a stored password against one provided by user"""
        return hashed_password == self.hash_password(user_password)
    
    def validate_login(self, username, password):
        """Validate user credentials against the database"""
        conn = self.create_connection()
        if conn is None:
            return None
            
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password, full_name FROM users WHERE username = ?", 
                (username,)
            )
            user = cursor.fetchone()
            
            if user and self.verify_password(user[0], password):
                return user[1]  # Return full_name if credentials are valid
            return None
        except Error as e:
            print(f"Login validation error: {e}")
            return None
        finally:
            conn.close()
    
    def register_user(self, user_data):
        """Register a new user in the database"""
        conn = self.create_connection()
        if conn is None:
            return False
            
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, full_name, farm_size) "
                "VALUES (?, ?, ?, ?)",
                (user_data['username'], 
                 self.hash_password(user_data['password']),
                 user_data['full_name'],
                 user_data['farm_size'])
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists!")
        except Error as e:
            raise Exception(f"Database error: {e}")
        finally:
            conn.close()


class AuthGUI:
    """Handles the authentication user interface"""
    def __init__(self, root, db_manager, on_login_success):
        self.root = root
        self.db = db_manager
        self.on_login_success = on_login_success
        self.setup_main_window()
        self.create_login_frame()
        
    def setup_main_window(self):
        """Configure the main window settings"""
        self.root.title("Farmwise - Login")
        self.root.geometry('450x650')
        self.root.configure(bg='#e8f5e9')
        
        # Create header with logo
        self.create_header()
    
    def create_header(self):
        """Create the application header with logo"""
        header = tk.Frame(self.root, bg='#2e7d32', height=120)
        header.pack(fill='x')
        
        # Load and display logo
        logo_img = self.load_logo()
        logo_label = tk.Label(header, image=logo_img, bg='#2e7d32')
        logo_label.image = logo_img
        logo_label.pack(side='top', pady=10)
    
    @staticmethod
    def load_logo():
        """Load application logo or create a default one"""
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
            img = Image.open(logo_path)
            img = img.resize((200, 200))  
            return ImageTk.PhotoImage(img)
        except Exception:
            # Create a default logo if file not found
            img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse((0, 0, 199, 199), fill='#2e7d32')
            draw.line((100, 40, 100, 160), fill='white', width=8) 
            for y in range(60, 161, 30):  
                draw.line((90, y, 110, y+16), fill='white', width=6)
            return ImageTk.PhotoImage(img)
    
    def create_login_frame(self):
        """Create the login form"""
        self.frame = tk.Frame(
            self.root, bg='white', padx=30, pady=30, 
            highlightbackground='#81c784', highlightthickness=2
        )
        self.frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Application title
        tk.Label(
            self.frame, text="FarmWise", bg='white', fg='#2e7d32', 
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0,20))
        
        # Username field
        self.create_input_field(
            row=1, label="👨‍🌾 Username:", 
            entry_var=tk.StringVar(), is_password=False
        )
        
        # Password field
        self.create_input_field(
            row=2, label="🔑 Password:", 
            entry_var=tk.StringVar(), is_password=True
        )
        
        # Login button
        login_button = tk.Button(
            self.frame, text="Login", bg="#2e7d32", fg="#FFFFFF", 
            font=("Arial", 14, "bold"), command=self.login,
            activebackground="#388e3c", padx=20, pady=8,
            relief='flat', borderwidth=0
        )
        login_button.grid(row=3, column=0, columnspan=2, pady=30, sticky='ew')
        
        # Footer links
        self.create_footer_links()
        
        # Make responsive
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
    
    def create_input_field(self, row, label, entry_var, is_password=False):
        """Helper method to create consistent input fields"""
        tk.Label(
            self.frame, text=label, bg='white', fg='#2e7d32', 
            font=("Arial", 12)
        ).grid(row=row, column=0, sticky='w', pady=(10 if row == 1 else 10))
        
        entry = tk.Entry(
            self.frame, font=("Arial", 12), bg='#f1f8e9', 
            relief='flat', highlightthickness=1, 
            highlightbackground='#a5d6a7',
            show="•" if is_password else None,
            textvariable=entry_var
        )
        entry.grid(row=row, column=1, pady=20, sticky='ew')
        
        # Store references to entry variables
        if "Username" in label:
            self.username_entry = entry_var
        else:
            self.password_entry = entry_var
    
    def create_footer_links(self):
        """Create footer links below login form"""
        footer_frame = tk.Frame(self.frame, bg='white')
        footer_frame.grid(row=4, column=0, columnspan=2)
        
        # Register link
        register_label = tk.Label(
            footer_frame, text="🌱 New farmer? Register", bg='white', 
            fg='#1b5e20', font=("Arial", 10, "underline"),
            cursor="hand2"
        )
        register_label.pack(side='left', padx=5)
        register_label.bind("<Button-1>", lambda e: self.show_registration_form())
        
        tk.Label(footer_frame, text="•", bg='white', fg='gray').pack(side='left')
    
    def login(self):
        """Handle login button click"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Login Failed", "Please enter both username and password")
            return
        
        full_name = self.db.validate_login(username, password)
        
        if full_name:
            messagebox.showinfo(
                "Login Success", 
                f"🌻 Welcome {full_name} to FarmWise!\n"
                f"Access granted to farm dashboard."
            )
            self.root.destroy()  # Close the login window
            self.on_login_success()  # Call the callback to open main app
        else:
            messagebox.showerror(
                "Login Failed", 
                "🚜 Invalid credentials!\n"
                "Try the default: farmer/harvest"
            )
    
    def show_registration_form(self):
        """Create and show the registration form"""
        self.reg_window = tk.Toplevel(self.root)
        self.reg_window.title("New Farmer Registration")
        self.reg_window.geometry('450x600')
        self.reg_window.configure(bg='#e8f5e9')
        
        # Registration frame
        reg_frame = tk.Frame(
            self.reg_window, bg='white', padx=30, pady=30, 
            highlightbackground='#81c784', highlightthickness=2
        )
        reg_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Title
        tk.Label(
            reg_frame, text="New Farmer Registration", bg='white', fg='#2e7d32', 
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0,20))
        
        # Form fields
        fields = [
            ("👨‍🌾 Username:", "username", False),
            ("🔑 Password:", "password", True),
            ("🔑 Confirm Password:", "confirm_password", True),
            ("👤 Full Name:", "full_name", False),
            ("🌾 Farm Size:", "farm_size", False)
        ]
        
        self.reg_vars = {}
        for i, (label, name, is_password) in enumerate(fields, 1):
            self.reg_vars[name] = tk.StringVar()
            self.create_reg_field(reg_frame, i, label, self.reg_vars[name], is_password)
        
        # Register Button
        register_btn = tk.Button(
            reg_frame, text="Register", bg="#2e7d32", fg="#FFFFFF", 
            font=("Arial", 14, "bold"), command=self.register_user,
            activebackground="#388e3c", padx=20, pady=8,
            relief='flat', borderwidth=0
        )
        register_btn.grid(row=len(fields)+1, column=0, columnspan=2, pady=20, sticky='ew')
        
        # Make responsive
        reg_frame.grid_columnconfigure(0, weight=1)
        reg_frame.grid_columnconfigure(1, weight=2)
    
    def create_reg_field(self, frame, row, label, var, is_password):
        """Helper to create registration form fields"""
        tk.Label(
            frame, text=label, bg='white', fg='#2e7d32', 
            font=("Arial", 12)
        ).grid(row=row, column=0, sticky='w', pady=(10 if row == 1 else 10))
        
        entry = tk.Entry(
            frame, font=("Arial", 12), bg='#f1f8e9', 
            relief='flat', highlightthickness=1,
            highlightbackground='#a5d6a7',
            show="•" if is_password else None,
            textvariable=var
        )
        entry.grid(row=row, column=1, pady=10, sticky='ew')
    
    def register_user(self):
        """Handle user registration"""
        user_data = {
            'username': self.reg_vars['username'].get(),
            'password': self.reg_vars['password'].get(),
            'confirm_password': self.reg_vars['confirm_password'].get(),
            'full_name': self.reg_vars['full_name'].get(),
            'farm_size': self.reg_vars['farm_size'].get()
        }
        
        # Validate inputs
        if not all(user_data.values()):
            messagebox.showerror("Registration Error", "All fields are required!")
            return
            
        if user_data['password'] != user_data['confirm_password']:
            messagebox.showerror("Registration Error", "Passwords don't match!")
            return
            
        if len(user_data['password']) < 6:
            messagebox.showerror("Registration Error", "Password must be at least 6 characters!")
            return
        
        try:
            # Remove confirm_password before sending to database
            del user_data['confirm_password']
            
            if self.db.register_user(user_data):
                messagebox.showinfo(
                    "Registration Success", 
                    "🌱 Registration successful!\nYou can now login."
                )
                self.reg_window.destroy()
        except ValueError as e:
            messagebox.showerror("Registration Error", str(e))
        except Exception as e:
            messagebox.showerror("Registration Error", str(e))