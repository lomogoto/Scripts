#!/usr/bin/env python2.7
import g
import particle
import display
import forces

running=True
compute_times=0

g.particles.append(particle.particle([100,403], 1, 1, 0, [4,0]))
g.particles.append(particle.particle([100,398], 1, 1, 0, [-3,0]))
g.particles.append(particle.particle([100,400], 1000, -1, 1))
g.particles.append(particle.particle([120,400], 1000, -1, 1))

g.particles.append(particle.particle([100,401], 1000, -1, 1))
g.particles.append(particle.particle([120,401], 1000, -1, 1))

while running:
	while compute_times>0:
		for i in range(len(g.particles)):
			force=forces.gravitational(g.particles[i])
			for j in range(len(g.particles)):
				if not i==j:
					Fe=forces.electric(g.particles[i], g.particles[j])
					Fm=forces.magnetic(g.particles[i], g.particles[j])
					Fs=forces.strong(g.particles[i], g.particles[j])
					force = [force[0]+Fe[0]+Fm[0]+Fs[0], force[1]+Fe[1]+Fm[1]+Fs[1]]
			g.particles[i].apply_force(force)
		for particle in g.particles:
			particle.update()
			print(particle.position, particle.velocity)
		compute_times=compute_times-1
	display.update()
	command = raw_input('>>> ')
	if command=='exit':
		exit()
	else:
		try:
			compute_times=int(command)
		except:
			pass
