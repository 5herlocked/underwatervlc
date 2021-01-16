from binascii import unhexlify
from enum import Enum

import Jetson.GPIO as GPIO
import pyzed.sl as sl
import time
import logging
import sys
import signal

input_pin = 18  # BCM pin 18, BOARD pin 12
cam = sl.Camera()  # Initialise Camera


class Receiving(Enum):
    STARTED = 1
    ENDED = 2
    NEITHER = 3


def convert_gpio_to_value(gpio_value):
    if gpio_value == GPIO.HIGH:
        return 1
    else:
        return 0


def print_bits(bits):
    print()
    i = 0
    internal_counter = 0
    while i < len(bits):
        print(bits[i], end="")
        i += 1
        internal_counter += 1
        if internal_counter == 8:
            print(end=" ")
        if internal_counter == 16:
            print()
            internal_counter = 0
    print()


def interrupt_handler(sig, frame):
    print("You've pressed Ctrl+C!")
    # End camera recording
    cam.disable_recording()
    cam.close()
    logging.info("Program ending")
    GPIO.cleanup(input_pin)
    sys.exit(0)


def text_from_bits(bits, encoding='ascii', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)


def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return unhexlify(hex_string.zfill(n + (n & 1)))


def transmission_state(bits):
    start = True if bits[0] == 1 else False
    if len(bits) == 32:
        for i in bits:
            if start:
                if i != 1:
                    return Receiving.NEITHER
                else:
                    continue
            else:
                if i != 0:
                    return Receiving.NEITHER
                else:
                    continue
        # Checks if the transmission should be starting or ending
        logging.info("Receiving Started" if start else "Receiving Ended")
        return Receiving.STARTED if start else Receiving.ENDED
    else:
        # bits for some reason is other than 32 (really shouldn't be happening)
        return Receiving.NEITHER


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

    receiving = Receiving.NEITHER

    transmission_bits = [0, 0]
    value_array = []
    tracking_window = [0, 0]

    while True:
        cam.grab(runtime)  # Grab frame
        pin_value = convert_gpio_to_value(GPIO.input(input_pin))  # Poll pin value
        value_array.append(pin_value)  # add value to array
        logging.info("Polled: {0}".format(pin_value))  # log added value

        if tracking_window[1] >= 32:
            receiving = transmission_state(value_array[tracking_window[0]:tracking_window[1]])
            tracking_window[0] += 1

        if receiving == Receiving.STARTED or receiving == Receiving.ENDED:
            if receiving == Receiving.STARTED:
                transmission_bits[0] = tracking_window[0]

            if receiving == Receiving.ENDED:
                transmission_bits[1] = tracking_window[1]

                print("Transmission received successfully")
                print("Received Binary Transmission: ")

                print_bits(value_array)
                logging.info("Received: {0}".format(value_array))

                print("Conversion to ASCII: ")
                # value array is at 60 Hz while the transmission is only 30 hz
                # stepping by two to half the bits in the transmission (to set it into 30hz)
                # We'll need to improve this so that we can actually analyse all the bits to ensure
                # maximum accuracy
                ascii_transmission = text_from_bits(value_array[transmission_bits[0]:transmission_bits[1]:2])
                logging.info("Received: {0}".format(ascii_transmission))
                print(ascii_transmission)
                # Clear all instance variables because transmission has ended
                value_array.clear()
                tracking_window = [-1, 0]  # to compensate for tracking_windows[1] += 1
                transmission_bits = [0, 0]

        tracking_window[1] += 1

        time.sleep(1 / 60)  # Effectively a 60Hz polling rate


if __name__ == '__main__':
    main()
