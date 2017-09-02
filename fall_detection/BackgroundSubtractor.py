import cv2
import numpy as np
import MotionDetection

cv2.ocl.setUseOpenCL(False)

class BackGroundSubtraction:
    bcksubMOG2 = cv2.createBackgroundSubtractorMOG2(500, 100, True)
    md = MotionDetection.MotionDetection()

    @staticmethod
    def __thresholding(subtracted):
        # Remove MOG2 shadows = 127
        # cv2.imshow("the", subtracted)
        threshold = cv2.threshold(subtracted.copy(), 128, 255, cv2.THRESH_BINARY)[1]

        threshold = cv2.blur(threshold.copy(), (31, 31))
        # cv2.imshow("the", subtracted)
        threshold = cv2.threshold(threshold.copy(), 50, 255, cv2.THRESH_BINARY)[1]
        # cv2.imshow("the", subtracted)
        kernel = np.ones((5, 5), np.uint8)
        threshold = cv2.dilate(threshold, kernel, iterations=5)
        threshold = cv2.erode(threshold, kernel, iterations=5)

        # threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
        # threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
        # threshold = cv2.threshold(threshold, 128, 255, cv2.THRESH_BINARY)[1]
        # cv2.imshow("threshold", threshold)
        return threshold

    def do_backgroundsubtract(self, image):
        subtracted = self.bcksubMOG2.apply(image)
        threshold = self.__thresholding(subtracted)
        # cv2.imshow("threshold", threshold)
        # subtracted = cv2.Canny(subtracted,240,255)
        (im2, contours, hierarchy) = cv2.findContours(threshold.copy(), cv2.RETR_TREE,
                                                      cv2.CHAIN_APPROX_SIMPLE)

        return contours, threshold, subtracted

    def bounding_box_centroid(self, contours):
        bounding_box1 = None
        centroid1 = None
        bounding_box2 = None
        centroid2 = None
        # b_box = []
        contours1 = None
        maxcontour = None
        second_max_contour = None
        maxcontour, second_max_contour = self.md.find_max_contour(contours)
        if maxcontour is not None:
            bounding_box1 = cv2.boundingRect(maxcontour)
            centroid1 = self.md.find_centroid(maxcontour)
            # contours1= maxcontour
        if second_max_contour is not None:
            bounding_box2 = cv2.boundingRect(second_max_contour)
            centroid2 = self.md.find_centroid(second_max_contour)
        # if second_max_contour is not None:
        #     bounding_box.append(cv2.boundingRect(second_max_contour))
        #     centroid.append(self.md.find_centroid(second_max_contour))
        #     contours1.append(second_max_contour)
        # for contour in contours:
        #     b_box.append(cv2.boundingRect(contour))
        # if not bounding_box:
        #     (x, y, w, h) = bounding_box
        #     # if w*h < 8000:
            #     bounding_box = None
        # print b_box, bounding_box
        return bounding_box1, centroid1, bounding_box2, centroid2, contours
