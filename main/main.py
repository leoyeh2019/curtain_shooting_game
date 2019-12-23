import pygame, sys, random, math 
from pygame.locals import *
from os import path


# ----------------------Constants----------------------
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
PLAYERBULLETWIDTH = 5
PLAYERBULLETHEIGHT = 10

ENEMYWIDTH = 20
ENEMYHEIGHT = 20


# ----------------------Pygame Initiate----------------------
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Curtain_Shooting_Game")
pygame.mouse.set_visible(False)

# ----------------------Load Image----------------------
img_dir = path.join(path.dirname(__file__), 'img')

background_raw = pygame.image.load(path.join(img_dir, 'background2.png')).convert()
background = pygame.transform.scale(background_raw, (WINDOWWIDTH, WINDOWHEIGHT))
background.set_colorkey(WHITE)
background_rect = background.get_rect()

playerImg_raw = pygame.image.load(path.join(img_dir, 'player1.png')).convert()
playerImg = pygame.transform.scale(playerImg_raw, (PLAYERWIDTH, PLAYERHEIGHT))
playerCollisionBoxImg_raw = pygame.image.load(path.join(img_dir, 'playerCollisionBox.png')).convert()
playerCollisionBoxImg = pygame.transform.scale(playerCollisionBoxImg_raw, (PLAYERCOLISIONBOXSIZE, PLAYERCOLISIONBOXSIZE))
playerCollisionBoxImg.set_colorkey(WHITE)

enemyImg_raw = pygame.image.load(path.join(img_dir, 'enemy1.png')).convert()
enemyImg = pygame.transform.scale(background_raw, (ENEMYWIDTH, ENEMYHEIGHT))

playerBulletImg_raw = pygame.image.load(path.join(img_dir, 'bullet1.png')).convert()
playerBulletImg = pygame.transform.scale(playerBulletImg_raw, (PLAYERBULLETWIDTH, PLAYERBULLETHEIGHT))

enemyBulletImg_raw = pygame.image.load(path.join(img_dir, 'bullet2.png')).convert()

# ----------------------Classes----------------------
class playerCollisionBox(pygame.sprite.Sprite):
    def __init__(self, collisionBoxImage, playerRect):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = collisionBoxImage
        self.image = self.image_origin.copy()
        self.rect = self.image.get_rect(center = playerRect.center)
        self.axis = 0
        self.rotateSpeed = 5 
        self.lastUpdate = pygame.time.get_ticks()
    def rotate(self):
        now = pygame.time.get_ticks() 
        if now - self.lastUpdate > 100: 
            self.lastUpdate = now
            self.axis = (self.axis + self.rotateSpeed) % 360
            newImage = pygame.transform.rotate(self.image_origin, self.axis)
            oldCenter = self.rect.center
            self.image = newImage
            self.rect = self.image.get_rect(center = oldCenter)

        

      
        

class Player(pygame.sprite.Sprite):
    def __init__(self, name, lifes, image, collisionBoxImage, playerBulletImage, playerSpeed, playerDamage, putBulletPattern, shootBulletPattern):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.lifes = lifes
        self.image = image
        self.collisionBoxImage = collisionBoxImage
        self.playerBulletImage = playerBulletImage
        self.playerDamage = playerDamage
        self.playerFastSpeed = playerSpeed[0]
        self.playerSlowSpeed = playerSpeed[1]
        self.putBulletPattern = putBulletPattern
        self.shootBulletPattern = shootBulletPattern

        self.rect = self.image.get_rect(center = (GAMEAREA.centerx, GAMEAREA.bottom - 50))
        

        self.collisionBox = playerCollisionBox(collisionBoxImage = self.collisionBoxImage, playerRect = self.rect)

        self.radius = int(self.collisionBox.rect.width / 2)

        

        self.lastShootingTime = pygame.time.get_ticks()
        

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
        if keystate[pygame.K_z]:
            self.shoot()  
        
        self.collisionBox.rect.center = self.rect.center
        # self.collisionBox.rotate()
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.lastShootingTime > 100:
            playerBullet = Bullet(name = "playerBullet", \
                                  image = self.playerBulletImage, \
                                  bulletRadius = 1, \
                                  bulletDamage = self.playerDamage, \
                                  putBulletPattern = (self.putBulletPattern(now)[0] + self.rect.center[0], self.putBulletPattern(now)[1] + self.rect.center[1]), \
                                  shootBulletPattern = self.shootBulletPattern)
            self.lastShootingTime = now
            allSprites.add(playerBullet)
            playerBulletSprites.add(playerBullet)
            


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, Hp, image, movePattern, enemyBulletImage, putBulletPattern, shootBulletPattern):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.Hp = Hp
        self.image = image
        self.movePattern = movePattern
        self.enemyBulletImage = enemyBulletImage
        self.putBulletPattern = putBulletPattern
        self.shootBulletPattern = shootBulletPattern

        self.rect = self.image.get_rect(center = (movePattern(-1)[0] + GAMEAREA.left, movePattern(-1)[1] + GAMEAREA.top))
        self.radius = int((self.rect.width / 2) * 0.5)

        self.generateTime = pygame.time.get_ticks()


    def update(self):
        now = pygame.time.get_ticks()
        self.rect.move_ip(self.movePattern(now - self.generateTime)[0], self.movePattern(now - self.generateTime)[1])
        if not self.rect.colliderect(GAMEAREA):
            self.kill()
            


        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = image
        self.image.set_colorkey(WHITE)
        self.radius = bulletRadius
        self.damage = bulletDamage
        self.shootBulletPattern = shootBulletPattern

        self.rect = self.image.get_rect(center = putBulletPattern)

        self.generateTime = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        self.rect.move_ip(self.shootBulletPattern(now - self.generateTime)) 

        if self.rect.bottom < 0:
            self.kill()
            
                

        
        
        


# ----------------------Functions----------------------
def terminate():
    pygame.quit()
    sys.exit()






# ----------------------Main----------------------

# Set Gamearea
GAMEAREA = pygame.Rect(40, 20, GAMEAREAWIDTH, GAMEAREAHEIGHT)
GAMEAREAFRAME = pygame.Rect(20, -10, 400, 400)

# Set parameter
running = True 
timer = 0
allSprites = pygame.sprite.Group()
playerBulletSprites =  pygame.sprite.Group()
enemySprites = pygame.sprite.Group()


# Set player, enemy, bullet
def playerPutbulletPattern(time):
    return 0, -30
def playerShootBulletPattern(time):
    return 0, -10
player = Player(name = "player", \
                lifes = 1, \
                image = playerImg, \
                collisionBoxImage = playerCollisionBoxImg, \
                playerBulletImage = playerBulletImg, \
                playerSpeed = (4, 2), \
                playerDamage = 10, \
                putBulletPattern = playerPutbulletPattern, \
                shootBulletPattern = playerShootBulletPattern)



def enemyMovePattern(time):
    if time < 0:
        return 0, 0
    elif 0< time < 3000:
        return 2, 1
    else:
        return -1, 1

enemy = Enemy(name = "enemy", \
              Hp = 100, \
              image = enemyImg, \
              movePattern = enemyMovePattern, \
              enemyBulletImage = None, \
              putBulletPattern = None, \
              shootBulletPattern = None)



allSprites.add(player)
allSprites.add(player.collisionBox)
allSprites.add(enemy)
enemySprites.add(enemy)
# Game loop
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                running = False
            
    
    
    allSprites.update()

    
    for e in enemySprites:
        for pb in playerBulletSprites:
            if pygame.sprite.collide_rect(e, pb):
                pb.kill()
                e.Hp -= pb.damage
                if e.Hp < 0:
                    e.kill()
                    
    
    windowSurface.fill(BLACK)
    pygame.draw.rect(windowSurface, BLUE, GAMEAREA)
    allSprites.draw(windowSurface)

    windowSurface.blit(background, background_rect)
    
    pygame.display.update()

    mainClock.tick(FPS)
    timer += 1

terminate()

