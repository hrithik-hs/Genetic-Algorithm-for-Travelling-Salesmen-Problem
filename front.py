import pygame as pg
import random
import math

class Front:
	def __init__(self,back):
		pg.init()
		self.screen=pg.display.set_mode((1000,710))
		pg.display.set_caption("Travelling Salesmen Problem")
		self.back=back
		self.mode=1
		self.vertex_lst=[]
		self.max_cities=30
		self.myfont = pg.font.SysFont('Comic Sans MS', 30)
		self.update_utility()

	def draw_vertex(self,x,y,width,vertex_lst,range=100):
		for (xx,yy) in vertex_lst:
			#print (xx,yy)
			pg.draw.circle(self.screen,(255,0,0),(x+10+int(xx*width/range),y+10+int(yy*width/range)),5)

	def draw_solution(self,x,y,width,lst):
		best_solution=[]
		for (xx,yy) in lst:
			xx=x+10+int(xx*width/100)
			yy=y+10+int(yy*width/100)
			best_solution.append((xx,yy))
		pg.draw.polygon(self.screen,(0,255,240),best_solution,3)
	
	def update(self):
		for event in pg.event.get():
			if event.type ==pg.QUIT:
				return False
		# print("***** ",self.mode)
		if self.mode==1:
			left_m , middle_m, right_m = pg.mouse.get_pressed()
			if left_m:
				self.update_utility()
		elif self.mode==0:
			self.update_utility()
		elif self.mode==2:
			self.create_custom_graph()

		return True

	def update_utility(self):
		self.back.s.next_gen()
		self.screen.fill((255,255,255))
		
		pg.draw.rect(self.screen,(0,0,0),(5,2,730,700),3)
		pg.draw.line(self.screen,(0,0,0),(5,350),(735,350),3)
		pg.draw.line(self.screen,(0,0,0),(367,2),(367,702),3)
		pg.draw.rect(self.screen,(200,255,0),(280,335,190,30))
		
		slider=Button(self,"",745,70,240,10,(200,255,255),30,self.change_cities)
		slider.create_button()
		pg.draw.line(self.screen,(0,0,0),(745,74),(984,74),3)
		pg.draw.circle(self.screen,(0,0,255),(int(((self.back.no_of_vertex-1)*240)/self.max_cities)+745,74),10)
		textsurface5 = self.myfont.render('No of cities : '+str(self.back.no_of_vertex), False, (0, 0, 0))
		self.screen.blit(textsurface5,(745,20))

		textsurface = self.myfont.render('Generation : '+str(self.back.s.gen), False, (0, 0, 0))
		self.screen.blit(textsurface,(290,340))
		textsurface1 = self.myfont.render('Best Solution :'+str(round(self.back.s.population[0].fitness,2)), False, (0, 0, 0))
		self.screen.blit(textsurface1,(10,6))
		textsurface2 = self.myfont.render('Good Solution :'+str(round(self.back.s.population[250].fitness,2)), False, (0, 0, 0))
		self.screen.blit(textsurface2,(500,6))
		textsurface3 = self.myfont.render('Average Solution :'+str(round(self.back.s.population[500].fitness,2)), False, (0, 0, 0))
		self.screen.blit(textsurface3,(10,355))
		textsurface4 = self.myfont.render('Worst Solution :'+str(round(self.back.s.population[999].fitness,2)), False, (0, 0, 0))
		self.screen.blit(textsurface4,(500,355))

		custom_graph=Button(self,"CUSTOM",765,160,200,50,(0,200,200),30,self.custom_graph)
		custom_graph.create_button()

		auto=Button(self,"AUTO",765,250,200,50,(0,155,155),30,self.auto)
		auto.create_button()
		click=Button(self,"CLICK",765,330,200,50,(124,252,0),30,self.click)
		click.create_button()
		quit=Button(self,"QUIT",765,410,200,50,(218,28,28),30,self.quittsp)
		quit.create_button()

		solution=[]
		solution.append(self.back.get_solution(0))
		solution.append(self.back.get_solution(250))
		solution.append(self.back.get_solution(500))
		solution.append(self.back.get_solution(999))
		self.draw(20,20,300,solution[0])
		self.draw(370,20,300,solution[1])
		self.draw(20,380,300,solution[2])
		self.draw(370,380,300,solution[3])
		self.draw_vertex(20,20,300,self.back.vertex_lst)
		self.draw_vertex(370,20,300,self.back.vertex_lst)
		self.draw_vertex(20,380,300,self.back.vertex_lst)
		self.draw_vertex(370,380,300,self.back.vertex_lst)
		
		pg.display.update()

	def draw(self,x,y,width,solution):
		self.draw_solution(x,y,width,solution)
		


	def change_cities(self):
		mouse = pg.mouse.get_pos()
		n=int(((mouse[0]-745)*self.max_cities/240)+1)
		if n<2:
			n=2
		self.back.reset(n)
		self.update()

	def auto(self):
		self.mode=0

	def click(self):
		self.mode=1

	def quittsp(self):
		pg.quit()
		quit()

	def custom_graph(self):
		self.mode=2
		self.vertex_lst=[]
	
	def create_custom_graph(self):
		self.screen.fill((255,255,255))
		
		pg.draw.rect(self.screen,(0,0,0),(5,2,700,700),3)
		
		textsurface5 = self.myfont.render('No of cities : '+str(len(self.vertex_lst)), False, (0, 0, 0))
		self.screen.blit(textsurface5,(745,20))
		done=Button(self,"DONE",765,330,200,50,(0,155,155),30,self.done)
		done.create_button()
		quit=Button(self,"QUIT",765,410,200,50,(218,28,28),30,self.quittsp)
		quit.create_button()
		if(self.mode !=2 ):
			return

		mouse = pg.mouse.get_pos()
		click = pg.mouse.get_pressed()
		x=int(((mouse[0]-12)*100)/700)
		y=int(((mouse[1]-10)*100)/700)
		if(mouse[0]>5 and mouse[0]<700 and mouse[1]>2 and mouse[1]<700):
			if click[0]==1:
				if (len(self.vertex_lst)==0 ) or ((x,y)!=self.vertex_lst[len(self.vertex_lst)-1]):
					#print (mouse)
					if (len(self.vertex_lst)<self.max_cities):
						self.vertex_lst.append((x,y))
		if(self.mode==2):
			self.draw_vertex(5,2,700,self.vertex_lst)
		pg.display.update()

	def done(self):
		if len(self.vertex_lst)>1:
			
			self.back.custom_reset(len(self.vertex_lst),self.vertex_lst)
			self.mode=1
			self.update_utility()



class Button:
    def __init__(self,front,message,x,y,w,h,c,font_size,action=None):
        self.x=x
        self.y=y
        self.front=front
        self.width=w
        self.height=h
        self.message=message
        self.color=c
        self.action=action
        self.font_size=font_size
    def create_button(self):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        if (self.x+self.width>mouse[0]>self.x) and (self.y+self.height>mouse[1]>self.y):
            pg.draw.rect(self.front.screen,self.color,(self.x,self.y,self.width,self.height))
            if click[0]==1 and self.action!=None:
                self.action()
        else:
            pg.draw.rect(self.front.screen,self.color,(self.x,self.y,self.width,self.height))

        smallText = pg.font.SysFont('comicsansms',self.font_size)
        textSurf, textRect = self.text_objects(smallText)
        textRect.center = ((self.x+(self.width/2)),(self.y+(self.height/2)))
        self.front.screen.blit(textSurf, textRect)
    def text_objects(self,font):
        textSurface = font.render(self.message,True,(0,0,0))
        return textSurface, textSurface.get_rect()