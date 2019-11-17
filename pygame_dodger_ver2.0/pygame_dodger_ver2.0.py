import pygame, sys, random, time
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
# addNewBaddieRate = 7
PLAYERMOVERATE = 6 
PLAYERMOVERATESLOW = 3

def terminate():
  pygame.quit()
  sys.exit()

def waitForPlayerToPressKey():
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        terminate()
      if event.type == KEYUP:
        if event.key == K_ESCAPE:
          terminate()
        return

def waitForPlayerToChooseDifficulty():
  windowSurface.fill(BACKGROUNDCOLOR)
  drawText("Choose the difficulty of the game.", fontSmall, windowSurface, (WINDOWWIDTH / 6), (WINDOWHEIGHT / 3))
  drawText("1: Easy, 2:Normal, 3:Hard, 4:Lunatic", fontSmall, windowSurface, (WINDOWWIDTH / 6) - 30, (WINDOWHEIGHT / 3) + 50)
  pygame.display.update()
  while True:
    for event in pygame.event.get():
      if event.type == KEYUP:
        if event.key == K_1:
          return 7
        if event.key == K_2:
          return 5
        if event.key == K_3:
          return 3  
        if event.key == K_4:
          return 1       
        if event.key == K_ESCAPE:
          terminate()

def playerHasHitsBaddie(playerRect, baddies):
  for b in baddies:
    if playerRect.colliderect(b["rect"]):
      return True
  return False

def drawText(text, font, surface, x, y):
  textobj = font.render(text, 1, TEXTCOLOR)
  textrect = textobj.get_rect()
  textrect.topleft = (x, y)
  surface.blit(textobj, textrect)

# Set up pygame, the window and the mouse cursor. 
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Dodger")
pygame.mouse.set_visible(False)

# Set up fonts.
font = pygame.font.SysFont(None, 48)
fontSmall = pygame.font.SysFont(None, 36)

# Set up sounds.
gameOverSound = pygame.mixer.Sound("gameover.wav")
pygame.mixer.music.load("background.mid")

# Set up images.
playerImage = pygame.image.load("smallerPlayer.png")
playerRect = playerImage.get_rect()
playerBody = pygame.image.load("player.png")
playerBodyRect = playerBody.get_rect()
baddieImage = pygame.image.load("baddie.png")

topScore = 0

# Set the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText("Dodger", font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText("Press a key to start.", font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
time.sleep(1)
waitForPlayerToPressKey()

while True:
  # Set the "Choose" screen.
  time.sleep(1)
  addNewBaddieRate = waitForPlayerToChooseDifficulty()
  

  # Set up the start of the game. 
  baddies = []
  score = 0
  playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
  moveLeft = moveRight = moveUp = moveDown = False
  reverseCheat = slowCheat = clearScreen = False
  slowMode = False
  baddieAddCounter = 0 
  pygame.mixer.music.play(-1, 0.0)

  while True: # The game loop runs while the game part is playing.
    # Increase score.
    scoreRate = int((9 - addNewBaddieRate) / 2)
    score += scoreRate
    for event in pygame.event.get():
      if event.type == QUIT:
        terminate()
        
      if event.type == KEYDOWN:
        if event.key == K_c:
          reverseCheat = True
        if event.key == K_x:
          slowCheat = True
        if event.key == K_LEFT or event.key == K_a:
          moveLeft = True
          moveRight = False
        if event.key == K_RIGHT or event.key == K_d:
          moveRight = True
          moveLeft = False
        if event.key == K_UP or event.key == K_w:
          moveUp = True
          moveDown = False
        if event.key == K_DOWN or event.key == K_s:
          moveDown = True
          moveUp = False
        if event.key == K_z:
          clearScreen = True
        if event.key == K_LSHIFT or event.key == K_RSHIFT:
          slowMode = True
          
      if event.type == KEYUP:
        if event.key == K_c:
          reverseCheat = False
          score = 0
        if event.key == K_x:
          slowCheat = False
          score = 0
        if event.key == K_LEFT or event.key == K_a:
          moveLeft = False
        if event.key == K_RIGHT or event.key == K_d:
          moveRight = False
        if event.key == K_UP or event.key == K_w:
          moveUp = False
        if event.key == K_DOWN or event.key == K_s:
          moveDown = False
        if event.key == K_LSHIFT or event.key == K_RSHIFT:
          slowMode = False
        if event.key == K_ESCAPE:
          terminate()


      if event.type == MOUSEMOTION:
        # If the mouse moves, move the player to the cursor.
        playerRect.centerx = event.pos[0]  
        playerRect.centery = event.pos[1]
    
    # Add new baddies at the top of the screen, if need.
    if not reverseCheat and not slowCheat:
      baddieAddCounter += 1

    if baddieAddCounter ==  addNewBaddieRate:
      baddieAddCounter = 0
      baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
      newBaddie = {"rect" : pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize), 
                   "speed" : random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                   "surface" : pygame.transform.scale(baddieImage, (baddieSize, baddieSize))}
      baddies.append(newBaddie)
    
    # Move the player around.
    if slowMode == True:
      if moveLeft and playerRect.left > 0:
        playerRect.move_ip(-1 * PLAYERMOVERATESLOW, 0)
      if moveRight and playerRect.right < WINDOWWIDTH:
        playerRect.move_ip(PLAYERMOVERATESLOW, 0)
      if moveUp and playerRect.top > 0:
        playerRect.move_ip(0, -1 * PLAYERMOVERATESLOW)
      if moveDown and playerRect.bottom < WINDOWHEIGHT:
        playerRect.move_ip(0, PLAYERMOVERATESLOW)
    else:
      if moveLeft and playerRect.left > 0:
        playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
      if moveRight and playerRect.right < WINDOWWIDTH:
        playerRect.move_ip(PLAYERMOVERATE, 0)
      if moveUp and playerRect.top > 0:
        playerRect.move_ip(0, -1 * PLAYERMOVERATE)
      if moveDown and playerRect.bottom < WINDOWHEIGHT:
        playerRect.move_ip(0, PLAYERMOVERATE)
  
    # Let player body follow the player collision box.
    playerBodyRect.centerx = playerRect.centerx
    playerBodyRect.centery = playerRect.centery

    # Move the baddies down.
    for b in baddies:
      if not reverseCheat and not slowCheat:
        b["rect"].move_ip(0, b["speed"])
      elif reverseCheat:
        b["rect"].move_ip(0, -5)
      elif slowCheat:
        b["rect"].move_ip(0, 1)

    if clearScreen:
      for b in baddies[:]:
        if b["rect"].centerx in range(playerRect.centerx-200, playerRect.centerx +200) and b["rect"].centery in range(playerRect.centery-200, playerRect.centery+200):
          baddies.remove(b)
      score -= 500   

      clearScreen = False
    
    # Delet baddies that have fallen past the bottom.
    for b in baddies[:]:
      if b["rect"].top > WINDOWHEIGHT:
        baddies.remove(b)


    # Draw the game world on the window.
    windowSurface.fill(BACKGROUNDCOLOR)

    # Draw the player body's rectangle.
    windowSurface.blit(playerBody, playerBodyRect)   

    # Draw the player collision box's rectangle.
    windowSurface.blit(playerImage, playerRect)

    # Draw each baddie.
    for b in baddies:
      windowSurface.blit(b["surface"], b["rect"])
    
    
    # Draw the score and top score.
    drawText("Score: %s" %(score), font, windowSurface, 10, 0)
    drawText("Top Score: %s" %(topScore), font, windowSurface, 10, 40)

    pygame.display.update()

    # Check if any of the baddies have hit the player.
    if playerHasHitsBaddie(playerRect, baddies):
      if score > topScore:
        topScore = score
      break
    
    mainClock.tick(FPS)
  
  # Stop the game and show the "Game Over" screen.
  pygame.mixer.music.stop()
  gameOverSound.play()

  drawText("Game Over", font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
  drawText("Press a key to play again.", font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
  pygame.display.update()
  time.sleep(3)
  waitForPlayerToPressKey()
  gameOverSound.stop()




