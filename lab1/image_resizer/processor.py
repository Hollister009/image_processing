import cv2
import numpy as np
from PIL import Image
from tkinter import simpledialog

class ImageProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.original_image = Image.open(file_path)
        self.resized_image = self.original_image

    def update_resolution(self, use_super_resolution=True):
        # OpenCV requires an image in numpy array format
        image_np = cv2.imread(self.file_path)

        # Get the new resolution from the user
        new_resolution = simpledialog.askstring("New Resolution", "Enter the new resolution (e.g. 640x480):")

        if new_resolution:
            # Split the new resolution string into width and height
            new_width, new_height = new_resolution.split("x")
            new_width = int(new_width)
            new_height = int(new_height)

            # Use super-resolution algorithm to increase resolution
            if use_super_resolution:
                # Define the path to the pre-trained super-resolution model
                model_path = "path/to/super_resolution_model.pb"

                # Load the model using OpenCV's dnn module
                sr_model = cv2.dnn.readNetFromTensorflow(model_path)

                # Define the input and output sizes for the super-resolution model
                input_size = (image_np.shape[1], image_np.shape[0])
                output_size = (new_width, new_height)

                # Preprocess the input image for the super-resolution model
                input_blob = cv2.dnn.blobFromImage(image_np, scalefactor=1/255.0)

                # Set the input for the super-resolution model
                sr_model.setInput(input_blob)

                # Run the super-resolution model to get the output image
                output_blob = sr_model.forward()
                output_np = np.clip(output_blob[0], 0, 1) * 255
                output_np = output_np.astype(np.uint8)
                output_np = cv2.cvtColor(output_np, cv2.COLOR_BGR2RGB)

                # Resize the super-resolved image to the target resolution using OpenCV
                output_np = cv2.resize(output_np, output_size)

                # Convert the numpy array back to a PIL image
                resized_image = Image.fromarray(output_np)

            # Use regular resizing to change the resolution
            else:
                # Resize the image using OpenCV
                image_np = cv2.resize(image_np, (new_width, new_height))

                # Convert the numpy array back to a PIL image
                resized_image = Image.fromarray(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))

            # Update the stored resized image
            self.resized_image = resized_image

            return resized_image

        else:
            return self.resized_image
