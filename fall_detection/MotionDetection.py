import cv2


class MotionDetection:
    @staticmethod
    def find_max_contour(contours):
        max_contour = None
        max_area = 0
        second_max_contour = None
        for c in contours:
            area = cv2.contourArea(c)

            # if area >  6500 and area < 100000:  # These numbers depend on image size
            if area > max_area:
                second_max_contour = max_contour
                max_contour = c
                max_area = area

        return max_contour, second_max_contour

    @staticmethod
    def find_centroid(contour):
        M = cv2.moments(contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        return cx, cy


class DrawMotionDetection:

    def draw(self, bounding_box1, centroid1, bounding_box2, centroid2, contours, max_contour, image_out, thresh):

        if bounding_box1 is not None:
            # for b_box in bounding_box:
            (x1, y1, w1, h1) = bounding_box1
            # if w*h > 2000:
            cv2.rectangle(image_out, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 3)
            cx, cy = centroid1

            cv2.circle(image_out, (cx, cy), 2, (0, 255, 100), 10)
            cv2.circle(thresh, (cx, cy), 2, (0, 255, 100), 10)
        if bounding_box2 is not None:

            (x2, y2, w2, h2) = bounding_box2
            cv2.rectangle(image_out, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 3)
            # cv2.drawContours(image_out, [max_contour], 0, (0, 0, 255), 3)


        for i, c in enumerate(contours):
            area = cv2.contourArea(c)
            # if area > 7500:
            cv2.drawContours(image_out, max_contour, -1, (0, 255, 255), 1)
                # print("area",area)
