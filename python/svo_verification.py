import pyzed.sl as sl
import getopt
import sys

WVGA = (672, 376, [15, 30, 60, 100])
HD720 = (1280, 720, [15, 30, 60])
HD1080 = (1920, 1080, [15, 30])
ULTRAHD = (2208, 1242, [15])


def usage():
    print('svo_verification.py -f <file_path> -v <expected_resolution> -r <expected_frame_rate>')
    print('-f or --file\t: File path of the svo file to verify')
    print('-v or --resolution\t: Expected Resolution, accepts the following values: 4K, 1080, 720, WVGA')
    print('-r or --rate\t: Expected Framerate, accepts the following values: 15, 30, 60, 100 within the limits of the '
          'ZED capabilities')


def main(argv):
    file = ""
    try:
        opts, args = getopt.getopt(argv, "hf:v:r:", ["help", "file="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-f', '--file'):
            file = arg

    input_type = sl.InputType()
    input_type.set_from_svo_file(file)
    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
    cam = sl.Camera()
    status = cam.open(init)

    if status != sl.ERROR_CODE.SUCCESS:
        print('Cam.Open failed')
        print(repr(status))
        exit()

    print("File Resolution: {0}x{1}".format(round(cam.get_camera_information().camera_resolution.width, 2), cam.get_camera_information().camera_resolution.height))
    print("Frame Rate: {0}".format(cam.get_camera_information().camera_fps))


if __name__ == '__main__':
    main(sys.argv[1:])