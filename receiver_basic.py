from binascii import unhexlify
from enum import Enum

import Jetson.GPIO as GPIO
import subprocess as sp
import time
import logging
import sys
import signal

input_pin = 18  # BCM pin 18, BOARD pin 12
cam = sl.Camera()  # Initialise Camera


def interrupt_handler(sig, frame):
    print("You've pressed Ctrl+C!")
    # End camera recording
    cam.disable_recording()
    cam.close()
    logging.info("Program ending")
    GPIO.cleanup(input_pin)
    sys.exit(0)


def main():
    logging.basicConfig(filename="receiver.log", level=logging.INFO, format='%(asctime)s %(message)s')
    signal.signal(signal.SIGINT, interrupt_handler)
    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering as in Raspberry Pi

    # set pin as an input pin with initial state
    GPIO.setup(input_pin, GPIO.IN)

    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.VGA
    init.depth_mode = sl.DEPTH_MODE.NONE

    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    path_output = "./videos/{0}".format(time.localtime())
    recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.H264)
    err = cam.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    runtime = sl.RuntimeParameters()

    print("Welcome to the receiver readout")
    print("Camera is recording")
    print("This will print out the receiver values and auto formats it into 2 bit chunks")

    value_array = []
    while True:


if __name__ == '__main__':
    main()