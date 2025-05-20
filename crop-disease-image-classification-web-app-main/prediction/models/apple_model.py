import torch
import torchvision.transforms as transforms
from torchvision.models import ResNet50_Weights  
import torch.nn as nn
from .base_model import BasePlantModel

class AppleModel(BasePlantModel):
    CLASSES = ['healthy', 'multiple_diseases', 'rust', 'scab']
    
    def __init__(self, model_path, device=None):
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model(model_path)
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def _load_model(self, model_path):
        # Initialize with proper weights handling
        model = PlantDiseaseModel(num_classes=len(self.CLASSES))
        state_dict = torch.load(model_path, map_location=self.device)
        
        # Handle potential state_dict mismatches
        if 'model_state_dict' in state_dict:  # Common if model was saved with torch.save(model.state_dict())
            state_dict = state_dict['model_state_dict']
            
        model.load_state_dict(state_dict)
        model = model.to(self.device)
        model.eval()
        return model
    
    def predict(self, image_path):
        img = self.load_image(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img = self.transform(img).unsqueeze(0).to(self.device)
        
        with torch.no_grad(), torch.cuda.amp.autocast():  # Add mixed precision if available
            outputs = self.model(img)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, class_idx = torch.max(probabilities, 1)
            
            return {
                'class': self.CLASSES[class_idx.item()],
                'confidence': confidence.item() * 100,
                'all_predictions': {
                    cls: prob.item() * 100 
                    for cls, prob in zip(self.CLASSES, probabilities.squeeze())
                },
                'model_name': 'Apple Disease Classifier'
            }

class PlantDiseaseModel(nn.Module):
    def __init__(self, num_classes=4):
        super(PlantDiseaseModel, self).__init__()
        # Use new weights API instead of pretrained parameter
        self.backbone = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
        
        # Freeze early layers if you want
        for param in self.backbone.parameters():
            param.requires_grad = False
            
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        return self.backbone(x)