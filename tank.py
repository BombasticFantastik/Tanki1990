import pygame
import random
objects=[]
bullets=[]
TILE=32
FPS=60
DIRECTS=[[0,-1],[1,0],[0,1],[-1,0]]
size=(1200,1000)
clock=pygame.time.Clock()
window=pygame.display.set_mode(size)

class Tank:
    def __init__(self,color,px,py,direct):
        objects.append(self)
        self.type='tank'
        self.color=color
        self.rect=pygame.Rect(px,py,TILE,TILE)
        self.direct=direct
        self.move_speed=3

        self.shotTimer=0
        self.shotDelay=30


        self.bullet_speed=5
        self.bullet_damage=1

        
    def update(self):
        if keys[pygame.K_a]:
            self.rect.x-=self.move_speed
            self.direct=3
        elif keys[pygame.K_d]:
            self.rect.x+=self.move_speed
            self.direct=1
        elif keys[pygame.K_w]:
            self.rect.y-=self.move_speed
            self.direct=0
        elif keys[pygame.K_s]:
            self.rect.y+=self.move_speed
            self.direct=2     
        if keys[pygame.K_e] and self.shotTimer==0:
            dx=DIRECTS[self.direct][0]*30
            dy=DIRECTS[self.direct][1]*30
            Bullet(self,self.rect.centerx,self.rect.centery,dx,dy,self.bullet_damage)
            self.shotTimer=self.shotDelay
        if self.shotTimer>0:
            self.shotTimer-=1

    def draw(self):
        pygame.draw.rect(window,self.color,self.rect)
        x=self.rect.centerx+DIRECTS[self.direct][0]*30
        y=self.rect.centery+DIRECTS[self.direct][1]*30
        pygame.draw.line(window,'white',self.rect.center,(x,y),4)




class EnemyTank:
    def __init__(self,color,px,py,direct):
        objects.append(self)
        self.type='tank'
        self.color=color
        self.rect=pygame.Rect(px,py,TILE,TILE)
        self.direct=direct
        self.new_direct=direct
        self.move_speed=3

        self.shotTimer=0
        self.shotDelay=60


        self.bullet_speed=5
        self.bullet_damage=1

        self.heroPositionx,self.heroPositiony=objects[0].rect.centerx,objects[0].rect.centery

        self.rndPosition=True
        self.rndTimer=60
        self.rndDelay=30

        
        
    def update(self):
        
        #1-right
        #3-left
        #0-up
        #2-down
        if self.rndPosition:
            if self.rndTimer==0 :
                self.new_direct=random.randint(0,3)
                self.rndTimer+=self.rndDelay 
            if self.new_direct==3 and self.rect.centerx>20:
                self.rect.x-=self.move_speed
                self.direct=3
            if self.new_direct==1 and self.rect.centerx<size[0]-20:
                self.rect.x+=self.move_speed
                self.direct=1
            if self.new_direct==0 and self.rect.centery>20:
                self.rect.y-=self.move_speed
                self.direct=0
            if self.new_direct==2 and self.rect.centery<size[1]-20:
                self.rect.y+=self.move_speed
                self.direct=2 
            self.rndTimer-=1

        if random.randint(0,1) and self.shotTimer==0:
            dx=DIRECTS[self.direct][0]*30
            dy=DIRECTS[self.direct][1]*30
            Bullet(self,self.rect.centerx,self.rect.centery,dx,dy,self.bullet_damage)
            self.shotTimer=self.shotDelay
        if self.shotTimer>0:
            self.shotTimer-=1
        #else:

        #self.heroPositionx,self.heroPositiony=objects[0].rect.centerx,objects[0].rect.centery

    def draw(self):
        pygame.draw.rect(window,self.color,self.rect)
        x=self.rect.centerx+DIRECTS[self.direct][0]*30
        y=self.rect.centery+DIRECTS[self.direct][1]*30
        pygame.draw.line(window,'white',self.rect.center,(x,y),4)


class Bullet:
    def __init__(self,parent,px,py,dx,dy,damage):
        bullets.append(self)
        self.parent=parent
        self.px,self.py=px,py
        self.dx,self.dy=dx,dy
        self.damage=damage
    def update(self):
        self.px+=self.dx
        self.py+=self.dy

        if self.px==0 or self.py==0 or self.px>size[0] or self.py>size[1]:
            bullets.remove(self)
    def draw(self):
        pygame.draw.circle(window,'yellow',(self.px,self.py),2)

Tank('blue',100,275,0)
EnemyTank('Red',650,275,0)

play=True
while play:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            play=False

    keys=pygame.key.get_pressed()
    for obj in objects:
        obj.update()
    for bullet in bullets:
        bullet.update()
    window.fill('black')
    for obj in objects:
        obj.draw()
    for bullet in bullets:
        bullet.draw()

    pygame.display.update()
    clock.tick(FPS)