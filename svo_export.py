import numpy as np
import pyzed.sl as sl
import getopt
import sys
import cv2
import os


def progress_bar(percent_done, bar_length=50):
    done_length = int(bar_length * percent_done / 100)
    bar = '=' * done_length + '-' * (bar_length - done_length)
    sys.stdout.write('[%s] %f%s\r' % (bar, percent_done, '%'))
    sys.stdout.flush()


def usage():
    print('svo_export.py -f <file_path> -o <output_name>')
    print('-f or --file\t: File path of the svo file to export')
    print('-o or --output\t: Output names for the mp4 and obj files')


def main(argv):
    file = ""
    output_name = ""
    try:
        opts, args = getopt.getopt(argv, "hf:o:", ["file=", "output="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ('-f', '--file'):
            file = arg
        elif opt in ('-o', '--output'):
            output_name = arg
        else:
            print('Unrecognised option')
            usage()
            exit()

    if output_name == "":
        print('You need to define the output name using the -o option')
        usage()
        sys.exit(-1)

    # Make directory to put the video, depth image sequences and SBS pngs
    video_path = "{0}/".format(output_name)
    png_path = video_path + "png_sequences/"
    depth_path = video_path + "depth_sequences/"

    try:
        os.makedirs(video_path)
        os.makedirs(png_path)
        os.makedirs(depth_path)
    except OSError:
        print('Creation of directories failed')
        exit()
    else:
        print('Directories created')

    # set the input type as from file
    input_type = sl.InputType()
    input_type.set_from_svo_file(file)
    # initialise the camera parameters
    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
    init.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP
    init.coordinate_units = sl.UNIT.METER

    # initialise the camera
    cam = sl.Camera()
    status = cam.open(init)

    # camera parameters mismatch
    if status != sl.ERROR_CODE.SUCCESS:
        print('Cam.Open failed')
        print(repr(status))
        exit()

    frame_size = cam.get_camera_information().camera_resolution
    height = frame_size.height
    width = frame_size.width
    width_sbs = width * 2
    # prepare side by side container
    svo_image_sbs_rgba = np.zeros((height, width_sbs, 4), dtype=np.uint8)

    video_writer = cv2.VideoWriter(video_path + '{0}.avi'.format(output_name), cv2.VideoWriter_fourcc('M', '4', 'S', '2'),
                                   max(cam.get_camera_information().camera_fps, 25), (width_sbs, height))

    if not video_writer.isOpened():
        sys.stdout.write("OpenCV video writer cannot be opened. Please check .avi file path and write "
                         "permissions\n")
        cam.close()
        exit(-1)

    runtime = sl.RuntimeParameters()

    py_transform = sl.Transform()
    tracking_parameters = sl.PositionalTrackingParameters(py_transform)
    err = cam.enable_positional_tracking(tracking_parameters)
    if err != sl.ERROR_CODE.SUCCESS:
        print('Positional Tracking cannot be enabled')
        exit(1)

    mapping_parameters = sl.SpatialMappingParameters(map_type=sl.SPATIAL_MAP_TYPE.FUSED_POINT_CLOUD)
    err = cam.enable_spatial_mapping(mapping_parameters)
    if err != sl.ERROR_CODE.SUCCESS:
        print('Spatial Mapping failed')
        exit(1)

    sys.stdout.write('Converting SVO to OBJ Use Ctrl-C to interrupt\n')
    py_fpc = sl.FusedPointCloud()

    print('Extracting Point Cloud')
    err = cam.extract_whole_spatial_map(py_fpc)
    print(repr(err))
    print('Saving Point Cloud')
    py_fpc.save(video_path + "{0}.obj".format(output_name))

    cam.disable_spatial_mapping()
    cam.disable_positional_tracking()

    # Start SVO conversion to AVI/SEQUENCE
    sys.stdout.write("Converting SVO to AVI Use Ctrl-C to interrupt conversion.\n")
    nb_frames = cam.get_svo_number_of_frames()
    left_image = sl.Mat()
    right_image = sl.Mat()
    depth_image = sl.Mat()

    while True:
        if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            svo_position = cam.get_svo_position()

            cam.retrieve_image(left_image, sl.VIEW.LEFT)
            cam.retrieve_image(right_image, sl.VIEW.RIGHT)
            cam.retrieve_measure(depth_image, sl.MEASURE.DEPTH)

            svo_image_sbs_rgba[0:height, 0:width, :] = left_image.get_data()
            svo_image_sbs_rgba[0:, width:, :] = right_image.get_data()

            ocv_image_sbs_rgb = cv2.cvtColor(svo_image_sbs_rgba, cv2.COLOR_RGBA2RGB)

            video_writer.write(ocv_image_sbs_rgb)
            cv2.imwrite(depth_path + '{0}-{1}.png'.format(output_name, svo_position),
                        depth_image.get_data().astype(np.uint16))
            cv2.imwrite(png_path + '{0}-{1}.png'.format(output_name, svo_position), ocv_image_sbs_rgb)

            progress_bar((svo_position + 1) / nb_frames * 100, 30)

            if svo_position >= (nb_frames - 1):  # end of SVO
                sys.stdout.write("\nSVO end has been reached. Exiting.")
                break

    video_writer.release()
    cam.close()
    return 0


if __name__ == '__main__':
    main(sys.argv[1:])
