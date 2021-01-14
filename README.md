## Jetson Nano Setup Instructions
Follow the steps given to prepare the Jetson Nano:
1. Download the [Jetson Developer Kit Image](https://developer.nvidia.com/jetson-nano-sd-card-image)
2. Write the image to an SD card using one of the following:
	* Unix Disk Utilities (Disk Analyser) using the restore image/restore disk function
	* Windows Disk Manager (diskmgmgt) using the restore image/restore disk function
	* Balena Etcher (with low-medium sucess) using the flash button
3. Insert the SD card into the Jetson Nano
4. Boot it up, follow setup instructions until you boot into the linux desktop (it will restart once)
5. Run the command `sudo apt-get update` and follow instructions to update all tools
6. Run the command `sudo apt-get upgrade` and follow instructions to upgrade all tools
7. Ensure python 3 is installed by running the command `python3 --version` if you get an output it is installed and proceed to step 9
8. Python3 is not installed: install using the command `sudo apt-get install python3`
9. Python3 is installed and all packages are updated to latest version. Install the wheel package using `pip3 install wheel`
10. Install the Jetson.GPIO package with the command `pip3 install Jetson.GPIO`
11. Visit the [GitHub page](https://github.com/NVIDIA/jetson-gpio) for the Jetson.GPIO package and follow the instructions for setting user permissions
11. Follow [instructions](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to make an SSH key, adding it to your account in GitHub and use it to authenticate with GitHub.
12. Clone our github repository by typing in `git clone git@github.com:ashwinashok/underwatervlc.git` and the following the prompt to get our code
Next instructions are [here](#Transmitter-Instructions):

## Xavier Setup Instructions
These are the steps to get the Xavier's setup and ready for experimentation:
1. Download the [Jetson Xavier NX Developer Kit Image](https://developer.nvidia.com/jetson-nx-developer-kit-sd-card-image)
2. Write the image to an SD card using one of the following:
	* Unix Disk Utilities (Disk Analyser) using the restore image/restore disk function
	* Windows Disk Manager (diskmgmgt) using the restore image/restore disk function
	* Balena Etcher (with low-medium sucess) using the flash button
3. Insert the SD card into the Jetson Xavier NX.
4. Boot it up, follow setup instructions until you boot into the linux desktop (it will restart once)
5. Run the command `sudo apt-get update` and follow instructions to update all tools
6. Run the command `sudo apt-get upgrade` and follow instructions to upgrade all tools
7. Ensure python 3 is installed by running the command `python3 --version` if you get an output, it is installed and proceed to step 9
8. Python3 is not installed: install using the command `sudo apt-get install python3`
9. Python3 is installed and all packages are updated to latest version. Install the wheel package using `pip3 install wheel`
10. Install the Jetson.GPIO package with the command `pip3 install Jetson.GPIO`
11. Visit the [GitHub page](https://github.com/NVIDIA/jetson-gpio) for the Jetson.GPIO package and follow the instructions for setting user permissions
11. Follow [instructions](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to make an SSH key, adding it to your account in GitHub and use it to authenticate with GitHub.
12. Clone our github repository by typing in `git clone git@github.com:ashwinashok/underwatervlc.git` and then follow the prompt to get our code
13. Get the [ZED SDK](https://download.stereolabs.com/zedsdk/3.3/jp44/jetsons) make it an executable and run it to install the ZED SDK
14. Use the command `cd /usr/local/zed` and then run `python3 get_python_api.py` to install the python api for the ZED SDK.

## Transmitter Instructions
Follow the given steps to start transmitting on the Jetson Nanos:
1. 

## GPIO setup
Follow the steps given to prepare the Jetson's for proper GPIO pin setup:
1.

## Stereo Camera from ZED Labs
Follow the given steps to prepare the Xavier for the ZED camera:
1. 

## Thor Labs photo-diode setup
Follow the given steps to prepare the Xavier for Photo-Diodes:
1. 

# Receiver Instructions
Follow the given steps to start receiving on the Xavier:
1. 
2. 
3.
4. Start the receiver on the Jetson Xavier's: `python3 receiver.py`