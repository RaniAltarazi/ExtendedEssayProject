import pygame
from pygame.locals import*
import time

def draw_block1():
    surface.fill((255,255,255))
    pygame.draw.rect(surface, (0,0,0),pygame.Rect(100,0,302,625),2)
    print(posrotate)
    block12 = pygame.transform.rotate(block5, posrotate)
    surface.blit(block12,(posx,posy))
    pygame.display.flip()


if __name__== "__test__":
    pygame.init() 

surface = pygame.display.set_mode((500,700))
surface.fill((255,255,255))
pygame.draw.rect(surface, (0,0,0),pygame.Rect(100,0,305,625),2)
pygame.display.flip()
block1 = pygame.image.load("shape1.png")
block2 = pygame.image.load("shape2.png")
block3 = pygame.image.load("shape3.png")
block4 = pygame.image.load("shape4.png")
block5 = pygame.image.load("shape5.png")
block6 = pygame.image.load("shape6.png")
posrotate = 180
block12 = pygame.transform.rotate(block5, posrotate)
posx = 160
posy = 0
surface.blit(block12,(posx,posy))
pygame.display.flip()
running =True

while running:
    for event in pygame.event.get():
        if event.type ==KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                
            if event.key == K_LEFT:
                posx-=30
                draw_block1()
            if event.key == K_RIGHT:
                posx+=30
                draw_block1()
            if event.key == K_UP:
                posrotate -=90  
                draw_block1() 
            if event.key == K_DOWN:
                posy+=30 
                draw_block1()
                

        elif event.type == QUIT:
            running =  False
        