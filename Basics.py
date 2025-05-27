import cv2
import numpy as np
import face_recognition_models
import face_recognition

imgTarget = face_recognition.load_image_file('imageBasics/will_ferrel.jpg')
imgTarget = cv2.cvtColor(imgTarget, cv2.COLOR_BGR2RGB)

imgTest = face_recognition.load_image_file("imageBasics/chad_smith.jpg")
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)


# This step is looking for the face locations

# We get the locations of the face of our images
targetFaceLocation = face_recognition.face_locations(imgTarget)[0]
print("Target Face Location: ", targetFaceLocation)  # Locations are (top, right, bottom, left)
# Essentially, this gives you the (y-axis of top, x-axis of right, y-axis of bottom, x-axis of left)
encodeTarget = face_recognition.face_encodings(imgTarget)[0]
cv2.rectangle(imgTarget, (targetFaceLocation[3], targetFaceLocation[0]), (targetFaceLocation[1], targetFaceLocation[2]),(255, 0, 255), 2)

testFaceLocation = face_recognition.face_locations(imgTest)[0]
print("Test Face Location: ", testFaceLocation)
encodeTest = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest, (testFaceLocation[3], testFaceLocation[0]), (testFaceLocation[1], testFaceLocation[2]),(255, 0, 255), 2)

results = face_recognition.compare_faces([encodeTarget], encodeTest)
print(results)  # If return True, then they believe to be the same person, if false they believe to be different person
faceDistance = face_recognition.face_distance([encodeTarget], encodeTest);
# print(faceDistance) # The lower the distance, the better the match
cv2.putText(imgTest, f'{results[0]} {round(faceDistance[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)


# Showing the images

cv2.imshow("Will Ferrel", imgTarget)
cv2.imshow("Will Ferrel Test", imgTest)
cv2.waitKey(0)








