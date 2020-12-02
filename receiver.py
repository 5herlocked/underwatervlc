from binascii import unhexlify
import Jetson.GPIO as GPIO
import time

input_pin = 18  # BCM pin 18, BOARD pin 12


def convert_gpio_to_value(gpio_value):
    if gpio_value == GPIO.HIGH:
        return 1
    else:
        return 0


def text_from_bits(bits, encoding='ascii', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)


def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return unhexlify(hex_string.zfill(n + (n & 1)))


def get_ascii_from_transmission_bits(bits):
    ascii_array = ""

    for i in range(len(bits)):
        if i <= 17 or i >= len(bits) - 16:
            continue
        if i % 2 == 0:
            continue
        ascii_array += str(bits[i])
    return str(ascii_array)


def transmission_started(bits):
    if len(bits) == 16:
        for i in bits:
            if i != 1:
                return False
            else:
                continue
    else:
        return False

    return True


def transmission_ended(bits):
    if len(bits) == 16:
        for i in bits:
            if i != 0:
                return False
            else:
                continue
    else:
        return False


def main():
    # Pin Setup:
    # Board pin-numbering
    GPIO.setmode(GPIO.BCM)

    # set pin as an input pin with initial state
    GPIO.setup(input_pin, GPIO.IN)

    print("Starting demo now! Press Ctrl+C to exit")

    receiving = False

    value_array = []
    bit_buffer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 16 bit buffer
    buffer_counter = 0

    # not receiving loop
    while True:
        bit_buffer[buffer_counter] = convert_gpio_to_value(GPIO.input(input_pin))
        # we only need to check when buffer_counter hits 15
        if buffer_counter == 15:
            value_array.append(bit_buffer)
            receiving = transmission_started(bit_buffer)
            if receiving:
                buffer_counter = 0  # reset counter before we head into the receiving loop
                break
            buffer_counter = 0
        time.sleep(0.016666667)  # Effectively a 60Hz polling rate

    # receiving loop
    while receiving:
        bit_buffer[buffer_counter] = convert_gpio_to_value(GPIO.input(input_pin))

        if buffer_counter == 15:
            value_array.append(bit_buffer)
            receiving = transmission_ended(bit_buffer)
            if not receiving:
                break
            buffer_counter = 0
        time.sleep(0.016666667)  # Effectively a 60Hz polling rate

    message = get_ascii_from_transmission_bits(value_array)
    print(message)


if __name__ == '__main__':
    main()
