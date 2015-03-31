#!/usr/bin/env python2.7
import g
import display
import forces

running=True
compute_times=0
command=''

while running:
	while compute_times>0:
		for i in range(len(g.particles)):
			g.particles[i].apply_force(forces.gravitational(g.particles[i]))
			for j in range(len(g.particles)):
				if not i==j:
					g.particles[i].apply_force(forces.electric(g.particles[i], g.particles[j]))
					g.particles[i].apply_force(forces.magnetic(g.particles[i], g.particles[j]))
					g.particles[i].apply_force(forces.strong(g.particles[i], g.particles[j]))
		for particle in g.particles:
			particle.update()
		compute_times=compute_times-1

	display.update()

	c = raw_input('>>> ')
	if c!='':
		command=c

	if command=='exit':
		exit()
	elif command=='clear':
		g.particles=[]
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
		except:
			pass
