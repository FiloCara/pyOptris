import pyOptris as optris
import cv2

optris.usb_init('config_file.xml')

optris.set_palette(9)

w, h = optris.get_thermal_image_size()
print('{} x {}'.format(w, h))

while True:
    frame = optris.get_palette_image(w, h)
    cv2.imshow('IR streaming', frame)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

optris.terminate()
cv2.destroyAllWindows()