from binascii import hexlify
import Jetson.GPIO as GPIO
import time

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


def main(to_transmit):
    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering as in Raspberry Pi

    # set pin as an output pin with initial state low
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)

    print("Starting transmission now")
    transmission_bits = convert_ascii_to_transmission_bits()
    print_bits(transmission_bits)

    current_pos = 0
    try:
        while True:
            if current_pos == len(transmission_bits):
                current_pos = 0

            GPIO.output(output_pin, transmission_bits[current_pos])
            current_pos += 1
            time.sleep(0.033333333)  # effectively a 30Hz transmission rate
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main("hello world")