## Jetson Nano Setup Instructions
Follow the steps given to prepare the Jetson Nano:
1. Download the [Jetson Developer Kit Image](https://developer.nvidia.com/jetson-nano-2gb-sd-card-image)
2. Format the SD card with the formatter from the [SDA](https://www.sdcard.org/downloads/formatter/sd-memory-card-formatter-for-windows-download/)
2. Write the image to an SD card using one of the following:
	* Unix Disk Utilities (Disk Analyser) using the restore image/restore disk function
	* Windows Disk Manager (diskmgmgt) using the restore image/restore disk function
	* Balena Etcher using the flash button
3. Insert the SD card into the Jetson Nano
4. Boot it up, follow setup instructions until you boot into the linux desktop (it will restart once)
5. Run the command `sudo apt-get update` and follow instructions to update all tools
6. Run the command `sudo apt-get upgrade` and follow instructions to upgrade all tools
7. Ensure python 3 is installed by running the command `python3 --version` if you get an output it is installed and proceed to step 9
8. Python3 is not installed: install using the command `sudo apt-get install python3`
9. Python3 is installed and all packages are updated to the latest version. Install the wheel package using `pip3 install wheel`
10. Install the Jetson.GPIO package with the command `pip3 install Jetson.GPIO`
11. Visit the [GitHub page](https://github.com/NVIDIA/jetson-gpio) for the Jetson.GPIO package and follow the instructions for setting user permissions
11. Follow [instructions](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to make an SSH key, adding it to your account in GitHub and use it to authenticate with GitHub.
12. Clone our github repository by typing in `git clone git@github.com:ashwinashok/underwatervlc.git` and the following the prompt to get our code

Next instructions are [here](#Transmitter-Instructions):

## Jetson Xavier Setup Instructions
These are the steps to get the Xavier's setup and ready for experimentation:
1. Download the [Jetson Xavier NX Developer Kit Image](https://developer.nvidia.com/jetson-nx-developer-kit-sd-card-image)
2. Format the SD card with the formatter from the [SDA](https://www.sdcard.org/downloads/formatter/sd-memory-card-formatter-for-windows-download/)
2. Write the image to an SD card using one of the following:
	* Unix Disk Utilities (Disk Analyser) using the restore image/restore disk function
	* Windows Disk Manager (diskmgmgt) using the restore image/restore disk function
	* Balena Etcher using the flash button
3. Insert the SD card into the Jetson Xavier NX.
4. Boot it up, follow setup instructions until you boot into the linux desktop (it will restart once)
5. Run the command `sudo apt-get update` and follow instructions to update all tools
6. Run the command `sudo apt-get upgrade` and follow instructions to upgrade all tools
7. Ensure python 3 is installed by running the command `python3 --version` if you get an output, it is installed and proceed to step 9
8. Python3 is not installed: install using the command `sudo apt-get install python3`
9. Python3 is installed and all packages are updated to the latest version. Install the wheel package using `pip3 install wheel`
10. Install the Jetson.GPIO package with the command `pip3 install Jetson.GPIO`
11. Visit the [GitHub page](https://github.com/NVIDIA/jetson-gpio) for the Jetson.GPIO package and follow the instructions for setting user permissions
11. Follow [instructions](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to make an SSH key, adding it to your account in GitHub and use it to authenticate with GitHub.
12. Clone our github repository by typing in `git clone git@github.com:ashwinashok/underwatervlc.git` and then follow the prompt to get our code
13. Get the [ZED SDK](https://www.stereolabs.com/developers/release/) make it an executable and run it to install the ZED SDK
14. You will need to install numpy and cython using the commands `pip3 install numpy` and then `pip3 install cython`
14. Use the command `cd /usr/local/zed` and then run `python3 get_python_api.py` to install the python api for the ZED SDK.

## LED Transmitter Instructions
Follow the given steps to start transmitting on the Jetson Nanos:
1. Connect the LED array positive diode to Board Pin 12
2. Connect the LED ground pin to one of the GND pins on the Jetson
3. Use the command `python3 transmitter.py -h` to get help on how to use the transmitter command. 
4. There will be a file called `transmitter.log` this will contain all the logs including time stamps of each of the transmitted bits

## Photodiode (PD) Receiver Instructions
Follow the given steps to start receiving on the Xavier:
1. Connect the Photo-diode to Board Pin 12 and stereo camera to the Xavier
2. Connect Photo-diode ground to one of the GND pins on the Xavier
3. Use the command `python3 receiver.py -h` to get help on how to use the receiver interface
4. You will see live printed chunks of data as it receives a confirmed transmission.
5. There will be a file called `receiver.log` this will contain all the logs including time stamps of each of the received bits
6. There will be a folder called `recordings` in the same folder as the source code. It will contain all the recordings from the stereo cameras which show each receiving phase

## ZED Intructions
Follow the given steps to start recording stereo recording with the Xavier:
1. Connect the ZED Camera to the Jetson Xavier.
2. Ensure it's being detected using the 
