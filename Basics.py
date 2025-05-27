import cv2
import numpy as np
import face_recognition_models
import face_recognition

imgTarget = face_recognition.load_image_file('imageBasics/will_ferrel.jpg')
imgTarget = cv2.cvtColor(imgTarget, cv2.COLOR_BGR2RGB)

imgTest = face_recognition.load_image_file("imageBasics/will_ferrel_test.jpg")
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)




cv2.imshow("Will Ferrel", imgTarget)
cv2.imshow("Will Ferrel Test", imgTest)
cv2.waitKey(0)








