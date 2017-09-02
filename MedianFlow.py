import cv2
import sys

class MedianFlow():
    # Initialize the class
    def __init__(self):
        self.bbox = None
        self.ok = None
        self.tracker = None

    # Initialize the parameters
    def init_params(self, frame):
        self.tracker = cv2.Tracker_create("MEDIANFLOW")
        self.bbox = (7, 73, 106, 290)
        self.ok = tracker.init(frame, bbox)


    # Track person in a frame based on the coordinates set initially
    def track_person(self,frame ):
        self.ok, self.bbox = self.tracker.update(frame)
        # print (ok)
        # Draw bounding box
        if self.ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0, 0, 255))

        # Display result
        cv2.imshow("Tracking", frame)
