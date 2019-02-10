import sys
import cv2

# Read the image. The first command line argument is the image
# Second argument is a flag which specifies the way image should be read.
# cv2.IMREAD_COLOR : Loads a color image. Any transparency of image will be neglected. It is the default flag.
# cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode
# cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel
image = cv2.imread(sys.argv[1])

# load the OpeCV default cascade for detecting faces 
cascPath = './cascades/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascPath)

#convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
'''
The detectMultiScale function is a general function that detects objects. Since we are calling it on the face cascade, that’s what it detects. The first option is the grayscale image.
The second is the scaleFactor. Since some faces may be closer to the camera, they would appear bigger than those faces in the back. The scale factor compensates for this.
The detection algorithm uses a moving window to detect objects. minNeighbors defines how many objects are detected near the current one before it declares the face found. minSize, meanwhile, gives the size of each window.
'''
faces = face_cascade.detectMultiScale(
    gray_image,
    scaleFactor = 1.2,
    minNeighbors = 5,
    minSize = (30,30)
    )

print("Found {0} faces!".format(len(faces)))
 
# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Faces found" ,image)

# wait for ESC key to quit
k = cv2.waitKey(0) & 0xFF
if k == 27: # ESC
  cv2.destroyAllWindows()

#Use the function cv2.imwrite() to save an image.
#First argument is the file name, second argument is the image you want to save.
#cv2.imwrite('faces.png',image)
