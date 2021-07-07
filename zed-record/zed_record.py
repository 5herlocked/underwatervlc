import pyzed.sl as sl
import signal
import sys
from datetime import *
import getopt

cam = sl.Camera()  # Initialise Camera


def update_sysout(frames_grabbed, frames_missed):
    sys.stdout.write('Frames Grabbed:{0}\tFrames Missed: {1}\r'.format(frames_grabbed, frames_missed))
    sys.stdout.flush()


def interrupt_handler(sig, frame):
    # End camera recording
    cam.disable_recording()
    cam.close()
    sys.exit(0)


def progress_bar(percent_done, bar_length=50):
    done_length = int(bar_length * percent_done / 100)
    bar = '=' * done_length + '-' * (bar_length - done_length)
    sys.stdout.write('[%s] %f%s\r' % (bar, percent_done, '%'))
    sys.stdout.flush()


def usage():
    print('zed_record.py -o <output_name>')
    print('-o or --output\t:  File path of the svo to generate')
    print('-r or --resolution\t: Resolution to capture in, accepted values: WVGA, HD, FULLHD, 4K')
    print('-f or --framerate\t: Framerate to capture in, limited by the resolution: 15, 30, 60, 100')


def get_res_framerate (resolution_string: str, frame_rate: str):
    cleaned = resolution_string.lower()

    res = sl.RESOLUTION.VGA

    if cleaned in ('wvga', 'vga'):
        res = sl.RESOLUTION.VGA
    elif cleaned in ('hd'):
        res = sl.RESOLUTION.HD720
    elif cleaned in ('fullhd', 'fhd'):
        res = sl.RESOLUTION.HD1080
    elif cleaned in ('4k', '2k', '2.2k'):
        res = sl.RESOLUTION.HD2K
    else:
        print('Incorrect Resolution requested, use WVGA, HD, FULLHD, 4K')
        usage()
        exit()

    fps_request = int(frame_rate)
    rate = 100
    if fps_request not in (15, 30, 60, 100):
        print('Incorrect framerate requested, use 15, 30, 60, 100')
        usage()
        exit()
    elif fps_request == 15:
         rate = 15
    elif fps_request == 30 and res in (sl.RESOLUTION.VGA, sl.RESOLUTION.HD720, sl.RESOLUTION.HD1080):
        rate = 30
    elif fps_request == 60 and res in (sl.RESOLUTION.VGA, sl.RESOLUTION.HD720):
        rate = 60
    elif fps_request == 100 and res == sl.RESOLUTION.VGA:
        rate = 100
    else:
        print('Something incredible has happened, you have somehow broken everything')
        usage()
        exit()

    return res, rate


def main(argv):
    output_name = datetime.now().strftime('%m-%d-%Y_%H-%M-%S')
    possible_res_string = "WVGA"
    possible_frame_string = "100"

    signal.signal(signal.SIGINT, interrupt_handler)
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.VGA
    init.camera_fps = 100
    init.depth_mode = sl.DEPTH_MODE.ULTRA
    init.coordinate_units = sl.UNIT.MILLIMETER
    init.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

    try:
        opts, args = getopt.getopt(argv, "ho:r:f:", ["output=", "resolution=", "framerate="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(argv) == 0:
        print('Using default values of WVGA at 100fps and defualt output name of date time')

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ('-r', '--resolution'):
            possible_res_string = arg
        elif opt in ('-f', '--framerate'):
            possible_frame_string = arg
        elif opt in ('-o', '--output'):
            output_name = arg
        else:
            print('Unrecognised option')
            usage()
            exit()

    init.camera_resolution, init.camera_fps = get_res_framerate(possible_res_string, possible_frame_string)

    print('Resolution: {0}, Frame rate: {1}'.format(init.camera_resolution, init.camera_fps))
    
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print('Camera.open failed')
        print(repr(status))
        exit(1)

    path_output = "./{0}.svo".format(output_name)
    recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.H264)
    err = cam.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print('Enable Recording failed')
        print(repr(err))
        exit(1)

    runtime = sl.RuntimeParameters()
    frames_grabbed = 0
    frames_missed = 0

    while True:
        if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            frames_grabbed += 1
        else:
            frames_missed += 1
        update_sysout(frames_grabbed, frames_missed)


if __name__ == '__main__':
    main(sys.argv[1:])
