#!/bin/env python2

import socket
import thread
import curses
import time

port = 4682

yourIP = socket.gethostbyname(socket.gethostname())

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

address=('',0)

server = True

if raw_input('\nServer?(Y/n) ')!='n':
	print "\nYour IP address:", yourIP
	s.bind(('', port))
	address=s.recvfrom(1024)[1]
	server = False

else:
	address=(raw_input("\nOpponent's IP address: " ),port)
	s.sendto('connected', address)

#### #### #### #### ####

gameMap=[]
resourceNames=('@', 'o', '#', '%', '*', '&', '$')
resources=    [ 0,   0,   0,   0,   0,   0,   0]
itemNames=('Traps', 'Powder', 'Guns', 'Bombs', 'Runners', 'Gunners', 'Bombers', 'Towers', 'Farms', 'Walls', 'Bridges')
items=    [ 0,       0,        0,      0,       0,         0,         0,         0,        0,       0,       0]
pos=[9,23,15]
menuPos=0
running = True

def main(screen):

	curses.curs_set(0)
	curses.init_pair(1,7,0)
	curses.init_pair(2+server,1,0)
	curses.init_pair(3-server,6,0)
	curses.init_pair(4,7,7)
	curses.init_pair(5,4,0)

	global running
	global menuPos

	makeMap()
	
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
		elif c=='k':
			if menu:
				if menuPos>0:
					menuPos-=1
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
				char='?'
				row.append(char)
			level.append(row)
		gameMap.append(level)
	gameMap[pos[0]-1][pos[1]-2][pos[2]]='f'
	gameMap[pos[0]-1][pos[1]-1][pos[2]]='F'
	gameMap[pos[0]-1][pos[1]][pos[2]]='X'
	gameMap[pos[0]-1][pos[1]+1][pos[2]]='~'

def printMap(screen):

	enemies='fgsbt-i'
	friends='FGSBT_!'

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
				char=gameMap[pos[0]+1][pos[1]-2+i][pos[2]-3+j]
				try:
					displaychar=friends[enemies.index(char)]
				except:
					displaychar=char
				screen.addstr(i+4, 17+j ,displaychar ,curses.color_pair(1 + (enemies.find(char)!=-1) + 2*(friends.find(char)!=-1)+3*(char=='X')+4*(char=='~')))

	if pos[0]==0:
		for i in range(5):
			screen.addstr(i+10,17,' '*7)
		screen.addstr(12,17,'BEDROCK')
	else:
		for i in range(5):
			for j in range(7):
				char=gameMap[pos[0]-1][pos[1]-2+i][pos[2]-3+j]
				try:
					displaychar=friends[enemies.index(char)]
				except:
					displaychar=char
				screen.addstr(i+10, 17+j ,displaychar ,curses.color_pair(1 + (enemies.find(char)!=-1) + 2*(friends.find(char)!=-1)+3*(char=='X')+4*(char=='~')))

	for i in range(11):
		for j in range(15):
			char=gameMap[pos[0]][pos[1]-5+i][pos[2]-7+j]
			try:
				displaychar=friends[enemies.index(char)]
			except:
				displaychar=char
			screen.addstr(i+4, 1+j ,displaychar ,curses.color_pair(1 + (enemies.find(char)!=-1) + 2*(friends.find(char)!=-1)+3*(char=='X')+4*(char=='~')))



def displayNum(n):
	if n<10:
		return '0'+str(n)
	else:
		return str(n)

curses.wrapper(main)
s.close()
