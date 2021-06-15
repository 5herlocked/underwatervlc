import getopt
import signal
import time
import logging
import sys
import csv
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)
# ads.gain = 2/3

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P3)

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

frequency = 1

def interrupt_handler(sig, frame):
    print("You've pressed Ctrl+C!")
    sys.exit(0)


def main(argv):
    signal.signal(signal.SIGINT, interrupt_handler)

    print("Started Polling")
    print("Raw Value\t Voltage")
    print("==============================================")
    while True:
        print("{0}\t{1}".format(chan.value, chan.voltage))
        time.sleep(1 / 2)


if __name__ == '__main__':
    main(sys.argv[1:])
