#!/bin/env python2

#import curses
#curses is built in and does not add dependencies
import curses

#create a main method to be run with a curses screen object
def main(screen):
	#make running variable
	running = True

	#print text while running
	while running:
		#add text starting at (5,5) from top left corner
		screen.addstr(5,5,'Hello World')

		#note in curses the X and Y positions are switched
		screen.addstr(6,5,'Press Q to quit')

		#try to get a character
		#getch would throw an error if an arrow key were pressed for example
		try:
			c = chr(screen.getch())

		#allow any error to be caught
		except:
			#do nothing if an error is thrown
			pass

		#quit if 'q' is pressed
		if c == 'q' or c == 'Q':
			running = False

#start curses running the main method
curses.wrapper(main)
