#!/usr/bin/env python2.7
import g
import f
import c
import display
import forces

running=True
compute_times=0
command=''
time=0
while running:
	while compute_times>0:
		for i in range(len(g.particles)):
			g.particles[i].apply_force(forces.gravitational(g.particles[i]))
			for j in range(len(g.particles)):
				if not i==j:
					g.particles[i].apply_force(forces.electric(g.particles[i], g.particles[j]))
					g.particles[i].apply_force(forces.strong(g.particles[i], g.particles[j]))
		for particle in g.particles:
			particle.update()
		compute_times-=1
		time+=1

	display.update()

	cmd = raw_input('>>> ')
	if cmd!='':
		command=cmd

	if command=='exit':
		exit()
	elif command=='clear':
		time=0
		display.move_position=(0,0)
		g.particles=[]
		print('Time: 0')
	elif command=='m':
		display.move()
	elif command=='e':
		display.add_electron()
	elif command=='p':
		display.add_proton()
	elif command=='n':
		display.add_neutron()
	else:
		try:
			compute_times=int(command)
			print('Time: '+str(time+compute_times))
		except:
			pass
