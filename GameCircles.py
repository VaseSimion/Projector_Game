


#*****************************************************************************************************************
#*********   this version of the game has circles as wright figure and squares as the forbiden one      **********
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
		
	Game.state='FIRSTFIGURE'
	return Game.state		
 
def FirstFigure(Game):
	#declare the coordinates for the figures drawn:
	#circle as center and raduis
	circlecenterx=300
	circlecentery=300
	circleradius=100
	#square as corners
	SquarePoint1=(600,300)
	SquarePoint2=(800,500)
	
	#import black picture to have a black canvas to draw on
	board= cv2.imread('blank.png',1)
	
	#draw circle with small circle inside
	cv2.circle(board,(circlecenterx,circlecentery), circleradius, (0,255,0), -1)
	cv2.circle(board,(circlecenterx,circlecentery), int(circleradius/2), (0,255,255), -1)
	
	#draw rectangle with X drawn in it
	cv2.rectangle(board,SquarePoint1,SquarePoint2,(0,0,255),-1)
	cv2.line(board,SquarePoint1,SquarePoint2,(255,255,255),3)
	cv2.line(board,(SquarePoint1[0],SquarePoint2[1]),(SquarePoint2[0],SquarePoint1[1]),(255,255,255),3)
	cv2.rectangle(board,SquarePoint1,SquarePoint2,(0,0,0),3)
	
	#project image drawn
	cv2.imshow('Projector',board)
	
	#create templates for what needs to be clicked (templatecorrect) and the thing that is not to be touched (templategresit)
	cv2.waitKey(100)
	for i in range(3):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
	
	templatecorrect=cv2.cvtColor(img_rgb[ScaleY(circlecentery-circleradius/2):ScaleY(circlecentery+circleradius/2),ScaleX(circlecenterx-circleradius/2):ScaleX(circlecenterx+circleradius/2)], cv2.COLOR_BGR2GRAY)
	templategresit=cv2.cvtColor(img_rgb[ScaleY(SquarePoint1[1]):ScaleY(SquarePoint2[1]),ScaleX(SquarePoint1[0]):ScaleX(SquarePoint2[0])], cv2.COLOR_BGR2GRAY)

	#look for the right thing, if found it will get out of while, if not it will look for the forbidden thing to touch
	#if the forbiden thing is touched the score becomes 0 and the game ends, if not we repeat until one of the two is touched
	while(imageFindonCamera(Game,templatecorrect,ScaleX(circlecenterx-circleradius/2),ScaleY(circlecentery-circleradius/2),60,0.8)==1):
		Game.timer-=1
		if(imageFindonCamera(Game,templategresit,ScaleX(SquarePoint1[0]),ScaleY(SquarePoint1[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
	
	#move to next stage of the game	
	Game.state='SECONDFIGURE'
	return Game.state
	
def SecondFigure(Game):
	circlecenterx=600
	circlecentery=600
	circleradius=100
	SquarePoint1=(200,200)
	SquarePoint2=(400,400)
	
	#print on the projector where the hand should be placed
	board= cv2.imread('blank.png',1)
	cv2.circle(board,(circlecenterx,circlecentery), circleradius, (255,0,0), -1)
	cv2.circle(board,(circlecenterx,circlecentery), int(circleradius/2), (255,255,0), -1)
	
	cv2.rectangle(board,SquarePoint1,SquarePoint2,(0,0,255),-1)
	cv2.line(board,SquarePoint1,SquarePoint2,(255,255,255),3)
	cv2.line(board,(SquarePoint1[0],SquarePoint2[1]),(SquarePoint2[0],SquarePoint1[1]),(255,255,255),3)
	cv2.rectangle(board,SquarePoint1,SquarePoint2,(0,0,0),3)
	
	cv2.imshow('Projector',board)
	#create template
	cv2.waitKey(100)

	for i in range(5):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
		#cv2.imshow('Debug',img_rgb)
	
	ret, img_rgb = Game.cap.read()

	templatecorrect=cv2.cvtColor(img_rgb[ScaleY(circlecentery-circleradius/2):ScaleY(circlecentery+circleradius/2),ScaleX(circlecenterx-circleradius/2):ScaleX(circlecenterx+circleradius/2)], cv2.COLOR_BGR2GRAY)
	templategresit=cv2.cvtColor(img_rgb[ScaleY(SquarePoint1[1]):ScaleY(SquarePoint2[1]),ScaleX(SquarePoint1[0]):ScaleX(SquarePoint2[0])], cv2.COLOR_BGR2GRAY)
	
	while(imageFindonCamera(Game,templatecorrect,ScaleX(circlecenterx-circleradius/2),ScaleY(circlecentery-circleradius/2),60,0.8)==1):
		Game.timer-=1
		if(imageFindonCamera(Game,templategresit,ScaleX(SquarePoint1[0]),ScaleY(SquarePoint1[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
			
			
	cv2.waitKey(100)		
	Game.state='THIRDFIGURE'
	return Game.state
		
def ThirdFigure(Game):
	circlecenterx=200
	circlecentery=400
	circleradius=100
	SquarePoint1=(400,500)
	SquarePoint2=(600,700)
	
	#print on the projector where the hand should be placed
	board= cv2.imread('blank.png',1)
	cv2.circle(board,(circlecenterx,circlecentery), circleradius, (0,255,0), -1)
	cv2.circle(board,(circlecenterx,circlecentery), int(circleradius/2), (255,255,0), -1)

	cv2.rectangle(board,SquarePoint1,SquarePoint2,(0,0,255),-1)
	cv2.line(board,SquarePoint1,SquarePoint2,(255,255,255),3)
	cv2.line(board,(SquarePoint1[0],SquarePoint2[1]),(SquarePoint2[0],SquarePoint1[1]),(255,255,255),3)
	cv2.rectangle(board,SquarePoint1,SquarePoint2,(0,0,0),3)
	
	cv2.imshow('Projector',board)
	#create template
	cv2.waitKey(100)

	for i in range(5):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
		#cv2.imshow('Debug',img_rgb)
	
	ret, img_rgb = Game.cap.read()

	templatecorrect=cv2.cvtColor(img_rgb[ScaleY(circlecentery-circleradius/2):ScaleY(circlecentery+circleradius/2),ScaleX(circlecenterx-circleradius/2):ScaleX(circlecenterx+circleradius/2)], cv2.COLOR_BGR2GRAY)
	templategresit=cv2.cvtColor(img_rgb[ScaleY(SquarePoint1[1]):ScaleY(SquarePoint2[1]),ScaleX(SquarePoint1[0]):ScaleX(SquarePoint2[0])], cv2.COLOR_BGR2GRAY)

	while(imageFindonCamera(Game,templatecorrect,ScaleX(circlecenterx-circleradius/2),ScaleY(circlecentery-circleradius/2),60,0.8)==1):
		Game.timer-=1
		if(imageFindonCamera(Game,templategresit,ScaleX(SquarePoint1[0]),ScaleY(SquarePoint1[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
			
	cv2.waitKey(100)		
	Game.state='FOURTHFIGURE'
	return Game.state	
	
def FourthFigure(Game):
	circlecenterx=700
	circlecentery=500
	circleradius=100
	SquarePoint1=(200,400)
	SquarePoint2=(400,600)
	
	#print on the projector where the hand should be placed
	board= cv2.imread('blank.png',1)
	cv2.circle(board,(circlecenterx,circlecentery), circleradius, (255,255,0), -1)
	cv2.circle(board,(circlecenterx,circlecentery), int(circleradius/2), (0,255,0), -1)

	cv2.rectangle(board,SquarePoint1,SquarePoint2,(0,0,255),-1)
	cv2.line(board,SquarePoint1,SquarePoint2,(255,255,255),3)
	cv2.line(board,(SquarePoint1[0],SquarePoint2[1]),(SquarePoint2[0],SquarePoint1[1]),(255,255,255),3)
	cv2.rectangle(board,SquarePoint1,SquarePoint2,(0,0,0),3)
	
	cv2.imshow('Projector',board)
	#create template
	cv2.waitKey(100)

	for i in range(5):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
		#cv2.imshow('Debug',img_rgb)
	
	ret, img_rgb = Game.cap.read()

	templatecorrect=cv2.cvtColor(img_rgb[ScaleY(circlecentery-circleradius/2):ScaleY(circlecentery+circleradius/2),ScaleX(circlecenterx-circleradius/2):ScaleX(circlecenterx+circleradius/2)], cv2.COLOR_BGR2GRAY)
	templategresit=cv2.cvtColor(img_rgb[ScaleY(SquarePoint1[1]):ScaleY(SquarePoint2[1]),ScaleX(SquarePoint1[0]):ScaleX(SquarePoint2[0])], cv2.COLOR_BGR2GRAY)

	while(imageFindonCamera(Game,templatecorrect,ScaleX(circlecenterx-circleradius/2),ScaleY(circlecentery-circleradius/2),60,0.8)==1):
		Game.timer-=1
		if(imageFindonCamera(Game,templategresit,ScaleX(SquarePoint1[0]),ScaleY(SquarePoint1[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
			
	cv2.waitKey(100)		
	Game.state='FIFTHFIGURE'
	return Game.state	

def FifthFigure(Game):
	circlecenterx=150
	circlecentery=150
	circleradius=100
	SquarePoint1=(700,300)
	SquarePoint2=(900,500)
	
	#print on the projector where the hand should be placed
	board= cv2.imread('blank.png',1)
	cv2.circle(board,(circlecenterx,circlecentery), circleradius, (0,255,255), -1)
	cv2.circle(board,(circlecenterx,circlecentery), int(circleradius/2), (255,0,0), -1)

	cv2.rectangle(board,SquarePoint1,SquarePoint2,(0,0,255),-1)
	cv2.line(board,SquarePoint1,SquarePoint2,(255,255,255),3)
	cv2.line(board,(SquarePoint1[0],SquarePoint2[1]),(SquarePoint2[0],SquarePoint1[1]),(255,255,255),3)
	cv2.rectangle(board,SquarePoint1,SquarePoint2,(0,0,0),3)
	
	cv2.imshow('Projector',board)
	#create template
	cv2.waitKey(100)

	for i in range(5):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
		#cv2.imshow('Debug',img_rgb)
	
	ret, img_rgb = Game.cap.read()

	templatecorrect=cv2.cvtColor(img_rgb[ScaleY(circlecentery-circleradius/2):ScaleY(circlecentery+circleradius/2),ScaleX(circlecenterx-circleradius/2):ScaleX(circlecenterx+circleradius/2)], cv2.COLOR_BGR2GRAY)
	templategresit=cv2.cvtColor(img_rgb[ScaleY(SquarePoint1[1]):ScaleY(SquarePoint2[1]),ScaleX(SquarePoint1[0]):ScaleX(SquarePoint2[0])], cv2.COLOR_BGR2GRAY)

	while(imageFindonCamera(Game,templatecorrect,ScaleX(circlecenterx-circleradius/2),ScaleY(circlecentery-circleradius/2),60,0.8)==1):
		Game.timer-=1
		if(imageFindonCamera(Game,templategresit,ScaleX(SquarePoint1[0]),ScaleY(SquarePoint1[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
			
	cv2.waitKey(100)		
	Game.state='SIXTHFIGURE'
	return Game.state	

def SixthFigure(Game):
	circlecenterx=500
	circlecentery=500
	circleradius=100
	SquarePoint1=(100,100)
	SquarePoint2=(300,300)
	
	#print on the projector where the hand should be placed
	board= cv2.imread('blank.png',1)
	cv2.circle(board,(circlecenterx,circlecentery), circleradius, (255,0,255), -1)
	cv2.circle(board,(circlecenterx,circlecentery), int(circleradius/2), (0,0,0), -1)

	cv2.rectangle(board,SquarePoint1,SquarePoint2,(0,0,255),-1)
	cv2.line(board,SquarePoint1,SquarePoint2,(255,255,255),3)
	cv2.line(board,(SquarePoint1[0],SquarePoint2[1]),(SquarePoint2[0],SquarePoint1[1]),(255,255,255),3)
	cv2.rectangle(board,SquarePoint1,SquarePoint2,(0,0,0),3)
	
	cv2.imshow('Projector',board)
	#create template
	cv2.waitKey(100)

	for i in range(5):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
		#cv2.imshow('Debug',img_rgb)
	
	ret, img_rgb = Game.cap.read()

	templatecorrect=cv2.cvtColor(img_rgb[ScaleY(circlecentery-circleradius/2):ScaleY(circlecentery+circleradius/2),ScaleX(circlecenterx-circleradius/2):ScaleX(circlecenterx+circleradius/2)], cv2.COLOR_BGR2GRAY)
	templategresit=cv2.cvtColor(img_rgb[ScaleY(SquarePoint1[1]):ScaleY(SquarePoint2[1]),ScaleX(SquarePoint1[0]):ScaleX(SquarePoint2[0])], cv2.COLOR_BGR2GRAY)

	while(imageFindonCamera(Game,templatecorrect,ScaleX(circlecenterx-circleradius/2),ScaleY(circlecentery-circleradius/2),60,0.8)==1):
		Game.timer-=1
		if(imageFindonCamera(Game,templategresit,ScaleX(SquarePoint1[0]),ScaleY(SquarePoint1[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
			
	cv2.waitKey(100)		
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
	
