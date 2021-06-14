//
// Created by sherlock on 12/05/2021.
//

#include "zed_record.h"
#include <ctime>
#include <sl/Camera.hpp>


using namespace std;

void showUsage();
void print(const string& msg_prefix, ERROR_CODE err_code = ERROR_CODE::SUCCESS, const string& msg_suffix = "");
void parseArgs(int argc, char *argv[], InitParameters &param, string& file_name);
void getResFrameRate(const string& resStr, const string& frameStr, InitParameters& param);
int getValidFrameRate(RESOLUTION resolution, int rate);

int main(int argc, char *argv[]) {
    Camera zed;

    InitParameters init;
    init.camera_resolution = RESOLUTION::VGA;
    init.camera_fps = 100;
    init.depth_mode = DEPTH_MODE::ULTRA;
    init.coordinate_units = UNIT::MILLIMETER;
    init.coordinate_system = COORDINATE_SYSTEM::RIGHT_HANDED_Y_UP;

    string fileName;
    parseArgs(argc, argv, init, fileName);

    // TODO: the actual record loop
}

void print(const string& msg_prefix, ERROR_CODE err_code, const string& msg_suffix) {
    if (err_code != ERROR_CODE::SUCCESS)
        cout << "[Error] ";
    else
        cout << " ";
    cout << msg_prefix << " ";
    if (err_code != ERROR_CODE::SUCCESS) {
        cout << " | " << toString(err_code) << " : ";
        cout << toVerbose(err_code);
    }
    if (!msg_suffix.empty())
        cout << " " << msg_suffix;
    cout << endl;
}

void parseArgs(int argc, char *argv[], InitParameters &param, string& file_name) {
    time_t tt;
    struct tm* ti;
    time(&tt);
    ti = localtime_s(&tt);

    if (argc == 1) {
        cout << "Using default values of WVGA@100fps with the filename being " << asctime_s(ti) << ".svo" << endl;
    }

    string frameRateStr;
    string resStr;

    // TODO: Add error checking in each of the if branches
    for (int i = 1; i < argc; ++i) {
        string arg = argv[i];
        if ((arg == "-h") || (arg == "--help")) {
            showUsage();
            return;
        } else if ((arg == "-r") || (arg == "--resolution")) {
            resStr = argv[i + 1];
        } else if ((arg == "-f") || (arg == "--framerate")) {
            frameRateStr = argv[i + 1];
        } else if ((arg == "-o") || (arg == "--output")) {
            file_name = argv[i + 1];
        } else {
            cout << "Unknown option: <" << argv[i] << endl;
        }
    }

    getResFrameRate(resStr, frameRateStr, param);
}

void getResFrameRate(const string& resStr, const string& frameStr, InitParameters& param) {
    int frameRate = stoi(frameStr, nullptr, 10);
    if (resStr == "WVGA" || resStr == "VGA") {
        param.camera_resolution = RESOLUTION::VGA;
        param.camera_fps = getValidFrameRate(param.camera_resolution, frameRate);
    } else if (resStr == "HD" || resStr == "720P") {
        param.camera_resolution = RESOLUTION::HD720;
        param.camera_fps = getValidFrameRate(param.camera_resolution, frameRate);
    } else if (resStr =="FULLHD" || resStr == "1080P") {
        param.camera_resolution = RESOLUTION::HD1080;
        param.camera_fps = getValidFrameRate(param.camera_resolution, frameRate);
    } else if (resStr == "ULTRAHD" || resStr == "4K") {
        param.camera_resolution = RESOLUTION::HD2K;
        param.camera_fps = getValidFrameRate(param.camera_resolution, frameRate);
    }
}

int getValidFrameRate(RESOLUTION resolution, int rate) {
    switch (resolution) {
        case RESOLUTION::VGA:
            // acceptable framerates 15, 30, 60, 100
            if (rate == 15) {
                return 15;
            } else if (rate == 30) {
                return 30;
            } else if (rate == 60) {
                return 60;
            } else {
                return 100;
            }
        case RESOLUTION::HD720:
            // acceptable framerates 15, 30, 60
            if (rate == 15) {
                return 15;
            } else if (rate == 30) {
                return 30;
            } else {
                return 60;
            }
        case RESOLUTION::HD1080:
            // acceptable framerates 15, 30
            if (rate == 15) {
                return 15;
            } else {
                return 30;
            }
        case RESOLUTION::HD2K:
            // acceptable framerate 15
            return 15;
        case RESOLUTION::LAST:
            break;
    }
}

void showUsage () {
    cout << "./zed_record -r <resolution> -f <frameRate> -o <output_name>" << endl;
    cout << "-r or --resolution\t: Define the resolution of the recording. Accepted values: WVGA, HD, FULLHD, 4K" << endl;
    cout << "-f or --framerate\t: Define the framerate of the recording. Limited by the resolution. Accepted values are 15, 30, 60, 100" << endl;
    cout << "-o or --output\t: Define the output name of the file. Limited only by the filesystem" << endl;

    exit(-1);
}