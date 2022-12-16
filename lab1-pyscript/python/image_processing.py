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

resizer = None
original_width_to_height_ratio = 0


async def open_file(x):
    fileInput.click()


async def image_load(x):
    global original_width_to_height_ratio
    global original_image
    widthField.value = original_image.naturalWidth
    heightField.value = original_image.naturalHeight
    original_width_to_height_ratio = original_image.naturalWidth / original_image.naturalHeight


load_event = create_proxy(image_load)


async def process_file(event):
    global resizer
    global original_image
    file_list = event.target.files
    target_file = file_list.item(0)

    # File might not be passed!
    if not target_file:
        return

    resizer = Resizer(widthField=widthField, heightField=heightField, targetFile=target_file)
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


async def save_file(x):
    if not resizer:
        alert('Please open the image first!')
        return

    converted_image = resizer.convert_to_file()

    if not converted_image:
        alert('Please resize the image!')
        return

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
    if not resizer:
        return

    save_aspect = aspectRatio.checked
    width_value = int(event.target.value)
    height_value = round(width_value /
                         original_width_to_height_ratio) if save_aspect else int(heightField.value)

    await resizer.resize(width_value, height_value)


async def height_change(event):
    if not resizer:
        return

    save_aspect = aspectRatio.checked
    height_value = int(event.target.value)
    width_value = round(height_value *
                        original_width_to_height_ratio) if save_aspect else int(widthField.value)

    await resizer.resize(width_value, height_value)


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
