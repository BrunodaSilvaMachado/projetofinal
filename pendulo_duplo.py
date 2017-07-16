#_*_ coding: utf-8 _*_
#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

#constant
dt = 0.03
g = 9.81 
#end

class PenduloDuplo(object):
	def __init__(self,m1,m2,l1,l2,theta1,theta2,v1,v2):
		self.m1 = m1
		self.m2 = m2
		self.l1 = l1 
		self.l2 = l2 
		self.x1 = theta1
		self.x2 = theta2
		self.v1 = v1
		self.v2 = v2
		
	def a2(self,x1,x2,v1,v2):
		return (2*np.sin(x1-x2)*((v1**2)*self.l1*(self.m1+self.m2)+g*(self.m1+self.m2)*np.cos(x1)+(v2**2)*self.l2*self.m2*np.cos(x1-x2)))/(self.l2*(2*self.m1+self.m2-self.m2*np.cos(2*x1-2*x2))) 
	
	def a1(self,x1,x2,v1,v2):
		return (-g*(2*self.m1+self.m2)*np.sin(x1)-self.m2*g*np.sin(x1-2*x2)-2*np.sin(x1-x2)*self.m2*((v2**2)*self.l2-(v1**2)*self.l1*np.cos(x1-x2)))/(self.l1*(2*self.m1+self.m2-self.m2*np.cos(2*x1-2*x2)))
				
	def move(self):
	
		at1 = self.a1(self.x1,self.x2,self.v1,self.v2)
		at2 = self.a2(self.x1,self.x2,self.v1,self.v2)
			
		self.x1 += self.v1*dt + at1*dt*dt/2.
		self.x2 += self.v2*dt + at2*dt*dt/2.
		
		a_tmp1 = self.a1(self.x1,self.x2,self.v1,self.v2)
		a_tmp2 = self.a2(self.x1,self.x2,self.v1,self.v2)
		
		v_tmp1 = self.v1+(at1+a_tmp1)*dt/2. 
		v_tmp2 = self.v2+(at2+a_tmp2)*dt/2.
		
		a_tmp1 = self.a1(self.x1,self.x2,v_tmp1,v_tmp2)
		a_tmp2 = self.a2(self.x1,self.x2,v_tmp1,v_tmp2)
		
		self.v1 += (a_tmp1+at1)*dt/2.
		self.v2 += (a_tmp2+at2)*dt/2.
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

'''pendulo dublo com massa iguais e coprimentos iguais'''
p1 = PenduloDuplo(1,1,0.5,0.5,-np.pi/4,np.pi/4,0,0)

tmax=20
t=np.arange(0,tmax,dt)
x1=np.zeros(t.size)
x2=np.zeros(t.size)
v1=np.zeros(t.size)
v2=np.zeros(t.size)
x1[0],x2[0],v1[0],v2[0]=p1.x1,p1.x2,p1.v1,p1.v2

for i in range(t.size):
	p1.move()
	x1[i],x2[i],v1[i],v2[i]=p1.x1,p1.x2,p1.v1,p1.v2

fig = plt.figure(figsize=(7,6),facecolor='white')

l1=p1.l1
l2=p1.l2

xp=np.sin(x1+x2)*(l1+l2)
yp=-np.cos(x1-x2)*(l1+l2)

vxp= np.cos(x1)*l1
vyp= np.sin(x1)*l1

xp2= np.sin(x2)*l2
yp2=-np.cos(x2)*(l2)

vxp2=(np.cos(x2)*l2)
vyp2=(np.sin(x2)*l2)

pendulo = plt.axes(xlim=(-2,2),ylim=(-2,2),aspect = 'equal')
grafico(r'Pendulo Duplo')

line5 = [] 
lob = pendulo.plot([], [], 'r-')[0]
line5.append(lob)
lob = pendulo.plot([], [], 'ko-',markersize=8)[0]
line5.append(lob)
lob = pendulo.plot([], [], 'b-')[0]
line5.append(lob)
lob = pendulo.plot([], [], 'ko-',markersize=8)[0]
line5.append(lob)

def init():
	for lined in line5:
		lined.set_data([], [])	
	return line5

#funcao animacao
def animate(i):
	imin = 0 if  i < 10 else i-10
	
	pendx = xp[imin:i+1]
	pendy = yp[imin:i+1]
	massx = [0 ,xp2[i],xp[i]] #posiciona o eixo da animação no local correto (*) e adiciona a mola (fator de acoplamento)
	massy = [0,yp2[i],yp[i]]
	
	pendx2 = xp2[imin:i+1]
	pendy2 = yp2[imin:i+1]
	massx2 = [xp[i] , xp2[i]]#posiciona o eixo da animação no local correto (**) e adiciona a mola (fator de acoplamento)
	massy2 = [yp[i] , yp2[i]]
	
	line5[0].set_data(pendx,pendy)
	line5[1].set_data(massx,massy)
	line5[2].set_data(pendx2,pendy2)
	line5[3].set_data(massx2,massy2)
	
	return line5

#cria animacao
anim = animation.FuncAnimation(fig,animate,init_func = init, frames=t.size,interval=1,blit=True,repeat = False)#'''

plt.show()