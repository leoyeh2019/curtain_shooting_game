import pygame, sys, random, math 
from pygame.locals import *
from os import path


# ----------------------Unchangeable Variables----------------------
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
GAMEAREAWIDTH = 480
GAMEAREAHEIGHT = 560

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 255, 255)

FPS = 60

PLAYERWIDTH = 30
PLAYERHEIGHT = 30
PLAYERCOLISIONBOXSIZE = 10

ENEMYWIDTH = 20
ENEMYHEIGHT = 20



# ----------------------Classes----------------------
class playerCollisionBox(pygame.sprite.Sprite):
    def __init__(self, collisionBoxImage, playerRect):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = collisionBoxImage
        self.image_origin.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image_origin.copy(), (PLAYERCOLISIONBOXSIZE, PLAYERCOLISIONBOXSIZE))
        self.rect = self.image.get_rect(center = playerRect.center)
        self.radius = 0
        self.rotateSpeed = 5 
        self.lastUpdate = pygame.time.get_ticks()
    def rotate(self):
        now = pygame.time.get_ticks() 
        if now - self.lastUpdate > 100: 
            self.lastUpdate = now
            self.radius = (self.radius + self.rotateSpeed) % 360
            oldCenter = self.rect.center
            self.image = pygame.transform.scale(pygame.transform.rotate(self.image_origin, self.radius), (PLAYERCOLISIONBOXSIZE, PLAYERCOLISIONBOXSIZE))
            self.rect = self.image.get_rect()
            self.rect.center = oldCenter

        
    
        

class Player(pygame.sprite.Sprite):
    def __init__(self, name, lifes, image, collisionBoxImage, playerBulletImage, playerSpeed, putbulletPattern, shootBulletPattern):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.lifes = lifes
        self.image = image
        self.collisionBoxImage = collisionBoxImage
        self.playerBulletImage = playerBulletImage
        self.playerFastSpeed = playerSpeed[0]
        self.playerSlowSpeed = playerSpeed[1]
        self.putbulletPattern = putbulletPattern
        self.shootBulletPattern = shootBulletPattern

        self.rect = self.image.get_rect()
        self.rect.center = (GAMEAREA.centerx, GAMEAREA.bottom - 50)

        self.collisionBox = playerCollisionBox(collisionBoxImage = self.collisionBoxImage, playerRect = self.rect)

        self.radius = int(self.collisionBox.rect.width / 2)
        

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LSHIFT]:
            speed = self.playerSlowSpeed
        else:
            speed = self.playerFastSpeed
        if keystate[pygame.K_LEFT] and self.rect.left > GAMEAREA.left:
            self.rect.move_ip(-1 * speed, 0)
            if self.rect.left < GAMEAREA.left:
                self.rect.left = GAMEAREA.left
        if keystate[pygame.K_RIGHT] and self.rect.right < GAMEAREA.right:
            self.rect.move_ip(speed, 0)
            if self.rect.right > GAMEAREA.right:
                self.rect.right = GAMEAREA.right
        if keystate[pygame.K_UP] and self.rect.top > GAMEAREA.top:
            self.rect.move_ip(0, -1 * speed)
            if self.rect.top < GAMEAREA.top:
                self.rect.top = GAMEAREA.top
        if keystate[pygame.K_DOWN] and self.rect.bottom < GAMEAREA.bottom:
            self.rect.move_ip(0, speed)
            if self.rect.bottom > GAMEAREA.bottom:
                self.rect.bottom = GAMEAREA.bottom  
        
        self.collisionBox.rect.center = self.rect.center
        self.collisionBox.rotate()

                



# ----------------------Functions----------------------
def terminate():
    pygame.quit()
    sys.exit()

# ----------------------Pygame Initiate----------------------
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Curtain_Shooting_Game")
pygame.mouse.set_visible(False)

# ----------------------Load Image----------------------
img_dir = path.join(path.dirname(__file__), 'img')

background_row = pygame.image.load(path.join(img_dir, 'background2.png')).convert()
background = pygame.transform.scale(background_row, (WINDOWWIDTH, WINDOWHEIGHT))
background.set_colorkey(WHITE)
background_rect = background.get_rect()

palyerImg_row = pygame.image.load(path.join(img_dir, 'player1.png')).convert()
playerImg = pygame.transform.scale(palyerImg_row, (PLAYERWIDTH, PLAYERHEIGHT))
playerCollisionBoxImg_row = pygame.image.load(path.join(img_dir, 'playerCollisionBox.png')).convert()
playerCollisionBoxImg = pygame.transform.scale(playerCollisionBoxImg_row, (PLAYERCOLISIONBOXSIZE, PLAYERCOLISIONBOXSIZE))

enemyImg_row = pygame.image.load(path.join(img_dir, 'enemy1.png')).convert()
enemyImg = pygame.transform.scale(background_row, (ENEMYWIDTH, ENEMYHEIGHT))



# ----------------------Main----------------------

# Set Gamearea
GAMEAREA = pygame.Rect(40, 20, GAMEAREAWIDTH, GAMEAREAHEIGHT)
GAMEAREAFRAME = pygame.Rect(20, -10, 400, 400)

# Set parameter
running = True 
timer = 0
allSprites = pygame.sprite.Group()

# Set player, enemy, bullet
player = Player(name = "player", \
                lifes = 1, \
                image = playerImg, \
                collisionBoxImage = playerCollisionBoxImg_row, \
                playerBulletImage = None, \
                playerSpeed = (4, 2), \
                putbulletPattern = None, \
                shootBulletPattern = None)

allSprites.add(player)
allSprites.add(player.collisionBox)

# Game loop
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()


    allSprites.update()
    
    windowSurface.fill(BLACK)
    pygame.draw.rect(windowSurface, BLUE, GAMEAREA)
    

    
    allSprites.draw(windowSurface)

    windowSurface.blit(background, background_rect)
    
    pygame.display.update()

    mainClock.tick(FPS)
    timer += 1

# terminate()

