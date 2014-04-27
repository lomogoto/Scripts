#!/bin/env python2

import socket
import thread
import curses
import time
from os import getenv
from random import randint

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
items=    [ 0,       0,        0,      0,       0,         0,         0,         0,        0,       0,       0]
pos=[9,22,14+31*server]
menuPos=0
running = True


enemies='fgsbt-i'
friends='FGSBT_!'
clear=enemies+friends+'@~ Z'


def main(scr):
	global screen
	screen=scr

	curses.curs_set(0)
	curses.init_pair(1,7,0)
	curses.init_pair(2+server,1,0)
	curses.init_pair(3-server,6,0)
	curses.init_pair(4,7,7)
	curses.init_pair(5,4,0)
	curses.init_pair(6,0,6)

	global running
	global menuPos
	global pos
	if server:
		makeMap()
		sendMap()
		thread.start_new_thread(addAnimals,())
	else:
		getMap()
	
	thread.start_new_thread(harvest,())
	thread.start_new_thread(getUpdates,())
	
	menu=False

	while running:
		printMap()
		try:
			c=chr(screen.getch())
		except:
			c=0

		if c==menuToggleKey:
			menu=not menu

		elif c==downKey:
			if menu:
				if menuPos<10:
					menuPos+=1
			elif pos[1]<44:
				pos[1]+=1

		elif c==upKey:
			if menu:
				if menuPos>0:
					menuPos-=1
			elif pos[1]>0:
				pos[1]-=1

		elif c==digKey:
			if pos[0]>0:
				pos[0]-=1

		elif c==climbKey:
			if pos[0]<9:
				pos[0]+=1

		elif c==leftKey:
			if pos[2]>0:
				pos[2]-=1

		elif c==rightKey:
			if pos[2]<59:
				pos[2]+=1

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
					update(formatUpdate(pos[0],pos[1],pos[2]+1-2*server,char))
					update(formatUpdate(pos[0],pos[1],pos[2]+2-4*server,char))
					
				update(formatUpdate(pos[0],pos[1],pos[2],char))

		elif c==quitKey:
			screen.addstr(0,0,'quit?(y/N)')
			if chr(screen.getch())=='y':
				running=False
				sock.sendto('quit', address)
			else:
				screen.addstr(0,0,' '*10)

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

	if server:
		pass #thread.start_new_thread(checkConflicts,())
	else:
		pass #thread.start_new_thread(checkCaveIns,())

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
		update(formatUpdate(9,y,x,'@'))

def formatUpdate(z,y,x,c):
	return str(z)+'0'*(y<10)+str(y)+'0'*(x<10)+str(x)+c

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
			time.sleep(0.01)
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
				try:
					displaychar=friends[enemies.index(char)]
				except:
					displaychar=char
				screen.addstr(i+4, 17+j ,displaychar ,curses.color_pair(1 + (enemies.find(char)!=-1) + 2*(friends.find(char)!=-1)+3*(char=='X')+4*(char=='~')))

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
				try:
					displaychar=friends[enemies.index(char)]
				except:
					displaychar=char
				screen.addstr(i+10, 17+j ,displaychar ,curses.color_pair(1 + (enemies.find(char)!=-1) + 2*(friends.find(char)!=-1)+3*(char=='X')+4*(char=='~')))

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
			try:
				displaychar=friends[enemies.index(char)]
			except:
				displaychar=char
			if i==5 and j==7:
				color=6
			else:
				color=1 + (enemies.find(char)!=-1) + 2*(friends.find(char)!=-1)+3*(char=='X')+4*(char=='~')
			screen.addstr(i+4, 1+j ,displaychar ,curses.color_pair(color))

	screen.addstr(21,0,str(pos))
	screen.refresh()

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
sock.close()
