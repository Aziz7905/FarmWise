import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
from compenents.sidebar import SidebarButton, SidebarHeader, SidebarFooter

class FarmWiseUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.sidebar_visible = False
        self.sidebar_width = 250
        self.setup_window()
        self.create_styles()
        self.setup_ui()

    def show_detection(self):
        self.clear_content()
        self.current_view = "detection"
        self.setup_detection_view()

    def show_dashboard(self):
        self.clear_content()
        self.current_view = "dashboard"
    
   
    def setup_window(self):
        self.root.title("FarmWise - Agricultural Disease Classifier")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg="#f0f5f0")  # Softer background
        
    def create_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles with left-aligned buttons
        self.style.configure('TFrame', background="#f0f5f0")
        self.style.configure('TLabel', background="#f0f5f0", font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Montserrat', 24, 'bold'), foreground="#3a7d44")
        self.style.configure('TButton', font=('Arial', 11), padding=8, borderwidth=0, anchor='w')  # Left alignment
        self.style.configure('Accent.TButton', background="#5cb85c", foreground="white", anchor='w')
        self.style.configure('Sidebar.TFrame', background="#3a7d44")
        self.style.configure('Sidebar.TLabel', background="#3a7d44", foreground="#e8f4ea", font=('Arial', 11, 'bold'))
        
        # New style for left-aligned sidebar buttons with consistent padding
        self.style.configure('Sidebar.TButton', 
                           background="#3a7d44", 
                           foreground="#e8f4ea", 
                           font=('Arial', 11), 
                           borderwidth=0,
                           padding=(15, 10, 10, 10),  # Left, Top, Right, Bottom padding
                           anchor='w')  # Left alignment
                           
        self.style.map('Sidebar.TButton', 
                      background=[('active', '#4cae4c')],
                      foreground=[('active', '#ffffff')])
        
    def setup_ui(self):
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Hamburger menu button
        self.hamburger_frame = ttk.Frame(self.main_frame, width=50, style='Sidebar.TFrame')
        self.hamburger_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Create the hamburger icon (3 lines)
        self.hamburger_btn = tk.Canvas(self.hamburger_frame, width=30, height=30, 
                                      bg="#3a7d44", highlightthickness=0)
        self.hamburger_btn.pack(pady=20)
        
        # Draw the 3 lines
        self.hamburger_btn.create_line(5, 10, 25, 10, width=2, fill="#e8f4ea")
        self.hamburger_btn.create_line(5, 15, 25, 15, width=2, fill="#e8f4ea")
        self.hamburger_btn.create_line(5, 20, 25, 20, width=2, fill="#e8f4ea")
        
        self.hamburger_btn.bind("<Button-1>", self.toggle_sidebar)
        
        # Create sidebar (initially hidden)
        self.create_sidebar()
        
        # Main content area
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Status bar
        self.create_status_bar()
        
    def create_sidebar(self):
        """Create the sidebar navigation with properly aligned buttons"""
        self.sidebar = ttk.Frame(self.main_frame, width=0, style='Sidebar.TFrame')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        self.sidebar.pack_propagate(False)
        
        # Sidebar header with logo
        self.sidebar_header = ttk.Frame(self.sidebar, style='Sidebar.TFrame')
        self.sidebar_header.pack(fill=tk.X, pady=(20, 30), padx=10)
        
        # Load logo
        try:
            logo_img = Image.open("logo.png").resize((40, 40), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(logo_img)
            ttk.Label(self.sidebar_header, image=self.logo_img, style='Sidebar.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        except:
            pass

        ttk.Label(self.sidebar_header, text="FarmWise", style='Sidebar.TLabel', 
                 font=('Montserrat', 14, 'bold')).pack(side=tk.LEFT)
        
        # Navigation buttons container with consistent padding
        nav_container = ttk.Frame(self.sidebar, style='Sidebar.TFrame')
        nav_container.pack(fill=tk.X, padx=5, pady=10)
        
        nav_buttons = [
            ("Home", "📊", self.controller.show_dashboard),
            ("Disease Detection", "🔍", self.controller.show_detection),
            ("Crop Suitability", "📚", self.controller.show_suitability),
             ("Crop Yield", "📈", self.controller.show_yield),
            ("Crop Rotation Recommendation", "☀️", self.controller.show_rotation),
            ("Market Prices", "💲", self.controller.show_prices),
            ("Settings", "⚙️", self.controller.show_settings)
        ]
        
        for text, icon, command in nav_buttons:
            # Create a frame for each button to ensure consistent alignment
            btn_frame = ttk.Frame(nav_container, style='Sidebar.TFrame')
            btn_frame.pack(fill=tk.X, pady=2)
            
            # Create button with left-aligned text
            btn = ttk.Button(
                btn_frame,
                text=f"  {icon}  {text}",  # Added extra spaces for better icon spacing
                style='Sidebar.TButton',
                command=command
            )
            btn.pack(fill=tk.X, anchor='w')  # Ensure left alignment
            
            # Bind hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.configure(style='Sidebar.TButton'))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(style='Sidebar.TButton'))
        
        # Footer in sidebar
        footer_container = ttk.Frame(self.sidebar, style='Sidebar.TFrame')
        footer_container.pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=5)
        
        # Help button
        help_frame = ttk.Frame(footer_container, style='Sidebar.TFrame')
        help_frame.pack(fill=tk.X, pady=5)
        ttk.Button(
            help_frame,
            text="  ℹ️  Help",
            style='Sidebar.TButton',
            command=self.controller.show_help
        ).pack(fill=tk.X, anchor='w')
        
        # Contact button
        contact_frame = ttk.Frame(footer_container, style='Sidebar.TFrame')
        contact_frame.pack(fill=tk.X, pady=5)
        ttk.Button(
            contact_frame,
            text="  ✉️  Contact",
            style='Sidebar.TButton',
            command=self.controller.show_contact
        ).pack(fill=tk.X, anchor='w')

    
    def toggle_sidebar(self, event=None):
        """Toggle sidebar with animation"""
        if self.sidebar_visible:
            # Hide sidebar with animation
            for i in range(self.sidebar_width, -1, -10):
                self.sidebar.config(width=i)
                self.sidebar.update()
                time.sleep(0.01)
            self.sidebar_visible = False
        else:
            # Show sidebar with animation
            self.sidebar.pack(side=tk.LEFT, fill=tk.Y)  # Ensure it's packed before animating
            for i in range(0, self.sidebar_width + 1, 10):
                self.sidebar.config(width=i)
                self.sidebar.update()
                time.sleep(0.01)
            self.sidebar_visible = True
    
    def create_status_bar(self):
        """Create the status bar at the bottom"""
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var,
            relief="flat",
            anchor=tk.W,
            font=('Arial', 9),
            background="#e0e0e0",
            foreground="#333333"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def setup_detection_view(self):
        """Setup the disease detection view"""
        self.clear_content()
        
        # Header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="Disease Detection", style='Header.TLabel').pack(expand=True)
        
        # Content area
        content_frame = ttk.Frame(self.content_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (controls)
        left_panel = ttk.Frame(content_frame, width=300, style='Card.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20), ipady=10, ipadx=10)
        
        # Right panel (image and results)
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Control widgets
        ttk.Label(left_panel, text="Select Crop Type", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(15, 5))
        
        # Crop selection dropdown
        self.crop_var = tk.StringVar(value='Grape')
        crop_options = ['Grape', 'Dates', 'Orange', 'Apple']
        
        self.crop_dropdown = ttk.Combobox(
            left_panel,
            textvariable=self.crop_var,
            values=crop_options,
            state='readonly',
            font=('Arial', 11),
            width=18,
            style='TCombobox'
        )
        self.crop_dropdown.pack(fill=tk.X, padx=10, pady=(0, 20))
        
        # Upload button
        self.upload_btn = ttk.Button(
            left_panel, 
            text="📤 Upload Image", 
            command=self.controller.upload_image,
            style='Accent.TButton',
            width=20
        )
        self.upload_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Help section
        help_frame = ttk.Frame(left_panel, style='Card.TFrame')
        help_frame.pack(fill=tk.X, padx=5, pady=20, ipadx=5, ipady=5)
        
        ttk.Label(help_frame, text="How to use:", font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=5, pady=(5, 0))
        ttk.Label(help_frame, text="1. Select your crop type", style='Card.TLabel').pack(anchor=tk.W, padx=5)
        ttk.Label(help_frame, text="2. Upload a clear image", style='Card.TLabel').pack(anchor=tk.W, padx=5)
        ttk.Label(help_frame, text="3. View diagnosis and recommendations", style='Card.TLabel').pack(anchor=tk.W, padx=5, pady=(0, 5))
        
        # Image display area
        self.img_frame = ttk.LabelFrame(right_panel, text="Image Preview", style='Card.TFrame', width=550, height=400)
        self.img_frame.pack_propagate(False)
        self.img_frame.pack(fill=tk.BOTH, expand=True)
        
        self.img_label = ttk.Label(self.img_frame, background="white")
        self.img_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Results area
        self.results_frame = ttk.LabelFrame(right_panel, text="Analysis Results", style='Card.TFrame', height=220)
        self.results_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.result_text = tk.Text(
            self.results_frame, 
            wrap=tk.WORD, 
            height=8, 
            font=('Arial', 11), 
            bg="white", 
            padx=10, 
            pady=10,
            relief="flat",
            borderwidth=0
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.insert(tk.END, "Upload an image to get started...")
        self.result_text.config(state=tk.DISABLED)
    
    def display_image(self, image_path):
        """Display the selected image"""
        img = Image.open(image_path)
        img.thumbnail((550, 550))
        self.current_image = ImageTk.PhotoImage(img)
        self.img_label.config(image=self.current_image)
    
    def show_results(self, disease, confidence, recommendations):
        """Display the analysis results"""
        # Format results
        result_text = f"""=== DIAGNOSIS ===
Disease: {disease}
Confidence: {confidence:.2f}%


=== PESTICIDE RECOMMENDATIONS ===
"""
        
        # Add pesticide recommendations
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                result_text += f"\n{i}. {rec['pesticide']} ({rec['concentration']}) by {rec['company']}\n"
                result_text += f"   Usage: {rec['usage']}\n"
                result_text += f"   Match Score: {rec['score']}%\n"
        else:
            result_text += "\nNo specific pesticide recommendations available for this disease."
        
        # Display results
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)
        
        # Highlight sections
        self.result_text.tag_add("title", "1.0", "1.15")
        self.result_text.tag_add("title", "4.0", "4.26")
        self.result_text.tag_add("title", "7.0", "7.28")
        self.result_text.tag_config("title", font=('Arial', 11, 'bold'))
        
        self.result_text.config(state=tk.DISABLED)
    
    def update_status(self, message):
        """Update the status bar message"""
        self.status_var.set(message)
    


