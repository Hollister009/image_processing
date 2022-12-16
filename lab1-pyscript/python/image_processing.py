from js import document, window, console, confirm, Object, Uint8Array, File
from pyodide.ffi import create_proxy, to_js
from PIL import Image
import pathlib
import io
import asyncio

root = document.getElementById('root')
fileInput = document.getElementById('file')
openButton = document.getElementById('openButton')
saveButton = document.getElementById('saveButton')
previewArea = document.getElementById('previewArea')
widthField = document.getElementById('width')
heightField = document.getElementById('height')
aspectRatio = document.getElementById('ratio')
original_image = document.getElementById('originalImage')

target_file = None
pillow_image = None
original_width_to_height_ratio = 0


async def open_file(x):
    fileInput.click()


async def image_load(x):
    global original_width_to_height_ratio
    global original_image
    widthField.value = original_image.naturalWidth
    heightField.value = original_image.naturalHeight
    original_width_to_height_ratio = original_image.naturalWidth / \
        original_image.naturalHeight


load_event = create_proxy(image_load)


async def process_file(event):
    global original_image
    global target_file
    file_list = event.target.files
    target_file = file_list.item(0)

    # File might not be passed!
    if not target_file:
        return

    original_image.removeEventListener('load', load_event)

    new_image = document.createElement('img')
    new_image.setAttribute('id', 'originalImage')
    new_image.setAttribute('src', window.URL.createObjectURL(target_file))
    original_image = new_image
    original_image.addEventListener('load', load_event)

    previewArea.innerHTML = ''
    previewArea.appendChild(new_image)


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


def convert_to_file():
    # Convert Pillow object array back into File type that createObjectURL will take
    my_stream = io.BytesIO()
    format = pathlib.Path(target_file.name).suffix[1:].upper()
    format = 'JPEG' if format == 'JPG' else format
    pillow_image.save(my_stream, format=format)

    # Create a JS File object with our data and the proper mime type
    return File.new([Uint8Array.new(my_stream.getvalue())], target_file.name, {type: f'image/{format.lower()}'})


async def save_file(x):
    if not target_file or not pillow_image:
        return

    converted_image = convert_to_file()

    if not hasattr(window, 'showSaveFilePicker'):
        await save_file_fallback(converted_image)
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


async def width_change(event):
    if not target_file:
      return

    save_aspect = aspectRatio.checked
    width_value = int(event.target.value)
    height_value = round(width_value /
                         original_width_to_height_ratio) if save_aspect else int(heightField.value)

    await resize(width_value, height_value)


async def height_change(event):
    if not target_file:
      return

    save_aspect = aspectRatio.checked
    height_value = int(event.target.value)
    width_value = round(height_value *
                        original_width_to_height_ratio) if save_aspect else int(widthField.value)

    await resize(width_value, height_value)


async def resize(width, height):
    global pillow_image
    widthField.value = width
    heightField.value = height

    array_buf = Uint8Array.new(await target_file.arrayBuffer())
    # BytesIO wants a bytes-like object, so convert to bytearray first
    bytes_list = bytearray(array_buf)
    my_bytes = io.BytesIO(bytes_list)

    # Create PIL image from np array
    pillow_image = Image.open(my_bytes).resize((width, height))

    # Log some of the image data for testing
    console.log(
        f"{pillow_image.format= } {pillow_image.width= } {pillow_image.height= }")


def main():
    # Create a Python proxy for the callback function
    open_event = create_proxy(open_file)
    save_event = create_proxy(save_file)
    file_event = create_proxy(process_file)
    width_event = create_proxy(width_change)
    height_event = create_proxy(height_change)

    openButton.addEventListener('click', open_event)
    saveButton.addEventListener('click', save_event)
    fileInput.addEventListener('change', file_event)
    widthField.addEventListener('change', width_event)
    widthField.addEventListener('input', width_event)
    heightField.addEventListener('change', height_event)
    heightField.addEventListener('input', height_event)


main()
