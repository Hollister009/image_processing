import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2

FILETYPES = (
    ("JPEG files", "*.jpg"),
    ("PNG files", "*.png"),
    ("All files", "*.*")
)

PLACEHOLDER_PATH = "assets/placeholder.jpg"

class ImageResizer(tk.Tk):
    def __init__(self, canvas_width, canvas_height):
        super().__init__()
        self.resizable(0, 0)
        self.title('Image Resizer')

        # Opened image references
        self.original_image = None
        self.resized_image = None
        self.file_path = None

        # Picture frame
        self.picture_frame = ttk.Frame(self)
        
        # Controls frame
        self.controls_frame = ttk.Frame(self)

        # Canvas width & height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Canvas
        self.canvas = tk.Canvas(
            self.picture_frame,
            width=self.canvas_width,
            height=self.canvas_height)
        self.canvas.grid(row=0, column=0)

        # Resolution label
        self.resolution_label = ttk.Label(self.picture_frame, text="Original resolution: -x-\nResized resolution: -x-")
        self.resolution_label.grid(row=1, column=0)

        self.picture_frame.grid(row=0, column=0)
        self.controls_frame.grid(row=1, column=0)
        
        self.set_picture(PLACEHOLDER_PATH)

        # Buttons
        open_button = ttk.Button(self.controls_frame, text='Open')
        open_button['command'] = self.open_picture
        open_button.grid(row=0, column=0)

        save_button = ttk.Button(self.controls_frame, text='Save')
        save_button['command'] = self.save_picture
        save_button.grid(row=0, column=1)

        save_button = ttk.Button(self.controls_frame, text='Resize')
        save_button['command'] = self.resize_picture
        save_button.grid(row=0, column=2)

        save_button = ttk.Button(self.controls_frame, text='Clear')
        save_button['command'] = self.clear_picture
        save_button.grid(row=0, column=3)

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
        self.resized_image = self.update_resolution()
        new_width, new_height = self.resized_image.size
        
        # Update the resolution label
        self.resolution_label.config(text=f"Original resolution: {width}x{height}\nResized resolution: {new_width}x{new_height}")

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

    def set_picture(self, file_path, cache_img=False):
        """ Set the picture to the canvas """
        pil_img = Image.open(file_path)

        if cache_img:
            # Save the image object for future reference
            self.original_image = pil_img
            self.file_path = file_path

        # Resize the picture for canvas
        resized_img = pil_img.resize(
            (self.canvas_width, self.canvas_height),
            Image.ANTIALIAS)

        self.tk_image = ImageTk.PhotoImage(resized_img)

        # Set background image
        self.bg = self.canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.tk_image)
        
    def update_resolution(self):
        if self.original_image is None:
            return
        
        # OpenCV requires an image in numpy array format
        image_np = cv2.imread(self.file_path)

        # Get the new resolution from the user
        new_resolution = simpledialog.askstring("New Resolution", "Enter the new resolution (e.g. 640x480):")

        if new_resolution:
            # Split the new resolution string into width and height
            new_width, new_height = new_resolution.split("x")
            new_width = int(new_width)
            new_height = int(new_height)

            # Resize the image using OpenCV
            image_np = cv2.resize(image_np, (new_width, new_height))

            # Convert the numpy array back to a PIL image
            resized_image = Image.fromarray(image_np)

            return resized_image

if __name__ == '__main__':
    app = ImageResizer(640, 480)
    app.mainloop()