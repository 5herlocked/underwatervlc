import pyzed.sl as sl
import signal
import sys
from datetime import *

cam = sl.Camera()  # Initialise Camera


def interrupt_handler(sig, frame):
    # End camera recording
    cam.disable_recording()
    cam.close()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, interrupt_handler)
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.VGA
    init.camera_fps = 100
    init.depth_mode = sl.DEPTH_MODE.ULTRA
    init.coordinate_units = sl.UNIT.METER
    init.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP
    
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print('Camera.open failed')
        print(repr(status))
        exit(1)

    path_output = "./{0}.svo".format(datetime.now().strftime('%m-%d-%Y_%H:%M:%S'))
    recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.H264)
    err = cam.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print('Enable Recording failed')
        print(repr(err))
        exit(1)

    runtime = sl.RuntimeParameters()

    while True:
        cam.grab(runtime)


if __name__ == '__main__':
    main()
