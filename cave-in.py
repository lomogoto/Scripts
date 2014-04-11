#!/bin/env python2

import socket
import thread
import curses
import time
from random import randint

port = 4682

yourIP = socket.gethostbyname(socket.gethostname())

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

address=('',0)

server = False

if raw_input('\nServer?(Y/n) ')!='n':
	print "\nYour IP address:", yourIP
	s.bind(('', port))
	address=s.recvfrom(1024)[1]
	server = True

else:
	address=(raw_input("\nOpponent's IP address: " ),port)
	print address
	if address[0].find('.')==-1:
		if address[0]=='':
			address=('127.0.0.1',address[1])
		else:
			address=('192.168.0.'+address[0], address[1])
	s.sendto('connected', address)

#### #### #### #### ####

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


def main(screen):

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
		sendMap(screen)
	else:
		getMap(screen)
	
	menu=False

	while running:
		printMap(screen)
		try:
			c=chr(screen.getch())
		except:
			c=0

		if c==' ':
			menu=not menu

		elif c=='j':
			if menu:
				if menuPos<10:
					menuPos+=1
			elif pos[1]<44:
				pos[1]+=1

		elif c=='k':
			if menu:
				if menuPos>0:
					menuPos-=1
			elif pos[1]>0:
				pos[1]-=1

		elif c=='J':
			if pos[0]>0:
				pos[0]-=1

		elif c=='K':
			if pos[0]<9:
				pos[0]+=1

		elif c=='h':
			if pos[2]>0:
				pos[2]-=1

		elif c=='l':
			if pos[2]<59:
				pos[2]+=1

		elif c=='!':
			pos=[9,22,14+31*server]

		elif c=='q':
			screen.addstr(0,0,'quit?(y/N)')
			if chr(screen.getch())=='y':
				running=False
			else:
				screen.addstr(0,0,' '*10)

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
	

def sendMap(screen):
	screen.addstr(4,2,'Sending Map')
	for z in range(10):
		for y in range(45):
			s.sendto(str(gameMap[z][y]), address)
			time.sleep(0.01)
		screen.addstr(5,z+3,'#')
		screen.refresh()

def getMap(screen):
	screen.addstr(4,2,'Getting Map')
	for z in range(10):
		level=[]
		for y in range(45):
			level.append(eval(s.recvfrom(2048)[0]))
		gameMap.append(level)
		screen.addstr(5,z+3,'#')
		screen.refresh()

def printMap(screen):
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
s.close()
