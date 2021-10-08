# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform

try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('/home/ahnsun98/fallDetection/openpose/build/python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "/home/ahnsun98/fallDetection/openpose/models/"
    params['video'] = '/home/ahnsun98/fallDetection/openpose/build/examples/tutorial_api_python/workspace/demo/demovideo_fakefall.mp4'
    params["net_resolution"] = "-1x320"
    params["disable_blending"] = True
    params['number_people_max'] = 1

    # Starting OpenPose
    opWrapper = op.WrapperPython(op.ThreadManagerMode.Synchronous)
    opWrapper.configure(params)
    opWrapper.execute()

except ImportError as e:    
    print(e)
    sys.exit(-1)
