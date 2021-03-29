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
random_size = 500
times = 1
# variables for perma state transmission
state_flag = False
perma_state = GPIO.LOW


def progress_bar(percent_done, bar_length=50):
    done_length = int(bar_length * percent_done / 100)
    bar = '=' * done_length + '-' * (bar_length - done_length)
    sys.stdout.write('[%s] %f%s\r' % (bar, percent_done, '%'))
    sys.stdout.flush()


def interrupt_handler(sig, frame):
    print("You've pressed Ctrl+C!")
    logging.info("Program ending")
    GPIO.cleanup(output_pin)
    sys.exit(0)


def create_transmission(bitstream, times_to_multiply):
    return bitstream * times_to_multiply  # multiplies it by the number of times to be repeated


def transmit(transmission_bits):
    total_bits = len(transmission_bits)
    counter = 0
    try:
        # Pin Setup:
        GPIO.setmode(GPIO.BOARD)

        # set pin as an output pin with initial state low
        GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)
        for bit in transmission_bits:
            GPIO.output(output_pin, int(bit))
            counter += 1
            logging.info("Transmitted: {0}".format(bit))
            progress_bar((counter + 1)/total_bits * 100, 30)
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
    if input_state in ('ON', 'on'):
        state = GPIO.HIGH
    elif input_state in ('OFF', 'off'):
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
        opts, args = getopt.getopt(argv, "hs:r:f:t:", ["state=", "random=", "frequency=", "times="])
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
            random_size = int(arg)
        elif opt in ('-t', '--times'):
            times = int(arg)

    signal.signal(signal.SIGINT, interrupt_handler)

    if state_flag:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(output_pin, GPIO.OUT, initial=perma_state)
        GPIO.output(output_pin, perma_state)
        print('Output set to permanent state: {0}'.format(perma_state))
        GPIO.cleanup(output_pin)
    elif random_flag:
        # logging config
        # ToDo: Change the filename here if in the future our datasets change
        logging.basicConfig(filename='transmitter_{0}Hz_{1}_cycles-{2}_bits.log'.format(frequency, times, random_size),
                            level=logging.INFO, format='%(asctime)s %(message)s')
        random_bits = generate_random_bitstream(random_size)
        logging.info("Generated bitstream: {0}".format(random_bits))
        transmission = create_transmission(random_bits, times)
        f = open('raw_bitsream_{0}Hz_{1}_cycles-{2}_bits.txt'.format(frequency, times, random_size), "w+")
        f.write(transmission)
        print("Transmitting")
        logging.info("Starting Transmission")
        transmit(transmission)
        logging.info("Transmisssion Ended")
    else:
        print('No flags set, exiting')
        usage()
        sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
