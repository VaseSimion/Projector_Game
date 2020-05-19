

#******************************************************************************************************************************************
#***********************************      Game developed by Sularea Vasile Simion in 11 Apr 2019           ********************************
#******************************************************************************************************************************************

#library used for the UI
from tkinter import * 
#games imported
import GameCircles 
import GameSquares
import GameMath
import GameAlphabet
# An included library with Python install. Used for the popup message
import ctypes  


#Define the popup message based on the game played
def Mbox(gameselector,style):

	if not gameselector:
		title="Unselected game"
		text="You need to select a game you noob"
		
	elif gameselector[0]==0:
		title="Circle game"
		text="You need to put your hand on the circles and avoid placing it on the squares"
		
	elif gameselector[0]==1:
		title="Square game"
		text="You need to put your hand on the squares and avoid placing it on the circles"

	elif gameselector[0]==2:
		title="Math game"
		text="You need to put your hand on the square that makes the math equation valid"

	elif gameselector[0]==3:
		title="Alphabet game"
		text="You need to put your hand on the alphabet continuous letter"
		
	elif gameselector[0]==10:
		title="Why?"
		text="For the love of God, I told you not to press"
			
	else:
		title="TBD game"
		text="The game has not been developed yet, please contact the developer"

	#  Styles:
	#  0 : OK
	#  1 : OK | Cancel
	#  2 : Abort | Retry | Ignore
	#  3 : Yes | No | Cancel
	#  4 : Yes | No
	#  5 : Retry | No 
	#  6 : Cancel | Try Again | Continue
	return ctypes.windll.user32.MessageBoxW(0, text, title, style)
	
#Define running the game selected from the list
def RunGame(gameselector):
	if not gameselector:
		Mbox(gameselector,0)
		print('You are supposed to select a game you numbskul!')
		return 0
		
	elif gameselector[0]==0:
		GameCircles.GameRun()
		return 0
	
	elif gameselector[0]==1:
		GameSquares.GameRun()
		return 0
	
	elif gameselector[0]==2:
		GameMath.GameRun()
		return 0

	elif gameselector[0]==3:
		GameAlphabet.GameRun()
		return 0
		
	else:
		Mbox(gameselector,0)
		print("Game is not yet developed")

def CloseApp(frame):
	ctypes.windll.user32.MessageBoxW(0, "Thank you for playing! <3", "You are my hero", 0)
	frame.quit()
		
#define the frame where the buttons and lists are
top = Tk()
frame=Frame(top)
frame.grid(column = 0, row = 0, sticky=(N, W, E, S))
top.columnconfigure(0,weight=1)
top.rowconfigure(0,weight=1)
top.title('Game for kids')

#define the list with the options
ListaOptiuni=Listbox(frame)
ListaOptiuni.grid(column=1,row=1,sticky=S)
ListaOptiuni.insert(1, "Game Circles")
ListaOptiuni.insert(2, "Game Squares")
ListaOptiuni.insert(3, "Game Math")
ListaOptiuni.insert(4, "Game Alphabet")
ListaOptiuni.insert(5, "Game not developed")

#define buttons
GetInfo = Button(frame,text="Get info on the game",command = lambda: Mbox(ListaOptiuni.curselection(),0),padx=10,pady=10).grid(column=4,row=1)
Runapp = Button(frame,text="Run the game",command = lambda: RunGame(ListaOptiuni.curselection()),padx=10,pady=10).grid(column=0,row=3,sticky=S)
Close = Button(frame,text="Close the game",command = lambda: CloseApp(top),padx=10,pady=10).grid(column=4,row=3,sticky=S)
FutureUse = Button(frame,text="Do not press",command = lambda: Mbox((10,0),0),padx=10,pady=10).grid(column=1,row=3,sticky=S)

#define labels with text
LabelLeft = Label(frame, text="Created by Vasile-Simion Sularea \nin April 2019",width=30,height=10)
LabelLeft.grid(column=0,row=1,sticky=N )

#define labels just for arranging things in the frame
LabelLeft = Label(frame, text="",height=1)
LabelLeft.grid(column=1,row=2,sticky=N )
#LabelLeft = Label(frame, text="",height=0)
#LabelLeft.grid(column=1,row=0,sticky=N )
LabelLeft = Label(frame, text="",width=2)
LabelLeft.grid(column=3,row=1)
LabelLeft = Label(frame, text="",width=2)
LabelLeft.grid(column=5,row=1)


#Run UI
top.mainloop()