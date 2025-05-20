from ultralytics import YOLO
import os
import cv2

class OliveFruitDetector:
    def __init__(self, model_path, avg_olive_weight=9):  
        self.model = YOLO(model_path)
        self.avg_weight = avg_olive_weight

    def detect(self, image_path, save_dir):
        results = self.model(image_path)
        result = results[0]

      
        plotted_img = result.plot()
        filename = os.path.basename(image_path)
        output_path = os.path.join(save_dir, f"detected_{filename}")
        cv2.imwrite(output_path, cv2.cvtColor(plotted_img, cv2.COLOR_RGB2BGR))

       
        olive_count = len(result.boxes)
        total_weight = olive_count * self.avg_weight 

        return {
            "saved_path": output_path,
            "boxes": olive_count,
            "labels": [self.model.names[int(cls)] for cls in result.boxes.cls],
            "confidences": [float(conf) for conf in result.boxes.conf],
            "estimated_weight_g": total_weight
        }
