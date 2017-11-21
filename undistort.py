# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:01:14 2017

@author: lorky
"""

import cv2
import numpy as np

K = np.array([[  360,     0.  ,  400],
              [    0.  ,   360,   300],
              [    0.  ,     0.  ,     1.  ]])

# zero distortion coefficients work well for this image
D = np.array([0., 0., 0., 0.])

# use Knew to scale the output
Knew = K.copy()
Knew[(0,1), (0,1)] = 0.4 * Knew[(0,1), (0,1)]


img = cv2.imread('C://Users//lorky//Desktop//smartfarm//now.jpg')
cv2.imshow('now',img)
img_undistorted = cv2.fisheye.undistortImage(img, K, D=D, Knew=Knew)
cv2.imwrite('fisheye_sample_undistorted.jpg', img_undistorted)
cv2.imshow('undistorted', img_undistorted)
#
pts1 = np.array([[304,170],[552,162],[295,383],[533,403]])
pts2 = np.array([[0,0],[640,0],[0,480],[640,480]])

h, status = cv2.findHomography(pts1, pts2)

dst = cv2.warpPerspective(img_undistorted,h,(640,480))
cv2.imshow('dst',dst)


gray = cv2.cvtColor(dst,cv2.COLOR_BGR2GRAY)
cv2.imshow('gray',gray)

th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,2501,2)
cv2.imshow('th2',th2)

th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,2501,11)
cv2.imshow('th3',th3)

kernel = np.ones((2,2),np.uint8)
open=cv2.morphologyEx(th3,cv2.MORPH_OPEN,kernel,iterations=2)
cv2.imshow('open',open)




im2, contours, hierarchy = cv2.findContours(open,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
draw = cv2.drawContours(dst, contours, -1, (0,255,0), 3)
cv2.imshow('drawn',draw)

for i in range(0,len(contours)):
    if cv2.contourArea(contours[i])<50:
        map2 = cv2.drawContours(open,contours, i , color=(0,0,0), thickness=cv2.FILLED)
        print('filling')
        
cv2.imshow('map2',map2)
        
    




