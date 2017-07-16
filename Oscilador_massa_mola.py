#_*_ coding: utf-8 _*_
#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt 
from matplotlib import animation

#constants
g = 9.81
dt = 0.01
#end

class Oscilador_massa_mola(object):
	def __init__(self,
				 massa,# massa do bloco 
				 k,# coeficiente de mola
				 b,#comprimento da mola
				 l,#comprimento da haste
				 theta,#angulo
				 v#velocidade
				 ):
		self.m = massa
		self.l = l 
		self.b = b
		self.x = theta
		self.v = v
		self.vl = v
		self.k = k
		
	def a1(self,l,x,v,vl):
		return g/self.l*math.sin(x)-2*vl/l*v
	def a2(self,l,x,v):
		return l*v**2-g*math.cos(x)-self.k/self.m*(l-self.b)
				
	def move(self):
		at1 = self.a1(self.l,self.x,self.v,self.vl)
		at2 = self.a2(self.l,self.x,self.v)
			
		self.x += self.v*dt + at1*dt*dt/2.
		self.l += self.vl*dt + at2*dt*dt/2.
		
		a_tmp1 = self.a1(self.l,self.x,self.v,self.vl)
		a_tmp2 = self.a2(self.l,self.x,self.v)
		
		v_tmp1 = self.v+(at1+a_tmp1)*dt/2. 
		v_tmp2 = self.vl+(at2+a_tmp2)*dt/2.
		
		a_tmp1 = self.a1(self.l,self.x,v_tmp1,v_tmp2)
		a_tmp2 = self.a2(self.l,self.x,v_tmp1)
		
		self.v += (a_tmp1+at1)*dt/2.
		self.vl += (a_tmp2+at2)*dt/2.
#end

def grafico(title,visivel = True):
	axes = plt.gca()
	axes.axes.get_xaxis().set_visible(visivel)
	axes.spines['top'].set_color('none')
	axes.spines['right'].set_color('none')
	axes.yaxis.set_ticks_position('left')
	axes.xaxis.set_ticks_position('bottom')
	axes.spines['bottom'].set_position(('data',0))
	axes.spines['left'].set_position(('data',0))
	plt.grid(True)
	plt.xlabel('X(m)')
	plt.ylabel('Y(m)')
	plt.rc('text',usetex = True)
	plt.rc('font',**{'sans-serif':'Arial','family':'sans-serif'})
	plt.title(r'\raggedright{\textit{'+title+'}}')
#end

#begin
p1 = Oscilador_massa_mola(1,30,3,10,np.pi/2,18)

tmax=30
t=np.arange(0,tmax,dt)
x1=np.zeros(t.size)
x2=np.zeros(t.size)

x1[0],x2[0]=p1.x,p1.l

for i in range(t.size):
	p1.move()
	x1[i],x2[i]=p1.x,p1.l

xBloco = x2*np.sin(x1)
yBloco = x2*np.cos(x1)

fig = plt.figure(figsize=(6,6),facecolor='white')

pendulo = plt.axes(xlim=(-45,45),ylim=(-45,45),aspect = 'equal')
grafico(r'Oscilador Masssa Mola')

line1 = [] 
Osc = pendulo.plot([],[],'r-',lw = 1)[0]
line1.append(Osc)
Osc = pendulo.plot([], [], 'ko-',markersize=8)[0]
line1.append(Osc)

def init():
	for lined in line1:
		lined.set_data([],[])
	return line1,

def animate(i):
	imin = 0 if  i < 10 else i-10
	b = xBloco[:i]
	c = yBloco[:i]
	d = [0,xBloco[i]]
	e = [0,yBloco[i]]
	line1[0].set_data(b,c)
	line1[1].set_data(d,e)
	return line1,
	
anim = animation.FuncAnimation(fig,animate,init_func = init, frames=t.size,interval=1,blit=False,repeat = False)

plt.show()

print 'concluido'