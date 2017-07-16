#_*_ coding: utf-8 _*_
#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

#constant
dt = 0.02
g = 9.8 
k = 25
#end

class Pendulo(object):
	'''__init__(self,massa,l,theta,v):
	l = comprimento do pendulo (raio)
	theta = angulo de partida
	v = velocidade inicial
	'''
	def __init__(self,massa,l,theta,v):
		self.m = massa
		self.l = l 
		self.x = theta
		self.v = v
		self.w2 = g/l 
		self.k = massa*self.w2
		self.e = 0.5*massa*(l*v)**2+massa*g*l*(1.-math.cos(theta))
		
	def a(self,r1,r2,v,t):
		return -self.w2*r1+(k/self.m)*(r2-r1)
				
	def move(self,r2,t):
		at = self.a(self.x,r2,self.v,t)
		self.x += self.v*dt + at*dt*dt/2.
		a_tmp = self.a(self.x,r2,self.v,t)
		v_tmp = self.v+(at+a_tmp)*dt/2. 
		a_tmp = self.a(self.x,r2,v_tmp,t)
		self.v += (a_tmp+at)*dt/2.
		self.e = 0.5*self.m*(self.l*self.v)**2 + (self.m*g*self.l*(1.-math.cos(self.x)))
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

p1 = Pendulo(0.25,0.5,-np.pi/2,0)
p2 = Pendulo(0.25,0.5,np.pi/2,0.1)

tmax=10
t=np.arange(0,tmax,dt)

r1=np.zeros(t.size)
v1=np.zeros(t.size)
e1=np.zeros(t.size)
r1[0],v1[0],e1[0]=p1.x,p1.v,p1.e

r2=np.zeros(t.size)
v2=np.zeros(t.size)
e2=np.zeros(t.size)
r2[0],v2[0],e2[0]=p2.x,p2.v,p2.e

for i in range(t.size):
	p1.move(p2.x,t[i])
	r1[i],v1[i],e1[i]=p1.x,p1.v,p1.e
	
	p2.move(p1.x,t[i])
	r2[i],v2[i],e2[i]=p2.x,p2.v,p2.e

fig = plt.figure(figsize=(12,6),facecolor='white')

# Agora faremos um distanciamento simetrico dos pendulos em relação a origem
l=p1.l
xp=np.sin(r1)*l-0.5 # (*) translada o eixo x para a esquerda
yp=-np.cos(r1)*l

l2=p2.l
xp2=(np.sin(r2)*l2)+0.5 # (**) translada o eixo x para a direita
yp2=-(np.cos(r2)*l2)

xxt = fig.add_subplot(321,xlim=(0,10),ylim=(-4,4))
ax = plt.gca()
ax.xaxis.grid(True)
ax.yaxis.grid(True)
plt.setp(xxt.get_xticklabels(), visible = True) 
line2, = xxt.plot([], [], 'b-')

vxt = fig.add_subplot(323,xlim=(0,10),ylim=(-16,16))
ax = plt.gca()
ax.xaxis.grid(True)
ax.yaxis.grid(True)
plt.setp(vxt.get_xticklabels(), visible = True) 
line3, = vxt.plot([], [], 'r-')


ext = fig.add_subplot(325,xlim=(0,10),ylim=(0,35))
ax = plt.gca()
ax.xaxis.grid(True)
ax.yaxis.grid(True)
plt.setp(ext.get_xticklabels(), visible = True) 
line4, = ext.plot([], [], 'g-')

pendulo = fig.add_subplot(122,xlim=(-max(l,l2)*2.,max(l,l2)*2.),ylim=(-max(l,l2)*2.,max(l,l2)*2.),aspect = 'equal')
grafico(r'Oscila\c{c}\~oes acopladas')

line5 = [] 
lob = pendulo.plot([], [], 'r-')[0]
line5.append(lob)
lob = pendulo.plot([], [], 'ko-',markersize=8)[0]
line5.append(lob)
lob = pendulo.plot([], [], 'b-')[0]
line5.append(lob)
lob = pendulo.plot([], [], 'ko-',markersize=8)[0]
line5.append(lob)
timeseg = pendulo.text(0.05, 0.9, '', transform=pendulo.transAxes)

#frame base
def init():
	line2.set_data([], [])
	line3.set_data([], [])
	line4.set_data([], [])
	
	for lined in line5:
		lined.set_data([], [])
	timeseg.set_text('')
	return line2,line3,line4, line5,timeseg

#funcao animacao
def animate(i):
	imin = 0 if  i < 10 else i-10
	
	pendx = xp[imin:i+1]
	pendy = yp[imin:i+1]
	massx = [-0.5 , xp[i],xp2[i]] #posiciona o eixo da animação no local correto (*) e adiciona a mola (fator de acoplamento)
	massy = [0. , yp[i],yp2[i]]
	
	pendx2 = xp2[imin:i+1]
	pendy2 = yp2[imin:i+1]
	massx2 = [0.5 , xp2[i]]#posiciona o eixo da animação no local correto (**) e adiciona a mola (fator de acoplamento)
	massy2 = [0. , yp2[i]]
	e = e1+e2
	x = r1+r2
	v = v1+v2
	
	line2.set_data(t[:i],x[:i])
	line3.set_data(t[:i],v[:i])
	line4.set_data(t[:i],e[:i])
	line5[0].set_data(pendx,pendy)
	line5[1].set_data(massx,massy)
	line5[2].set_data(pendx2,pendy2)
	line5[3].set_data(massx2,massy2)
	timeseg.set_text('time = %.1fs' % t[i])
	
	return line2,line3,line4, line5,timeseg

#cria animacao
anim = animation.FuncAnimation(fig,animate,init_func = init, frames=t.size,interval=1,blit=False,repeat = False)#o blit esta desligado

#salva e mostra(tem que ter ffmpeg instalado)
#anim.save('Oscilador_acoplado.mp4', fps =30 , extra_args = ['-vcodec','libx264'])
plt.show()
