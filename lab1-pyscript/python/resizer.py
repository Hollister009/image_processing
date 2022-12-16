# noinspection PyUnresolvedReferences
from js import Uint8Array, File, console
from PIL import Image
from pathlib import Path
import asyncio
import io


class Resizer:
    def __init__(self, **kwargs):
        self.widthField = kwargs['widthField']
        self.heightField = kwargs['heightField']
        self.target_file = kwargs['targetFile']
        self.pillow_image = None
        self.resized_image = None

    def convert_to_file(self):
        # The original image has not been resized yet
        if not self.resized_image:
            return None

        # Convert Pillow object array back into File type that createObjectURL will take
        my_stream = io.BytesIO()
        _format = Path(self.target_file.name).suffix[1:].upper()
        _format = 'JPEG' if _format == 'JPG' else _format
        self.resized_image.save(my_stream, format=_format)

        # Create a JS File object with our data and the proper mime type
        return File.new([Uint8Array.new(my_stream.getvalue())],
                        self.target_file.name,
                        {type: f'image/{_format.lower()}'})

    async def create_pillow_image(self):
        array_buf = Uint8Array.new(await self.target_file.arrayBuffer())
        # BytesIO wants a bytes-like object, so convert to bytearray first
        bytes_list = bytearray(array_buf)
        img_bytes = io.BytesIO(bytes_list)

        # Create PIL image from np array
        return Image.open(img_bytes)

    async def resize(self, width, height):
        self.widthField.value = width
        self.heightField.value = height

        if not self.pillow_image:
            self.pillow_image = await self.create_pillow_image()

        self.resized_image = self.pillow_image.resize((width, height))

        # Log some image data for testing
        console.log(
            f"{self.resized_image.format= } {self.resized_image.width= } {self.resized_image.height= }")
