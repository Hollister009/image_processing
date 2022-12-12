from js import document, window, console, Object
from pyodide.ffi import create_proxy, to_js
import asyncio

root = document.getElementById('root')
fileInput = document.getElementById('file')
openButton = document.getElementById('openButton')
saveButton = document.getElementById('saveButton')
previewArea = document.getElementById('previewArea')

target_file = None

async def open_file(x):
  fileInput.click()

async def process_file(event):
  global target_file 
  file_list = event.target.files
  target_file = file_list.item(0)

  new_image = document.createElement('img')
  new_image.setAttribute('src', window.URL.createObjectURL(target_file))
  previewArea.innerHTML = ''
  previewArea.appendChild(new_image)

async def save_file_old(file):
  blob = window.URL.createObjectURL(file)
  tag = document.createElement('a')
  tag.href = blob
  tag.download = file.name
  tag.click()

async def save_file(x):
  if not target_file:
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
    await save_file_old(target_file)

def main():
  # Create a Python proxy for the callback function
  open_event = create_proxy(open_file)
  save_event = create_proxy(save_file)
  file_event = create_proxy(process_file)

  openButton.addEventListener('click', open_event)
  saveButton.addEventListener('click', save_event)
  fileInput.addEventListener('change', file_event)
main()
