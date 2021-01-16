from binascii import hexlify
import Jetson.GPIO as GPIO

import time
import logging

output_pin = 18  # BCM pin 18, Board Pin 12


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
        transmission.append(int(bit))

    # transmission end mask
    for i in range(16):
        transmission.append(0)
    return transmission


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


def convert_ascii_to_transmission_bits(text):
    bit_array = text_to_bits(text)
    bit_array = transmission_mask(bit_array)

    return bit_array


def create_transmission(commands):
    times = int(commands[1])  # find out how many times we want to transmit
    transmission = convert_ascii_to_transmission_bits(commands[0])  # converts ascii to bits
    print_bits(transmission)  # prints out the transmission
    return transmission * times  # multiplies it by the number of times to be repeated


def transmit(transmission_bits):
    try:
        for bit in transmission_bits:
            GPIO.output(output_pin, bit)
            time.sleep(1 / 30)  # effectively a 30Hz transmission rate
    finally:
        GPIO.cleanup()


def main():
    # logging config
    logging.basicConfig(filename='transmitter.log', level=logging.INFO, format='%(asctime)s %(message)s')

    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering as in Raspberry Pi

    # set pin as an output pin with initial state low
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)

    print("Welcome to the transmission REPL.")
    print("Command format is: <String>, <number>(optional)")

    while True:
        line = input('> ')
        command = line.split(',')
        if len(command) < 2:
            command.append("1")
        transmission = create_transmission(command)
        print("Transmitting")
        logging.info("{0}, {1} times".format(convert_ascii_to_transmission_bits(command[0]), command[1]))
        transmit(transmission)


if __name__ == '__main__':
    main()
