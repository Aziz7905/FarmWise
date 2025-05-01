import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os

class CropYieldView:
    def __init__(self, parent_frame, controller):
        self.controller = controller
        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Current image reference
        self.current_image = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the crop yield prediction interface"""
        # Header
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, 
                 text="Crop Yield Prediction", 
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
        
        # Crop selection
        ttk.Label(left_panel, 
                 text="Select Crop", 
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
        
      
        
        # Get prediction button
        self.predict_btn = ttk.Button(
            left_panel, 
            text="📈 Predict Yield", 
            command=self.predict_yield,
            style='Accent.TButton',
            width=20
        )
        self.predict_btn.pack(fill=tk.X, padx=10, pady=20)
        
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
                 text="2. Select crop and enter soil data", 
                 style='Card.TLabel').pack(anchor=tk.W, padx=5)
        ttk.Label(help_frame, 
                 text="3. Get yield prediction", 
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
            text="Yield Prediction", 
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
        self.result_text.insert(tk.END, "Upload an image and enter parameters to get yield prediction...")
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
    
    def predict_yield(self):
        """Predict crop yield (simulated for now)"""
        crop = self.crop_var.get()
        nitrogen = self.nitrogen_var.get()
        phosphorus = self.phosphorus_var.get()
        potassium = self.potassium_var.get()
        
        # Validate inputs
        try:
            nitrogen = float(nitrogen)
            phosphorus = float(phosphorus)
            potassium = float(potassium)
        except ValueError:
            self.controller.ui.update_status("Please enter valid numbers for soil parameters")
            tk.messagebox.showerror("Error", "Please enter valid numbers for soil parameters")
            return
        
        # Simulate analysis (in a real app, this would call your ML model)
        self.controller.ui.update_status("Analyzing data and predicting yield...")
        
        # Simulate processing delay
        self.frame.after(1500, lambda: self.show_simulated_results(crop, nitrogen, phosphorus, potassium))
    
    def show_simulated_results(self, crop, nitrogen, phosphorus, potassium):
        """Display simulated yield prediction (replace with real model predictions)"""
        # This is simulated data - replace with actual model predictions
        base_yields = {
            'Wheat': 3500,
            'Corn': 9000,
            'Soybean': 2800,
            'Rice': 4500,
            'Barley': 3000,
            'Cotton': 800  # kg per hectare
        }
        
        # Simulate yield calculation based on nutrients
        base_yield = base_yields.get(crop, 2500)
        nutrient_factor = (nitrogen/50 * 0.4) + (phosphorus/30 * 0.3) + (potassium/40 * 0.3)
        predicted_yield = base_yield * nutrient_factor
        
        # Generate recommendations
        recommendations = []
        if nitrogen < 30:
            recommendations.append("Apply nitrogen fertilizer to increase yield potential")
        if phosphorus < 20:
            recommendations.append("Add phosphorus to improve root development")
        if potassium < 30:
            recommendations.append("Supplement potassium to enhance plant health")
        
        if not recommendations:
            recommendations.append("Nutrient levels are optimal for good yield")
        
        # Format results
        result_text = f"""=== CROP YIELD PREDICTION ===
Crop: {crop}
Predicted Yield: {predicted_yield:.1f} kg/ha

=== SOIL ANALYSIS ===
Nitrogen: {nitrogen} kg/ha
Phosphorus: {phosphorus} kg/ha
Potassium: {potassium} kg/ha

=== RECOMMENDATIONS ===
"""
        
        for i, rec in enumerate(recommendations, 1):
            result_text += f"\n{i}. {rec}"
        
        result_text += "\n\n=== OPTIMIZATION TIPS ==="
        result_text += "\n- Regular soil testing improves prediction accuracy"
        result_text += "\n- Proper irrigation can increase yield by 10-20%"
        result_text += "\n- Timely pest control prevents yield losses"
        
        # Display results
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)
        
        # Highlight sections
        self.result_text.tag_add("title", "1.0", "1.22")
        self.result_text.tag_add("title", "4.0", "4.16")
        self.result_text.tag_add("title", "9.0", "9.16")
        self.result_text.tag_add("title", "12.0", "12.19")
        self.result_text.tag_config("title", font=('Arial', 11, 'bold'))
        
        # Highlight yield value
        self.result_text.tag_add("yield", "2.17", f"2.{17+len(str(predicted_yield))}")
        self.result_text.tag_config("yield", foreground="green", font=('Arial', 11, 'bold'))
        
        self.result_text.config(state=tk.DISABLED)
        self.controller.ui.update_status("Yield prediction completed")
    
    def clear(self):
        """Clear the view"""
        self.frame.destroy()