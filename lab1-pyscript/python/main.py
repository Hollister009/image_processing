# noinspection PyUnresolvedReferences
from js import document, window, console, confirm, alert, Object
# noinspection PyUnresolvedReferences
from pyodide.ffi import create_proxy, to_js
import asyncio

from python.resizer import Resizer

root = document.getElementById('root')
fileInput = document.getElementById('file')
openButton = document.getElementById('openButton')
saveButton = document.getElementById('saveButton')
previewArea = document.getElementById('previewArea')
widthField = document.getElementById('width')
heightField = document.getElementById('height')
aspectRatio = document.getElementById('ratio')
original_image = document.getElementById('originalImage')

class Program:
    def __init__(self):
        self.resizer = None
        self.original_width_to_height_ratio = 0

        # Create a Python proxy for the callback function
        self.open_event = create_proxy(self.open_file)
        self.save_event = create_proxy(self.save_file)
        self.file_event = create_proxy(self.process_file)
        self.width_event = create_proxy(self.width_change)
        self.height_event = create_proxy(self.height_change)
        self.load_event = create_proxy(self.image_load)

    async def open_file(self, x):
        fileInput.click()


    async def image_load(self, x):
        global original_image
        widthField.value = original_image.naturalWidth
        heightField.value = original_image.naturalHeight
        self.original_width_to_height_ratio = original_image.naturalWidth / \
            original_image.naturalHeight


    async def process_file(self, event):
        global original_image
        file_list = event.target.files
        target_file = file_list.item(0)

        # File might not be passed!
        if not target_file:
            return

        self.resizer = Resizer(widthField=widthField,
                        heightField=heightField, targetFile=target_file)
        original_image.removeEventListener('load', self.load_event)

        new_image = document.createElement('img')
        new_image.setAttribute('id', 'originalImage')
        new_image.setAttribute('src', window.URL.createObjectURL(target_file))
        original_image = new_image
        original_image.addEventListener('load', self.load_event)

        previewArea.innerHTML = ''
        previewArea.appendChild(new_image)


    @staticmethod
    async def save_file_fallback(file):
        if confirm('Do you confirm to save?'):
            try:
                blob = window.URL.createObjectURL(file)
                tag = document.createElement('a')
                tag.href = blob
                tag.download = file.name
                tag.click()
            except Exception as e:
                console.log('Exception: ' + str(e))


    async def save_file(self, x):
        if not self.resizer:
            alert('Please open the image first!')
            return

        converted_image = self.resizer.convert_to_file()

        if not converted_image:
            alert('Please resize the image!')
            return

        if not hasattr(window, 'showSaveFilePicker'):
            await Program.save_file_fallback(converted_image)
            return

        try:
            options = {
                "startIn": "downloads",
                "suggestedName": converted_image.name
            }
            file_handle = await window.showSaveFilePicker(Object.fromEntries(to_js(options)))
            file = await file_handle.createWritable()
            await file.write(converted_image)
            await file.close()
        except Exception as e:
            console.log('Exception: ' + str(e))


    async def width_change(self, event):
        if not self.resizer:
            return

        save_aspect = aspectRatio.checked
        width_value = int(event.target.value)
        height_value = round(width_value /
                            self.original_width_to_height_ratio) if save_aspect else int(heightField.value)

        await self.resizer.resize(width_value, height_value)


    async def height_change(self, event):
        if not self.resizer:
            return

        save_aspect = aspectRatio.checked
        height_value = int(event.target.value)
        width_value = round(height_value *
                            self.original_width_to_height_ratio) if save_aspect else int(widthField.value)

        await self.resizer.resize(width_value, height_value)

    def main(self):
        openButton.addEventListener('click', self.open_event)
        saveButton.addEventListener('click', self.save_event)
        fileInput.addEventListener('change', self.file_event)
        widthField.addEventListener('change', self.width_event)
        widthField.addEventListener('input', self.width_event)
        heightField.addEventListener('change', self.height_event)
        heightField.addEventListener('input', self.height_event)
