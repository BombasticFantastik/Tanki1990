import pygame
import random
import os
from utils import gif_player
from config import WIDTH,HEIGHT,TILE,DIRECTS,all_enemys,win,lose

class UI:
    def __init__(self,hero_tank,window,imgLose,imgWins,imgTextLose):
        self.hero_tank=hero_tank
        self.win_frame=0
        self.lose_frame=0
        self.lose_text_frame=0
        self.window=window
        self.hero_tank=hero_tank
        self.imgLose=imgLose
        self.imgWins=imgWins
        self.imgTextLose=imgTextLose
        #шрифт
        self.fontUI=pygame.font.Font(None,30)
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
        pygame.draw.rect(self.window,self.hero_tank.color,(5,5,22,22))
        text=self.fontUI.render(str(self.hero_tank.hp),1,self.hero_tank.color)
        rect=text.get_rect(center=(5+32,5+11))
        self.window.blit(text,rect)

        #противники
        pygame.draw.rect(self.window,'Red',(80,5,22,22))
        text=self.fontUI.render(str(all_enemys),1,'Red')
        rect=text.get_rect(center=(80+32,5+11))
        self.window.blit(text,rect)

        if win:
            gif_player(self.window,self.imgWins,WIDTH,53,self.win_frame)
        if lose:
            gif_player(self.window,self.imgLose,WIDTH,38,self.win_frame)
            gif_player(self.window,self.imgTextLose,WIDTH,4,self.win_frame)

                # self.window.blit(pygame.image.load(self.imgLose[int(self.lose_frame)]),((WIDTH//3)+64,(HEIGHT//3)+64))
                # self.window.blit(pygame.image.load(self.imgTextLose[int(self.lose_text_frame)]),((WIDTH//3)-64,(HEIGHT//3)-32))
                # #global objects
                


class Tank:
    def __init__(self,color,px,py,direct,objects,imgHero,window):
        self.window=window
        self.objects=objects
        objects.append(self)
        self.type='hero_tank'
        self.color=color
        self.rect=pygame.Rect(px,py,TILE,TILE)
        self.direct=direct
        self.move_speed=3
        self.shoot_enemy_sound = pygame.mixer.Sound('Music/выстрел_противника.wav')

        self.hp=3
        self.shotTimer=0
        self.shotDelay=30


        self.bullet_speed=5
        self.bullet_damage=1
        self.imgHero=imgHero

        self.image=pygame.transform.rotate(self.imgHero,-self.direct*90 - 270)
        self.rect=self.image.get_rect(center=self.rect.center)

        
    def update(self):

        self.image=pygame.transform.rotate(self.imgHero,-self.direct*90 - 270)
        self.image=pygame.transform.scale(self.image,(self.image.get_width()-5,self.image.get_height()-5))
        self.rect=self.image.get_rect(center=self.rect.center)

        oldX,oldY=self.rect.topleft

        #управление танком
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.centerx>20:
            self.rect.x-=self.move_speed
            self.direct=3
        elif keys[pygame.K_d] and self.rect.centerx<WIDTH-20:
            self.rect.x+=self.move_speed
            self.direct=1
        elif keys[pygame.K_w] and self.rect.centery>20:
            self.rect.y-=self.move_speed
            self.direct=0
        elif keys[pygame.K_s] and self.rect.centery<HEIGHT-20:
            self.rect.y+=self.move_speed
            self.direct=2    

        for obj in self.objects:
            if obj!=self and (obj.type=='block' or obj.type=='enemy_tank') and self.rect.colliderect(obj.rect):
                self.rect.topleft=oldX,oldY 

        if keys[pygame.K_e] and self.shotTimer==0:
            dx=DIRECTS[self.direct][0]*30
            dy=DIRECTS[self.direct][1]*30
            Bullet(self,self.rect.centerx,self.rect.centery,dx,dy,self.bullet_damage)
            self.shotTimer=self.shotDelay
            self.shoot_sound.play()


        if self.shotTimer>0:
            self.shotTimer-=1



    def draw(self):
        self.window.blit(self.image,self.rect)

    def damage(self,value):
        self.hp-=value
        if self.hp<=0:
            self.objects.remove(self)





class EnemyTank:
    def __init__(self,color,px,py,direct,objects,window):
        objects.append(self)
        self.window=window
        self.objects=objects
        self.type='enemy_tank'
        self.color=color
        self.rect=pygame.Rect(px,py,TILE,TILE)
        self.direct=direct
        self.new_direct=direct
        self.move_speed=3
        self.hp=1
        self.imgEnemy=pygame.image.load('Images/враг.png')
        self.shoot_enemy_sound=pygame.mixer.Sound('Music/выстрел_противника.wav')
        
        

        self.shotTimer=0
        self.shotDelay=60


        self.bullet_speed=5
        self.bullet_damage=1

        self.heroPositionx,self.heroPositiony=objects[0].rect.centerx,objects[0].rect.centery

        self.rndPosition=True
        self.rndTimer=60
        self.rndDelay=30
        

        self.image=pygame.transform.rotate(self.imgEnemy,-self.direct*90 - 90)
        self.rect=self.image.get_rect(center=self.rect.center)

        
        
    def update(self):
        
        #1-right
        #3-left
        #0-up
        #2-down

        self.image=pygame.transform.rotate(self.imgEnemy,-self.direct*90-90)
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
            if self.new_direct==1 and self.rect.centerx<WIDTH-20:
                self.rect.x+=self.move_speed
                self.direct=1
            if self.new_direct==0 and self.rect.centery>20:
                self.rect.y-=self.move_speed
                self.direct=0
            if self.new_direct==2 and self.rect.centery<WIDTH-20:
                self.rect.y+=self.move_speed
                self.direct=2 
            for obj in self.objects:
                if obj!=self and (obj.type=='block' or obj.type=='enemy_tank' or obj.type=='hero_tank') and self.rect.colliderect(obj.rect):
                    self.rect.topleft=oldX,oldY 

            self.rndTimer-=1

        if random.randint(0,1) and self.shotTimer==0:
            dx=DIRECTS[self.direct][0]*30
            dy=DIRECTS[self.direct][1]*30
            Bullet(self,self.rect.centerx,self.rect.centery,dx,dy,self.bullet_damage)
            self.shotTimer=self.shotDelay
            self.shoot_enemy_sound.play()
        if self.shotTimer>0:
            self.shotTimer-=1

    def draw(self):

        self.window.blit(self.image,self.rect)

    def damage(self,value):
        self.hp-=value
        if self.hp<=0:
            self.objects.remove(self)


class Bullet:
    def __init__(self,parent,px,py,dx,dy,damage,bullets,objects):
        bullets.append(self)
        self.bullets=bullets
        self.parent=parent
        self.px,self.py=px,py
        self.dx,self.dy=dx,dy
        self.damage=damage
        self.objects=objects
    def update(self):
        self.px+=self.dx
        self.py+=self.dy

        if self.px==0 or self.py==0 or self.px>WIDTH or self.py>HEIGHT:
            self.bullets.remove(self)
        else:
            for obj in self.objects:
                if obj!=self.parent and obj.type!='explode' and obj.rect.collidepoint(self.px,self.py) and obj.type!=self.parent.type:
                    obj.damage(self.damage)
                    self.bullets.remove(self)
                    Explode(self.px,self.py)
                    break

    def draw(self):
        pygame.draw.circle(window,'yellow',(self.px,self.py),2)


class Explode:
    def __init__(self,px,py,objects,window):
        self.window=window
        objects.append(self)
        self.objects=objects
        self.type='explode'
        self.px,self.py=px,py
        self.frame=0
        self.imgExplodes=[
    pygame.image.load('Images/взрывы/взрыв0.png'),
    pygame.image.load('Images/взрывы/взрыв1.png'),
    pygame.image.load('Images/взрывы/взрыв2.png'),
    pygame.image.load('Images/взрывы/взрыв3.png'),
    pygame.image.load('Images/взрывы/взрыв4.png'),
]
    def update(self):
        self.frame+=0.2
        if self.frame>4:
            self.objects.remove(self)
    def draw(self):
        image=self.imgExplodes[int(self.frame)] 
        image=pygame.transform.scale(image,(image.get_width()+30,image.get_height()+30)) 
        rect=image.get_rect(center=(self.px,self.py))
        self.window.blit(image,rect)

class Block:
    def __init__(self,px,py,size,objects,window):
        objects.append(self)
        self.objects=objects
        self.window=window
        self.type='block'
        self.rect=pygame.Rect(px,py,size,size)
        self.hp=2
        self.imgBrick=pygame.image.load('Images/кирпич.png')
    def update(self):
        pass
    def draw(self):
        #создание изображения
        self.window.blit(self.imgBrick,self.rect)

    def damage(self,value):
        self.hp-=value
        if self.hp<=0:
            self.objects.remove(self)

class EnemySpawner:
    def __init__(self,px,py,max_count,spawners,objects,hero_tank,window,imgSpawn):
        spawners.append(self)
        self.spawners=spawners
        self.objects=objects
        self.window=window
        self.hero_tank=hero_tank
        self.px=px
        self.py=py
        self.max_count=max_count
        self.tanks=[]
        self.imgSpawn=imgSpawn

        self.spawnTimer=300
        self.spawnDelay=500

    def update(self):
        global all_enemys
        if self.spawnTimer==0 and len(self.tanks)<self.max_count and all_enemys>0:
            
            rect=pygame.Rect(self.px,self.py,64,64)
            fined=False
            for obj in self.objects:
                if obj.type!='explode' and rect.colliderect(obj.rect):
                    fined=True

            if not(fined):
                self.tanks.append(EnemyTank('Red',self.px,self.py,0))
                self.spawnTimer=self.spawnDelay 
                all_enemys-=1

        all_tanks=[tk for tk in self.objects if tk.type=='enemy_tank']


        global lose
        global win
        #условие победы
        if all_enemys==0 and len(all_tanks)==0 and not(lose):
            win=True
            if self.hero_tank in self.objects:
                self.objects.remove(self.hero_tank)

        #условие поражения
        if self.hero_tank.hp==0:
            
            lose=True
            #print(lose)
            for obj in self.objects:
                if obj.type=='enemy_tank':
                    self.objects.remove(obj)



        for tank in self.tanks:
            if tank not in self.objects:
                self.tanks.remove(tank)       
        if self.spawnTimer>0:
            self.spawnTimer-=1

        
    def draw(self):
        self.window.blit(self.imgSpawn,(self.px,self.py))
