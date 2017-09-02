import cv2
import time
import numpy as np
import speech_recognition as sr
import pyttsx
import twilio
import twilio.rest
import os

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

cam = cv2.VideoCapture('burglar.mp4')

winName = "Movement Indicator"
# cv2.namedWindow(winName, cv2.WND_PROP_AUTOSIZE)

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_minus1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

(g, f) = cam.read()
m,n,o = f.shape
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('output.avi', fourcc, 10, (n,m))
 
while True:
  (grabbed, frame) = cam.read()
  crop_frame = frame.copy()
  display_frame = frame.copy()
  # time.sleep(.1)
  diff_image = diffImg(t_minus, t, t_plus)
  edges = diff_image
  new_image = frame.copy()
  x_offset=y_offset=0
  threshold = cv2.threshold(edges.copy(), 35, 255, cv2.THRESH_BINARY)[1]
  # Detect adges based on the image difference
  # edges = cv2.Canny(diff_image,10,200)
  cv2.imshow('frame', frame)
  cv2.imshow("edges1", threshold)
  # Find the maximum and minimum in both axis
  # (max1,min1) = (edges>0).nonzero()

   if len(max1) > 0:
       height =  max1.max() - max1.min()
       width =  min1.max() - min1.min()
       miny = max1.min()
       maxy = max1.max()
       minx = min1.min()
       maxx = min1.max()
      # print width * height
       if width > 0 and height > 0 and width * height > 6500:
           crop_frame = crop_frame[miny:maxy,minx:maxx]
      #     # print crop_frame.shape, new_image.shape
           # crop_frame = cv2.resize(crop_frame, (0,0),  fx = 1, fy = 1)
      #     new_image = new_image*0
           new_image[y_offset:y_offset+crop_frame.shape[0], x_offset:x_offset+crop_frame.shape[1]] = crop_frame
           doing = "Someone is there"
      #     print ("Someone is there")
           cv2.rectangle(display_frame, (minx, miny), (minx + width, miny + height), (0, 255, 0), 3)
           cv2.imshow("rectangle", display_frame)
           cv2.putText(display_frame, doing, (5, 545), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
           output.write(display_frame)
      #     print (1.0*width/height)
      #
           if 1.0*width/height > 1.8:
      #         print ("test")
               engine = pyttsx.init()
               engine.say('If you need help reply with yes or no?')
               engine.runAndWait()
               r = sr.Recognizer()
               with sr.Microphone() as source:
                   print("Say something!")
                   audio = r.listen(source)
                   try:
                         print("You said: " + r.recognize_google(audio))
                   except sr.UnknownValueError:
                         engine.say("Google Speech Recognition could not understand audio")
                         engine.runAndWait()
                   except sr.RequestError as e:
                         engine.say("Could not request results from Google Speech Recognition service; {0}".format(e))
                         engine.runAndWait()
                   # if r.recognize_google(audio) == "yes":
                         engine.say('Please stay still, Help is on the way')
                         twilio_account_sid = 'AC2d74ff88b931f6e3e50a0ac'
                         twilio_auth_token = '203e053b94acdc4b6c193'
                         print (twilio_account_sid)
                         client = twilio.rest.Client(twilio_account_sid, twilio_auth_token)
                         message = client.messages.create(
                             body="Ritesh is in trouble, he needs help",
                             to="+18123498991",
                             from_="+13174582882"
                             )
                         engine.runAndWait()
                         exit()

   else:
       doing = "No one is there"
       # print ("No one is there")
       cv2.putText(display_frame, doing, (5, 545), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
       output.write(display_frame)


  # Read next image
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
  t_minus1 = t1
  t1 = t_plus1
  t_plus1 = cv2.cvtColor(new_image, cv2.COLOR_RGB2GRAY)

  key = cv2.waitKey(1)
  if key == 27:
    cv2.destroyWindow(winName)
    break

# https://pythonspot.com/speech-recognition-using-google-speech-api/
# https://pythonspot.com/en/speech-recognition-using-google-speech-api/
# https://www.twilio.com/docs/tutorials/server-notifications-python-django#configuring-the-twilio-client
# http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
