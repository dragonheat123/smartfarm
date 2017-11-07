# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 20:40:27 2017

@author: lorky
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('C://Users//lorky//Desktop//smartfarm//2.jpg')
pts1 = np.array([[0,0],[640,0],[0,380],[640,360]])
pts2 = np.array([[0,0],[640,0],[0,480],[640,480]])

h, status = cv2.findHomography(pts1, pts2)

dst = cv2.warpPerspective(img,h,(640,480))
cv2.imshow('dst',dst)

kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
im = cv2.filter2D(gray, -1, kernel)
cv2.imshow("Sharpening",im)
#
#aw = cv2.addWeighted(dst, 4, cv2.blur(dst, (50, 50)), -4, 150)
#cv2.imshow("Add_weighted", aw)

img2 = cv2.copyMakeBorder(dst,10,10,10,10,cv2.BORDER_CONSTANT)

gray = cv2.cvtColor(dst,cv2.COLOR_BGR2GRAY)
constant= cv2.copyMakeBorder(gray,10,10,10,10,cv2.BORDER_CONSTANT)

edges = cv2.Canny(constant,50,100)                      ###from grayscale
cv2.imshow('canny',edges)

edges2 = cv2.Canny(img2,120,170)                         ###from color
cv2.imshow('canny2',edges2)

map = cv2.add(edges2,edges)


kernel = np.ones((2,2),np.uint8)
map=cv2.dilate(map,kernel,iterations=5)

cv2.imshow('map',map)

map2 = map.copy()

im2, contours, hierarchy = cv2.findContours(map2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
draw = cv2.drawContours(img2, contours, -1, (0,255,0), 3)
cv2.imshow('drawn',draw)


for i in range(0,len(contours)):
    if cv2.contourArea(contours[i])<50:
        map2 = cv2.drawContours(map2,contours, i , color=(0,0,0), thickness=cv2.FILLED)
        print('filling')
        
cv2.imshow('map2',map2)        


kernel = np.ones((2,2),np.uint8)
dilatemore=cv2.dilate(map,kernel,iterations=5)

cv2.imshow('dilatemore',dilatemore)


im3, contours2, hierarchy2 = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
draw = cv2.drawContours(img2, contours, -1, (0,255,0), 3)
cv2.imshow('drawn2',img2)

cv2.imwrite('cropped.jpg',dst)