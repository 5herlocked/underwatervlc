import pyzed.sl as sl
import signal
import sys
import time

cam = sl.Camera()  # Initialise Camera


def interrupt_handler(sig, frame):
    # End camera recording
    cam.disable_recording()
    cam.close()
    sys.exit(0)


def main():
    signal.signal(signal.SIGTERM, interrupt_handler)
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.VGA
    init.depth_mode = sl.DEPTH_MODE.NONE

    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    path_output = "./videos/{0}".format(time.localtime())
    recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.H264)
    err = cam.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    runtime = sl.RuntimeParameters()

    while True:
        cam.grab(runtime)
        time.sleep(1/100)


if __name__ == '__main__':
    main()