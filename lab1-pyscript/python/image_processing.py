from js import document, window, console
from pyodide.ffi import create_proxy
import asyncio

root = document.getElementById('root')
fileInput = document.getElementById('file')
openButton = document.getElementById('openButton')
saveButton = document.getElementById('saveButton')
previewArea = document.getElementById('previewArea')

is_save_disabbled = True

async def open_file(x):
  fileInput.click()

async def process_file(event):
  file_list = event.target.files
  first_item = file_list.item(0)

  new_image = document.createElement('img')
  new_image.setAttribute('src', window.URL.createObjectURL(first_item))
  previewArea.innerHTML = ''
  previewArea.appendChild(new_image)

async def save_file(x):
  pass

def main():
  # Create a Python proxy for the callback function
  open_event = create_proxy(open_file)
  save_event = create_proxy(save_file)
  file_event = create_proxy(process_file)

  openButton.addEventListener('click', open_event)
  saveButton.addEventListener('click', save_event)
  fileInput.addEventListener('change', file_event)
main()
