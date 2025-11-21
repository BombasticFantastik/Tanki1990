import pygame
import random

pygame.init()
objects=[]
bullets=[]
TILE=32#??????????????????
FPS=60
DIRECTS=[[0,-1],[1,0],[0,1],[-1,0]]

WIDTH=1200
HEIGHT=1000
size=(WIDTH,HEIGHT)
clock=pygame.time.Clock()
window=pygame.display.set_mode(size)

fontUI=pygame.font.Font(None,30)


imgBrick=pygame.image.load('Images/кирпич.png')
imgHero=pygame.image.load('Images/герой.png')
imgEnemy=pygame.image.load('Images/враг.png')



class UI:
    def __init__(self,hero_tank):
        self.hero_tank=hero_tank
    def update(self):
        pass
    def draw(self):
        #мой танк
        pygame.draw.rect(window,hero_tank.color,(5,5,22,22))
        text=fontUI.render(str(hero_tank.hp),1,hero_tank.color)
        rect=text.get_rect(center=(5+32,5+11))
        window.blit(text,rect)

        #противники
        enemy=[obj for obj in objects if obj!=self.hero_tank and obj.type=='tank']
        pygame.draw.rect(window,'Red',(80,5,22,22))
        text=fontUI.render(str(len(enemy)),1,'Red')
        rect=text.get_rect(center=(80+32,5+11))
        window.blit(text,rect)

class Tank:
    def __init__(self,color,px,py,direct):
        objects.append(self)
        self.type='tank'
        self.color=color
        self.rect=pygame.Rect(px,py,TILE,TILE)
        self.direct=direct
        self.move_speed=3

        self.hp=3

        self.shotTimer=0
        self.shotDelay=30


        self.bullet_speed=5
        self.bullet_damage=1

        self.image=pygame.transform.rotate(imgHero,-self.direct*90 - 270)
        self.rect=self.image.get_rect(center=self.rect.center)

        
    def update(self):

        self.image=pygame.transform.rotate(imgHero,-self.direct*90 - 270)
        self.rect=self.image.get_rect(center=self.rect.center)

        oldX,oldY=self.rect.topleft

        #управление танком
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

        for obj in objects:
            if obj!=self and self.rect.colliderect(obj.rect):
                self.rect.topleft=oldX,oldY 








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

        window.blit(self.image,self.rect)

    def damage(self,value):
        self.hp-=value
        if self.hp<=0:
            objects.remove(self)





class EnemyTank:
    def __init__(self,color,px,py,direct):
        objects.append(self)
        self.type='tank'
        self.color=color
        self.rect=pygame.Rect(px,py,TILE,TILE)
        self.direct=direct
        self.new_direct=direct
        self.move_speed=3
        self.hp=1

        

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
            oldX,oldY=self.rect.topleft

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
            for obj in objects:
                if obj!=self and self.rect.colliderect(obj.rect):
                    self.rect.topleft=oldX,oldY 

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

    def damage(self,value):
        self.hp-=value
        if self.hp<=0:
            objects.remove(self)


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
        else:
            for obj in objects:
                if obj!=self.parent and obj.rect.collidepoint(self.px,self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break

    def draw(self):
        pygame.draw.circle(window,'yellow',(self.px,self.py),2)


class Block:
    def __init__(self,px,py,size):
        objects.append(self)
        self.type='block'
        self.rect=pygame.Rect(px,py,size,size)
        self.hp=1
    def update(self):
        pass
    def draw(self):
        #создание изображения
        #window.blit(imgBrick,self.rect)
        pygame.draw.rect(window,'green',self.rect)
        pygame.draw.rect(window,'gray20',self.rect,2)

    def damage(self,value):
        self.hp-=value
        if self.hp<=0:
            objects.remove(self)

hero_tank=Tank('blue',100,275,0)
EnemyTank('Red',650,275,0)
ui=UI(hero_tank)

#Создание стен
for _ in range(200):
    while True:
        x= random.randint(0,WIDTH//TILE-1) * TILE
        y= random.randint(0,HEIGHT//TILE-1) * TILE
        rect=pygame.Rect(x,y,TILE,TILE)
        fined=False
        for obj in objects:
            if not(rect.colliderect(obj.rect)):
                fined=  True
        if fined:
            break
    Block(x,y,TILE)



play=True
while play:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            play=False

    keys=pygame.key.get_pressed()
    for obj in objects:
        obj.update()
    ui.update()
    for bullet in bullets:
        bullet.update()
    window.fill('black')
    for obj in objects:
        obj.draw()
    for bullet in bullets:
        bullet.draw()
    ui.draw()

    pygame.display.update()
    clock.tick(FPS)