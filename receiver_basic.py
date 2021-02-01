import Jetson.GPIO as GPIO
import time
import logging
import subprocess
import sys
import signal

input_pin = 18  # BCM pin 18, BOARD pin 12
zed_recorder = subprocess.Popen(['python3', 'zed_record.py'])  # runs the ZED record script


def interrupt_handler(sig, frame):
    print("You've pressed Ctrl+C!")
    logging.info("Program ending")
    zed_recorder.send_signal(signal.SIGTERM)
    GPIO.cleanup(input_pin)
    sys.exit(0)


def main():
    logging.basicConfig(filename="receiver.log", level=logging.INFO, format='%(asctime)s %(message)s')
    signal.signal(signal.SIGINT, interrupt_handler)
    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering as in Raspberry Pi

    # set pin as an input pin with initial state
    GPIO.setup(input_pin, GPIO.IN)

    print("Welcome to the receiver readout")
    print("Camera is recording")
    print("This will print out the receiver values and auto formats it into 2 bit chunks")

    value_array = []
    while True:
        time.sleep(1/60)


if __name__ == '__main__':
    main()