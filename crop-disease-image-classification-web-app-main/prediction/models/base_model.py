from abc import ABC, abstractmethod
from PIL import Image

class BasePlantModel(ABC):
    @abstractmethod
    def predict(self, image_path):
        pass

    @staticmethod
    def load_image(image_path):
        return Image.open(image_path).convert('RGB')