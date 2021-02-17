import logging
import signal
import subprocess
import sys
import time
import getopt

import Jetson.GPIO as GPIO

input_pin = 18  # BCM pin 18, BOARD pin 12
frequency = 1/60  # Predefined frequency
zed_recorder = subprocess.Popen(['python3', 'zed_record.py'])  # runs the ZED record script
value_array = []  # Common memory space for all polled values


def convert_gpio_to_value(gpio_value):
    if gpio_value == GPIO.HIGH:
        return 1
    else:
        return 0


def pretty_bits(bits):
    prettified_bits = ""

    i = 0
    internal_counter = 0
    while i < len(bits):
        prettified_bits += bits[i]
        i += 1
        internal_counter += 1
        if internal_counter == 8:
            prettified_bits += " "
        if internal_counter == 16:
            prettified_bits += "\n"
            internal_counter = 0

    return prettified_bits


def interrupt_handler(sig, frame):
    print("Received Binary Transmission: ")
    print(pretty_bits(value_array))
    print("You've pressed Ctrl+C!")
    logging.info("Received: {0}".format(pretty_bits(value_array)))
    logging.info("Program ending")
    zed_recorder.send_signal(signal.SIGTERM)
    GPIO.cleanup(input_pin)
    sys.exit(0)


def main(argv):
    global input_pin, frequency
    try:
        opts, args = getopt.getopt(argv, "hp:f:", ["pin=", "freq="])
    except getopt.GetoptError:
        print('receiver_basic.py -p <GPIO_Pin> -f <Frequency_for_polling>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('receiver_basic.py -p <GPIO_Pin> -f <Frequency_for_polling>')
            sys.exit()
        elif opt in ('-p', '--pin'):
            input_pin = arg
        elif opt in ('-f', '--freq'):
            frequency = arg

    logging.basicConfig(filename="receiver.log", level=logging.INFO, format='%(asctime)s %(message)s')
    signal.signal(signal.SIGINT, interrupt_handler)
    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering as in Raspberry Pi

    # set pin as an input pin with initial state
    GPIO.setup(input_pin, GPIO.IN)

    print("Welcome to the receiver readout")
    print("Camera is recording")
    print("This will print out the receiver values and auto formats it into 8 bit chunks")

    line_counter = 0

    while True:
        pin_value = convert_gpio_to_value(GPIO.input(input_pin))  # poll pin value
        value_array.append(pin_value)

        print(pin_value, end="")
        line_counter += 1
        if line_counter == 8:
            print(end=" ")
        if line_counter == 16:
            print()
            line_counter = 0

        logging.info("Polled: {0}".format(pin_value))
        time.sleep(1/60)


if __name__ == '__main__':
    main(sys.argv[1:])