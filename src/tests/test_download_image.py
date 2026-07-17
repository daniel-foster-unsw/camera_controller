import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.application import Application

app = Application()

#app.initialise()
app.startup()
"""
print("Storage directory:", app.storage.image_directory)
print()

print("Available images:")
for path in app.storage.image_directory.rglob("*.jpg"):
    print(" ", path)

print()
"""

"""
#filename="images\20260706_1035_CAM01\20260706_1035_CAM01_000001.jpg"
filename = "20260718_0915_CAM01_000001.jpg"

print(f"Downloading {filename}...")

transfer = app.download_image(filename)

assert transfer.filename == filename
assert transfer.filesize > 0
assert len(transfer.data) == transfer.filesize

print("✓ DOWNLOAD_IMAGE test passed")
"""

images = list(app.storage.image_directory.rglob("*.jpg"))

assert len(images) > 0, "No images found."

image = images[0]

transfer = app.download_image(image.name)

print("Filename :", transfer.filename)
print("Filesize :", transfer.filesize)
print("Data size:", len(transfer.data))

#assert transfer.filename == image.name
#assert transfer.filesize == len(transfer.data)

assert transfer.filesize > 0, "Image file is empty."
assert len(transfer.data) > 0, "No image data returned."
assert transfer.filesize == len(transfer.data)

print("✓ DOWNLOAD_IMAGE test passed")
