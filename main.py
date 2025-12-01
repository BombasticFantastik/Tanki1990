import pygame
import random
import os
from classes import UI,Tank,Block,EnemySpawner
from config import WIDTH,HEIGHT,TILE,FPS,win,lose

pygame.init()

objects=[]
bullets=[]
spawners=[]
clock=pygame.time.Clock()
window=pygame.display.set_mode((WIDTH,HEIGHT))

#запуск музыки
mix=pygame.mixer.init()
pygame.mixer.music.load('Music/sna.mp3')
pygame.mixer.music.play()

#звук выстрела
shoot_sound = pygame.mixer.Sound('Music/выстрел.wav')

#загрузка изображений
imgHero=pygame.image.load('Images/герой.png')


#победа
imgWins=[os.path.join('Images/победа',img) for img in os.listdir('Images/победа')]
imgWins.sort()


#поражение
imgLose=[os.path.join('Images/поражение',img) for img in os.listdir('Images/поражение')]
imgTextLose=[os.path.join('Images/поражение_текст',img) for img in os.listdir('Images/поражение_текст')]
imgLose.sort()
imgTextLose.sort()

#спавнер
imgSpawn=pygame.image.load('Images/спавнер0.png')


hero_tank=Tank('blue',100,275,0,objects,imgHero,window)
ui=UI(hero_tank,window,imgLose,imgWins,imgTextLose)


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
    Block(x,y,64,objects,window)


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
    EnemySpawner(x,y,3,spawners,objects,hero_tank,window,imgSpawn)

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