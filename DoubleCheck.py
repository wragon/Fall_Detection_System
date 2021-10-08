# To fall detectection
import os
import sys
from sys import platform
import cv2
import time
import datetime
import numpy as np
from scipy.spatial import distance
from collections import deque

sys.path.append('/home/ahnsun98/fallDetection/openpose/build/python');
from openpose import pyopenpose as op

class FallDetect:    
    videoFile = ""
    stream = ""
    params = dict()
    opWrapper = op.WrapperPython()

    frame = 0
    center_old = np.zeros([1,2])
    center_new = np.zeros([1,2])
    dist_old = 0
    dist_new = 0
    acc = 0
    count = 0

    dq_h = deque()
    dq_l = deque()
    dq_r = deque()
    cdq_h = deque()
    cdq_l = deque()
    cdq_r = deque()
    
    # cnt = []

    def __init__(self, videoFile):
        self.set_openpose(videoFile)
        self.stream = cv2.VideoCapture(self.videoFile)

    def set_params(self):
        params = dict()
        params["model_folder"] = "/home/ahnsun98/fallDetection/openpose/models/"
        params['video'] = self.videoFile
        params['camera'] = 0
        params['body'] = 1
        params["model_pose"] = "BODY_25"
        params["net_resolution"] = "-1x320"
        params["disable_blending"] = True
        params["logging_level"] = 3
        params['process_real_time'] = False
        params['frames_repeat'] = False
        # params['number_people_max'] = 1
        return params

    def set_openpose(self, videoFile):
        self.videoFile = videoFile
        self.params = self.set_params()

    def get_center(self, h, l, r):
        x_center = (h[0] + l[0] + r[0]) / 3
        y_center = (h[1] + l[1] + r[1]) / 3
        return [x_center, y_center]

    def fall_checking (self):
        print("---fall_checking---")
        start = time.time()
        checking = True
        while(time.time() - start <= 3):
            ret,img = self.stream.read()
            if img is None:
                break
            self.frame += 1
            datum = op.Datum()
            datum.cvInputData = img
            self.opWrapper.emplaceAndPop(op.VectorDatum([datum]))

            keypoints = np.array(datum.poseKeypoints)
            if keypoints.any() is None:
                # print("Keypoint is NONE. Frame pass!")
                continue

            h = np.array([keypoints[0][0][0],keypoints[0][0][1]])
            # rE = np.array([keypoints[0][15][0],keypoints[0][15][1]])
            # lE = np.array([keypoints[0][16][0],keypoints[0][16][1]])
            # h = np.array([sum(elem)/2 for elem in zip(rE,lE)])            h = 눈 중점
            l = np.array([keypoints[0][2][0],keypoints[0][2][1]])
            r = np.array([keypoints[0][5][0],keypoints[0][5][1]])
            
            prob_h = keypoints[0][0][2]
            # prob_h = (keypoints[0][15][2] + keypoints[0][16][2]) / 2      눈 prob 평균
            prob_l = keypoints[0][2][2]
            prob_r = keypoints[0][5][2]

            self.cdq_h.append(h)
            if prob_h<0.7: # 이전 좌표 가져옴
                # self.cnt.append((frame,"h"))
                # print("PROB_H < 0.7!!")
                self.cdq_h.pop()
                if len(self.cdq_h)==0:
                    continue
                val = self.cdq_h.pop()
                self.cdq_h.append(val)
                self.cdq_h.append(val)
                h = val
            self.cdq_l.append(l)
            if prob_l<0.7: # 이전 좌표 가져옴
                # self.cnt.append((frame,"l"))
                # print("PROB_L < 0.7!!")
                self.cdq_l.pop()
                if len(self.cdq_l)==0:
                    continue
                val = self.cdq_l.pop()
                self.cdq_l.append(val)
                self.cdq_l.append(val)
                l = val
            self.cdq_r.append(r)
            if prob_r<0.7: # 이전 좌표 가져옴
                # self.cnt.append((frame,"r"))
                # print("PROB_R < 0.7!!")
                self.cdq_r.pop()
                if len(self.cdq_r)==0:
                    continue
                val = self.cdq_r.pop()
                self.cdq_r.append(val)
                self.cdq_r.append(val)
                r = val

            self.center_new = np.array(self.get_center(h, l, r))
            self.dist_new = distance.euclidean(self.center_new, self.center_old) # 속도
            self.acc = abs(self.dist_new - self.dist_old)
            print(f"time :  {time.time() - start} / acceleration : {self.acc} / Velocity : {self.dist_new}")
            if(self.dist_new > 5):
                self.count += 1
                if(self.count == 3): # 3번의 chance
                    self.count = 0
                    checking = False
                    print("False")
                    break

            self.dist_old = self.dist_new
            self.center_old = self.center_new

        if(time.time() - start < 3):  # 마지막에 그냥 낙상으로 끝나는 것을 방지
            checking = False
        return checking

    def catch_acc(self): # main
        self.opWrapper.configure(self.params)
        self.opWrapper.start()

        poseModel = op.PoseModel.BODY_25
        print(op.getPoseBodyPartMapping(poseModel))
        
        acc_array = [[0, 0]]
        pass_list = [-1]
        start = time.time()
        while True:
            ret,img = self.stream.read()
            if img is None:
                break
            self.frame += 1
            datum = op.Datum()
            datum.cvInputData = img
            self.opWrapper.emplaceAndPop(op.VectorDatum([datum]))
            # print("Body keypoints: \n" + str(datum.poseKeypoints))
            ''' keypoints
            [x0][y0][prob0]
            [x1][y1][prob2]
            ...
            [x24][y24][prob24] --> need 0,2,5
            '''
            keypoints = np.array(datum.poseKeypoints)

            print("\n----- Frame", self.frame, "-----")
            if keypoints.any() is None:
                print("Keypoint is NONE. Frame pass!")
                if 0 in pass_list:
                    continue
                pass_list.append(0)
                continue

            print("Num of People:", len(keypoints))
            if len(keypoints) > 1:
                print("Not ONE. Frame pass!")
                if 0 in pass_list:
                    continue
                pass_list.append(0)
                continue
            
            h = np.array([keypoints[0][0][0],keypoints[0][0][1]])
            # rE = np.array([keypoints[0][15][0],keypoints[0][15][1]])
            # lE = np.array([keypoints[0][16][0],keypoints[0][16][1]])
            # h = np.array([sum(elem)/2 for elem in zip(rE,lE)])            h = 눈 중점
            l = np.array([keypoints[0][2][0],keypoints[0][2][1]])
            r = np.array([keypoints[0][5][0],keypoints[0][5][1]])
            
            prob_h = keypoints[0][0][2]
            # prob_h = (keypoints[0][15][2] + keypoints[0][16][2]) / 2      눈 prob 평균
            prob_l = keypoints[0][2][2]
            prob_r = keypoints[0][5][2]

            self.dq_h.append(h)
            if prob_h<0.7: # 이전 좌표 가져옴
                # cnt.append((frame,"h"))
                # print("PROB_H < 0.7!!")
                self.dq_h.pop()
                if len(self.dq_h)==0:
                    continue
                val = self.dq_h.pop()
                self.dq_h.append(val)
                self.dq_h.append(val)
                h = val
            self.dq_l.append(l)
            if prob_l<0.7: # 이전 좌표 가져옴
                # cnt.append((frame,"l"))
                # print("PROB_L < 0.7!!")
                self.dq_l.pop()
                if len(self.dq_l)==0:
                    continue
                val = self.dq_l.pop()
                self.dq_l.append(val)
                self.dq_l.append(val)
                l = val
            self.dq_r.append(r)
            if prob_r<0.7: # 이전 좌표 가져옴
                # cnt.append((frame,"r"))
                # print("PROB_R < 0.7!!")
                self.dq_r.pop()
                if len(self.dq_r)==0:
                    continue
                val = self.dq_r.pop()
                self.dq_r.append(val)
                self.dq_r.append(val)
                r = val

            # print()
            # print("Head  :  ", h)
            # print("Left  :  ", l)
            # print("Right :  ", r)

            # print("\n< Prob >")
            # print("h: ", prob_h)
            # print("l: ", prob_l)
            # print("r: ", prob_r)

            # if self.frame==1: # frame 1, 2 가속도 계산x 처리
            #     self.center_old = np.array(self.get_center(h, l, r))
            #     continue
            # if self.frame==2:
            #     self.center_new = np.array(self.get_center(h, l, r))
            #     self.dist_old = distance.euclidean(self.center_new, self.center_old)
            #     continue

            self.center_new = np.array(self.get_center(h, l, r))
            self.dist_new = distance.euclidean(self.center_new, self.center_old)

            # if self.frame==1:
            #     self.dist_old = self.dist_new

            self.acc = abs(self.dist_new - self.dist_old)
            self.dist_old = self.dist_new
            self.center_old = self.center_new
            
            # if (acc > 2) or (acc < -2):
            #     self.cnt.append((frame,"acc"))
            if pass_list[-1] == 0:
                pass_list.append(1)
                continue
            if pass_list[-1] == 1:
                pass_list.clear()
                pass_list.append(-1)
                continue

            acc_array = np.append(acc_array, [[self.frame, self.acc]], axis = 0)
            print("\n< ACC >   :  ", self.acc)
            print("\n< VEL >   :  ", self.dist_new)
            fall = False
            if self.acc > 8:
                print("ACC > 8 DETECTION!")
                cv2.imwrite('../jy/jy_images/test/fall_expect_%f_%f.jpg' %(self.frame, self.acc), img)
                fall = self.fall_checking()

            if fall:
                print("Emergency!")
                cv2.imwrite('./image/fall.jpg', img)
                
                return fall

        end = time.time()
        print("OpenPose demo successfully finished. Total time: " + str(end - start) + " seconds")
        
        # for i in range(len(self.cnt)):
        #     print(self.cnt[i])
        ## npy파일 저장
        acc_np = np.array(acc_array)
        acc_np = np.delete(acc_np, 0, 0)
        np.save('/home/ahnsun98/fallDetection/openpose/build/examples/tutorial_api_python/workspace/jy/acc_dataset/test/kj02.npy', acc_np)