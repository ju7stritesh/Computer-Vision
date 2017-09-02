import threading
import time
# from scipy import ndimage
import cv2
import numpy as np
import BackgroundSubtractor
import MotionDetection
from PIL import Image
import imutils


cv2.ocl.setUseOpenCL(False)

md = MotionDetection.MotionDetection()
drawmd = MotionDetection.DrawMotionDetection()

reset_background_delay = 0

peep_ident = None
image = None
quit = False
sub = None


class FrameRate:
    last_frame = 0
    avg = 40
    count = 0
    f_sum = 0

    def print_frame_rate(self):
        now = time.time()
        self.f_sum += now - self.last_frame

        self.count += 1
        if self.count >= self.avg:
            frate = round(self.avg / self.f_sum)
            # print(str(frate) + ' fps')
            self.count = 0
            self.f_sum = 0
        self.last_frame = now
        return


fr = FrameRate()


def cam_backsub_loop(frame_lock):
    # cv2.namedWindow("Threshold", cv2.WND_PROP_AUTOSIZE)
    # cv2.moveWindow("Threshold", 100, 100)
    cv2.namedWindow("Camera", cv2.WND_PROP_AUTOSIZE)
    cv2.moveWindow("Camera", 50, 50)
    # cv2.namedWindow("bkgrd", cv2.WND_PROP_AUTOSIZE)
    # cv2.moveWindow("bkgrd", 100, 100)

    frame_num = 0

    last_identity = "none"
    doing = 'waiting'

    camera = cv2.VideoCapture("burglar.mp4")
    cv2.ocl.setUseOpenCL(False)
    bgsub = BackgroundSubtractor.BackGroundSubtraction()
    global peep_ident
    global image, sub
    global quit
    timer = 0
    (grabbed1, frame1) = camera.read()
    m,n,o = frame1.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter('output.avi', fourcc, 10, (n,m))
    while True:

        (grabbed, frame) = camera.read()
        # time.sleep(0.1)
        # cv2.imshow('gray_image',frame)
        frame = imutils.resize(frame, width=min(400, frame.shape[1]))
        if not grabbed:
            print('Camera read failed. No camera plugged in?')
            break
        new_frame = frame
        # cv2.imshow("before", frame)
        kernel = np.array([[-1,-1,-1,-1,-1],
                             [-1,2,2,2,-1],
                             [-1,2,8,2,-1],
                             [-1,2,2,2,-1],
                             [-1,-1,-1,-1,-1]]) / 8.0 # Applying filter for edge enhancement
        frame = cv2.filter2D(frame, -1, kernel)
        img_yuv = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0]) #for better contrast

        # convert the YUV image back to RGB format
        frame = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

        # cv2.imshow("after", frame)
        with frame_lock:
            # if image is None:
            image = frame.copy()
        edges1 = cv2.Canny(new_frame,100,200)
        # edges1 = cv2.medianBlur(edges1.copy(), 3)
        edges2 = cv2.Canny(image,50,200)
        edges3 = edges1-edges2
        # frame = edges3
        # cv2.imshow('edges3', edges3)

        contours, threshold, subtracted = bgsub.do_backgroundsubtract(frame)
        bounding_box1, centroid1, bounding_box2, centroid2, maxcontour = bgsub.bounding_box_centroid(contours)
        drawmd.draw(bounding_box1, centroid1, bounding_box2, centroid2, contours, maxcontour, frame, threshold)
        if bounding_box1 is not None:
            print bounding_box1[2]*bounding_box1[3]
        identity = peep_ident
        cv2.putText(frame, identity, (5, 580), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
        cv2.putText(frame, doing, (5, 545), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))

        path = 'Frames3/vid%s.jpg' % frame_num
        cv2.imwrite(path, frame)

        cv2.imshow("Camera", frame)
        # cv2.imshow("Threshold", threshold)
        # cv2.imshow('bkgrd', subtracted)
        output.write(frame)
        if isinstance(bounding_box1, tuple):
            if float(bounding_box1[2])/(bounding_box1[3]) > 1.6:
                timer += 1
                if timer > 5:
                    doing = 'fallen'
                    cv2.putText(frame, doing, (5, 545), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    print (timer)
            else:
                doing = "waiting"
                cv2.putText(frame, doing, (5, 545), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
                timer = 0
        else:
            doing = "waiting"
            cv2.putText(frame, doing, (5, 545), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        fr.print_frame_rate()

    quit = True
    camera.release()
    output.release()
    cv2.destroyAllWindows()

frame_lock = threading.Lock()
t1 = threading.Thread(target=cam_backsub_loop, name='backsub', args=(frame_lock,))
# t = threading.Thread(target=identify_people_thread, name='people', args=(frame_lock,))
t1.start()
# t.start()
t1.join()
# t.join(timeout=3)
# http://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html
# http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
# http://docs.opencv.org/3.1.0/d4/d13/tutorial_py_filtering.html
# http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
# http://docs.opencv.org/3.2.0/d4/d73/tutorial_py_contours_begin.html
# http://www.pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/
