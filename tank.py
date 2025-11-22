import pygame
import random
import os

pygame.init()
all_enemys=20
objects=[]
bullets=[]
spawners=[]
TILE=32#??????????????????
FPS=60
DIRECTS=[[0,-1],[1,0],[0,1],[-1,0]]

WIDTH=1200
HEIGHT=1000
size=(WIDTH,HEIGHT)
clock=pygame.time.Clock()
window=pygame.display.set_mode(size)

#ПОБЕДА



#запуск музыки
mix=pygame.mixer.init()
pygame.mixer.music.load('Music/sna.mp3')
pygame.mixer.music.play()

#звук выстрела
shoot_sound = pygame.mixer.Sound('Music/выстрел.wav')
shoot_enemy_sound = pygame.mixer.Sound('Music/выстрел_противника.wav')

fontUI=pygame.font.Font(None,30)


imgBrick=pygame.image.load('Images/кирпич.png')
imgHero=pygame.image.load('Images/герой.png')
imgEnemy=pygame.image.load('Images/враг.png')
imgExplodes=[
    pygame.image.load('Images/взрывы/взрыв0.png'),
    pygame.image.load('Images/взрывы/взрыв1.png'),
    pygame.image.load('Images/взрывы/взрыв2.png'),
    pygame.image.load('Images/взрывы/взрыв3.png'),
    pygame.image.load('Images/взрывы/взрыв4.png'),
]

#победа
imgWins=[os.path.join('Images/победа',img) for img in os.listdir('Images/победа')]
imgWins.sort()
win=False

#поражение
imgLose=[os.path.join('Images/поражение',img) for img in os.listdir('Images/поражение')]
imgTextLose=[os.path.join('Images/поражение_текст',img) for img in os.listdir('Images/поражение_текст')]
imgLose.sort()
imgTextLose.sort()
lose=False

#спавнер
imgSpawn=pygame.image.load('Images/спавнер0.png')

#rct=pygame.Rect(100,275,(0,0))

#window.u




# class Explode:
#     def __init__(self,px,py):
#         objects.append(self)
#         self.type='explode'
#         self.px,self.py=px,py
#         self.frame=0
#     def update(self):
#         self.frame+=0.2
#         if self.frame>4:
#             objects.remove(self)
#     def draw(self):
#         image=imgExplodes[int(self.frame)] 
#         image=pygame.transform.scale(image,(image.get_width()+30,image.get_height()+30)) 
#         rect=image.get_rect(center=(self.px,self.py))
#         window.blit(image,rect)

class UI:
    def __init__(self,hero_tank):
        self.hero_tank=hero_tank
        self.win_frame=0
        self.lose_frame=0
        self.lose_text_frame=0
    def update(self):
        self.win_frame+=1
        if self.win_frame>53:
            self.win_frame=0
        self.lose_frame+=1
        if self.lose_frame>38:
            self.lose_frame=0
        self.lose_text_frame+=1
        if self.lose_text_frame>4:
            self.lose_text_frame=0
    def draw(self):
        #мой танк
        pygame.draw.rect(window,hero_tank.color,(5,5,22,22))
        text=fontUI.render(str(hero_tank.hp),1,hero_tank.color)
        rect=text.get_rect(center=(5+32,5+11))
        window.blit(text,rect)

        #противники
        #enemy=[obj for obj in objects if obj!=self.hero_tank and obj.type=='enemy_tank']
        pygame.draw.rect(window,'Red',(80,5,22,22))
        text=fontUI.render(str(all_enemys),1,'Red')
        rect=text.get_rect(center=(80+32,5+11))
        window.blit(text,rect)

        if win:
            for i in range(53):
                if i<10:
                    idx='0'+str(i)
                else:
                    idx=str(i)
                window.blit(pygame.image.load(imgWins[int(self.win_frame)]),((WIDTH//3),HEIGHT//3))
                #global objects
        if lose:
            for i in range(38):
                if i<10:
                    idx='0'+str(i)
                else:
                    idx=str(i)
                window.blit(pygame.image.load(imgLose[int(self.lose_frame)]),((WIDTH//3)+64,(HEIGHT//3)+64))
                window.blit(pygame.image.load(imgTextLose[int(self.lose_text_frame)]),((WIDTH//3)-64,(HEIGHT//3)-32))
                #global objects
                


class Tank:
    def __init__(self,color,px,py,direct):
        objects.append(self)
        self.type='hero_tank'
        self.color=color
        self.rect=pygame.Rect(px,py,TILE,TILE)
        self.direct=direct
        self.move_speed=3

        self.hp=3
        #self.hp=0

        self.shotTimer=0
        self.shotDelay=30


        self.bullet_speed=5
        self.bullet_damage=1

        self.image=pygame.transform.rotate(imgHero,-self.direct*90 - 270)
        self.rect=self.image.get_rect(center=self.rect.center)

        
    def update(self):

        self.image=pygame.transform.rotate(imgHero,-self.direct*90 - 270)
        self.image=pygame.transform.scale(self.image,(self.image.get_width()-5,self.image.get_height()-5))
        self.rect=self.image.get_rect(center=self.rect.center)

        oldX,oldY=self.rect.topleft

        #управление танком
        if keys[pygame.K_a] and self.rect.centerx>20:
            self.rect.x-=self.move_speed
            self.direct=3
        elif keys[pygame.K_d] and self.rect.centerx<size[0]-20:
            self.rect.x+=self.move_speed
            self.direct=1
        elif keys[pygame.K_w] and self.rect.centery>20:
            self.rect.y-=self.move_speed
            self.direct=0
        elif keys[pygame.K_s] and self.rect.centery<size[1]-20:
            self.rect.y+=self.move_speed
            self.direct=2    

        for obj in objects:
            if obj!=self and (obj.type=='block' or obj.type=='enemy_tank') and self.rect.colliderect(obj.rect):
                self.rect.topleft=oldX,oldY 







        if keys[pygame.K_e] and self.shotTimer==0:
            dx=DIRECTS[self.direct][0]*30
            dy=DIRECTS[self.direct][1]*30
            Bullet(self,self.rect.centerx,self.rect.centery,dx,dy,self.bullet_damage)
            self.shotTimer=self.shotDelay
            shoot_sound.play()


        if self.shotTimer>0:
            self.shotTimer-=1



    def draw(self):
        
        # pygame.draw.rect(window,self.color,self.rect)
        # x=self.rect.centerx+DIRECTS[self.direct][0]*30
        # y=self.rect.centery+DIRECTS[self.direct][1]*30
        # pygame.draw.line(window,'white',self.rect.center,(x,y),4)

        window.blit(self.image,self.rect)

    def damage(self,value):
        self.hp-=value
        if self.hp<=0:
            objects.remove(self)





class EnemyTank:
    def __init__(self,color,px,py,direct):
        objects.append(self)
        self.type='enemy_tank'
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

        self.image=pygame.transform.rotate(imgEnemy,-self.direct*90 - 90)
        self.rect=self.image.get_rect(center=self.rect.center)

        
        
    def update(self):
        
        #1-right
        #3-left
        #0-up
        #2-down

        self.image=pygame.transform.rotate(imgEnemy,-self.direct*90-90)
        self.image=pygame.transform.scale(self.image,(self.image.get_width()-5,self.image.get_height()-5))
        self.rect=self.image.get_rect(center=self.rect.center)

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
                if obj!=self and (obj.type=='block' or obj.type=='enemy_tank' or obj.type=='hero_tank') and self.rect.colliderect(obj.rect):
                    self.rect.topleft=oldX,oldY 

            self.rndTimer-=1

        if random.randint(0,1) and self.shotTimer==0:
            dx=DIRECTS[self.direct][0]*30
            dy=DIRECTS[self.direct][1]*30
            Bullet(self,self.rect.centerx,self.rect.centery,dx,dy,self.bullet_damage)
            self.shotTimer=self.shotDelay
            shoot_enemy_sound.play()
        if self.shotTimer>0:
            self.shotTimer-=1
        #else:

        #self.heroPositionx,self.heroPositiony=objects[0].rect.centerx,objects[0].rect.centery

    def draw(self):
        # pygame.draw.rect(window,self.color,self.rect)
        # x=self.rect.centerx+DIRECTS[self.direct][0]*30
        # y=self.rect.centery+DIRECTS[self.direct][1]*30
        # pygame.draw.line(window,'white',self.rect.center,(x,y),4)

        window.blit(self.image,self.rect)

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
                if obj!=self.parent and obj.type!='explode' and obj.rect.collidepoint(self.px,self.py) and obj.type!=self.parent.type:
                    obj.damage(self.damage)
                    bullets.remove(self)
                    Explode(self.px,self.py)
                    break

    def draw(self):
        pygame.draw.circle(window,'yellow',(self.px,self.py),2)


class Explode:
    def __init__(self,px,py):
        objects.append(self)
        self.type='explode'
        self.px,self.py=px,py
        self.frame=0
    def update(self):
        self.frame+=0.2
        if self.frame>4:
            objects.remove(self)
    def draw(self):
        image=imgExplodes[int(self.frame)] 
        image=pygame.transform.scale(image,(image.get_width()+30,image.get_height()+30)) 
        rect=image.get_rect(center=(self.px,self.py))
        window.blit(image,rect)

class Block:
    def __init__(self,px,py,size):
        objects.append(self)
        self.type='block'
        self.rect=pygame.Rect(px,py,size,size)
        self.hp=2
    def update(self):
        pass
    def draw(self):
        #создание изображения
        window.blit(imgBrick,self.rect)
        # pygame.draw.rect(window,'green',self.rect)
        # pygame.draw.rect(window,'gray20',self.rect,2)

    def damage(self,value):
        self.hp-=value
        if self.hp<=0:
            objects.remove(self)

class EnemySpawner:
    def __init__(self,px,py,max_count):
        spawners.append(self)
        self.px=px
        self.py=py
        self.max_count=max_count
        self.tanks=[]

        self.spawnTimer=300
        self.spawnDelay=500

    def update(self):
        global all_enemys
        if self.spawnTimer==0 and len(self.tanks)<self.max_count and all_enemys>0:
            
            rect=pygame.Rect(self.px,self.py,64,64)
            fined=False
            for obj in objects:
                if obj.type!='explode' and rect.colliderect(obj.rect):
                    fined=True

            if not(fined):
                self.tanks.append(EnemyTank('Red',self.px,self.py,0))
                self.spawnTimer=self.spawnDelay 
                all_enemys-=1

        all_tanks=[tk for tk in objects if tk.type=='enemy_tank']


        global lose
        global win
        #условие победы
        if all_enemys==0 and len(all_tanks)==0 and not(lose):
            win=True
            if hero_tank in objects:
                objects.remove(hero_tank)

        #условие поражения
        if hero_tank.hp==0:
            
            lose=True
            #print(lose)
            for obj in objects:
                if obj.type=='enemy_tank':
                    objects.remove(obj)



        for tank in self.tanks:
            if tank not in objects:
                self.tanks.remove(tank)       
        if self.spawnTimer>0:
            self.spawnTimer-=1

        
    def draw(self):
        window.blit(imgSpawn,(self.px,self.py))

hero_tank=Tank('blue',100,275,0)
ui=UI(hero_tank)

#Создание стен
for _ in range(300):
    while True:
        x= random.randint(0,WIDTH//TILE-1)*64
        y= random.randint(0,HEIGHT//TILE-1) *64
        rect=pygame.Rect(x,y,64,64)
        fined=False
        for obj in objects:
            if rect.colliderect(obj.rect):
                fined=True
        if not fined:
            break
    Block(x,y,64)


#спавны
for _ in range(5):
    while True:
        x= random.randint(0,(WIDTH-128)//70)*70
        y= random.randint(0,(HEIGHT-128)//70) *70
        rect=pygame.Rect(x,y,80,80)
        fined=False
        for obj in objects:
            if rect.colliderect(obj.rect):
                fined=True
        if not fined:
            break
    EnemySpawner(x,y,max_count=3)

# spawn1=EnemySpawner(512,0,max_count=3)
# swawn2=EnemySpawner(1000,0,max_count=3)

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
    for spawn in spawners:
        spawn.update()
    window.fill('black')
    
    for spawn in spawners:
        spawn.draw()
    for obj in objects:
        obj.draw()
    for bullet in bullets:
        bullet.draw()

    ui.draw()

    pygame.display.update()
    clock.tick(FPS)