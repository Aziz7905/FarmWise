import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import cv2
from ultralytics import YOLO

class CropYieldView:
    def __init__(self, parent_frame, controller):
        self.controller = controller
        self.frame = ttk.Frame(parent_frame)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Load YOLO model
        self.model = YOLO("assets/oliveDetection3_YOLO11.pt")  # Update with your actual model path
        
        # Current image reference
        self.current_image = None
        self.current_image_path = None
        self.detection_results = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the simplified crop yield prediction interface"""
        # Header
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, 
                 text="Olive Yield Prediction", 
                 style='Header.TLabel').pack(expand=True)
        
        # Main content area
        content_frame = ttk.Frame(self.frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (controls)
        left_panel = ttk.Frame(content_frame, width=200, style='Card.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20), ipady=10, ipadx=10)
        
        # Right panel (image display)
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Upload button
        self.upload_btn = ttk.Button(
            left_panel, 
            text="📤 Upload Image", 
            command=self.upload_image,
            style='Accent.TButton',
            width=15
        )
        self.upload_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Predict button
        self.predict_btn = ttk.Button(
            left_panel, 
            text="📈 Predict Yield", 
            command=self.predict_yield,
            style='Accent.TButton',
            width=15
        )
        self.predict_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Image display area
        self.img_frame = ttk.LabelFrame(
            right_panel, 
            text="Field Image with Yield Prediction", 
            style='Card.TFrame'
        )
        self.img_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.img_label = ttk.Label(self.img_frame, background="white")
        self.img_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status label
        self.status_label = ttk.Label(
            left_panel,
            text="Upload an image to get started",
            wraplength=180,
            style='Card.TLabel'
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=20)
    
    def upload_image(self):
        """Handle image upload"""
        file_types = [('Image files', '*.jpg *.jpeg *.png'), ('All files', '*.*')]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        
        if not file_path:
            return
        
        try:
            # Display original image
            img = Image.open(file_path)
            img.thumbnail((800, 800))
            self.current_image = ImageTk.PhotoImage(img)
            self.current_image_path = file_path
            self.img_label.config(image=self.current_image)
            self.status_label.config(text="Image uploaded. Click 'Predict Yield' to analyze.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def predict_yield(self):
        """Predict olive yield and display results on image"""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please upload an image first")
            return
        
        try:
            # Run detection
            self.status_label.config(text="Analyzing image...")
            self.frame.update()  # Force UI update
            
            results = self.model(self.current_image_path)
            self.detection_results = results[0]
            
            # Count detected olives
            num_olives = len(self.detection_results.boxes)
            
            # Calculate yield (simplified calculation)
            yield_kg = num_olives * 0.005  # Assuming 5g per olive
            
            # Create annotated image
            plotted_img = self.detection_results.plot(line_width=2)
            plotted_img = cv2.cvtColor(plotted_img, cv2.COLOR_BGR2RGB)
            
            # Add yield prediction text to image
            pil_img = Image.fromarray(plotted_img)
            draw = ImageDraw.Draw(pil_img)
            
            # Add yield prediction box
            text = f"Predicted Yield: {yield_kg:.1f} kg\nOlives Detected: {num_olives}"
            draw.rectangle([10, 10, 300, 80], fill="black")
            draw.text((15, 15), text, fill="white", font_size=16)
            
            # Display final image
            pil_img.thumbnail((800, 800))
            self.current_image = ImageTk.PhotoImage(pil_img)
            self.img_label.config(image=self.current_image)
            
            self.status_label.config(text=f"Analysis complete\n{yield_kg:.1f} kg predicted yield")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {str(e)}")
            self.status_label.config(text="Error processing image")
    
    def clear(self):
        """Clear the view"""
        self.frame.destroy()