import os
import cv2
from PIL import Image
from cv2 import dnn_superres

MODELS_DIR = "models"

class SuperResolution:
    def __init__(self, file_path):
        self.file_path = file_path

    def upscale_image(self, scale_factor, model_path):
        sr = dnn_superres.DnnSuperResImpl_create()

        # OpenCV requires an image in numpy array format
        image_np = cv2.imread(self.file_path)

        # Load the model using the model path
        sr.readModel(os.path.join(MODELS_DIR, model_path))

        # Set the model by passing the value and the upsampling ratio
        sr.setModel("espcn", scale_factor) 

        # Upscale the image
        result = sr.upsample(image_np)

        # Convert the numpy array back to a PIL image
        return Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
