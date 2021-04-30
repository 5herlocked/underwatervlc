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
datapoints = list()
output_name = 'photodiode_{}Hz'.format(frequency)


def log_data():
    for deltaTime, value, voltage in datapoints:
        logging.info("{}: Value {}, Voltage {}".format(deltaTime, value, voltage))

    with open(output_name + "_data.csv", mode='w') as csv_file:
        csv_file = csv.writer(csv_file)
        csv_file.writerow(['time', 'value', 'voltage'])
        for deltaTime, value, voltage in datapoints:
            csv_file.writerow([deltaTime, value, voltage])


def interrupt_handler(sig, frame):
    print("You've pressed Ctrl+C!")
    print("Datapoints collected: {}".format(len(datapoints)))
    log_data()
    logging.info("Program ending")
    sys.stdout.flush()
    sys.exit(0)


def main(argv):
    signal.signal(signal.SIGINT, interrupt_handler)
    global frequency, datapoints, output_name
    try:
        opts, args = getopt.getopt(argv, "hf:o:", ["frequency=", "output="])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            sys.exit()
        elif opt == '-f':
            frequency = int(arg)
        elif opt == '-o':
            output_name = arg

    logging.basicConfig(filename=(output_name + ".log"))
    print("Started Polling")
    while True:
        datapoints.append((time.asctime(), chan.value, chan.voltage))
        time.sleep(1 / frequency)


if __name__ == '__main__':
    main(sys.argv[1:])
