#_*_ coding: utf-8 _*_
#!/usr/bin/env python

import pygame
import sys
import numpy as np
import math
from pygame.locals import*

#constant
dt = 0.03
g = 9.81 

SCREENSIZE = 600
BLUE = 0,0,255
WHITE = 255,255,255
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

#begin

pygame.init()
screen = pygame.display.set_mode((SCREENSIZE,SCREENSIZE))
pygame.display.set_caption("Pendulo duplo")

'''pendulo dublo com massa iguais e coprimentos iguais'''
p1 = PenduloDuplo(1,1,0.5,0.5,-np.pi/4,np.pi/4,0,0)

clock = pygame.time.Clock()
bloco1 = pygame.image.load("pf/bloco.png").convert_alpha()
bloco1 = pygame.transform.scale(bloco1,(40,40))
bloco2 = pygame.image.load("pf/bloco2.png").convert_alpha()
bloco2 = pygame.transform.scale(bloco2,(40,40))
alfinete = pygame.image.load("pf/tack_orange.png").convert_alpha()
space = pygame.image.load("pf/2.jpg").convert()
myfont1 = pygame.font.Font(None,24)

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

interator = 0

while True:
		for event in pygame.event.get():
			if event.type in (QUIT,KEYDOWN):
				sys.exit()
		
		#screen.fill(WHITE)
		
		screen.blit(space,(0,0))
		
		#rect primeiro pendulo
		rect = pygame.Rect(160*xp2[interator]+SCREENSIZE/2.,-160*yp2[interator]+SCREENSIZE/4.,20,20)
		
		#rect segundo pendulo
		
		rect2 = pygame.Rect(160*xp[interator]+SCREENSIZE/2.,-160*yp[interator]+SCREENSIZE/2.,20,20)
		
		#linha primeiro pendulo
		pygame.draw.aaline(screen,(0,0,0),(SCREENSIZE/2+15.,28),rect.center)
		
		#linha segundo pendulo
		pygame.draw.aaline(screen,(0,0,0),(160*xp2[interator]+SCREENSIZE/2.+20,-160*yp2[interator]+SCREENSIZE/4.+20),rect2.center)
		
		#pendulo 1
		screen.blit(bloco1,(160*xp2[interator]+SCREENSIZE/2.,-160*yp2[interator]+SCREENSIZE/4.))
		#pendulo 2
		screen.blit(bloco2,(160*xp[interator]+SCREENSIZE/2.,-160*yp[interator]+SCREENSIZE/2.))
		#alfinete
		screen.blit(alfinete,(SCREENSIZE/2.,0.))
		
		if(interator < t.size-1):
			interator = interator + 1
		else:
			textImage1 = myfont1.render(r"Fim da simulação",True,BLUE)
			screen.blit(textImage1,(SCREENSIZE/2,SCREENSIZE/2))
			
		pygame.display.update()
		tempo = clock.tick(30)

