import pyOptris.direct_binding as optris

DLL_path = "../irDirectSDK/sdk/x64/libirimager.dll"
optris.load_DLL(DLL_path)

# USB connection initialisation
optris.usb_init('config_file.xml')

w, h = optris.get_thermal_image_size()
print('{} x {}'.format(w, h))

while True:
    # Get the thermal frame (numpy array)
    thermal_frame = optris.get_thermal_image(w, h)
    # Conversion to temperature values are to be performed as follows:
    # t = ((double)data[x] - 1000.0) / 10.0;
    processed_thermal_frame = (thermal_frame - 1000.0) / 10.0 
    print(processed_thermal_frame)

optris.terminate()
