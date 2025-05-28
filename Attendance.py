import numpy as np
import face_recognition_models
import face_recognition
import cv2
import os

path = "attendeeImages"
images = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    curImage = cv2.imread(f'{path}/{cl}')
    images.append(curImage)
    fileName = os.path.splitext(cl)[0]
    classNames.append(fileName.split("_")[0] + " " + fileName.split("_")[1])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgEncodings = face_recognition.face_encodings(img)[0]
        encodeList.append(imgEncodings)

    return encodeList
print(classNames)

encodeListForKnownFaces = findEncodings(images)
print("Encoding Complete!")


# Using our webcam to see if the person is here
cap = cv2.VideoCapture(0)  # 0 is the id

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(imgS)
    encodingsCurrentFrame = face_recognition.face_encodings(imgS, facesCurrentFrame)

    for encodeFace, faceLocation in zip(encodingsCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListForKnownFaces, encodeFace)
        faceDistance = face_recognition.face_distance(encodeListForKnownFaces, encodeFace)
        # We will look for the image that has the lowest faceDistance
        print(faceDistance)
        bestMatchIndex = np.argmin(faceDistance)

        if matches[bestMatchIndex]:
            name = classNames[bestMatchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+ 6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    # We can opt to show the webcam
    cv2.imshow("Webcam", img)
    cv2.waitKey(1)



# imgTarget = face_recognition.load_image_file('imageBasics/will_ferrel.jpg')
# imgTarget = cv2.cvtColor(imgTarget, cv2.COLOR_BGR2RGB)
# imgTest = face_recognition.load_image_file("imageBasics/chad_smith.jpg")
# imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

