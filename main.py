import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from UI.ui_design import FarmWiseUI
from models.grape_model import GrapeModel
from models.dates_model import DatesModel
from models.orange_model import OrangeModel
from models.apple_model import AppleModel
from models.pesticide_model import load_pesticide_model
from models.gesture_controller import HandGestureController
from UI.show_suitability import SuitabilityView
from models.crop_suitability import load_suitability_model
from UI.show_crop_rotation_recommendation import CropRotationView
from UI.show_crop_yield import CropYieldView
from models.crop_yield import CropYieldView

class FarmWiseController:
    def __init__(self, root):
        self.root = root
        self.ui = FarmWiseUI(root, self)
        
        # Suppress TensorFlow info messages
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        
        # Initialize models
        self.grape_model = GrapeModel()
        self.dates_model = DatesModel()
        self.orange_model = OrangeModel()
        self.apple_model = AppleModel()
        self.pesticide_model = load_pesticide_model()
        self.suitability_view = None
        self.suitability_model = load_suitability_model()  
        
        # Initialize gesture controller
        self.gesture_controller = HandGestureController(self)
        self.gesture_controller.start()
        
        # Show detection view by default
        self.show_detection()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        """Clean up resources when closing the application"""
        self.gesture_controller.stop()
        self.root.destroy()
        
    def toggle_sidebar(self):
        """Toggle the sidebar visibility"""
        self.ui.toggle_sidebar()
        
    def navigate_next(self):
        """Navigate to next view"""
        views = ["dashboard", "detection", "guide", "weather", "prices", "settings", "suitability"]
        current_view = self.get_current_view()
        try:
            current_index = views.index(current_view)
            next_index = (current_index + 1) % len(views)
            getattr(self, f"show_{views[next_index]}")()
        except ValueError:
            self.show_detection()
        
    def navigate_previous(self):
        """Navigate to previous view"""
        views = ["dashboard", "detection", "guide", "weather", "prices", "settings", "suitability"]
        current_view = self.get_current_view()
        try:
            current_index = views.index(current_view)
            prev_index = (current_index - 1) % len(views)
            getattr(self, f"show_{views[prev_index]}")()
        except ValueError:
            self.show_detection()
            
    def confirm_selection(self):
        """Handle confirm gesture/action"""
        if self.get_current_view() == "detection":
            self.upload_image()
        elif self.get_current_view() == "suitability":
            self.predict_suitability()
            
    def cancel_selection(self):
        """Handle cancel gesture/action"""
        pass 
        
    def get_current_view(self):
        """Get the current active view"""
        if hasattr(self.ui, 'current_view'):
            return self.ui.current_view
        return "detection"
    
    def show_dashboard(self):
        """Show dashboard view"""
        self.ui.clear_content()
        self.ui.current_view = "dashboard"
        self.ui.setup_dashboard_view()
    
    def show_detection(self):
        """Show disease detection view"""
        self.ui.clear_content()
        self.ui.current_view = "detection"
        self.ui.setup_detection_view()
    
    def show_guide(self):
        """Show pesticide guide view"""
        self.ui.clear_content()
        self.ui.current_view = "guide"
        self.ui.setup_guide_view()
        
    def show_suitability(self):
        """Show crop suitability view"""
        self.ui.clear_content()
        self.ui.current_view = "suitability"
        if not self.suitability_view:
            self.suitability_view = SuitabilityView(self.ui.content_frame, self)
        else:
            self.suitability_view.clear()
            self.suitability_view = SuitabilityView(self.ui.content_frame, self)

    def show_weather(self):
        """Show weather information view"""
        self.ui.clear_content()
        self.ui.current_view = "weather"
        ttk.Label(self.ui.content_frame, text="Weather Information", style='Header.TLabel').pack(pady=20)
    
    def show_prices(self):
        """Show market prices view"""
        self.ui.clear_content()
        self.ui.current_view = "prices"
        ttk.Label(self.ui.content_frame, text="Market Prices", style='Header.TLabel').pack(pady=20)
    
    def show_settings(self):
        """Show settings view"""
        self.ui.clear_content()
        self.ui.current_view = "settings"
        ttk.Label(self.ui.content_frame, text="Settings", style='Header.TLabel').pack(pady=20)
    
    def show_help(self):
        """Show help dialog"""
        messagebox.showinfo("Help", "Contact support@farmwise.com for assistance.")
    
    def show_contact(self):
        """Show contact information dialog"""
        messagebox.showinfo("Contact Us", "Email: contact@farmwise.com\nPhone: +1 (555) 123-4567")
    
    def upload_image(self):
        """Handle image upload and analysis"""
        file_types = [
            ('Image files', '*.jpg *.jpeg *.png'),
            ('All files', '*.*')
        ]
        
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if not file_path:
            return
        
        try:
            # Display image
            self.ui.display_image(file_path)
            
            # Update status
            self.ui.update_status("Analyzing image...")
            self.root.update()
            
            # Get prediction
            crop_type = self.ui.crop_var.get().lower()
            
            if crop_type == 'grape':
                class_name, confidence = self.grape_model.predict(file_path)
            elif crop_type == 'dates':
                class_name, confidence = self.dates_model.predict(file_path)
            elif crop_type == 'orange':
                class_name, confidence = self.orange_model.predict(file_path)
            else:  # apple
                class_name, confidence = self.apple_model.predict(file_path)
            
            # Get recommendations
            recommendations = self.get_pesticide_recommendations(class_name)
            
            # Display results
            self.ui.show_results(class_name, confidence, recommendations)
            self.ui.update_status("Analysis complete")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {str(e)}")
            self.ui.update_status("Error processing image")

    def predict_suitability(self, params=None):
        """Predict suitable crops based on soil/climate parameters"""
        try:
            # If params is not provided, get from view
            if params is None:
                params = {
                    'N': float(self.suitability_view.entries['N'].get()),
                    'P': float(self.suitability_view.entries['P'].get()),
                    'K': float(self.suitability_view.entries['K'].get()),
                    'temperature': float(self.suitability_view.entries['temperature'].get()),
                    'humidity': float(self.suitability_view.entries['humidity'].get()),
                    'ph': float(self.suitability_view.entries['ph'].get()),
                    'rainfall': float(self.suitability_view.entries['rainfall'].get())
                }
            
            # Get predictions from model
            results = self.suitability_model.predict(params)
            
            # Show results
            self.suitability_view.show_results(results)
            
        except ValueError as e:
            self.suitability_view.show_message("Please enter valid numbers for all fields", "error")
        except Exception as e:
            self.suitability_view.show_message(f"An error occurred: {str(e)}", "error")

  
    
    def get_pesticide_recommendations(self, disease_name):
        """Get pesticide recommendations for a given disease"""
        try:
            raw_recommendations = self.pesticide_model.recommend(disease_name)
            
            if raw_recommendations is None:
                return []
                
            if isinstance(raw_recommendations, dict):
                return [self.format_recommendation(raw_recommendations)]
                
            elif isinstance(raw_recommendations, list):
                return [self.format_recommendation(rec) for rec in raw_recommendations]
                
            return []
            
        except Exception as e:
            print(f"Error processing recommendations: {e}")
            return []
    
    def format_recommendation(self, recommendation):
        """Format a pesticide recommendation dictionary"""
        return {
            'pesticide': recommendation.get('SUBSTANCE ACTIVE', 'Unknown'),
            'disease': recommendation.get('USAGE', 'Unknown'),
            'company': recommendation.get('SOCIETE', 'Unknown'),
            'concentration': recommendation.get('CONC.', 'Unknown'),
            'usage': recommendation.get('USAGE', 'Not specified'),
            'score': recommendation.get('score', 0)
        }
    def show_rotation(self):
        self.ui.clear_content()
        self.ui.current_view = "rotation"
        self.rotation_view = CropRotationView(self.ui.content_frame, self)

    def show_yield(self):
        self.ui.clear_content()
        self.ui.current_view = "yield"
        self.yield_view = CropYieldView(self.ui.content_frame, self)
    def show_yield(self):

        self.ui.clear_content()
        self.ui.current_view = "yield"
        self.yield_view = CropYieldView(self.ui.content_frame, self)

if __name__ == "__main__":
    root = tk.Tk()
    app = FarmWiseController(root)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()