# pyOptris

This package provides a pythonic interface to the Evocortex libirimager direct binding. 

The project is largely inspired by an old Github project which is no longer available.

## Installation Guide

### Windows
- Download the irDirectSDK from the [Evocortex website](https://evocortex.org/downloads/) (this package has been tested with libirimager7.2)
- Make sure to adapt the 'config_file.xml' to your specific setup. You should pay special attention to the <formatspath> and <calipath> tags because they need to point to the correct locations of the 'Formats.def' and calibration files. The calibration files are provided with the camera.
- `pip install git+https://github.com/FiloCara/pyOptris.git`

### Linux (Ubuntu 18.04)
- Attach your Optris device to the USB port
- run `bash libirimager_setup.sh` to automacally download and setup the libirimager library from the Evocortex website. The script also generate the XML config file. If not working, you can still manually download the SDK from [Evocortex website](https://evocortex.org/downloads/) 
- `pip3 install git+https://github.com/FiloCara/pyOptris.git`

## Troubleshooting
For any libirimager installation problems please refers to the [Evocortex documentation](http://documentation.evocortex.com/libirimager2/html/)

Warning: Gtk-Message: 21:31:44.478: Failed to load module "canberra-gtk-module"
`sudo apt install libcanberra-gtk-module libcanberra-gtk3-module`

## Implemented functions

|direct binding name|node-optris name|description|
|-------------------|----------------|-----------|
|evo_irimager_usb_init|usb_init      |Initializes an IRImager instance connected to this computer via USB|
|evo_irimager_usb_init|tcp_init      |Initializes the TCP connection to the daemon process (non-blocking)|
|evo_irimager_terminate |terminate   |Disconnects the camera, either connected via USB or TCP|
|evo_irimager_get_thermal_image_size|get_thermal_image_size|Accessor to image width and height|
|evo_irimager_get_palette_image_size|get_palette_image_size|Accessor to width and height of false color coded palette image| 
|evo_irimager_get_thermal_image | get_thermal_image |Accessor to thermal image by reference, Conversion to temperature values are to be performed as follows: `t = ((double)data[x] - 1000.0) / 10.0`|
|evo_irimager_get_palette_image | get_palette_image|Accessor to an RGB palette image by reference|
|evo_irimager_get_thermal_palette_image|get_thermal_palette_image|Accessor to an RGB palette image and a thermal image by reference|
|evo_irimager_set_palette|set_palette |Set RGB palette|
|evo_irimager_set_shutter_mode|set_shutter_mode|Sets shutter flag control mode (0:manual, 1:auto)|
|evo_irimager_trigger_shutter_flag|trigger_shutter_flag|Forces a shutter flag cycle|
|evo_irimager_daemon_launch|daemon_launch|Launch TCP daemon|
|evo_irimager_daemon_is_running|daemon_is_running|Check whether daemon is already running|
|evo_irimager_daemon_kill|daemon_kill|Kill TCP daemon|

## Examples

The folder provides two example scripts. 

*/examples/example_palette.py* shows how to get thermal images in RGB format (a colormap is applied over the termperature values). The example needs *OpenCV* installed.

 */examples/example_thermal.py* allows to get the thermal frame with Celsius temperature for each pixel. 

### /utils/example_palette.py 
```python
import cv2

import pyOptris as optris

DLL_path = "../irDirectSDK/sdk/x64/libirimager.dll"
optris.load_DLL(DLL_path)

# USB connection initialisation
optris.usb_init("config_file.xml")

optris.set_palette(9)

w, h = optris.get_palette_image_size()
print("{} x {}".format(w, h))

while True:
    # Get the palette image (RGB image)
    frame = optris.get_palette_image(w, h)
    cv2.imshow("IR streaming", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

optris.terminate()
cv2.destroyAllWindows()
```

### /utils/example_thermal.py 
```python
import pyOptris as optris

DLL_path = "../irDirectSDK/sdk/x64/libirimager.dll"
optris.load_DLL(DLL_path)

# USB connection initialisation
optris.usb_init('config_file.xml')

w, h = optris.get_thermal_image_size()
print('{} x {}'.format(w, h))

# Get the thermal frame (numpy array)
thermal_frame = optris.get_thermal_image(w, h)
# Conversion to temperature values are to be performed as follows:
# t = ((double)data[x] - 1000.0) / 10.0;
processed_thermal_frame = (thermal_frame - 1000.0) / 10.0 
print(processed_thermal_frame)

optris.terminate()
```
