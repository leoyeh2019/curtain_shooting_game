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
PLAYERSLOWSPEED = 1
PLAYERBULLETSIZE = 3
PLAYERBULLETSPEED = 1


class body:
  def __init__(self, name, rect, image, hp, bulletList, bulletPatternX, bulletPatternY):
    self.name = name
    self.rect = rect
    self.image = image
    self.hp = hp
    self.bulletList = bulletList
    self.bulletPatternX = bulletPatternX
    self.bulletPatternY = bulletPatternY

class bullet():
  def __init__(self, name, rect, image, damage):
    self.name = name
    self.rect = rect
    self.image = image
    self.damage = damage

  def bulletMove(self, patternX, patternY):
    self.rect.move_ip(patternX, patternY)
  

  

class player(body):
  def __init__(self, name, rect, image, hp, bulletList, bulletPatternX, bulletPatternY, fastspeed, slowspeed):
    body.__init__(self, name, rect, image, hp, bulletList, bulletPatternX, bulletPatternY)
    self.fastspeed = fastspeed
    self.slowspeed = slowspeed
  
  # Control the Movement of Plaer  
  def playerMove(self, gamearea, slowMode, moveLeft, moveRight, moveUp, moveDown):
    if slowMode:
      speed = self.slowspeed
    else:
      speed = self.fastspeed

    if moveLeft and self.rect.left > gamearea.left:
      self.rect.move_ip(-1 * speed, 0)
      if self.rect.left < gamearea.left:
        self.rect.left = gamearea.left
    if moveRight and self.rect.right < gamearea.right:
      self.rect.move_ip(speed, 0)
      if self.rect.right > gamearea.right:
        self.rect.right = gamearea.right
    if moveUp and self.rect.top > gamearea.top:
      self.rect.move_ip(0, -1 * speed)
      if self.rect.top < gamearea.top:
        self.rect.top = gamearea.top
    if moveDown and self.rect.bottom < gamearea.bottom:
      self.rect.move_ip(0, speed)
      if self.rect.bottom > gamearea.bottom:
        self.rect.bottom = gamearea.bottom  

  # Place the Bullet on the Screen
  def shootBullet(self, shooting, time, gamearea, patternX, patternY):
    # Set playerBullet = bullet(self, name, rect, image, damage)
    playerBullet = bullet("playerBullet", pygame.Rect(self.rect.centerx, self.rect.centery, PLAYERBULLETSIZE, PLAYERBULLETSIZE*2), None, 10)
    if shooting:
      # For every 5 frames, generate a new bullet
      print (time)
      # print(type(self.bulletList))
      if time % 5 == 0:
        # print(len(self.bulletList))
        self.bulletList.append(playerBullet)
        
      for b in self.bulletList:
        b.bulletMove(patternX, patternY)
        if b.rect.bottom > gamearea.top:
          self.bulletList.remove(b)

      





def terminate():
  pygame.quit()
  sys.exit()


# Pygame Initiate
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Curtain_Shooting_Game_Demo1")
pygame.mouse.set_visible(False)

# Set Gamearea
GAMEAREA = pygame.Rect(50, 50, GAMEAREAWIDTH, GAMEAREAHEIGHT)

# Set player1 = player(name, rect, image, hp, bulletList, bulletPatternX, bulletPatternY, fastspeed, slowspeed)
def player1BulletPatternX(t):
  return 0
def player1BulletPatternY(t):
  return 10 
player1 = player("1", pygame.Rect(GAMEAREA.centerx - PLAYERSIZE / 2, GAMEAREA.bottom - PLAYERSIZE *2, PLAYERSIZE, PLAYERSIZE), None, 1, [], player1BulletPatternX, player1BulletPatternY, PLAYERFASTSPEED, PLAYERSLOWSPEED)


windowSurface.fill(WHITE)
pygame.draw.rect(windowSurface, BLUE, GAMEAREA)
pygame.draw.rect(windowSurface, RED, player1.rect)

pygame.display.update()

# Setting Parameter
moveLeft = moveRight = moveUp = moveDown = False
slowMode = False
shooting = False
shootingTimer = 0

while True:
  # Key Control
  for event in pygame.event.get():
    if event.type == QUIT:
      terminate()
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
      if event.key == K_LSHIFT:
        slowMode = True
      if event.key == K_z:
        shooting = True
        shootingTimer = 0

    if event.type == KEYUP:
      if event.key == K_LEFT:
        moveLeft = False
      if event.key == K_RIGHT:
        moveRight = False
      if event.key == K_UP:
        moveUp = False
      if event.key == K_DOWN:
        moveDown = False
      if event.key == K_LSHIFT:
        slowMode = False
      if event.key == K_z:
        shooting = False
      if event.key == K_ESCAPE:
        terminate()
    

  # Move Player
  player1.playerMove(GAMEAREA, slowMode, moveLeft, moveRight, moveUp, moveDown)
  player1.shootBullet(shooting, shootingTimer, GAMEAREA, player1BulletPatternX(shootingTimer), player1BulletPatternY(shootingTimer))
  # Refresh Screen
  windowSurface.fill(WHITE)
  pygame.draw.rect(windowSurface, BLUE, GAMEAREA)
  pygame.draw.rect(windowSurface, RED, player1.rect)
  for b in player1.bulletList:
    pygame.draw.rect(windowSurface, GREEN, b.rect)

  shootingTimer += 1
  pygame.display.update()

  mainClock.tick(FPS)
