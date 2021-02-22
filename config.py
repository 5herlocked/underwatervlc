import configparser
import paramiko
import pysftp

config = configparser.ConfigParser()
config.read('settings.ini')

transmitters, receivers, cars = [], [], []
#Need to be global out of class scope? global transmitters, receivers, cars, new_var -K


def instantiate_config():
    global transmitters, receivers, cars
    # get all sections from config file
    sections = config.sections()
    transmitters = []
    receivers = []
    # Don't know how to define a car yet
    cars = []

    # convert them into objects
    for section in sections:
        if 'receiver' in section.lower():
            # Create Receiver
            receivers.append(Receiver(section))
        elif 'transmitter' in section.lower():
            # Create Transmitter
            transmitters.append(Transmitter(section))
        elif 'car' in section.lower():
            # Create Car
            cars.append(Car(section))

    # connect to each of the jetsons, raise errors when connection fails
    for receiver in receivers:
        try:
            receiver.connect()
        except:
            # Do the thing for exceptions
            pass
    for transmitter in transmitters:
        try:
            transmitter.connect()
        except:
            pass
    for car in cars:
        try:
            car.connect()
        except:
            pass


class Receiver(object):
    def __init__(self, name):
        self.name = name
        self.ip = config.get(name, 'ip_address')
        self.uname = config.get(name, 'uname')
        self.password = config.get(name, 'password')
        self.ssh_instance = paramiko.SSHClient()

    def connect(self):
        self.ssh_instance.connect(hostname=self.ip, username=self.uname, password=self.password)
        pass

    def start_receiver(self, pin, freq):
        command = "python3 receiver_basic.py -p {0} -f {1}".format(pin, freq)
        # exec_command is a non-blocking command, so we can do something with the stdout (if we need it)
        stdin, stdout, stderr = self.ssh_instance.exec_command(command)
        pass

    def stop_receiver(self):
        pass

    def get_receiver_log(self):
        # Secure copy the log file
        with pysftp.Connection(self.ip, username=self.uname, password=self.password) as sftp:
            with sftp.cd('public'):  # Need to set preferred directory for most recently received transmission
                sftp.get('receiver.log')  # We could set naming convention in settings.ini as well

    def disconnect(self):
        pass


class Transmitter(object):
    def __init__(self, name):
        self.name = name
        self.ip = config.get(name, 'ip_address')
        self.uname = config.get(name, 'uname')
        self.password = config.get(name, 'password')
        self.ssh_instance = paramiko.SSHClient()

    def connect(self):
        pass

    def start_transmission(self, pin, freq, message):
        command = "python3 transmitter.py -p {0} -f{1}"
        pass
        # subprocess.Popen(['python3', 'transmitter.py', '-p', pin, '-f', freq, '-m', message])

    def stop_transmission(self):
        pass

    def disconnect(self):
        pass


class Car(object):
    def __init__(self, name):
        self.name = name
        self.ip = config.get(name, 'ip_address')
        self.uname = config.get(name, 'uname')
        self.password = config.get(name, 'password')
        self.ssh_instance = paramiko.SSHClient()

    def connect(self):
        pass

    def start_transmission(self, pin, freq, message):
        pass

    def stop_transmission(self):
        pass

    def disconnect(self):
        pass
