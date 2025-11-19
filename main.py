# import pygame
# import random

# white=(255,255,255)
# blue=(255,0,0)
# red=(0,255,0)


# size=(1200,1000)
# pos_x=300
# pos_y=300
# clock=pygame.time.Clock()

# pygame.init()
# screen=pygame.display.set_mode(size)
# pygame.display.set_caption("ТАНКИ 1990 V0")

# game_over=False
# while not game_over:
#     keys=pygame.key.get_pressed()
#     for event in pygame.event.get():
#         #условие закрытия
#         if event.type==pygame.QUIT:
#             game_over=True

#     if keys[pygame.K_LEFT]:
#         pos_x+=-5
#         #y1_change=0
#     if keys[pygame.K_RIGHT]:
#         pos_x+=5
#         #y1_change=0
#     if keys[pygame.K_UP]:
#         pos_y+=-5

#     if keys[pygame.K_DOWN]:
#         pos_y+=5
    
#     screen.fill(white)
#     pygame.draw.rect(screen,blue,[pos_x,pos_y,30,30])
#     pygame.display.update()
#     clock.tick(30)
#     pygame.event.pump()

# pygame.quit()
# quit()