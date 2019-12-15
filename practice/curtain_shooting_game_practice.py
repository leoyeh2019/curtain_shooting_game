import pygame, sys, random, time
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
GAMEAREAWIDTH = 375
GAMEAREAHEIGHT = 500
PLAYERSIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 255, 255)
FPS = 60
PLAYERFASTSPEED = 4
PLAYERSLOWSPEED = 2
PLAYERBULLETSIZE = 2
PLAYERBULLETDAMAGE = 10
ENEMYSIZE = 20
ENEMYHP = 100



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
    playerBullet1 = bullet(name = "playerBullet", rect = pygame.Rect(self.rect.centerx - PLAYERBULLETSIZE / 2, self.rect.top + PLAYERBULLETSIZE * 2, PLAYERBULLETSIZE, PLAYERBULLETSIZE*2), image = None, damage = PLAYERBULLETDAMAGE)
    playerBullet2 = bullet(name = "playerBullet", rect = pygame.Rect(self.rect.left                          , self.rect.top + PLAYERBULLETSIZE * 2, PLAYERBULLETSIZE, PLAYERBULLETSIZE*2), image = None, damage = PLAYERBULLETDAMAGE)
    playerBullet3 = bullet(name = "playerBullet", rect = pygame.Rect(self.rect.right - PLAYERBULLETSIZE      , self.rect.top + PLAYERBULLETSIZE * 2, PLAYERBULLETSIZE, PLAYERBULLETSIZE*2), image = None, damage = PLAYERBULLETDAMAGE)
    if shooting:
      # For every 5 frames, generate a new bullet
      if time % 5 == 0:
        self.bulletList.append(playerBullet1)
        self.bulletList.append(playerBullet2)
        self.bulletList.append(playerBullet3)
        
    for b in self.bulletList:
      b.bulletMove(patternX, patternY)
      if b.rect.top < gamearea.top:
        self.bulletList.remove(b)

class enemy():
  def __init__(self, name, rect, image, hp, movingPatternX, movingPatternY):
    self.name = name
    self.rect = rect
    self.image = image
    self.hp = hp
    self.movingPatternX = movingPatternX
    self.movingPatternY = movingPatternY
  def enemyMove(self):
    self.rect.move_ip(self.movingPatternX, self.movingPatternY)
    
def terminate():
  pygame.quit()
  sys.exit()

def generateEnemyParameter(time):
  if time in range(0, 1800):
    return 10
  elif time in range(1800, 3600):
    return 8
  elif time in range(3600, 5400):
    return 6
  elif time in range(5400, 7200): 
    return 4
  else:
    return 2

def ifEnemyHasHitPlayer(player, enemyList):
  for e in enemyList:
    if player.rect.colliderect(e.rect):
      return True
  return False

def drawText(surf, text, size, x, y):
  font = pygame.font.Font(None, size)
  text_surface = font.render(text, True, BLACK)
  text_rect = text_surface.get_rect()
  text_rect.topleft = (x, y)
  surf.blit(text_surface, text_rect)

  
# Pygame Initiate
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Curtain_Shooting_Game_ver0.2")
pygame.mouse.set_visible(False)

# Set Gamearea
GAMEAREA = pygame.Rect(50, 50, GAMEAREAWIDTH, GAMEAREAHEIGHT)
GAMEAREAFRAME = [pygame.Rect(0, 0, GAMEAREAWIDTH + 50, 50), pygame.Rect(0, 0, 50, GAMEAREAHEIGHT + 50), pygame.Rect(0, GAMEAREAHEIGHT + 50, GAMEAREAWIDTH + 50, 50), pygame.Rect(GAMEAREAWIDTH + 50, 0, 100, GAMEAREAHEIGHT + 50)]

# Set player1 = player(name, rect, image, hp, bulletList, bulletPatternX, bulletPatternY, fastspeed, slowspeed)
def player1BulletPatternX(t):
  return 0
def player1BulletPatternY(t):
  return -10 
player1 = player(name = "1", rect = pygame.Rect(GAMEAREA.centerx - PLAYERSIZE / 2, GAMEAREA.bottom - PLAYERSIZE *2, PLAYERSIZE, PLAYERSIZE), image = None, hp = 1, bulletList = [], bulletPatternX = player1BulletPatternX, bulletPatternY = player1BulletPatternY, fastspeed = PLAYERFASTSPEED, slowspeed = PLAYERSLOWSPEED)



while True:
  windowSurface.fill(WHITE)
  pygame.draw.rect(windowSurface, BLUE, GAMEAREA)
  pygame.draw.rect(windowSurface, RED, player1.rect)

  pygame.display.update()



  # Setting Parameter
  moveLeft = moveRight = moveUp = moveDown = False
  slowMode = False
  shooting = False
  shootingTimer = 0
  generateEnemyTimer = 0
  enemy_list = []
  score = 0


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
      

    # Generate Enemy in a Time Dependent Rate
    if generateEnemyTimer % (generateEnemyParameter(generateEnemyTimer)) == 0:
      enemy_list.append(enemy(name = "enemyA", rect = pygame.Rect(random.randint(50, (50 + GAMEAREAWIDTH - ENEMYSIZE)), random.randint(50, (50 + GAMEAREAHEIGHT/4 - ENEMYSIZE)), ENEMYSIZE, ENEMYSIZE), image = None, hp = ENEMYHP, movingPatternX = random.randint(-1, 1), movingPatternY = random.randint(1, 7)))
              
    
    # Move Enemy
    for e in enemy_list:
      e.enemyMove()
      if (e.rect.top > GAMEAREA.bottom) or (e.rect.left > GAMEAREA.right) or (e.rect.right < GAMEAREA.left):
        enemy_list.remove(e)
    # Move Player
    player1.playerMove(GAMEAREA, slowMode, moveLeft, moveRight, moveUp, moveDown)
    player1.shootBullet(shooting, shootingTimer, GAMEAREA, player1BulletPatternX(shootingTimer), player1BulletPatternY(shootingTimer))
    
    # Detect Collidion
    for b in player1.bulletList:
      for e in enemy_list:
        if b.rect.colliderect(e.rect):
          e.hp -=10
    if ifEnemyHasHitPlayer(player1, enemy_list):
      time.sleep(0.5)
      break
    
    for e in enemy_list:
      if e.hp <= 0:
        enemy_list.remove(e)
        score += 100
    

    # Refresh Screen
    windowSurface.fill(WHITE)
    pygame.draw.rect(windowSurface, BLUE, GAMEAREA)
    for e in enemy_list:
      pygame.draw.rect(windowSurface, LIGHTBLUE, e.rect)
    pygame.draw.rect(windowSurface, RED, player1.rect)
    for b in player1.bulletList:
      pygame.draw.rect(windowSurface, GREEN, b.rect)
    for gf in GAMEAREAFRAME:
      pygame.draw.rect(windowSurface, WHITE, gf)

    stage = int(generateEnemyParameter(generateEnemyTimer))
    score += (12 - stage)
    drawText(windowSurface, "stage : {0:8}".format(stage), 32, 450, 50)
    drawText(windowSurface, "score : {0:8}".format(score), 32, 450, 100)

    shootingTimer += 1
    generateEnemyTimer += 1
    pygame.display.update()

    mainClock.tick(FPS)


