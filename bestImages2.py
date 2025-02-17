import cv2
import os 
import numpy as np
import shutil

#find video to use
homeDirectory = os.listdir()
#print(homeDirectory)
for file in homeDirectory:
    found = False
    if file.find(".mp4") != -1:
        videoName = file
        found = True
        break
if not found:
    print("no .mp4 found!")
    exit()
else:
    print("using " + videoName)

cap = cv2.VideoCapture(videoName)

#count number of frames in video
totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print("frame count (may be innacurate): " + str(totalFrames))

#user input for number of images
keepNumber = int(input("number of photos to keep: "))
#get images folder name
imagesFolder = videoName + "_" + str(keepNumber) + "_photos"
print("saving images to: " + imagesFolder)
#make images folder
if os.path.isdir(imagesFolder):
    print("replacing: " + imagesFolder)
    shutil.rmtree(imagesFolder)
os.mkdir(imagesFolder)

def getVariance(frame):
    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply the Laplacian function
    dst = cv2.Laplacian(gray, cv2.CV_64F)
    # Calculate the variance of the Laplacian
    variance = np.var(dst)

    return variance

os.chdir(imagesFolder)

ret = True
imageNumber = 0
while(ret):
    imageNumber += 1
    bestVariance = 0
    worstVariance = 0
    for y in range (int(totalFrames/keepNumber)):
        ret, currentFrame = cap.read()
        if ret:
            variance = getVariance(currentFrame)
            if variance > bestVariance:
                bestVariance = variance
                bestFrame = currentFrame
            if worstVariance == 0:
                worstVariance = variance
            if worstVariance > variance:
                worstVariance = variance
    if ret: 
        cv2.imwrite("frame" + str(imageNumber) + ".jpeg", bestFrame)
        print("Frame(current/total): " + str(imageNumber) + "/" + str(keepNumber) + ", Sharpness(chosen/worst): " + str(int(bestVariance)) + "/" +str(int(worstVariance)) + "        ", end='\r')
print("Frame(current/total): " + str(imageNumber) + "/" + str(keepNumber) + ", Sharpness(chosen/worst): " + str(int(bestVariance)) + "/" +str(int(worstVariance)) + "        ")



