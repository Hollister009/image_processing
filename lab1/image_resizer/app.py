import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from PIL.Image import Resampling

from custom_dialog import CustomDialog
from super_resolution import SuperResolution

FILETYPES = (
    ("JPEG files", "*.jpg"),
    ("PNG files", "*.png"),
    ("All files", "*.*")
)

PLACEHOLDER_PATH = "assets/placeholder.jpg"
HEIGHT_OFFSET = 70
MODELS_DIR =  "models"

class ImageResizer(tk.Tk):
    def __init__(self, canvas_width, canvas_height):
        super().__init__()
        self.title('Image Resizer')
        self.resizable(0, 0)
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.center_window()
        self.setup_ui()

    def center_window(self):
        """ Center the window on the screen """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width - self.canvas_width) / 2)
        y = int((screen_height - self.canvas_height) / 2)
        self.geometry(f"{self.canvas_width}x{self.canvas_height+HEIGHT_OFFSET}+{x}+{y}")

    def setup_ui(self):
        self.setup_picture_frame()
        self.setup_controls_frame()

    def setup_picture_frame(self):
        # Picture frame
        self.picture_frame = ttk.Frame(self)
        self.picture_frame.grid(row=0, column=0)

        # Canvas
        self.canvas = tk.Canvas(
            self.picture_frame,
            width=self.canvas_width,
            height=self.canvas_height)
        self.canvas.grid(row=0, column=0)

        # Resolution label
        self.resolution_label = ttk.Label(
            self.picture_frame,
            text="Original resolution: -x-\nResized resolution: -x-")
        self.resolution_label.grid(row=1, column=0)
        self.set_picture(PLACEHOLDER_PATH)

    def setup_controls_frame(self):
        # Controls frame
        self.controls_frame = ttk.Frame(self)
        self.controls_frame.grid(row=1, column=0)

        # Buttons
        ttk.Button(self.controls_frame, text='Open', command=self.open_picture).grid(row=0, column=0)
        ttk.Button(self.controls_frame, text='Save', command=self.save_picture).grid(row=0, column=1)
        ttk.Button(self.controls_frame, text='Resize', command=self.resize_picture).grid(row=0, column=2)
        ttk.Button(self.controls_frame, text='Clear', command=self.clear_picture).grid(row=0, column=3)

    def open_picture(self):
        """ Open the picture """
        filename = filedialog.askopenfilename(
            initialdir='images/',
            title='Select an image',
            filetypes=FILETYPES)

        if filename:
            self.set_picture(filename, True)

    def save_picture(self):
        """ Save the picture """
        if self.original_image is None:
            messagebox.showinfo("Information", "Please open the image to resize first")
            return

        if self.resized_image is None:
            messagebox.showinfo("Information", "Please resize the image first")
            return

        filename = filedialog.asksaveasfilename(
            initialdir='images/', 
            title='Save as...', 
            filetypes=FILETYPES)

        if filename:
            # Save the resized_image in the given path.
            self.resized_image.save(filename)

    def resize_picture(self):    
        """ Resize the picture """
        if self.original_image is None:
            return

        # Get the size of the image object
        width, height = self.original_image.size

        # Show the input dialog to get new resolution and model path
        input_result = self.show_input_dialog()

        if input_result is not None:
            w, h, model_path = input_result

            print(model_path)

            if model_path:
                sr = SuperResolution(self.file_path)
                scale_factor = int(re.findall(r'\d+', model_path)[0])

                self.resized_image = sr.upscale_image(scale_factor, model_path)
            else:
                self.resized_image = self.update_resolution(w, h)

        try:
            if self.resized_image is not None:
                new_width, new_height = self.resized_image.size
                self.set_picture('', pil_img=self.resized_image)
                self.resolution_label.config(text=f"Original resolution: {width}x{height}\nResized resolution: {new_width}x{new_height}")
        except Exception as e:
            print(f"Error: {e}")

    def clear_picture(self):
        """ Clear the picture """
        # Set the default placeholder image
        self.set_picture(PLACEHOLDER_PATH)
        # Update the resolution label
        self.resolution_label.config(text="Original resolution: -x-\nResized resolution: -x-")
        # Clear the image references
        self.original_image = None
        self.resized_image = None
        self.file_path = None

    def set_picture(self, file_path, cache_img=False, pil_img=None):
        """ Set the picture to the canvas """
        if pil_img is None:
            pil_img = Image.open(file_path)

        if cache_img:
            # Save the image object for future reference
            self.original_image = pil_img
            self.file_path = file_path

            width, height = self.original_image.size
            self.resolution_label.config(text=f"Original resolution: {width}x{height}\nResized resolution: -x-")

        # Resize the picture for canvas
        resized_img = pil_img.resize(
            (self.canvas_width, self.canvas_height),
            Resampling.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(resized_img)

        # Set background image
        self.bg = self.canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.tk_image)
        
    def update_resolution(self, new_width, new_height):
        """ Update the resolution """
        return self.original_image.resize((new_width, new_height), Image.NEAREST)

    def show_input_dialog(self):
        # Define the input fields and options
        model_options = [f for f in os.listdir(MODELS_DIR) if f.endswith(".pb")]
        options = {"Model Path": model_options}

        # Create a CustomDialog instance
        dialog = CustomDialog(self, "Enter new resolution and model path:",
                            fields=[("New Width", 640), ("New Height", 480), ("Model Path", "", "select")],
                            options=options)

        # Show the dialog and wait for user input
        result = dialog.show()

        # Return the result
        if result:
            return int(result["New Width"]), int(result["New Height"]), result["Model Path"]
        else:
            return None

if __name__ == '__main__':
    app = ImageResizer(640, 480)
    app.mainloop()