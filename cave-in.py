#!/bin/env python2

import socket
import thread
import curses
import time
from os import getenv
from random import randint
from sys import argv

def gameHelp():
	print '\nCave In Help Page\n'
	print 'Configuration file: ~/.cave-in'
	print 'Variables:'
	print '  leftKey'
	print '  rightKey'
	print '  upKey'
	print '  downKey'
	print '  digKey'
	print '  climbKey'
	print '  menuToggleKey'
	print '  mineKey'
	print '  buyKey'
	print '  placeKey'
	print '  homeKey'
	print '  quitKey'
	print '  loadTime'
	print 'Examples:'
	print '  Copy into dot file to use WASD control:'
	print "    leftKey='a'"
	print "    rightKey='d'"
	print "    upKey='w'"
	print "    downKey='s'"
	print '  Add to set load time to 3 seconds:'
	print '    loadTime=3'

	exit()

for arg in argv:
	if arg[0]=='-' and len(arg)>1:
		for flag in arg[1:]:
			if flag=='h':
				gameHelp()

leftKey='h'
rightKey='l'
upKey='k'
downKey='j'
digKey='J'
climbKey='K'
menuToggleKey=' '
mineKey='m'
buyKey='b'
placeKey='p'
homeKey='!'
quitKey='q'

loadTime=5

try:
	with open(getenv('HOME')+'/.cave-in','r') as configFile:
		for line in configFile:
			try:
				exec(line)
			except:
				print '\nERROR FOUND. Skipping line:', line.strip('\n')
	print('\nConfiguration Complete')
except:
	pass #print('\nNo Configuration Found\nUsing default settings')

port = 4682

yourIP = socket.gethostbyname(socket.gethostname())

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

address=('',0)

server = False

if raw_input('\nServer?(Y/n) ')!='n':
	print "\nYour IP address:", yourIP
	sock.bind(('', port))
	address=sock.recvfrom(1024)[1]
	server = True

else:
	address=(raw_input("\nOpponent's IP address: " ),port)
	#print address
	if address[0].find('.')==-1:
		if address[0]=='':
			address=('127.0.0.1',address[1])
		else:
			try:
				int(address[0])
				address=('192.168.0.'+address[0], address[1])
			except:
				address=(eval(address[0]),address[1])
	sock.sendto('connected', address)

#### #### #### #### ####

screen=None

gameMap=[]
resourceNames=('@', 'o', '#', '%', '*', '&', '$')
resources=    [ 0,   0,   0,   0,   0,   0,   0]
itemNames=('Traps', 'Powder', 'Guns', 'Bombs', 'Runners', 'Gunners', 'Bombers', 'Towers', 'Farms', 'Walls', 'Bridges')
items=    [ 0,       0,        0,      0,       0,         0,         0,         0,        1,       0,       0]
itemPrices=(((0,2,1,0,0,1,0),(0,0,0,1,0,0,0,0,0,0,0)),
			((0,2,0,1,1,0,0),(0,0,0,0,0,0,0,0,0,0,0)),
			((0,0,1,0,0,0,0),(0,1,0,0,0,0,0,0,0,0,0)),
			((0,0,2,0,1,1,0),(0,2,0,0,0,0,0,0,0,0,0)),
			((2,0,1,0,0,0,0),(0,0,0,0,0,0,0,0,0,0,0)),
			((1,0,0,0,0,0,0),(0,0,1,0,1,0,0,0,0,0,0)),
			((1,0,0,0,0,0,0),(0,0,0,1,0,1,0,0,0,0,0)),
			((2,10,5,0,0,0,0),(0,0,0,0,0,1,1,0,0,0,0)),
			((15,0,0,0,0,0,0),(0,0,0,0,0,0,0,0,0,0,0)),
			((0,2,1,0,0,0,0),(0,0,0,0,0,0,0,0,0,0,0)),
			((0,20,10,0,0,0,0),(0,0,0,0,0,0,0,0,0,0,0)))
pos=[9,22,14+31*server]
menuPos=0
running = True


enemies='fgrbt-i'
friends='FGRBT_!'
if server:
	swap=enemies
	enemies=friends
	friends=swap
clear=enemies+friends+'@~ Z'
solid='o#%*&$X~'
canMine='o#%*&$'
support='o#%*&$X'
canNotMove='!iZ'

def main(scr):
	global screen
	screen=scr
	curses.curs_set(0)
	curses.init_pair(1,7,0)
	curses.init_pair(2,1,0)
	curses.init_pair(3,6,0)
	curses.init_pair(4,7,7)
	curses.init_pair(5,4,0)
	curses.init_pair(6,0,6)
	curses.init_pair(7,3,0)

	global running
	global menuPos
	global pos
	if server:
		makeMap()
		sendMap()
		thread.start_new_thread(addAnimals,())
		thread.start_new_thread(caveIn,())
	else:
		getMap()
		thread.start_new_thread(fixConflicts,())
	
	thread.start_new_thread(harvest,())
	thread.start_new_thread(getUpdates,())

	menu=False
	mine=False

	moveChar=' '
	while running:
		printMap()
		try:
			c=chr(screen.getch())
		except:
			c=0

		if c==menuToggleKey:
			menu=not menu
		
		elif c==mineKey:
			if not mine:
				mine=True
				moveChar=gameMap[pos[0]][pos[1]][pos[2]]
				if canNotMove.find(moveChar)!=-1:
					moveChar=' '
				else:
					formatUpdate(pos[0],pos[1],pos[2], ' ')
			elif canNotMove.find(gameMap[pos[0]][pos[1]][pos[2]])==-1:
				mine=False
				formatUpdate(pos[0],pos[1],pos[2], moveChar)

		elif c==downKey:
			if menu:
				if menuPos<10:
					menuPos+=1
			else:
				tryMove((0,1,0), mine)
		
		elif c==upKey:
			if menu:
				if menuPos>0:
					menuPos-=1
			else:
				tryMove((0,-1,0), mine)

		elif c==digKey:
			tryMove((-1,0,0), mine)

		elif c==climbKey:
			tryMove((1,0,0), mine)

		elif c==leftKey:
			tryMove((0,0,-1), mine)

		elif c==rightKey:
			tryMove((0,0,1), mine)

		elif c==homeKey:
			pos=[9,22,7+45*server]

		elif c==buyKey:
			canBuy=True
			if canBuy:
				items[menuPos]+=1
		elif c==placeKey:
			canPlace=(menuPos==0 or menuPos>3)
			if canPlace and items[menuPos]>0:
				items[menuPos]-=1
				char=' '
				if menuPos==0:
					char='-'*server+'_'*(not server)
				elif menuPos==4:
					char='r'*server+'R'*(not server)
				elif menuPos==5:
					char='g'*server+'G'*(not server)
				elif menuPos==6:
					char='b'*server+'B'*(not server)
				elif menuPos==7:
					char='t'*server+'T'*(not server)
				elif menuPos==8:
					char='f'*server+'F'*(not server)
				elif menuPos==9:
					char='X'
				elif menuPos==10:
					formatUpdate(pos[0],pos[1],pos[2]+1-2*server,char)
					formatUpdate(pos[0],pos[1],pos[2]+2-4*server,char)
					
				formatUpdate(pos[0],pos[1],pos[2],char)

		elif c==quitKey:
			screen.addstr(0,0,'quit?(y/N)')
			c=chr(screen.getch())
			if running and c=='y':
				running=False
			elif c==':':
				good=True
				for letter in upKey*2+downKey*2+leftKey+rightKey+leftKey+rightKey+'ba':
					if good:
						good=chr(screen.getch())==letter
					else:
						break
				if good:
					global resources
					resources=[99,99,99,99,99,99,99]
			screen.addstr(0,0,' '*10)
				

		elif c=='E':
			return Exception('Testing Exception')

def fixConflicts():
	while running:
		conflictList=[]
		for z in range(10):
			for y in range(45):
				for x in range(60):
					char=gameMap[z][y][x]
					if friends.find(char)!=-1:
					 	for i in range(7):
							for j in range(7):
								eChar=gameMap[z][y-3+i][x-3+j]
								if enemies.find(eChar)!=-1:
									conflictList.append(((z,y,x),(z,y-3+i,x-3+j)))
		for conflict in conflictList:
			fPos=conflict[0]
			ePos=conflict[1]
			fChar=gameMap[fPos[0]][fPos[1]][fPos[2]]
			eChar=gameMap[ePos[0]][ePos[1]][ePos[2]]
			if friends.find(fChar)!=-1 and enemies.find(eChar)!=-1:
				order=randint(0,1)
				if order:
					actFighter(fChar,fPos,eChar,ePos)
				else:
					actFighter(eChar,ePos,fChar,fPos)
										
			screen.addstr(0,0,str(z))
		time.sleep(0.1)

def actFighter(fChar,fPos,eChar,ePos):
	distance=abs(fPos[1]-ePos[1])+abs(fPos[2]-ePos[2])
	direction=((ePos[1]-fPos[1]),(ePos[2]-fPos[2]))
	if 'Rr'.find(fChar)!=-1:
		if distance<2 and '!i'.find(eChar)==-1:
			formatUpdate(ePos[0],ePos[1],ePos[2],' ')
		else:
			fighterMove(fPos,direction)		
	elif 'Gg'.find(fChar)!=-1:
		if distance<3 and '!i_-'.find(eChar)==-1:
			formatUpdate(ePos[0],ePos[1],ePos[2],' ')
		else:
			fighterMove(fPos,direction)		
	elif 'Bb'.find(fChar)!=-1:
		if distance<3 and '_-'.find(eChar)==-1:
			for i in range(3):
				formatUpdate(fPos[0],fPos[1]-2,fPos[2]-1+i,' ')
				formatUpdate(fPos[0],fPos[1]+2,fPos[2]-1+i,' ')
			for i in range(3):
				for j in range(5):
					formatUpdate(fPos[0],fPos[1]-1+i,fPos[2]-2+j,' ')
		else:
			fighterMove(fPos,direction)		
	elif 'Tit!'.find(fChar)!=-1:
		if distance<5 and '!i_-'.find(eChar)==-1:
			formatUpdate(ePos[0],ePos[1],ePos[2],' ')
	elif '_-'.find(fChar)!=-1:
		if distance<2 and '!i_-'.find(eChar)==-1:
			formatUpdate(ePos[0],ePos[1],ePos[2],' ')
			formatUpdate(fPos[0]-1,fPos[1],fPos[2],eChar)

def fighterMove(fPos,direction):
	char=gameMap[fPos[0]][fPos[1]][fPos[2]]
	if direction[1]>0 and gameMap[fPos[0]][fPos[1]][fPos[2]+1]==' ':
		formatUpdate(fPos[0],fPos[1],fPos[2],' ')
		formatUpdate(fPos[0],fPos[1],fPos[2]+1,char)
	elif direction[1]<0 and gameMap[fPos[0]][fPos[1]][fPos[2]-1]==' ':
		formatUpdate(fPos[0],fPos[1],fPos[2],' ')
		formatUpdate(fPos[0],fPos[1],fPos[2]-1,char)
	if direction[0]>0 and gameMap[fPos[0]][fPos[1]+1][fPos[2]]==' ':
		formatUpdate(fPos[0],fPos[1],fPos[2],' ')
		formatUpdate(fPos[0],fPos[1]+1,fPos[2],char)
	elif direction[0]<0 and gameMap[fPos[0]][fPos[1]-1][fPos[2]]==' ':
		formatUpdate(fPos[0],fPos[1],fPos[2],' ')
		formatUpdate(fPos[0],fPos[1]-1,fPos[2],char)

def caveIn():
	for z in range(9):
		for y in range(45):
			for x in range(60):
				willCave=True
				for i in range(5):
					for j in range(5):
						try:
							char=gameMap[z][y-2+i][x-2+j]
						except:
							char='o'
						if support.find(char)!=-1:
							willCave=False
				if willCave:
					for i in range(5):
						for j in range(5):
							if y+i-2<45 and y+i-2>=0 and x+j-2<60 and x+j-2>=0:
								formatUpdate(z,y-2+i,x-2+j,'o')
								time.sleep(0.2)
					formatUpdate(z,y,x,'$')

def tryMove(direction, mining=False):
	priceSameLevel=2
	priceUpDown=6
	global pos
	newpos=(pos[0]+direction[0], pos[1]+direction[1], pos[2]+direction[2])
	if newpos[0]>=0 and newpos[0]<10 and newpos[1]>=0 and newpos[1]<45 and newpos[2]>=0 and newpos[2]<60:
		char=gameMap[newpos[0]][newpos[1]][newpos[2]]
		isSolid=solid.find(char)!=-1
		isUpDown=direction[0]!=0
		if isUpDown and (char!='Z' and gameMap[pos[0]][pos[1]][pos[2]]!='Z'):
			isSolid=True
		if mining and (canMine.find(char)!=-1 or (char==' ' and isUpDown)):
			if isUpDown:
				if resources[0]+resources[6]>=priceUpDown:
					resources[0]-=priceUpDown
					if resources[0]<0:
						resources[6]+=resources[0]
						resources[0]=0
					formatUpdate(pos[0],pos[1],pos[2],'Z')
					formatUpdate(newpos[0],newpos[1],newpos[2],'Z')
				else:
					mining=False
			else:
				if resources[0]+resources[6]>=priceSameLevel:
					resources[0]-=priceSameLevel
					if resources[0]<0:
						resources[6]+=resources[0]
						resources[0]=0
					resources[resourceNames.index(char)]+=1
					formatUpdate(newpos[0],newpos[1],newpos[2],' ')
				else:
					mining=False
		else:
			mining=False

		if char=='@':
			resources[0]+=1
			formatUpdate(newpos[0],newpos[1],newpos[2],' ')

		if mining or not isSolid:
			if not inRange(newpos):
				pos=newpos

def inRange(pos):
	for i in range(3):
		try:
			if enemies.find(gameMap[pos[0]][pos[1]-1+i][pos[2]-2])!=-1:
				return True
		except:
			pass
		try:
			if enemies.find(gameMap[pos[0]][pos[1]-1+i][pos[2]+2])!=-1:
				return True
		except:
			pass
	for i in range(5):
		for j in range(3):
			try:
				if enemies.find(gameMap[pos[0]][pos[1]-2+i][pos[2]-1+j])!=-1:
					return True
			except:
				pass
	return False

def getUpdates():
	global running
	while running:
		text=sock.recvfrom(1024)[0]
		if text!='quit':
			update(text, False)
		else:
			running=False
			screen.addstr(0,0,'GAME QUIT')
			screen.refresh()

def update(s, send=True):
	try:
		z=int(s[0])
		y=int(s[1:3])
		x=int(s[3:5])
		c=s[5]
	except:
		pass
	gameMap[z][y][x]=c
	printMap()

	if send:
		sock.sendto(s ,address)
		time.sleep(0.05)

def harvest():
	while running:
		time.sleep(randint(10,15))
		for y in range(0,45):
			for x in range(0,60):
				if gameMap[9][y][x]==('f'*server + 'F'*(not server)):
					resources[0]+=1
		printMap()

def addAnimals():
	while running:
		time.sleep(randint(10,20))
		
		y=randint(0,44)
		x=randint(0,59)
		
		while gameMap[9][y][x]!=' ':
			y=randint(0,44)
			x=randint(0,59)
		formatUpdate(9,y,x,'@')

def formatUpdate(z,y,x,c):
	update(str(z)+'0'*(y<10)+str(y)+'0'*(x<10)+str(x)+c)

def checkCaveIns():
	toFill=[]
	for z in range(0,9):
		for y in range(0,44):
			for x in range(0,59):
				wontCave='o#%&*$'
				willCave=(z!=9)
				for i in range(-2,3):
					for j in range(-2,3):
						if wontCave.find(gameMap[z][y+j][x+i])==-1:
							willCave==False
				if willCave:
					for i in range(-2,3):
						for j in range(-2,3):
							toFill.append((z,y+j,x+i))

	for place in toFill:
		z,y,x=place
		char='o'
		rand = randint(0,24)
		if rand==0:
			rand=randint(0,2)
			char=wontCave[2+rand]
		else:
			rand=randint(0,1)
			char=wontCave[rand]
		gameMap[z][y+j][x+i]=char

def makeMap():
	global gameMap
	for z in range(10):
		level=[]
		for y in range(45):
			row=[]
			for x in range(60):
				char='o'
				rand = randint(0,25-z)

				if rand > 24:
					char=resourceNames[6]
				elif rand > 22:
					char=resourceNames[5]
				elif rand > 19:
					char=resourceNames[4]
				elif rand > 15:
					char=resourceNames[3]
				elif rand > 10:
					char=resourceNames[2]
				elif rand > 5:
					char=resourceNames[1]
				elif rand > 0:
					if not randint(0,10) and z<5:
						char = 'X'

				row.append(char)
			level.append(row)
		gameMap.append(level)
	for i in range(4,56):
		gameMap[9][22][i]=' '
	for i in range(5,10):
		gameMap[9][21][i]=' '
		gameMap[9][23][i]=' '
	for i in range(50,55):
		gameMap[9][21][i]=' '
		gameMap[9][23][i]=' '
	gameMap[9][22][7]='!'
	gameMap[9][22][52]='i'
		
	j=44
	for i in range(22):
		gameMap[9][21-i][j]=' '
		if i%2==0:
			j=j-1+randint(0,2)
	j=44
	for i in range(22):
		gameMap[9][23+i][j]=' '
		if i%2==0:
			j=j-1+randint(0,2)
	
	j=15
	for i in range(22):
		j2=j
		while gameMap[9][21-i][j2]!=' ':
			gameMap[9][21-i][j2]=' '
			j2+=1
		if i%2==0:
			j=j-1+randint(0,2)
	j=15
	for i in range(22):
		j2=j
		while gameMap[9][23+i][j2]!=' ':
			gameMap[9][23+i][j2]=' '
			j2+=1
		if i%2==0:
			j=j-1+randint(0,2)
	
	gameMap[9][22][29]='~'
	gameMap[9][22][30]='~'

	j=29
	for i in range(22):
		gameMap[9][23+i][j]='~'
		gameMap[9][23+i][j+1]='~'
		j=j-1+randint(0,2)
	

	j=29
	for i in range(22):
		gameMap[9][21-i][j]='~'
		gameMap[9][21-i][j+1]='~'
		j=j-1+randint(0,2)
	

def sendMap():
	screen.addstr(4,2,'Sending Map')
	for z in range(10):
		for y in range(45):
			sock.sendto(str(gameMap[z][y]), address)
			time.sleep(loadTime/450.0)
		screen.addstr(5,z+3,'#')
		screen.refresh()

def getMap():
	screen.addstr(4,2,'Getting Map')
	for z in range(10):
		level=[]
		for y in range(45):
			level.append(eval(sock.recvfrom(2048)[0]))
		gameMap.append(level)
		screen.addstr(5,z+3,'#')
		screen.refresh()

def printMap():
	for i in range(len(resources)):
		if resources[i]>99:
			resources[i]=99
	for i in range(len(items)):
		if items[i]>99:
			items[i]=99
	screen.addstr(0,18,'Cave  In')
	screen.addstr(menuPos+3,26,' ')
	screen.addstr(menuPos+4,26,'>')
	screen.addstr(menuPos+5,26,' ')
	screen.addstr(1,1,'-'*42)
	screen.addstr(3,1,'-'*42)
	screen.addstr(15,1,'-'*42)
	screen.addstr(9,17,'-'*7)
	for i in range(13):
		screen.addstr(i+2,0,'|')
		screen.addstr(i+2,43,'|')
		if i>1:
			screen.addstr(i+2,16,'|')
			screen.addstr(i+2,24,'|')
			screen.addstr(i+2,37,':')
	for i in range(7):
		screen.addstr(2, 2+i*6, resourceNames[i]+':'+displayNum(resources[i]))
	for i in range(11):
		screen.addstr(i+4, 28, itemNames[i])
		screen.addstr(i+4, 40, displayNum(items[i]))
	
	if pos[0]==9:
		for i in range(5):
			screen.addstr(i+4,17,' '*7)
		screen.addstr(6,19,'SKY')
	else:
		for i in range(5):
			for j in range(7):
				char='/'
				try:
					if pos[1]-2+i>=0 and pos[2]-3+j>=0:
						char=gameMap[pos[0]+1][pos[1]-2+i][pos[2]-3+j]
						if not visible(pos[0]+1,pos[1]-2+i,pos[2]-3+j):
							char='.'
				except:
					pass
				displaychar=char
				if friends<enemies:
					try:
						displaychar=friends[enemies.index(char)]
					except:
						pass
				else:
					try:
						displaychar=enemies[friends.index(char)]
					except:
						pass
						
				if displaychar=='_' and enemies.find(char)!=-1:
					displaychar=' '

				screen.addstr(i+4, 17+j ,displaychar ,curses.color_pair(2*(enemies.find(char)!=-1) + 3*(friends.find(char)!=-1) + 4*(char=='X') + 5*(char=='~') + 7*('$Z@'.find(char)!=-1)))

	if pos[0]==0:
		for i in range(5):
			screen.addstr(i+10,17,'/'*7)
		screen.addstr(12,17,'BEDROCK')
	else:
		for i in range(5):
			for j in range(7):
				char='/'
				try:
					if pos[1]-2+i>=0 and pos[2]-3+j>=0:
						char=gameMap[pos[0]-1][pos[1]-2+i][pos[2]-3+j]
						if not visible(pos[0]-1,pos[1]-2+i,pos[2]-3+j):
							char='.'
				except:
					pass
				displaychar=char
				if friends<enemies:
					try:
						displaychar=friends[enemies.index(char)]
					except:
						pass
				else:
					try:
						displaychar=enemies[friends.index(char)]
					except:
						pass

				if displaychar=='_' and enemies.find(char)!=-1:
					displaychar=' '

				screen.addstr(i+10, 17+j ,displaychar ,curses.color_pair(2*(enemies.find(char)!=-1) + 3*(friends.find(char)!=-1) + 4*(char=='X') + 5*(char=='~') + 7*('$Z@'.find(char)!=-1)))

	for i in range(11):
		for j in range(15):
			char='/'
			try:
				if pos[1]-5+i>=0 and pos [2]-7+j>=0:
					char=gameMap[pos[0]][pos[1]-5+i][pos[2]-7+j]
					if not visible(pos[0],pos[1]-5+i,pos[2]-7+j):
						char='.'
			except:
				pass
			displaychar=char
			if friends<enemies:
				try:
					displaychar=friends[enemies.index(char)]
				except:
					pass
			else:
				try:
					displaychar=enemies[friends.index(char)]
				except:
					pass

			if displaychar=='_' and enemies.find(char)!=-1:
				displaychar=' '

			if i==5 and j==7:
				color=6
			else:
				color=2*(enemies.find(char)!=-1) + 3*(friends.find(char)!=-1) + 4*(char=='X') + 5*(char=='~') + 7*('$Z@'.find(char)!=-1)
			screen.addstr(i+4, 1+j ,displaychar ,curses.color_pair(color))

	screen.addstr(16,0,' '*40)
	screen.addstr(16,0,getPriceString())
	#screen.addstr(21,0,str(enemies + ' ' + friends))
	screen.refresh()

def getPriceString():
	price=''
	for i in range(7):
		if itemPrices[menuPos][0][i]>0:
			price+=str(itemPrices[menuPos][0][i])+' '+resourceNames[i]+', '
	for i in range(11):
		if itemPrices[menuPos][1][i]>0:
			price+=str(itemPrices[menuPos][1][i])+' '+itemNames[i]+', '
	price=price[0:-2]
	return price

def visible(z,y,x):
	if clear.find(gameMap[z][y][x])!=-1:
		return 1
	if z!=0 and clear.find(gameMap[z-1][y][x])!=-1:
		return 1
	if z!=9 and clear.find(gameMap[z+1][y][x])!=-1:
		return 1
	if y!=0 and clear.find(gameMap[z][y-1][x])!=-1:
		return 1
	if y!=44 and clear.find(gameMap[z][y+1][x])!=-1:
		return 1
	if x!=0 and clear.find(gameMap[z][y][x-1])!=-1:
		return 1
	if x!=59 and clear.find(gameMap[z][y][x+1])!=-1:
		return 1
	return 0

def displayNum(n):
	if n<10:
		return '0'+str(n)
	else:
		return str(n)

curses.wrapper(main)

sock.sendto('quit', address)
sock.close()
