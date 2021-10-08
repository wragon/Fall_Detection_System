import DoubleCheck as fd
import message
import user


# set User Information
userInfo = user.UserInfo()
userInfo.get_user()

# deteting fall
# videoFile = 0
videoFile = '/home/ahnsun98/fallDetection/openpose/build/examples/tutorial_api_python/workspace/demo/sample_video/demovideo_fakefall.mp4'
fallDetect = fd.FallDetect(videoFile)
isFall = fallDetect.catch_acc()
# print("FALL", isFall)

if (isFall):
    # sms = message.SMS(userInfo.number, userInfo.name, userInfo.location)
    mms = message.MMS(userInfo.number, userInfo.name, userInfo.location, './image/fall.jpg')

    # print(sms.get_data())
    # print(mms.get_data())

    # sms.send()
    mms.send()