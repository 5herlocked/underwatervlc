# This is a file for storing all the commonly used functions to maximise code reuse
import sys


WVGA = (672, 376, [15, 30, 60, 100])
HD720 = (1280, 720, [15, 30, 60])
HD1080 = (1920, 1080, [15, 30])
ULTRAHD = (2208, 1242, [15])


def pretty_bits(bits):
    prettified_bits = ""

    i = 0
    internal_counter = 0
    while i < len(bits):
        prettified_bits += str(bits[i])
        i += 1
        internal_counter += 1
        if internal_counter == 8:
            prettified_bits += " "
        if internal_counter == 16:
            prettified_bits += "\n"
            internal_counter = 0

    return prettified_bits


def progress_bar(percent_done, bar_length=50):
    done_length = int(bar_length * percent_done / 100)
    bar = '=' * done_length + '-' * (bar_length - done_length)
    sys.stdout.write('[%s] %f%s\r' % (bar, percent_done, '%'))
    sys.stdout.flush()
