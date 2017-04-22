#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created by BoBo and Bexx
import os
import time
from time import sleep
import picamera
from picamera import PiCamera
import RPi.GPIO as GPIO
import atexit
import sys
import random
import pygame

import smtplib # for email
from email.mime.text import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

#import cups    # for printing
import glob
import gc
from PIL import Image
from signal import alarm,signal,SIGALRM,SIGKILL
import subprocess

#--------Variablen Konfiguration-------
camera = PiCamera()

# ilyama prolite e17 monitor resolution
w = 1280
h = 1024

# 16:9:
#bexx w = 1920
#bexx h = 1080

# Picture format
pic_w = 15
pic_h = 10

# PiCamera resolution in picture format
cam_w = 2880
cam_h = (cam_w * pic_h) / pic_w
cam_rotation = 0

#button1_pin = 37 # pin for the big red button
#led1_pin = 37 # LED 1

# emailserver
smtpserver='smtp.gmail.com:587' # 465
server = smtplib.SMTP(smtpserver)

file_path = "/home/pi/Desktop/Bilder/"
#current_picture_name = file_path

restart = True

#--------OtherConfig-----------

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(led1_pin,GPIO.OUT) # LED 1
#GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # falling edge detection on button 1
#GPIO.output(led1_pin,False);
#GPIO.add_event_detect(button1_pin, GPIO.FALLING)

#--------Mailing---------------
def connectToSmtpServer():
    server.starttls()
    problem = server.login('rebecca.luehmann@gmail.com','****')
    print problem

def sendMail(send_from, send_to, subject, text, current_picture_name, server0="smtp.gmail.com:587"):

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    #msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    #part = MIMEBase('application', "octet-stream")
    #part.set_payload(open(current_picture_name, "rb").read())
    #Encoders.encode_base64(part)

    fp = open(current_picture_name, 'rb')
    #print "sending email"
    print fp
    msgImage = MIMEImage(fp.read())
    #print "read finished"
    fp.close()
    #print "fd closed"
    msgImage.add_header('Content-ID', '<image1>')
    #print "header added"
    msg.attach(msgImage)
    print "sending email"
    #part.add_header('Content-Disposition', 'attachment; filename="' + current_picture_name + '"')

    #msg.attach(part)
##    for f in files or []:
##        with open(f, "rb") as fil:
##            part = MIMEApplication(
##                fil.read(),
##                Name=basename(f)
##            )
##            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
##            msg.attach(part)
    problem = server.sendmail(send_from, send_to, msg.as_string())
    print "email send"
    print problem

def lockout():
    problem = server.quit()
    print problem

    
#--------Funktionen------------

def exit_photobooth():
    sleep(0.5)
    os.system("sudo reboot")

def countdown_overlay( ):#camera ):
    n = 4
    for i in range (1, n):
        gc.collect()
        img = Image.open("/home/pi/Desktop/Bilder/"+str(4-i)+".png")
        pad = Image.new("RGB" , (
            ((img.size[0] + 31) // 32) * 32,
            ((img.size[1] + 15) // 16) * 16,
            ))
        pad.paste(img, (0, 0))
        o = camera.add_overlay(pad.tostring(), size=img.size)
        o.alpha = 100
        o.layer = 3
        sleep(2)
        camera.remove_overlay(o)
    del img
    del pad

def start_camera():
    print "Get Ready" 
    #bexx camera = PiCamera() is global now
    camera.resolution = (w, h)
    camera.framerate = 24
    camera.vflip = True
    camera.hflip = True
    camera.rotation = cam_rotation
    camera.start_preview()

def stop_camera():
    print "byebye"
    camera.stop_preview()
    #camera.close()
    
def takePicture():
    countdown_overlay()

    print "Taking Pictures"
                
    #bobo pygame.init()
    #bobo screen = pygame.display.set_mode((640,480),pygame.FULLSCREEN)
    now = time.strftime("%Y%m%d%H%M%S")
    current_picture_name = file_path + now +".jpg"
    print current_picture_name
    camera.resolution = (2880,  2304)
    camera.capture(current_picture_name)

    
    #bobo screen.blit(img,(0,0))
    #bobo pygame.display.flip()

    return current_picture_name

def printPicture():
    pass
    #bexx http://www.howtogeek.com/169679/how-to-add-a-printer-to-your-raspberry-pi-or-other-linux-computer/

def mailPicture(current_picture_name):
    send_to = raw_input('An welche Adresse soll dieses Bild gesendet werden?')
    connectToSmtpServer()
    sendMail("rebecca.luehmann@gmail.com", send_to, "SPD Wahlkreiskonferenz am 11.02.2017", "Hier kommt Dein persoenliches Erinnerungsfoto.", current_picture_name, "smtp.gmail.com:587")
    lockout()

def askEmailAdress():
    adress = ""
    font = pygame.font.Font(None, 50)
    while True:
        for event in pygame.event.get():
            if eventevt.type == KEYDOWN:
                if eventevt.key == K_RETURN:
                    name = ""
                elif eventevt.key == K_BACKSPACE:
                    name = name[:-1]
                else: name += eventevt.unicode
            elif evt.type == QUIT:
                return

#---Hauptprogramm---

pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("SPD_Fotobox")
gc.enable()

breakp = False
print "OK"

while True:
    if restart:
        start_camera()
        pygame.init()
        screen = pygame.display.set_mode((640,480))
        pygame.display.set_caption("SPD_Fotobox")
        gc.enable()
        restart = False

    for i in range (4):
        sleep(0.5)
        for event in pygame.event.get():
            # event = pygame.event.poll()
            if(event.type == pygame.KEYUP): # or (restart == True):
                print "keyup event detected"
                print event.key
                #print(event)
                if (event.key == pygame.K_RETURN): 
                    imgName = takePicture()
                    stop_camera() 
                    #processPicture()
                    mail = raw_input('Sollen wir Dir dieses Bild zumailen? Tippe j oder n: ')
                    if "j" in mail:
                        mailPicture(imgName)
                    sys.exit()
                elif(event.key == pygame.K_ESCAPE):
                    stop_camera()
                    breakp = True

sys.exit()
        
    
    
