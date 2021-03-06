import pygame, sys, random 
from pygame.locals import *

#set up a game 
pygame.init()
mainClock = pygame.time.Clock()

#set up the window
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("Sprites and Sounds")

#set up colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

#set up the player and food deta structures
foodCounter = 0
NEWFOOD = 40 
FOODSIZE = 20
player = pygame.Rect(300, 100, 40, 40)
playerImage = pygame.image.load("player.png")
playerStretchedImage = pygame.transform.scale(playerImage, (40, 40))
foodImage = pygame.image.load("cherry.png")

#set up the music
pickUpSound = pygame.mixer.Sound("pickup.wav")
pygame.mixer.music.load("background.mid")
pygame.mixer.music.play(-1, 0.0)
musicPlaying = True

foods = []
for i in range(20):
  foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

#set up movement variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 6



#run the game loop 
while True:
  #check for events
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

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
      #setting flash
      if event.key == K_x:
        player.top = random.randint(0, WINDOWHEIGHT - player.height)
        player.left = random.randint(0, WINDOWWIDTH - player.width)
      if event.key == K_m:
        if musicPlaying:
          pygame.mixer.music.stop()
        else:
          pygame.mixer.music.play(-1, 0.0)
        musicPlaying = not musicPlaying

    
    if event.type == MOUSEBUTTONUP:
      foods.append(pygame.Rect(event.pos[0], event.pos[1], FOODSIZE, FOODSIZE))
    
    
  

  foodCounter += 1
  if foodCounter >= NEWFOOD: 
    #add new food 
    foodCounter = 0
    foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

  windowSurface.fill(WHITE)
  
  #move the player
  if moveDown and player.bottom < WINDOWHEIGHT:
    player.top += MOVESPEED
  if moveUp and player.top > 0:
    player.top -= MOVESPEED
  if moveRight and player.right < WINDOWWIDTH:
    player.left += MOVESPEED
  if moveLeft and player.left > 0:
    player.left -= MOVESPEED

  #draw the block onto the surface 
  windowSurface.blit(playerStretchedImage, player)

  #check whether the player has intersected with any food squares
  for food in foods[:]:
    if player.colliderect(food):
      player = pygame.Rect(player.left, player.top, player.width + 2, player.height + 2)
      playerStretchedImage = pygame.transform.scale(playerImage, (player.width, player.height))
      if musicPlaying:
        pickUpSound.play()
      foods.remove(food)
  
  #draw the food  
  for food in foods:
    windowSurface.blit(foodImage, food)

  #draw the window on to the screen
  pygame.display.update()
  mainClock.tick(40)
