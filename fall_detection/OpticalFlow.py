import cv2
import numpy as np
# cap = cv2.VideoCapture(0)
# ret, frame1 = cap.read()
# prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
# hsv = np.zeros_like(frame1)
# hsv[...,1] = 255

class OpticalFlow:
    def __init__(self):
        self.flow_value = 0
    def identify_movement(self,next, prvs):
        flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 10, 3, 5, 1.2, 0)
        self.flow_value = np.sum(np.fabs(flow))
        # print self.flow_value
        # mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        # hsv[...,0] = ang*180/np.pi/2
        # hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        # bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
        # cv2.imshow('frame2',bgr)
        return self.flow_value
    def find_motion(self, flow_value):
        if self.flow_value < 180211.0:
            print ("Low motion")
        elif self.flow_value > 180211.0 and self.flow_value < 253436.0:
            print ("Medium Motion")
        elif self.flow_value > 253436.0:
            print ("High Motion")


