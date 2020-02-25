import cv2
import socket
import time
import argparse
from datetime import datetime
import numpy as np
import pyOptris as optris

class _BaseRecorder:

    def __init__(self, xml_path):

        self.xml_path = xml_path

        optris.usb_init(self.xml_path)
        optris.set_palette(9)

        self.w, self.h = optris.get_thermal_image_size()
        print('{} x {}'.format(self.w, self.h)) 

        assert (self.w > 0) and (self.h > 0), "Camera has not been detected"

        self._remove_garbage()

        self.results = []

    def _remove_garbage(self):
        """
        Remove first 300 frames from streaming, no idea way but they contains some garbage values
        """
        i = 0
        while (i < 300):
            optris.get_thermal_image(self.w, self.h)
            i+=1
        print("Garbage removed")

class ShowRecorder(_BaseRecorder):

    def __init__(self, xml_path):
        super().__init__(xml_path)
    
    def show_frames(self):
        while True:
            frame = optris.get_palette_image(self.w, self.h)
            cv2.imshow('IR streaming', frame)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break

        optris.terminate()
        cv2.destroyAllWindows()


class CSVRecorder(_BaseRecorder):

    def __init__(self, xml_path):
        super().__init__(xml_path)
    
    def grab_pictures(self, wait=1, timeout=60):
        
        start_time = round(time.time(), 1)
        last_time = start_time

        while True:
            if round(time.time() - start_time) <= timeout:
                tic = time.time()
                # get thermal frame
                frame = optris.get_thermal_image(self.w, self.h)
                if (time.time() - last_time) > wait:
                    # Store frame and timestamp to dict
                    d = {"frame":frame, "time":datetime.timestamp(datetime.now())}
                    self.results.append(d)
                    print("Frame grabbed in {} [s]".format(time.time() - tic))
                    last_time = time.time()
            else:
                break   
        optris.terminate()
    
    def save_csv(self, path="./"):
        for i, elem in enumerate(self.results):
            np.savetxt(path + "thermal_IR_{}_{}.csv".format(i, round(elem['time'], 2)),
                 (elem["frame"] - 1000.0) / 10.0, delimiter=';', fmt='%1.2f')

# TODO: to be finished
class TCPRecorder(_BaseRecorder):

    def __init__(self, xml_path, ip):
        super().__init__(xml_path)

        self.ip = ip
        # Define a TCP server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def run(self):
        while True:
            pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-w', "--wait", type=int, default=1)
    parser.add_argument('-to', '--timeout', type=int, default=10)
    parser.add_argument('-p', '--path', type=str, default="./images/")

    args = parser.parse_args()

    instance = CSVRecorder("./config_file.xml")
    instance.grab_pictures(wait=args.wait, timeout=args.timeout)
    instance.save_csv(path=args.path)
