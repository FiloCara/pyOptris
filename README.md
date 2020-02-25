# pyOptris

**Warning**: The package is under developement.

This package provide a pythonic interface to the Evocortex libirimager direct binding. 

## Installation Guide

### Windows
- Install the irDirectSDK from the Evocortex website (this package has been tested with libirimager7.2)
- Clone this repository on you local PC
- cd inside the repository
- run `pip install .`

### Linux (Ubuntu 18.04)
- Clone this repository on your local PC
- `cd your/local/path/pyOptris`
- Attach your Optris device to the USB port
- run `bash libirimager_setup` to automacally download and setup the libirimager library.
- run `pip3 install .`

## Troubleshooting
For any libirimager installation problems please refers to the [Evocortex documentation](http://documentation.evocortex.com/libirimager2/html/)

Warning: Gtk-Message: 21:31:44.478: Failed to load module "canberra-gtk-module"
sudo apt install libcanberra-gtk-module libcanberra-gtk3-module

## Examples

The folder provides an example script (example.py). The example needs *OpenCV* installed.

```python
import pyOptris as optris
import cv2

optris.usb_init('config_file.xml')

optris.set_palette(9)

w, h = optris.get_palette_image_size()
print('{} x {}'.format(w, h))

while True:
    frame = optris.get_palette_image(w, h)
    cv2.imshow('IR streaming', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

optris.terminate()
cv2.destroyAllWindows()
```