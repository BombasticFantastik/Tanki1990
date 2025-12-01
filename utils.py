import pygame
def gif_player(window,imgs,width,frames,frame):
    for i in range(frames):
        if i<10:
            idx='0'+str(i)
        else:
            idx=str(i)
        window.blit(pygame.image.load(imgs[int(frame)]),((width//3),width//3))