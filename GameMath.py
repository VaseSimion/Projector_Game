


#*****************************************************************************************************************
#*********   this version of the game has squares as wright figure and circles as the forbiden one      **********
#*****************************************************************************************************************

import cv2
import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import time

def ScaleY(value):
	return int(125 + 0.484*value)
	
def ScaleX(value):
	return int(35+0.609*value)


class GameData:
	def __init__(self):
		self.timer=0
		self.cap=0
		self.state='INIT'
		self.xmapping=0
		self.ymapping=0
Game=GameData()

def imageFindonCamera(Game,template,position_x,position_y, tolerance, threshold = 0.7):
	ret, img_rgb = Game.cap.read()
	cv2.waitKey(200)
	match = 0 
	tolerance = 3
	counter = 0
	while(True):
		counter = counter +1
		w, h = template.shape[::-1]
		#print(w,h)
		ret, img_rgb = Game.cap.read()
		img_rgb=img_rgb[position_y-tolerance:position_y+h+tolerance, position_x-tolerance:position_x+w+tolerance]
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
		res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	
		cv2.imshow('res',img_rgb)
		
		print(max_val)
#		print(max_loc)
	
		#threshold = 0.75

		if (max_val > threshold):
			cv2.rectangle(img_rgb, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,0,255), 2)	
			match = 1
			
			break

	
		if cv2.waitKey(1) & 0xFF == ord('q'):
			match=1
			break
		
		if counter >0:
			cv2.destroyWindow("res")
			break
	return match

def Initialization(Game):
	
	Game.cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
	Game.timer=1000
	ret, img_rgb = Game.cap.read()
	#print on the projector where the PCBA should be placed in Projector window
	Start= cv2.imread('start.png',1)
	cv2.imshow('Projector',Start)	

	cv2.waitKey(100)
	for i in range(5):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
	
	Start=cv2.cvtColor(img_rgb[290:380,115:255], cv2.COLOR_BGR2GRAY)

	while(imageFindonCamera(Game,Start,115,290,60,0.8) == 1):
		state='INIT' #actually this does nothing as it does not get out of the loop 
	
	board = cv2.imread('blank.png',1)

	#write additional text
	cv2.putText(board,'Get ready',(200,200), cv2.FONT_HERSHEY_SIMPLEX, 4,(255,255,255),4,cv2.LINE_AA)
	#project image drawn
	cv2.imshow('Projector',board)
	cv2.waitKey(500)
	#do other stuff 3 2 1
	cv2.waitKey(500)
	
	Game.state='FIRSTFIGURE'
	return Game.state		
 
def FirstFigure(Game):
	#declare the coordinates for the figures drawn:
	#square as corners
	SquarePoint11=(200,50)
	SquarePoint12=(400,250)
	
	SquarePoint21=(500,50)
	SquarePoint22=(700,250)
	
	SquarePoint31=(25,350)
	SquarePoint32=(225,550)
	
	SquarePoint41=(250,350)
	SquarePoint42=(450,550)
	
	SquarePoint51=(475,350)
	SquarePoint52=(675,550)
	
	SquarePoint61=(700,350)
	SquarePoint62=(900,550)
	
	#import black picture to have a black canvas to draw on
	board= cv2.imread('blank.png',1)
	
	#draw rectangles for numbers
	cv2.rectangle(board,SquarePoint11,SquarePoint12,(0,255,0),-1)
	cv2.rectangle(board,SquarePoint21,SquarePoint22,(0,255,0),-1)
	
	cv2.rectangle(board,SquarePoint31,SquarePoint32,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint41,SquarePoint42,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint51,SquarePoint52,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint61,SquarePoint62,(0,0,255),-1)
	
	#write the numbers
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(board,'1',(SquarePoint11[0]+55,SquarePoint12[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'2',(SquarePoint21[0]+55,SquarePoint22[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'3',(SquarePoint31[0]+55,SquarePoint32[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)	
	cv2.putText(board,'4',(SquarePoint41[0]+55,SquarePoint42[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'5',(SquarePoint51[0]+55,SquarePoint52[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)	
	cv2.putText(board,'6',(SquarePoint61[0]+55,SquarePoint62[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)

	#write additional text
	cv2.putText(board,'+',(SquarePoint12[0]+2,SquarePoint12[1]-50), font, 4,(255,255,255),4,cv2.LINE_AA)
	
	#project image drawn
	cv2.imshow('Projector',board)
	
	#create templates for what needs to be clicked (templatecorrect) and the thing that is not to be touched (templategresit)
	cv2.waitKey(100)
	for i in range(3):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
	
	templatecorrect=cv2.cvtColor(img_rgb[ScaleY(SquarePoint31[1]):ScaleY(SquarePoint32[1]),ScaleX(SquarePoint31[0]):ScaleX(SquarePoint32[0])], cv2.COLOR_BGR2GRAY)
	templategresit1=cv2.cvtColor(img_rgb[ScaleY(SquarePoint41[1]):ScaleY(SquarePoint42[1]),ScaleX(SquarePoint41[0]):ScaleX(SquarePoint42[0])], cv2.COLOR_BGR2GRAY)
	templategresit2=cv2.cvtColor(img_rgb[ScaleY(SquarePoint51[1]):ScaleY(SquarePoint52[1]),ScaleX(SquarePoint51[0]):ScaleX(SquarePoint52[0])], cv2.COLOR_BGR2GRAY)
	templategresit3=cv2.cvtColor(img_rgb[ScaleY(SquarePoint61[1]):ScaleY(SquarePoint62[1]),ScaleX(SquarePoint61[0]):ScaleX(SquarePoint62[0])], cv2.COLOR_BGR2GRAY)
	
	#look for the right thing, if found it will get out of while, if not it will look for the forbidden thing to touch
	#if the forbiden thing is touched the score becomes 0 and the game ends, if not we repeat until one of the two is touched
	while(imageFindonCamera(Game,templatecorrect,ScaleX(SquarePoint31[0]),ScaleY(SquarePoint31[1]),60,0.8)==1):
		Game.timer-=1
		if(imageFindonCamera(Game,templategresit1,ScaleX(SquarePoint41[0]),ScaleY(SquarePoint41[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit2,ScaleX(SquarePoint51[0]),ScaleY(SquarePoint51[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit3,ScaleX(SquarePoint61[0]),ScaleY(SquarePoint61[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state


	board = cv2.imread('blank.png',1)

	#write additional text
	cv2.putText(board,'Correct',(200,200), font, 4,(255,255,255),4,cv2.LINE_AA)
	#project image drawn
	cv2.imshow('Projector',board)

	cv2.waitKey(500)							
	#move to next stage of the game	
	Game.state='SECONDFIGURE'
	return Game.state
	
def SecondFigure(Game):
	#declare the coordinates for the figures drawn:
	#square as corners
	SquarePoint11=(200,50)
	SquarePoint12=(400,250)
	
	SquarePoint21=(500,50)
	SquarePoint22=(700,250)
	
	SquarePoint31=(25,350)
	SquarePoint32=(225,550)
	
	SquarePoint41=(250,350)
	SquarePoint42=(450,550)
	
	SquarePoint51=(475,350)
	SquarePoint52=(675,550)
	
	SquarePoint61=(700,350)
	SquarePoint62=(900,550)
	
	#import black picture to have a black canvas to draw on
	board= cv2.imread('blank.png',1)
	
	#draw rectangles for numbers
	cv2.rectangle(board,SquarePoint11,SquarePoint12,(0,255,0),-1)
	cv2.rectangle(board,SquarePoint21,SquarePoint22,(0,255,0),-1)
	
	cv2.rectangle(board,SquarePoint31,SquarePoint32,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint41,SquarePoint42,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint51,SquarePoint52,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint61,SquarePoint62,(0,0,255),-1)
	
	#write the numbers, first 2 are on the top rest are answers
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(board,'4',(SquarePoint11[0]+55,SquarePoint12[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'5',(SquarePoint21[0]+55,SquarePoint22[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	
	cv2.putText(board,'6',(SquarePoint31[0]+55,SquarePoint32[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)	
	cv2.putText(board,'9',(SquarePoint41[0]+55,SquarePoint42[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'1',(SquarePoint51[0]+55,SquarePoint52[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)	
	cv2.putText(board,'3',(SquarePoint61[0]+55,SquarePoint62[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)

	#write additional text
	cv2.putText(board,'+',(SquarePoint12[0]+2,SquarePoint12[1]-50), font, 4,(255,255,255),4,cv2.LINE_AA)
	
	#project image drawn
	cv2.imshow('Projector',board)
	
	#create templates for what needs to be clicked (templatecorrect) and the thing that is not to be touched (templategresit)
	cv2.waitKey(100)
	for i in range(3):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
	
	templatecorrect=cv2.cvtColor(img_rgb[ScaleY(SquarePoint41[1]):ScaleY(SquarePoint42[1]),ScaleX(SquarePoint41[0]):ScaleX(SquarePoint42[0])], cv2.COLOR_BGR2GRAY)
	templategresit1=cv2.cvtColor(img_rgb[ScaleY(SquarePoint31[1]):ScaleY(SquarePoint32[1]),ScaleX(SquarePoint31[0]):ScaleX(SquarePoint32[0])], cv2.COLOR_BGR2GRAY)
	templategresit2=cv2.cvtColor(img_rgb[ScaleY(SquarePoint51[1]):ScaleY(SquarePoint52[1]),ScaleX(SquarePoint51[0]):ScaleX(SquarePoint52[0])], cv2.COLOR_BGR2GRAY)
	templategresit3=cv2.cvtColor(img_rgb[ScaleY(SquarePoint61[1]):ScaleY(SquarePoint62[1]),ScaleX(SquarePoint61[0]):ScaleX(SquarePoint62[0])], cv2.COLOR_BGR2GRAY)
	
	#look for the right thing, if found it will get out of while, if not it will look for the forbidden thing to touch
	#if the forbiden thing is touched the score becomes 0 and the game ends, if not we repeat until one of the two is touched
	while(imageFindonCamera(Game,templatecorrect,ScaleX(SquarePoint41[0]),ScaleY(SquarePoint41[1]),60,0.8)==1):
		Game.timer-=1
		if(imageFindonCamera(Game,templategresit1,ScaleX(SquarePoint31[0]),ScaleY(SquarePoint31[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit2,ScaleX(SquarePoint51[0]),ScaleY(SquarePoint51[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit3,ScaleX(SquarePoint61[0]),ScaleY(SquarePoint61[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state	
			
	board = cv2.imread('blank.png',1)

	#write additional text
	cv2.putText(board,'Correct',(200,200), font, 4,(255,255,255),4,cv2.LINE_AA)
	#project image drawn
	cv2.imshow('Projector',board)


				
	cv2.waitKey(500)		
	Game.state='THIRDFIGURE'
	return Game.state
		
def ThirdFigure(Game):
	#declare the coordinates for the figures drawn:
	#square as corners
	SquarePoint11=(200,50)
	SquarePoint12=(400,250)
	
	SquarePoint21=(500,50)
	SquarePoint22=(700,250)
	
	SquarePoint31=(25,350)
	SquarePoint32=(225,550)
	
	SquarePoint41=(250,350)
	SquarePoint42=(450,550)
	
	SquarePoint51=(475,350)
	SquarePoint52=(675,550)
	
	SquarePoint61=(700,350)
	SquarePoint62=(900,550)
	
	#import black picture to have a black canvas to draw on
	board= cv2.imread('blank.png',1)
	
	#draw rectangles for numbers
	cv2.rectangle(board,SquarePoint11,SquarePoint12,(0,255,0),-1)
	cv2.rectangle(board,SquarePoint21,SquarePoint22,(0,255,0),-1)
	
	cv2.rectangle(board,SquarePoint31,SquarePoint32,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint41,SquarePoint42,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint51,SquarePoint52,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint61,SquarePoint62,(0,0,255),-1)
	
	#write the numbers
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(board,'2',(SquarePoint11[0]+55,SquarePoint12[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'2',(SquarePoint21[0]+55,SquarePoint22[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'5',(SquarePoint31[0]+55,SquarePoint32[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)	
	cv2.putText(board,'3',(SquarePoint41[0]+55,SquarePoint42[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'4',(SquarePoint51[0]+55,SquarePoint52[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)	
	cv2.putText(board,'9',(SquarePoint61[0]+55,SquarePoint62[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)

	#write additional text
	cv2.putText(board,'+',(SquarePoint12[0]+2,SquarePoint12[1]-50), font, 4,(255,255,255),4,cv2.LINE_AA)
	
	#project image drawn
	cv2.imshow('Projector',board)
	
	#create templates for what needs to be clicked (templatecorrect) and the thing that is not to be touched (templategresit)
	cv2.waitKey(100)
	for i in range(3):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
	
	templatecorrect=cv2.cvtColor(img_rgb[ScaleY(SquarePoint51[1]):ScaleY(SquarePoint52[1]),ScaleX(SquarePoint51[0]):ScaleX(SquarePoint52[0])], cv2.COLOR_BGR2GRAY)
	templategresit1=cv2.cvtColor(img_rgb[ScaleY(SquarePoint41[1]):ScaleY(SquarePoint42[1]),ScaleX(SquarePoint41[0]):ScaleX(SquarePoint42[0])], cv2.COLOR_BGR2GRAY)
	templategresit2=cv2.cvtColor(img_rgb[ScaleY(SquarePoint31[1]):ScaleY(SquarePoint32[1]),ScaleX(SquarePoint31[0]):ScaleX(SquarePoint32[0])], cv2.COLOR_BGR2GRAY)
	templategresit3=cv2.cvtColor(img_rgb[ScaleY(SquarePoint61[1]):ScaleY(SquarePoint62[1]),ScaleX(SquarePoint61[0]):ScaleX(SquarePoint62[0])], cv2.COLOR_BGR2GRAY)
	
	#look for the right thing, if found it will get out of while, if not it will look for the forbidden thing to touch
	#if the forbiden thing is touched the score becomes 0 and the game ends, if not we repeat until one of the two is touched
	while(imageFindonCamera(Game,templatecorrect,ScaleX(SquarePoint51[0]),ScaleY(SquarePoint51[1]),60,0.8)==1):
		Game.timer-=1
		if(imageFindonCamera(Game,templategresit1,ScaleX(SquarePoint41[0]),ScaleY(SquarePoint41[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit2,ScaleX(SquarePoint31[0]),ScaleY(SquarePoint31[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit3,ScaleX(SquarePoint61[0]),ScaleY(SquarePoint61[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state	

	board = cv2.imread('blank.png',1)

	#write additional text
	cv2.putText(board,'Correct',(200,200), font, 4,(255,255,255),4,cv2.LINE_AA)
	#project image drawn
	cv2.imshow('Projector',board)
			
			
	cv2.waitKey(500)		
	Game.state='FOURTHFIGURE'
	return Game.state	
	
def FourthFigure(Game):
	#declare the coordinates for the figures drawn:
	#square as corners
	SquarePoint11=(200,50)
	SquarePoint12=(400,250)
	
	SquarePoint21=(500,50)
	SquarePoint22=(700,250)
	
	SquarePoint31=(25,350)
	SquarePoint32=(225,550)
	
	SquarePoint41=(250,350)
	SquarePoint42=(450,550)
	
	SquarePoint51=(475,350)
	SquarePoint52=(675,550)
	
	SquarePoint61=(700,350)
	SquarePoint62=(900,550)
	
	#import black picture to have a black canvas to draw on
	board= cv2.imread('blank.png',1)
	
	#draw rectangles for numbers
	cv2.rectangle(board,SquarePoint11,SquarePoint12,(0,255,0),-1)
	cv2.rectangle(board,SquarePoint21,SquarePoint22,(0,255,0),-1)
	
	cv2.rectangle(board,SquarePoint31,SquarePoint32,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint41,SquarePoint42,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint51,SquarePoint52,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint61,SquarePoint62,(0,0,255),-1)
	
	#write the numbers
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(board,'4',(SquarePoint11[0]+55,SquarePoint12[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'4',(SquarePoint21[0]+55,SquarePoint22[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'3',(SquarePoint31[0]+55,SquarePoint32[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)	
	cv2.putText(board,'4',(SquarePoint41[0]+55,SquarePoint42[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'5',(SquarePoint51[0]+55,SquarePoint52[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)	
	cv2.putText(board,'8',(SquarePoint61[0]+55,SquarePoint62[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)

	#write additional text
	cv2.putText(board,'+',(SquarePoint12[0]+2,SquarePoint12[1]-50), font, 4,(255,255,255),4,cv2.LINE_AA)
	
	#project image drawn
	cv2.imshow('Projector',board)
	
	#create templates for what needs to be clicked (templatecorrect) and the thing that is not to be touched (templategresit)
	cv2.waitKey(100)
	for i in range(3):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
	
	templatecorrect=cv2.cvtColor(img_rgb[ScaleY(SquarePoint61[1]):ScaleY(SquarePoint62[1]),ScaleX(SquarePoint61[0]):ScaleX(SquarePoint62[0])], cv2.COLOR_BGR2GRAY)
	templategresit1=cv2.cvtColor(img_rgb[ScaleY(SquarePoint41[1]):ScaleY(SquarePoint42[1]),ScaleX(SquarePoint41[0]):ScaleX(SquarePoint42[0])], cv2.COLOR_BGR2GRAY)
	templategresit2=cv2.cvtColor(img_rgb[ScaleY(SquarePoint51[1]):ScaleY(SquarePoint52[1]),ScaleX(SquarePoint51[0]):ScaleX(SquarePoint52[0])], cv2.COLOR_BGR2GRAY)
	templategresit3=cv2.cvtColor(img_rgb[ScaleY(SquarePoint31[1]):ScaleY(SquarePoint32[1]),ScaleX(SquarePoint31[0]):ScaleX(SquarePoint32[0])], cv2.COLOR_BGR2GRAY)
	
	#look for the right thing, if found it will get out of while, if not it will look for the forbidden thing to touch
	#if the forbiden thing is touched the score becomes 0 and the game ends, if not we repeat until one of the two is touched
	while(imageFindonCamera(Game,templatecorrect,ScaleX(SquarePoint61[0]),ScaleY(SquarePoint61[1]),60,0.8)==1):
		Game.timer-=1
		if(imageFindonCamera(Game,templategresit1,ScaleX(SquarePoint41[0]),ScaleY(SquarePoint41[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit2,ScaleX(SquarePoint51[0]),ScaleY(SquarePoint51[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit3,ScaleX(SquarePoint31[0]),ScaleY(SquarePoint31[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state	

	board = cv2.imread('blank.png',1)

	#write additional text
	cv2.putText(board,'Correct',(200,200), font, 4,(255,255,255),4,cv2.LINE_AA)
	#project image drawn
	cv2.imshow('Projector',board)

			
	cv2.waitKey(500)		
	Game.state='FIFTHFIGURE'
	return Game.state	

def FifthFigure(Game):
	#declare the coordinates for the figures drawn:
	#square as corners
	SquarePoint11=(200,50)
	SquarePoint12=(400,250)
	
	SquarePoint21=(500,50)
	SquarePoint22=(700,250)
	
	SquarePoint31=(25,350)
	SquarePoint32=(225,550)
	
	SquarePoint41=(250,350)
	SquarePoint42=(450,550)
	
	SquarePoint51=(475,350)
	SquarePoint52=(675,550)
	
	SquarePoint61=(700,350)
	SquarePoint62=(900,550)
	
	#import black picture to have a black canvas to draw on
	board= cv2.imread('blank.png',1)
	
	#draw rectangles for numbers
	cv2.rectangle(board,SquarePoint11,SquarePoint12,(0,255,0),-1)
	cv2.rectangle(board,SquarePoint21,SquarePoint22,(0,255,0),-1)
	
	cv2.rectangle(board,SquarePoint31,SquarePoint32,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint41,SquarePoint42,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint51,SquarePoint52,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint61,SquarePoint62,(0,0,255),-1)
	
	#write the numbers
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(board,'6',(SquarePoint11[0]+55,SquarePoint12[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'1',(SquarePoint21[0]+55,SquarePoint22[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'7',(SquarePoint31[0]+55,SquarePoint32[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)	
	cv2.putText(board,'4',(SquarePoint41[0]+55,SquarePoint42[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'5',(SquarePoint51[0]+55,SquarePoint52[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)	
	cv2.putText(board,'6',(SquarePoint61[0]+55,SquarePoint62[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)

	#write additional text
	cv2.putText(board,'+',(SquarePoint12[0]+2,SquarePoint12[1]-50), font, 4,(255,255,255),4,cv2.LINE_AA)
	
	#project image drawn
	cv2.imshow('Projector',board)
	
	#create templates for what needs to be clicked (templatecorrect) and the thing that is not to be touched (templategresit)
	cv2.waitKey(100)
	for i in range(3):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
	
	templatecorrect=cv2.cvtColor(img_rgb[ScaleY(SquarePoint31[1]):ScaleY(SquarePoint32[1]),ScaleX(SquarePoint31[0]):ScaleX(SquarePoint32[0])], cv2.COLOR_BGR2GRAY)
	templategresit1=cv2.cvtColor(img_rgb[ScaleY(SquarePoint41[1]):ScaleY(SquarePoint42[1]),ScaleX(SquarePoint41[0]):ScaleX(SquarePoint42[0])], cv2.COLOR_BGR2GRAY)
	templategresit2=cv2.cvtColor(img_rgb[ScaleY(SquarePoint51[1]):ScaleY(SquarePoint52[1]),ScaleX(SquarePoint51[0]):ScaleX(SquarePoint52[0])], cv2.COLOR_BGR2GRAY)
	templategresit3=cv2.cvtColor(img_rgb[ScaleY(SquarePoint61[1]):ScaleY(SquarePoint62[1]),ScaleX(SquarePoint61[0]):ScaleX(SquarePoint62[0])], cv2.COLOR_BGR2GRAY)
	
	#look for the right thing, if found it will get out of while, if not it will look for the forbidden thing to touch
	#if the forbiden thing is touched the score becomes 0 and the game ends, if not we repeat until one of the two is touched
	while(imageFindonCamera(Game,templatecorrect,ScaleX(SquarePoint31[0]),ScaleY(SquarePoint31[1]),60,0.8)==1):
		Game.timer-=1
		if(imageFindonCamera(Game,templategresit1,ScaleX(SquarePoint41[0]),ScaleY(SquarePoint41[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit2,ScaleX(SquarePoint51[0]),ScaleY(SquarePoint51[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit3,ScaleX(SquarePoint61[0]),ScaleY(SquarePoint61[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state

	board = cv2.imread('blank.png',1)

	#write additional text
	cv2.putText(board,'Correct',(200,200), font, 4,(255,255,255),4,cv2.LINE_AA)
	#project image drawn
	cv2.imshow('Projector',board)
			

	cv2.waitKey(500)		
	Game.state='SIXTHFIGURE'
	return Game.state	

def SixthFigure(Game):
	#declare the coordinates for the figures drawn:
	#square as corners
	SquarePoint11=(200,50)
	SquarePoint12=(400,250)
	
	SquarePoint21=(500,50)
	SquarePoint22=(700,250)
	
	SquarePoint31=(25,350)
	SquarePoint32=(225,550)
	
	SquarePoint41=(250,350)
	SquarePoint42=(450,550)
	
	SquarePoint51=(475,350)
	SquarePoint52=(675,550)
	
	SquarePoint61=(700,350)
	SquarePoint62=(900,550)
	
	#import black picture to have a black canvas to draw on
	board= cv2.imread('blank.png',1)
	
	#draw rectangles for numbers
	cv2.rectangle(board,SquarePoint11,SquarePoint12,(0,255,0),-1)
	cv2.rectangle(board,SquarePoint21,SquarePoint22,(0,255,0),-1)
	
	cv2.rectangle(board,SquarePoint31,SquarePoint32,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint41,SquarePoint42,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint51,SquarePoint52,(0,0,255),-1)
	cv2.rectangle(board,SquarePoint61,SquarePoint62,(0,0,255),-1)
	
	#write the numbers
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(board,'2',(SquarePoint11[0]+55,SquarePoint12[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'4',(SquarePoint21[0]+55,SquarePoint22[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'3',(SquarePoint31[0]+55,SquarePoint32[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)	
	cv2.putText(board,'4',(SquarePoint41[0]+55,SquarePoint42[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,'5',(SquarePoint51[0]+55,SquarePoint52[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)	
	cv2.putText(board,'6',(SquarePoint61[0]+55,SquarePoint62[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)

	#write additional text
	cv2.putText(board,'+',(SquarePoint12[0]+2,SquarePoint12[1]-50), font, 4,(255,255,255),4,cv2.LINE_AA)
	
	#project image drawn
	cv2.imshow('Projector',board)
	
	#create templates for what needs to be clicked (templatecorrect) and the thing that is not to be touched (templategresit)
	cv2.waitKey(100)
	for i in range(3):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
	
	templatecorrect=cv2.cvtColor(img_rgb[ScaleY(SquarePoint61[1]):ScaleY(SquarePoint62[1]),ScaleX(SquarePoint61[0]):ScaleX(SquarePoint62[0])], cv2.COLOR_BGR2GRAY)
	templategresit1=cv2.cvtColor(img_rgb[ScaleY(SquarePoint41[1]):ScaleY(SquarePoint42[1]),ScaleX(SquarePoint41[0]):ScaleX(SquarePoint42[0])], cv2.COLOR_BGR2GRAY)
	templategresit2=cv2.cvtColor(img_rgb[ScaleY(SquarePoint51[1]):ScaleY(SquarePoint52[1]),ScaleX(SquarePoint51[0]):ScaleX(SquarePoint52[0])], cv2.COLOR_BGR2GRAY)
	templategresit3=cv2.cvtColor(img_rgb[ScaleY(SquarePoint31[1]):ScaleY(SquarePoint32[1]),ScaleX(SquarePoint31[0]):ScaleX(SquarePoint32[0])], cv2.COLOR_BGR2GRAY)
	
	#look for the right thing, if found it will get out of while, if not it will look for the forbidden thing to touch
	#if the forbiden thing is touched the score becomes 0 and the game ends, if not we repeat until one of the two is touched
	while(imageFindonCamera(Game,templatecorrect,ScaleX(SquarePoint61[0]),ScaleY(SquarePoint61[1]),60,0.8)==1):
		Game.timer-=1
		if(imageFindonCamera(Game,templategresit1,ScaleX(SquarePoint41[0]),ScaleY(SquarePoint41[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit2,ScaleX(SquarePoint51[0]),ScaleY(SquarePoint51[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit3,ScaleX(SquarePoint31[0]),ScaleY(SquarePoint31[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state	

	board = cv2.imread('blank.png',1)

	#write additional text
	cv2.putText(board,'Correct',(200,200), font, 4,(255,255,255),4,cv2.LINE_AA)
	#project image drawn
	cv2.imshow('Projector',board)

			
	cv2.waitKey(500)		
	Game.state='CLEAN'
	return Game.state	
	
def Clean(Game):

	#project fuse 1 place and bin on the board
	Final= cv2.imread('final.png',1)
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(Final,'Your score is:'+str(Game.timer),(30,480), font, 2,(255,255,255),2,cv2.LINE_AA)
	if Game.timer<950:
		cv2.putText(Final,'You\'re a bit retarded',(30,280), font, 2,(255,255,255),2,cv2.LINE_AA)
	else:
		cv2.putText(Final,'Not bad',(30,280), font, 2,(255,255,255),2,cv2.LINE_AA)
	
	cv2.imshow('Projector',Final)
	cv2.waitKey(5000)
	Game.cap.release()
	cv2.destroyAllWindows()
	
	
	Game.state='END'
	return Game.state
 
 
switcher = {
        'INIT': Initialization,
        'FIRSTFIGURE': FirstFigure,
		'SECONDFIGURE': SecondFigure,
		'THIRDFIGURE': ThirdFigure,
		'FOURTHFIGURE' : FourthFigure,
		'FIFTHFIGURE' : FifthFigure,
		'SIXTHFIGURE' : SixthFigure,
		'CLEAN': Clean
    }
 
 
def run(argument):
    # Get the function from switcher dictionary
    func = switcher.get(argument, "nothing")
    # Execute the function
    return func(Game)


def GameRun():
	Game.state='INIT'
	while(Game.state!='END'):	
		print(run(Game.state))
		print(Game.timer)
	
