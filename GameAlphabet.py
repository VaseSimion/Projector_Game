


#*****************************************************************************************************************
#*********   this version of the game has squares as wright figure and circles as the forbiden one      **********
#*****************************************************************************************************************

import cv2
import numpy as np
import random 

def ScaleY(value):
	return int(125 + 0.484*value)
	
def ScaleX(value):
	return int(35+0.609*value)


class GameData:
	def __init__(self):
		self.timer=0
		self.cap=0
		self.state='A'
		self.CorrectPostion=1
		
Game=GameData()
AlphabetList=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


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
	
	Game.state='A'
	return Game.state		
 
def Clean(Game):

	#project fuse 1 place and bin on the board
	Final= cv2.imread('final.png',1)
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(Final,'Your score is:'+str(Game.timer),(30,480), font, 2,(255,255,255),2,cv2.LINE_AA)
	if Game.timer<900:
		cv2.putText(Final,"Go back to school!",(30,280), font, 2,(255,255,255),2,cv2.LINE_AA)
		cv2.putText(Final,"Stupid kid",(30,380), font, 2,(255,255,255),2,cv2.LINE_AA)
	else:
		cv2.putText(Final,'Not bad',(30,280), font, 2,(255,255,255),2,cv2.LINE_AA)
	
	cv2.imshow('Projector',Final)
	cv2.waitKey(5000)
	Game.cap.release()
	cv2.destroyAllWindows()
	
	
	Game.state='END'
	return Game.state
 
def PrintLetter(Game,ListOfLetters):
	if Game.state=='INIT':
		Initialization(Game)
		return Game.state
	
	if Game.state=='CLEAN':
		Clean(Game)
		return Game.state
	
	if Game.CorrectPostion==1:
		SquarePoint11=(random.randint(0,250),random.randint(0,100))
		SquarePoint12=(SquarePoint11[0]+200,SquarePoint11[1]+200)
		SquarePoint21=(random.randint(450,700),random.randint(0,100))
		SquarePoint22=(SquarePoint21[0]+200,SquarePoint21[1]+200)	 
		SquarePoint31=(random.randint(450,700),random.randint(300,400))
		SquarePoint32=(SquarePoint31[0]+200,SquarePoint31[1]+200)
		SquarePoint41=(random.randint(0,250),random.randint(300,400))
		SquarePoint42=(SquarePoint41[0]+200,SquarePoint41[1]+200)

	if Game.CorrectPostion==2:
		SquarePoint21=(random.randint(0,250),random.randint(0,100))
		SquarePoint22=(SquarePoint21[0]+200,SquarePoint21[1]+200)
		SquarePoint11=(random.randint(450,700),random.randint(0,100))
		SquarePoint12=(SquarePoint11[0]+200,SquarePoint11[1]+200)	 
		SquarePoint31=(random.randint(450,700),random.randint(300,400))
		SquarePoint32=(SquarePoint31[0]+200,SquarePoint31[1]+200)
		SquarePoint41=(random.randint(0,250),random.randint(300,400))
		SquarePoint42=(SquarePoint41[0]+200,SquarePoint41[1]+200)

	if Game.CorrectPostion==3:
		SquarePoint31=(random.randint(0,250),random.randint(0,100))
		SquarePoint32=(SquarePoint31[0]+200,SquarePoint31[1]+200)
		SquarePoint21=(random.randint(450,700),random.randint(0,100))
		SquarePoint22=(SquarePoint21[0]+200,SquarePoint21[1]+200)	 
		SquarePoint11=(random.randint(450,700),random.randint(300,400))
		SquarePoint12=(SquarePoint11[0]+200,SquarePoint11[1]+200)
		SquarePoint41=(random.randint(0,250),random.randint(300,400))
		SquarePoint42=(SquarePoint41[0]+200,SquarePoint41[1]+200)
	
	if Game.CorrectPostion==4:
		SquarePoint41=(random.randint(0,250),random.randint(0,100))
		SquarePoint42=(SquarePoint41[0]+200,SquarePoint41[1]+200)
		SquarePoint21=(random.randint(450,700),random.randint(0,100))
		SquarePoint22=(SquarePoint21[0]+200,SquarePoint21[1]+200)	 
		SquarePoint31=(random.randint(450,700),random.randint(300,400))
		SquarePoint32=(SquarePoint31[0]+200,SquarePoint31[1]+200)
		SquarePoint11=(random.randint(0,250),random.randint(300,400))
		SquarePoint12=(SquarePoint11[0]+200,SquarePoint11[1]+200)
		
	#import black picture to have a black canvas to draw on
	board= cv2.imread('blank.png',1)
	
	#draw rectangles for numbers
	cv2.rectangle(board,SquarePoint11,SquarePoint12,(0,255,0),-1)
	cv2.rectangle(board,SquarePoint21,SquarePoint22,(0,255,0),-1)
	cv2.rectangle(board,SquarePoint31,SquarePoint32,(0,255,0),-1)
	cv2.rectangle(board,SquarePoint41,SquarePoint42,(0,255,0),-1)
	
	#make the false answers
	FalseLetter1=ListOfLetters[random.randint(0,len(ListOfLetters)-1)]
	FalseLetter2=ListOfLetters[random.randint(0,len(ListOfLetters)-1)]
	FalseLetter3=ListOfLetters[random.randint(0,len(ListOfLetters)-1)]
	while (FalseLetter1 == Game.state):
		FalseLetter1=ListOfLetters[random.randint(0,len(ListOfLetters)-1)]
	while (FalseLetter2 == Game.state or FalseLetter2 == FalseLetter1):
		FalseLetter2=ListOfLetters[random.randint(0,len(ListOfLetters)-1)]
	while (FalseLetter3 == Game.state or FalseLetter3 == FalseLetter1  or FalseLetter3 == FalseLetter2):
		FalseLetter3=ListOfLetters[random.randint(0,len(ListOfLetters)-1)]	
	
	#write the numbers
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(board,Game.state,(SquarePoint11[0]+55,SquarePoint12[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,FalseLetter1,(SquarePoint21[0]+55,SquarePoint22[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	cv2.putText(board,FalseLetter2,(SquarePoint31[0]+55,SquarePoint32[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)	
	cv2.putText(board,FalseLetter3,(SquarePoint41[0]+55,SquarePoint42[1]-55), font, 4,(255,255,255),4,cv2.LINE_AA)
	
	#project image drawn
	cv2.imshow('Projector',board)

	#create templates for what needs to be clicked (templatecorrect) and the thing that is not to be touched (templategresit)
	cv2.waitKey(100)
	for i in range(3):
		ret, img_rgb = Game.cap.read()
		cv2.waitKey(100)
	
	templatecorrect=cv2.cvtColor(img_rgb[ScaleY(SquarePoint11[1]):ScaleY(SquarePoint12[1]),ScaleX(SquarePoint11[0]):ScaleX(SquarePoint12[0])], cv2.COLOR_BGR2GRAY)
	templategresit1=cv2.cvtColor(img_rgb[ScaleY(SquarePoint21[1]):ScaleY(SquarePoint22[1]),ScaleX(SquarePoint21[0]):ScaleX(SquarePoint22[0])], cv2.COLOR_BGR2GRAY)
	templategresit2=cv2.cvtColor(img_rgb[ScaleY(SquarePoint31[1]):ScaleY(SquarePoint32[1]),ScaleX(SquarePoint31[0]):ScaleX(SquarePoint32[0])], cv2.COLOR_BGR2GRAY)
	templategresit3=cv2.cvtColor(img_rgb[ScaleY(SquarePoint41[1]):ScaleY(SquarePoint42[1]),ScaleX(SquarePoint41[0]):ScaleX(SquarePoint42[0])], cv2.COLOR_BGR2GRAY)

	while(imageFindonCamera(Game,templatecorrect,ScaleX(SquarePoint11[0]),ScaleY(SquarePoint11[1]),60,0.8)==1):
		Game.timer-=1
		if(imageFindonCamera(Game,templategresit1,ScaleX(SquarePoint21[0]),ScaleY(SquarePoint21[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit2,ScaleX(SquarePoint31[0]),ScaleY(SquarePoint31[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
		if(imageFindonCamera(Game,templategresit3,ScaleX(SquarePoint41[0]),ScaleY(SquarePoint41[1]),60,0.6)==0):
			Game.state='CLEAN'
			Game.timer=0
			return Game.state
	
	board = cv2.imread('blank.png',1)

	#write additional text
	cv2.putText(board,'Correct',(200,200), font, 4,(255,255,255),4,cv2.LINE_AA)
	#project image drawn
	cv2.imshow('Projector',board)

	cv2.waitKey(1000)							
	#move to next stage of the game	
	
	if ListOfLetters.index(Game.state)==(len(AlphabetList)-1):
		Game.state='CLEAN'
	else:
		Game.state=ListOfLetters[ListOfLetters.index(Game.state)+1]
		Game.CorrectPostion=random.randint(1,4)
	return Game.state

	
def GameRun():
	Game.state='INIT'
	while(Game.state!='END'):	
		print(PrintLetter(Game,AlphabetList))		
		print(Game.timer)
	
