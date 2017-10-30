# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 20:40:27 2017

@author: lorky
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('C://Users//lorky//Desktop//smartfarm//2.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

cv2.imshow('gray',gray)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

kernel = np.ones((1,1),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
sure_bg = cv2.dilate(opening,kernel,iterations=3)
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)
ret, markers = cv2.connectedComponents(sure_fg)
markers = markers+1
markers[unknown==255] = 0
markers = cv2.watershed(img,markers)
img[markers == -1] = [255,0,0]
output=img.copy()
cv2.imshow('dfs',img)
for i in np.argwhere(markers==-1):
    output = cv2.circle(output,tuple([i[1],i[0]]), 1, (0,0,255), -1)
cv2.imshow('dfs',output)


#edges = cv2.Canny(thresh,50,100)
#cv2.imshow('edges',edges)
#kernel = np.ones((2,2),np.uint8)
#dilate = cv2.dilate(edges,kernel,iterations = 2)
#cv2.imshow('dilate',dilate)
##invert_image = cv2.bitwise_not(edges)
##output = cv2.addWeighted(invert_image,0.5,gray,0.1,0)
##cv2.imshow('output',output)
#
#ret, thresh = cv2.threshold(dilate,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
#cv2.imshow('threshold',thresh)
#
#cnted, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#cv2.imshow('cnted',cnted)
#contour_num=[]
#output = img.copy()
#a=[]
#for i in range(0,len(contours)-1):
#    if cv2.contourArea(contours[i])>0:
#        a.append(cv2.moments(contours[i])['m00'])
#        #epsilon = 0.01*cv2.arcLength(contours[i],True)
#        #contours[i] = cv2.approxPolyDP(contours[i],epsilon,True)
#        #contours[i] = cv2.convexHull(contours[i])
#        output = cv2.drawContours(output, contours, i, (0,255,0), 2)
#
#
#cv2.imshow('draw',output)
#
##invert_image = cv2.bitwise_not(thresh)
##
##cv2.imshow('invert',invert_image)
##
##
###kernel = np.ones((5,5),np.uint8)
###dilate = cv2.dilate(edges,kernel,iterations = 2)
##
###cv2.imshow('dilate',dilate)
##
##
##ret, thresh = cv2.threshold(dilate,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
##
##cv2.imshow('img',img) 
##
##cv2.imshow('thresh',thresh) 
##
#kernel = np.ones((1,1),np.uint8)
#opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
##
##
#cv2.imshow('opening',opening)
#
