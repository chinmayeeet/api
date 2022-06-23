
import numpy as np
import cv2

def read_transparent_png(filename):
    image_4channel = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    alpha_channel = image_4channel[:,:,3]
    rgb_channels = image_4channel[:,:,:3]

    # Alpha factor
    alpha_factor = alpha_channel[:,:,np.newaxis].astype(np.float32) / 255.0
    alpha_factor = np.concatenate((alpha_factor,alpha_factor,alpha_factor), axis=2)

    base = rgb_channels.astype(np.float32) * alpha_factor
    final_image = base 
    return final_image.astype(np.uint8)

def chpers(filename, ext):
 if(ext == "png"):
   img = read_transparent_png(filename)
 else:
   img = cv2.imread(filename)
 imgc = img.copy()
 img1 = img.copy()
 out = img.copy()
 y,x,z = img.shape
 ratio = img.shape[0] / 300.0
 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 #cv2.imshow('gray',gray)
 # find contours

 contours, hierarchy = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
 cv2.drawContours(imgc, contours, -1, (0,255,0), 2, cv2.LINE_AA)
 print ("contours:",len(contours))
 print ("largest contour has ",len(contours[0]),"points")
 #cv2.imshow('contours',imgc)
 # minAreaRect

 rect = cv2.minAreaRect(contours[0])
 box = cv2.boxPoints(rect)
 pts1 = box
 box = np.int0(box)


 cv2.drawContours(img1,[box],0,(255,255,255),3)
 #cv2.imshow('minAreaRect',img1)

 pts = box.reshape(4, 2)
 rect = np.zeros((4, 2), dtype = "float32")
 s = pts.sum(axis = 1)
 rect[0] = pts[np.argmin(s)]
 rect[2] = pts[np.argmax(s)]
 diff = np.diff(pts, axis = 1)
 rect[1] = pts[np.argmin(diff)]
 rect[3] = pts[np.argmax(diff)]

 (tl, tr, br, bl) = rect
 print(tl,tr,br,bl)
 widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
 widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
 # ...and now for the height of our new image
 heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
 heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
 # take the maximum of the width and height values to reach
 # our final dimensions
 maxWidth = max(int(widthA), int(widthB))
 maxHeight = max(int(heightA), int(heightB))
 # construct our destination points which will be used to
 # map the screen to a top-down, "birds eye" view
 dst = np.array([
	[0, 0],
	[maxWidth - 1, 0],
	[maxWidth - 1, maxHeight - 1],
	[0, maxHeight - 1]], dtype = "float32")
 # calculate the perspective transform matrix and warp
 # the perspective to grab the screen
 M = cv2.getPerspectiveTransform(rect, dst)
 print(rect, dst, maxWidth, maxHeight)
 out = cv2.warpPerspective(img, M, (  maxWidth, maxHeight))
 #cv2.imshow('final image', out)
 print("success")
 return out




