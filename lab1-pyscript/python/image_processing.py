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

target_file = None


async def open_file(x):
  fileInput.click()


async def image_load(x):
  original_image = document.getElementById('originalImage')
  widthField.value = original_image.naturalWidth
  heightField.value = original_image.naturalHeight

load_event = create_proxy(image_load)


async def process_file(event):
  global target_file
  file_list = event.target.files
  target_file = file_list.item(0)

  # File might not be passed!
  if not target_file:
    return

  original_image = document.getElementById('originalImage')
  original_image.removeEventListener('load', load_event)

  new_image = document.createElement('img')
  new_image.setAttribute('id', 'originalImage')
  new_image.setAttribute('src', window.URL.createObjectURL(target_file))
  new_image.addEventListener('load', load_event)

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
    fileHandle = await window.showSaveFilePicker(Object.fromEntries(to_js(options)))
    file = await fileHandle.createWritable()
    await file.write(target_file)
    await file.close()
  except Exception as e:
    console.log('Exception: ' + str(e))


def main():
  # Create a Python proxy for the callback function
  open_event = create_proxy(open_file)
  save_event = create_proxy(save_file)
  file_event = create_proxy(process_file)

  openButton.addEventListener('click', open_event)
  saveButton.addEventListener('click', save_event)
  fileInput.addEventListener('change', file_event)


main()
