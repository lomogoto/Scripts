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
			Fg=forces.gravitational(g.particles[i])
			Fe=Fm=Fs=(0,0)
			for j in range(len(g.particles)):
				if not i==j:
					Fe=f.vector_add(Fe, forces.electric(g.particles[i], g.particles[j]))
					Fm=f.vector_add(Fm, forces.magnetic(g.particles[i], g.particles[j]))
					Fs=f.vector_add(Fs, forces.strong(g.particles[i], g.particles[j]))
			if Fm[0]>c.spin_switch_force:
				g.particles[i].spin*=-1
				Fm=(0,0)
			#g.particles[i].apply_force(Fg)
			g.particles[i].apply_force(Fe)
			#g.particles[i].apply_force(Fm)
			#g.particles[i].apply_force(Fs)
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
