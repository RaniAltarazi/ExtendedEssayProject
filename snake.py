import pygame
from pygame.locals import *
import random

clock = pygame.time.Clock()
pygame.init()
font1 = pygame.font.SysFont(pygame.font.get_default_font(), 80)

class Apple:
    def __init__(self,parent_screen):
        self.image = pygame.image.load("resources/Apple.png").convert()
        self.parent_screen = parent_screen
        self.x = 200
        self.y = 500
    def randompos(self):
        self.x = random.randint(1,16)*50
        self.y = random.randint(1,14)*50
    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y,))
class Border:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.lengthx = 17
        self.lengthy = 15
        self.borderx = [0]*65
        self.bordery = [0]*65
    def draw(self):
        for i in range(self.lengthx):
            self.borderx[i]=50*i
            self.bordery[i] = 0
            self.border = pygame.draw.rect(self.parent_screen,(0,0,0),pygame.Rect((self.borderx[i]),(self.bordery[i]), 50,50))
        for k in range(self.lengthx,self.lengthx+self.lengthy,1):
            self.bordery[k]=50*(k-self.lengthx)
            self.borderx[k] = 0
            self.border = pygame.draw.rect(self.parent_screen,(0,0,0),pygame.Rect((self.borderx[k]),(self.bordery[k]), 50,50))
        for j in range(self.lengthx+self.lengthy,2*self.lengthx+self.lengthy,1):
            self.borderx[j]=50*(j-(self.lengthx+self.lengthy))
            self.bordery[j] = 750
            self.border = pygame.draw.rect(self.parent_screen,(0,0,0),pygame.Rect((self.borderx[j]),(self.bordery[j]), 50,50))
        for m in range(2*self.lengthx+self.lengthy,(2*self.lengthx+2*self.lengthy)+1,1):
            self.bordery[m]=50*(m-(2*self.lengthx+self.lengthy))
            self.borderx[m] = 850
            self.border = pygame.draw.rect(self.parent_screen,(0,0,0),pygame.Rect((self.borderx[m]),(self.bordery[m]), 50,50))
        
class Snake: 
    def __init__ (self,parent_screen,length):

        self.length = length
        self.parent_screen = parent_screen
        self.block_x = [150,100,50,0]
        self.block_y = [450]*self.length
        self.x_direction = 1
        self.apple = Apple(self.parent_screen)
        self.y_direction = 0
        self.border = Border(self.parent_screen)
    def draw (self):
        self.parent_screen.fill((26, 201, 29))
        self.apple.draw()
        self.border.draw()
        
        for i in range (self.length):
            self.block = pygame.draw.rect(self.parent_screen,(255,0,0),pygame.Rect((self.block_x[i]),(self.block_y[i]), 50,50))
            self.blockBorder = pygame.draw.rect(self.parent_screen,(0,0,0),pygame.Rect((self.block_x[i]),(self.block_y[i]), 50,50),2)
        pygame.display.flip()
    def moveLeft(self):
        self.x_direction = -1
        self.y_direction = 0
        ##self.draw()
    def moveRight(self):
        self.x_direction = 1
        self.y_direction = 0
       ## self.draw()
    def moveUp(self):
        self.x_direction = 0
        self.y_direction = -1
        ##self.draw()
    def moveDown(self):
        self.x_direction = 0
        self.y_direction = 1
        ##self.draw()
    def walk(self):
        for i in range (self.length-1,0,-1):
            self.block_x[i] = self.block_x[(i-1)]
            self.block_y[i] = self.block_y[(i-1)]

        
        self.block_x[0] = self.block_x[0] + ((50*self.x_direction))
        self.block_y[0] = self.block_y[0] + ((50*self.y_direction))
        self.draw()
    def increase(self):
        self.apple.randompos()
        self.length +=1
        self.block_x.append(-50)
        self.block_y.append(-50)

        




class Game:
    
    def __init__(self):
       
        pygame.init()
        self.surface = pygame.display.set_mode((900,800))
        self.surface.fill((255, 255, 255))
        self.snake = Snake(self.surface,4)
        self.snake.draw()
        self.alive = True
        self.dead = False

    def is_collision(self,x1,y1,x2,y2):
        if x1==x2:
            if y1==y2:
                return True
        return False
    def play(self):
        self.snake.walk()
        if self.is_collision(self.snake.block_x[0],self.snake.block_y[0],self.snake.apple.x,self.snake.apple.y):
            self.snake.increase()
        for i in range (65):
            if self.is_collision(self.snake.block_x[0],self.snake.block_y[0],self.snake.border.borderx[i],self.snake.border.bordery[i]):
                self.alive = False
                self.dead =True
        for k in range(1,self.snake.length,1):
            if self.is_collision(self.snake.block_x[0],self.snake.block_y[0],self.snake.block_x[k],self.snake.block_y[k]):
                self.alive = False
                self.dead =True
                

    def run(self):
        self.running = True
        while self.running:
            if self.alive:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.running =False
                        if event.key == K_UP and self.snake.y_direction !=1:
                            self.snake.moveUp()
                        if event.key == K_DOWN and self.snake.y_direction !=-1:
                            self.snake.moveDown()
                        if event.key == K_LEFT and self.snake.x_direction !=1:
                            self.snake.moveLeft()
                        if event.key == K_RIGHT and self.snake.x_direction !=-1:
                            self.snake.moveRight()         
                    elif event.type == QUIT:
                        self.running = False
                self.play()
                self.dt = clock.tick(12)
            elif self.dead:
                self.surface.fill((0, 0, 0))   
                img = font1.render('You Lost! Press enter to try again!', True, (255,0,0))
                img_rect = img.get_rect(center=(450, 400))
                self.surface.blit(img, img_rect)    
                pygame.display.flip()         

                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.running =False     
                        if event.key == K_RETURN:
                            self.surface = pygame.display.set_mode((900,800))
                            self.surface.fill((255, 255, 255))
                            self.snake = Snake(self.surface,4)
                            self.snake.draw()
                            self.alive = True
                            self.dead = False
                    elif event.type == QUIT:
                        self.running = False       
           
           
            

if __name__ == "__main__":
   game = Game()
   game.run()

   