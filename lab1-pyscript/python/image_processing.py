from js import document, window, console, confirm, Object
from pyodide.ffi import create_proxy, to_js
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
        blob = window.URL.createObjectURL(file)
        tag = document.createElement('a')
        tag.href = blob
        tag.download = file.name
        tag.click()


async def save_file(x):
    if not target_file:
        return

    if not hasattr(window, 'showSaveFilePicker'):
        await save_file_fallback(target_file)
        return

    try:
        options = {
            "startIn": "downloads",
            "suggestedName": target_file.name
        }
        file_handle = await window.showSaveFilePicker(Object.fromEntries(to_js(options)))
        file = await file_handle.createWritable()
        await file.write(target_file)
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

    resize(width_value, height_value)


async def height_change(event):
    if not target_file:
      return

    save_aspect = aspectRatio.checked
    height_value = int(event.target.value)
    width_value = round(height_value *
                        original_width_to_height_ratio) if save_aspect else int(widthField.value)

    resize(width_value, height_value)


def resize(width, height):
    widthField.value = width
    heightField.value = height


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
