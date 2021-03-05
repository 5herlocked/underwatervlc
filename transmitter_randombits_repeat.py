import binascii
from datetime import *

import Jetson.GPIO as GPIO

import signal
import sys
import time
import logging
import getopt
import random

output_pin = 12  # Board Pin 12
frequency = 30  # effectively a 30Hz transmission rate
# variables for random bit transmission
random_flag = False
random_size = 1000
times = 1
# variables for perma state transmission
state_flag = False
perma_state = GPIO.LOW


def interrupt_handler(sig, frame):
    print("You've pressed Ctrl+C!")
    logging.info("Program ending")
    GPIO.cleanup(output_pin)
    sys.exit(0)


def create_transmission(bitstream, times):
    return bitstream * times  # multiplies it by the number of times to be repeated


def transmit(transmission_bits):
    try:
        # Pin Setup:
        GPIO.setmode(GPIO.BOARD)

        # set pin as an output pin with initial state low
        GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)
        for bit in transmission_bits:
            GPIO.output(output_pin, bit)
            logging.info("Transmitted: {0}".format(bit))
            time.sleep(1/frequency)
    finally:
        GPIO.cleanup(output_pin)


def usage():
    print('transmitter_randombits_repeat.py -s <define_static_state> -r <length_of_random_bitstream> -f '
          '<frequency_to_transmit> -t <number_of_times>')
    print('-f or --frequency\t: Frequency to transmit at')
    print('-r or --random\t: Flag to set random bit transmission followed by the size of the bitstream')
    print('-t or --times\t: Number of times the random bitstream is to be repeated')
    print('-s or --state\t: Set the permanent state of the LED. This flag takes precedence so include only for LED '
          'ON/OFF experiment')


def get_perma_state(input_state):
    state = GPIO.LOW
    if input_state in ('ON', 'on'):
        state = GPIO.HIGH
    elif input_state in ('OFF', 'of'):
        state = GPIO.LOW
    else:
        usage()
        print('Expected values for state flag are: ON/OFF')
        sys.exit(2)

    return state


def generate_random_bitstream(size):
    bitstream = ""
    for i in range(size):
        bitstream += str(random.randint(0, 1))

    return bitstream


def main(argv):
    global output_pin, frequency, state_flag, perma_state, random_flag, random_size, times
    if len(argv) == 1:
        print('Using default values of: Output Pin = Board 12, Frequency = 30 Hz')
    try:
        opts, args = getopt.getopt(argv, "hs:r:f:", ["state=", "random=", "frequency="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ('-s', '--state'):
            state_flag = True
            perma_state = get_perma_state(arg)
        elif opt in ('-f', '--freq'):
            frequency = int(arg)
        elif opt in ('-r', '--random'):
            random_flag = True
            random_size = arg
        elif opt in ('-t', '--times'):
            times = int(arg)

    # logging config
    logging.basicConfig(filename='transmitter-{0}.log'.format(datetime.now().strftime('%m-%d-%Y-%H:%M:%S')), level=logging.INFO, format='%(asctime)s %(message)s')
    signal.signal(signal.SIGINT, interrupt_handler)

    if state_flag:
        GPIO.setup(output_pin, GPIO.OUT, initial=perma_state)
        GPIO.output(output_pin, perma_state)
        print('Output set to permanent state: {0}'.format(perma_state))
    elif random:
        transmission = create_transmission(generate_random_bitstream(random_size), times)
        print("Transmitting")
        logging.info("Starting Transmission")
        transmit(transmission)
    else:
        print('No flags set, exiting')
        sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
