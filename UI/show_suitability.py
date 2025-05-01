import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class SuitabilityView:
    def __init__(self, parent_frame, controller):
        self.parent = parent_frame
        self.controller = controller
        self.create_widgets()
        
    def create_widgets(self):
        """Create all widgets for the suitability view"""
        # Main container
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            header_frame, 
            text="Crop Suitability Prediction", 
            style='Header.TLabel'
        ).pack(expand=True)
        
        # Content frame
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (form)
        left_panel = ttk.LabelFrame(
            content_frame, 
            text="Soil & Climate Parameters",
            style='Card.TFrame',
            width=350
        )
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Right panel (results)
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create form fields
        self.create_form(left_panel)
        
        # Create results display
        self.create_results_display(right_panel)
        
    def create_form(self, parent):
        """Create the input form fields"""
        form_frame = ttk.Frame(parent, padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields configuration
        fields = [
            ('N', 'Nitrogen (ppm)', '0'),
            ('P', 'Phosphorus (ppm)', '0'),
            ('K', 'Potassium (ppm)', '0'),
            ('temperature', 'Temperature (°C)', '0'),
            ('humidity', 'Humidity (%)', '0'),
            ('ph', 'Soil pH', '6.5'),
            ('rainfall', 'Rainfall (mm)', '0')
        ]
        
        self.entries = {}
        
        for field, label, default in fields:
            row_frame = ttk.Frame(form_frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(
                row_frame, 
                text=label, 
                width=18,
                anchor='e'
            ).pack(side=tk.LEFT, padx=5)
            
            var = tk.StringVar(value=default)
            entry = ttk.Entry(
                row_frame, 
                textvariable=var,
                width=12,
                font=('Arial', 11)
            )
            entry.pack(side=tk.LEFT)
            
            self.entries[field] = var
        
        # Prediction button
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(
            btn_frame,
            text="Predict Suitable Crops",
            style='Accent.TButton',
            command=self.on_predict,
            width=20
        ).pack(pady=10, ipady=5)
        
    def create_results_display(self, parent):
        """Create the results display area"""
        results_frame = ttk.LabelFrame(
            parent,
            text="Prediction Results",
            style='Card.TFrame'
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = tk.Text(
            results_frame,
            wrap=tk.WORD,
            height=12,
            font=('Arial', 11),
            bg="white",
            padx=10,
            pady=10,
            relief="flat",
            borderwidth=0
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initial placeholder text
        self.results_text.insert(tk.END, "Enter soil and climate parameters then click 'Predict'")
        self.results_text.config(state=tk.DISABLED)
        
        # Configure tags for formatting
        self.results_text.tag_configure("header", font=('Arial', 11, 'bold'))
        self.results_text.tag_configure("highlight", foreground="#3a7d44", font=('Arial', 11, 'bold'))
        
    def on_predict(self):
        """Handle predict button click"""
        # Get all values from the form
        params = {field: var.get() for field, var in self.entries.items()}
        
        # Validate inputs
        try:
            validated_params = {}
            for field, value in params.items():
                validated_params[field] = float(value)
            
            # Call controller to process prediction
            self.controller.predict(validated_params)
            
        except ValueError:
            self.show_message("Please enter valid numbers for all fields", "error")
    
    def show_results(self, predictions):
        """Display the prediction results"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        if not predictions:
            self.results_text.insert(tk.END, "No suitable crops found for the given parameters.")
        else:
            self.results_text.insert(tk.END, "Most Suitable Crops:\n", "header")
            self.results_text.insert(tk.END, "\n")
            
            for crop, score in predictions.items():
                self.results_text.insert(tk.END, f"• {crop}: ", "highlight")
                self.results_text.insert(tk.END, f"{score:.1f}%\n")
            
            self.results_text.insert(tk.END, "\n")
            self.results_text.insert(tk.END, "Recommendations:\n", "header")
            self.results_text.insert(tk.END, "\n")
            self.results_text.insert(tk.END, "1. Select crops with highest suitability scores\n")
            self.results_text.insert(tk.END, "2. Consider crop rotation for soil health\n")
            self.results_text.insert(tk.END, "3. Consult local agricultural experts\n")
        
        self.results_text.config(state=tk.DISABLED)
    
    def show_message(self, message, msg_type="info"):
        """Show a message in the results area"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        if msg_type == "error":
            self.results_text.insert(tk.END, "Error: ", "highlight")
            self.results_text.insert(tk.END, message)
        else:
            self.results_text.insert(tk.END, message)
        
        self.results_text.config(state=tk.DISABLED)
    
    def clear(self):
        """Clear the view"""
        self.main_frame.pack_forget()
        self.main_frame.destroy()