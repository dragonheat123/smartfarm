# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 21:43:31 2017

@author: lorky
"""

import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import sys

dbx = dropbox.Dropbox("-maRW30I7sAAAAAAAAAAC6tQJp7TB2pp7-qZQ9mijGMPqhE4F48G3eMslstwzbZo")

a=dbx.users_get_current_account()

imagepath = 'C:/Users/lorky/Desktop/smartfarm/1.jpg'
dbpath = '/pic2.jpg'

def uploadimg():
    with open(imagepath, 'rb') as f:
        print("Uploading to Dropbop...")
        try:
            dbx.files_upload(f.read(), dbpath, mode=WriteMode('overwrite'))
        except ApiError as err:file:///G:/10112017.py
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()
                
uploadimg()


a = 0

while a<10:
    try:
        a+=1
        print(a)
    except a>4:
        print('kjh')
        