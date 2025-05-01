import torch
import torchvision.transforms as transforms
from torchvision import models
import torch.nn as nn
from PIL import Image

# define APPLE_CLASSES
APPLE_CLASSES = ['healthy', 'multiple_diseases', 'rust', 'scab']

#to define the model architecture 
class PlantDiseaseModel(nn.Module):
    def __init__(self, num_classes=4, pretrained=False):
        super(PlantDiseaseModel, self).__init__()
        self.backbone = models.resnet50(pretrained=pretrained)
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
    
#AppleModel Class designed for using the trained model 

class AppleModel:
    def __init__(self, model_path='assets/my_apple_classifier.pth'):
        self.model = PlantDiseaseModel(num_classes=len(APPLE_CLASSES), pretrained=False)
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.model.eval()

    def predict(self, img_path):
        img = Image.open(img_path).convert('RGB')
        apple_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        img = apple_transform(img).unsqueeze(0)
        with torch.no_grad():
            outputs = self.model(img)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, class_idx = torch.max(probabilities, 1)
        return APPLE_CLASSES[class_idx.item()], confidence.item() * 100
