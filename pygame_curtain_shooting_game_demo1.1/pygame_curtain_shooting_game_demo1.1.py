import pygame, sys, random
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
GAMEAREAWIDTH = 375
GAMEAREAHEIGHT = 500
PLAYERSIZE = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (255, 0, 0)
BLUE = (0, 0, 255)

FPS = 60
PLAYERFASTSPEED = 5

class body:
  def __init__(self, name, rect, image, hp):
    self.name = name
    self.rect = rect
    self.image = image
    self.hp = hp

class player(body):
  def __init__(self, name, rect, image, hp, fastspeed, slowspeed):
    body.__init__(self, name, rect, image, hp)
    self.fastspeed = fastspeed
    self.slowspeed = slowspeed
  def playerMove(self, gamearea):
    moveLeft = moveRight = moveUp = moveDown = False
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == K_LEFT:
          moveRight = False
          moveLeft = True
        if event.key == K_RIGHT:
          moveRight = True
          moveLeft = False
        if event.key == K_UP:
          moveUp = True
          moveDown = False
        if event.key == K_DOWN:
          moveUp = False
          moveDown = True

      if event.type == KEYUP:
        if event.key == K_LEFT:
          moveLeft = False
        if event.key == K_RIGHT:
          moveRight = False
        if event.key == K_UP:
          moveUp = False
        if event.key == K_DOWN:
          moveDown = False
    if moveLeft and self.rect.left > gamearea.left:
      self.rect.move_ip(-1 * self.fastspeed, 0)
      if self.rect.left < gamearea.left:
        self.rect.left = gamearea.left
    if moveRight and self.rect.right < gamearea.right:
      self.rect.move_ip(self.fastspeed, 0)
      if self.rect.right > gamearea.right:
        self.rect.right = gamearea.right
    if moveUp and self.rect.top > gamearea.top:
      self.rect.move_ip(0, -1 * self.fastspeed)
      if self.rect.top < gamearea.top:
        self.rect.top = gamearea.top
    if moveDown and self.rect.bottom < gamearea.bottom:
      self.rect.move_ip(0, self.fastspeed)
      if self.rect.bottom > gamearea.bottom:
        self.rect.bottom = gamearea.bottom  
    return self.rect.centerx, self.rect.centery


def terminate():
  pygame.quit()
  sys.exit()



pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Curtain_Shooting_Game_Demo1")
pygame.mouse.set_visible(False)

GAMEAREA = pygame.Rect(50, 50, GAMEAREAWIDTH, GAMEAREAHEIGHT)

player1 = player("1", pygame.Rect(GAMEAREA.centerx - PLAYERSIZE / 2, GAMEAREA.bottom - PLAYERSIZE *2, PLAYERSIZE, PLAYERSIZE), None, 1, PLAYERFASTSPEED, 1)

windowSurface.fill(WHITE)
pygame.draw.rect(windowSurface, BLUE, GAMEAREA)
pygame.draw.rect(windowSurface, RED, player1.rect)

pygame.display.update()


while True:


  for event in pygame.event.get():
    if event.type == QUIT:
      terminate()
    
  player1.rect.centerx, player1.rect.centery = player1.playerMove(GAMEAREA)

  windowSurface.fill(WHITE)
  pygame.draw.rect(windowSurface, BLUE, GAMEAREA)
  pygame.draw.rect(windowSurface, RED, player1)

  pygame.display.update()

  mainClock.tick(FPS)
