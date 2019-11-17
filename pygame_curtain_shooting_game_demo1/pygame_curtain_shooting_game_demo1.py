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

# class player:
#   def __init__(self, name, rect)

def terminate():
  pygame.quit()
  sys.exit()

pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Curtain_Shooting_Game_Demo1")
pygame.mouse.set_visible(False)

gamearea = pygame.Rect(50, 50, GAMEAREAWIDTH, GAMEAREAHEIGHT)
player = pygame.Rect(gamearea.centerx - PLAYERSIZE / 2, gamearea.bottom - PLAYERSIZE *2, PLAYERSIZE, PLAYERSIZE)
windowSurface.fill(WHITE)
pygame.draw.rect(windowSurface, BLUE, gamearea)
pygame.draw.rect(windowSurface, RED, player)

pygame.display.update()

moveLeft = moveRight = moveUp = moveDown = False

while True:


  for event in pygame.event.get():
    if event.type == QUIT:
      terminate()
    
    if event.type == KEYDOWN:
      if event.key == K_LEFT or event.key == K_a:
        moveRight = False
        moveLeft = True
      if event.key == K_RIGHT or event.key == K_d:
        moveRight = True
        moveLeft = False
      if event.key == K_UP or event.key == K_w:
        moveUp = True
        moveDown = False
      if event.key == K_DOWN or event.key == K_s:
        moveUp = False
        moveDown = True

    if event.type == KEYUP:
      if event.key == K_ESCAPE:
        pygame.quit()
        sys.exit()
      if event.key == K_LEFT or event.key == K_a:
        moveLeft = False
      if event.key == K_RIGHT or event.key == K_d:
        moveRight = False
      if event.key == K_UP or event.key == K_w:
        moveUp = False
      if event.key == K_DOWN or event.key == K_s:
        moveDown = False
  
  if moveLeft and player.left > gamearea.left:
    player.move_ip(-1 * PLAYERFASTSPEED, 0)
    if player.left < gamearea.left:
      player.left = gamearea.left
  if moveRight and player.right < gamearea.right:
    player.move_ip(PLAYERFASTSPEED, 0)
    if player.right > gamearea.right:
      player.right = gamearea.right
  if moveUp and player.top > gamearea.top:
    player.move_ip(0, -1 * PLAYERFASTSPEED)
    if player.top < gamearea.top:
      player.top = gamearea.top
  if moveDown and player.bottom < gamearea.bottom:
    player.move_ip(0, PLAYERFASTSPEED)
    if player.bottom > gamearea.bottom:
      player.bottom = gamearea.bottom  

  pygame.draw.rect(windowSurface, BLUE, gamearea)
  pygame.draw.rect(windowSurface, RED, player)

  pygame.display.update()

  mainClock.tick(FPS)





  