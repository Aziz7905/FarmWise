import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os

class CropRotationView:
    def __init__(self, parent_frame, controller):
        self.controller = controller
        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Current image reference
        self.current_image = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the crop rotation recommendation interface"""
        # Header
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, 
                 text="Crop Rotation Recommendations", 
                 style='Header.TLabel').pack(expand=True)
        
        # Main content area
        content_frame = ttk.Frame(self.frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (controls)
        left_panel = ttk.Frame(content_frame, width=300, style='Card.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20), ipady=10, ipadx=10)
        
        # Right panel (image and results)
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Control widgets
        ttk.Label(left_panel, 
                 text="Upload Field Image", 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(15, 5))
        
        # Upload button
        self.upload_btn = ttk.Button(
            left_panel, 
            text="📤 Upload Image", 
            command=self.upload_image,
            style='Accent.TButton',
            width=20
        )
        self.upload_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Current crop selection
        ttk.Label(left_panel, 
                 text="Current Crop", 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(15, 5))
        
        self.crop_var = tk.StringVar(value='Wheat')
        crop_options = ['Wheat', 'Corn', 'Soybean', 'Rice', 'Barley', 'Cotton']
        
        self.crop_dropdown = ttk.Combobox(
            left_panel,
            textvariable=self.crop_var,
            values=crop_options,
            state='readonly',
            font=('Arial', 11),
            width=18
        )
        self.crop_dropdown.pack(fill=tk.X, padx=10, pady=(0, 20))
        
        # Soil type selection
        ttk.Label(left_panel, 
                 text="Soil Type", 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(15, 5))
        
        self.soil_var = tk.StringVar(value='Loam')
        soil_options = ['Loam', 'Clay', 'Sandy', 'Silt', 'Peat', 'Chalky']
        
        self.soil_dropdown = ttk.Combobox(
            left_panel,
            textvariable=self.soil_var,
            values=soil_options,
            state='readonly',
            font=('Arial', 11),
            width=18
        )
        self.soil_dropdown.pack(fill=tk.X, padx=10, pady=(0, 20))
        
        # Get recommendations button
        self.recommend_btn = ttk.Button(
            left_panel, 
            text="🌱 Get Recommendations", 
            command=self.get_recommendations,
            style='Accent.TButton',
            width=20
        )
        self.recommend_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Help section
        help_frame = ttk.Frame(left_panel, style='Card.TFrame')
        help_frame.pack(fill=tk.X, padx=5, pady=20, ipadx=5, ipady=5)
        
        ttk.Label(help_frame, 
                 text="How to use:", 
                 font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=5, pady=(5, 0))
        ttk.Label(help_frame, 
                 text="1. Upload image of your field", 
                 style='Card.TLabel').pack(anchor=tk.W, padx=5)
        ttk.Label(help_frame, 
                 text="2. Select current crop and soil type", 
                 style='Card.TLabel').pack(anchor=tk.W, padx=5)
        ttk.Label(help_frame, 
                 text="3. Get rotation recommendations", 
                 style='Card.TLabel').pack(anchor=tk.W, padx=5, pady=(0, 5))
        
        # Image display area
        self.img_frame = ttk.LabelFrame(
            right_panel, 
            text="Field Image", 
            style='Card.TFrame', 
            width=550, 
            height=400
        )
        self.img_frame.pack_propagate(False)
        self.img_frame.pack(fill=tk.BOTH, expand=True)
        
        self.img_label = ttk.Label(self.img_frame, background="white")
        self.img_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Results area
        self.results_frame = ttk.LabelFrame(
            right_panel, 
            text="Rotation Recommendations", 
            style='Card.TFrame', 
            height=220
        )
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
        self.result_text.insert(tk.END, "Upload an image and select your current crop to get recommendations...")
        self.result_text.config(state=tk.DISABLED)
    
    def upload_image(self):
        """Handle image upload"""
        file_types = [
            ('Image files', '*.jpg *.jpeg *.png'),
            ('All files', '*.*')
        ]
        
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if not file_path:
            return
        
        try:
            # Display image
            self.display_image(file_path)
            self.controller.ui.update_status("Image uploaded successfully")
        except Exception as e:
            self.controller.ui.update_status("Error loading image")
            tk.messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def display_image(self, image_path):
        """Display the selected image"""
        img = Image.open(image_path)
        img.thumbnail((550, 550))
        self.current_image = ImageTk.PhotoImage(img)
        self.img_label.config(image=self.current_image)
    
    def get_recommendations(self):
        """Get crop rotation recommendations (simulated for now)"""
        current_crop = self.crop_var.get()
        soil_type = self.soil_var.get()
        
        # Simulate analysis (in a real app, this would call your ML model)
        self.controller.ui.update_status("Analyzing field and generating recommendations...")
        
        # Simulate processing delay
        self.frame.after(1500, lambda: self.show_simulated_results(current_crop, soil_type))
    
    def show_simulated_results(self, current_crop, soil_type):
        """Display simulated recommendations (replace with real model predictions)"""
        # This is simulated data - replace with actual model predictions
        recommendations = {
            'Wheat': [
                {'crop': 'Soybean', 'benefit': 'Nitrogen fixation improves soil fertility'},
                {'crop': 'Corn', 'benefit': 'Breaks disease cycles and improves yield'},
                {'crop': 'Canola', 'benefit': 'Helps control weeds and improves soil structure'}
            ],
            'Corn': [
                {'crop': 'Soybean', 'benefit': 'Replenishes soil nitrogen levels'},
                {'crop': 'Wheat', 'benefit': 'Breaks pest cycles and improves soil health'},
                {'crop': 'Alfalfa', 'benefit': 'Deep roots improve soil structure and fertility'}
            ],
            'Soybean': [
                {'crop': 'Corn', 'benefit': 'Utilizes fixed nitrogen efficiently'},
                {'crop': 'Wheat', 'benefit': 'Helps control soybean cyst nematode'},
                {'crop': 'Barley', 'benefit': 'Improves soil organic matter content'}
            ]
        }
        
        # Get recommendations for current crop or default
        crop_recs = recommendations.get(current_crop, [
            {'crop': 'Legume cover crop', 'benefit': 'Improves soil nitrogen levels'},
            {'crop': 'Small grains', 'benefit': 'Breaks pest cycles'},
            {'crop': 'Root crops', 'benefit': 'Improves soil structure'}
        ])
        
        # Format results
        result_text = f"""=== CROP ROTATION RECOMMENDATIONS ===
Current Crop: {current_crop}
Soil Type: {soil_type}

=== RECOMMENDED NEXT CROPS ===
"""
        
        for i, rec in enumerate(crop_recs, 1):
            result_text += f"\n{i}. {rec['crop']}\n"
            result_text += f"   Benefit: {rec['benefit']}\n"
        
        result_text += "\n=== ADDITIONAL TIPS ===\n"
        result_text += "- Rotate crops with different families for best results\n"
        result_text += "- Include cover crops to improve soil health\n"
        result_text += "- Monitor soil nutrients regularly\n"
        
        # Display results
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)
        
        # Highlight sections
        self.result_text.tag_add("title", "1.0", "1.34")
        self.result_text.tag_add("title", "5.0", "5.25")
        self.result_text.tag_add("title", "14.0", "14.22")
        self.result_text.tag_config("title", font=('Arial', 11, 'bold'))
        
        self.result_text.config(state=tk.DISABLED)
        self.controller.ui.update_status("Recommendations generated successfully")
    
    def clear(self):
        """Clear the view"""
        self.frame.destroy()