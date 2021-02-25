from binascii import hexlify
import Jetson.GPIO as GPIO

import signal
import sys
import time
import logging
import getopt

output_pin = 18  # BCM pin 18, Board Pin 12
frequency = 1/30  # effectively a 30Hz transmission rate
message = "Hello World"


def interrupt_handler(sig, frame):
    print("You've pressed Ctrl+C!")
    logging.info("Program ending")
    GPIO.cleanup(output_pin)
    sys.exit(0)


def text_to_bits(text, encoding='ascii', errors='surrogatepass'):
    bits = bin(int(hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def transmission_mask(bits):
    transmission = []
    # start transmission mask
    for i in range(16):
        transmission.append(1)

    # transmission with double poll rate
    for bit in bits:
        transmission.append(int(bit))

    # transmission end mask
    for i in range(16):
        transmission.append(0)
    return transmission


def convert_ascii_to_transmission_bits(text):
    bit_array = text_to_bits(text)
    bit_array = transmission_mask(bit_array)

    return bit_array


def create_transmission(commands):
    transmission = convert_ascii_to_transmission_bits(commands)  # converts ascii to bits
    return transmission  # multiplies it by the number of times to be repeated


def transmit(transmission_bits):
    try:
        # Pin Setup:
        GPIO.setmode(GPIO.BCM)  # BCM pin-numbering as in Raspberry Pi

        # set pin as an output pin with initial state low
        GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)
        for bit in transmission_bits:
            GPIO.output(output_pin, bit)
            logging.info("Transmitted: {0}".format(bit))
            time.sleep(frequency)
    finally:
        GPIO.cleanup(output_pin)


def main(argv):
    global output_pin, frequency, message
    if len(argv) == 1:
        print('Using default values of: Output Pin = Board 12, Frequency = 30 Hz')
    try:
        opts, args = getopt.getopt(argv, "hp:f:m:", ["pin=", "freq=", "message="])
    except getopt.GetoptError:
        print('receiver_basic.py -p <GPIO_Pin> -f <Frequency_for_polling>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('receiver_basic.py -p <GPIO_Pin> -f <Frequency_for_polling>')
            sys.exit()
        elif opt in ('-p', '--pin'):
            output_pin = arg
        elif opt in ('-f', '--freq'):
            frequency = arg
        elif opt in ('-m', '--message'):
            message = arg

    # logging config
    logging.basicConfig(filename='transmitter.log', level=logging.INFO, format='%(asctime)s %(message)s')
    signal.signal(signal.SIGINT, interrupt_handler)

    transmission = create_transmission(message)
    print("Transmitting")
    logging.info("Starting Transmission")
    transmit(transmission)


if __name__ == '__main__':
    main(sys.argv[1:])
