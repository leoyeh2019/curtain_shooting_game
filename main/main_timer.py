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

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_COLLISION_BOXSIZE = 10
PLAYER_BULLET_WIDTH = 5
PLAYER_BULLET_HEIGHT = 10

ENEMY_WIDTH = 20
ENEMY_HEIGHT = 20
ENEMY_BULLET_WIDTH = 5
ENEMY_BULLET_HEIGHT = 10

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
playerImg = pygame.transform.scale(playerImg_raw, (PLAYER_WIDTH, PLAYER_HEIGHT))
playerCollisionBoxImg_raw = pygame.image.load(path.join(img_dir, 'playerCollisionBox.png')).convert()
playerCollisionBoxImg = pygame.transform.scale(playerCollisionBoxImg_raw, (PLAYER_COLLISION_BOXSIZE, PLAYER_COLLISION_BOXSIZE))
playerCollisionBoxImg.set_colorkey(WHITE)

enemyImg_raw = pygame.image.load(path.join(img_dir, 'enemy1.png')).convert()
enemyImg = pygame.transform.scale(background_raw, (ENEMY_WIDTH, ENEMY_HEIGHT))

playerBulletImg_raw = pygame.image.load(path.join(img_dir, 'bullet1.png')).convert()
playerBulletImg = pygame.transform.scale(playerBulletImg_raw, (PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT))

enemyBulletImg_raw = pygame.image.load(path.join(img_dir, 'bullet2.png')).convert()
enemyBulletImg = pygame.transform.scale(enemyBulletImg_raw, (ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT))
enemyBulletImg.set_colorkey(WHITE)

# ----------------------Classes----------------------
class playerCollisionBox(pygame.sprite.Sprite):
    def __init__(self, collisionBoxImage, playerRect):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = collisionBoxImage
        self.image = self.image_origin.copy()
        self.rect = self.image.get_rect(center = playerRect.center)
        self.axis = 0
        self.rotateSpeed = 5 
        self.lastUpdate = timer
    def rotate(self):
        now = timer
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

        self.lastShootingTime = timer
        

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
        now = timer
        if now - self.lastShootingTime > 6:
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

        self.generateTime = timer
        self.lastShootingTime = timer


    def update(self):
        now = timer
        self.rect.move_ip(self.movePattern(now - self.generateTime))
        if not self.rect.colliderect(GAMEAREA):
            self.kill()

        self.shoot()

    def shoot(self):
        now =  timer
        if now - self.generateTime > self.putBulletPattern(now - self.generateTime)["delateTime"]:
            if now - self.lastShootingTime > self.putBulletPattern(now - self.generateTime)["intermediateTime"]:
                for i in range(self.putBulletPattern(now)["numbers"]):
                    enemyBullet = Bullet(name = "enemyBullet", \
                                         image = self.enemyBulletImage, \
                                         bulletRadius = 1, \
                                         bulletDamage = None, \
                                         putBulletPattern = (self.putBulletPattern(now)["position"][i][0] + self.rect.center[0], \
                                                             self.putBulletPattern(now)["position"][i][1] + self.rect.center[1]), \
                                         shootBulletPattern = self.shootBulletPattern(i))
                    allSprites.add(enemyBullet)
                    enemyBulletSprites.add(enemyBullet)
                self.lastShootingTime = now
                




        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image_origin = image
        self.image = self.image_origin.copy()
        self.image.set_colorkey(WHITE)
        self.radius = bulletRadius
        self.damage = bulletDamage
        self.shootBulletPattern = shootBulletPattern

        self.rect = self.image.get_rect(center = putBulletPattern)

        self.generateTime = timer
        

    def update(self):
        now = timer
        self.rect.move_ip(self.shootBulletPattern(now - self.generateTime)) 

        self.rotate(now)

        if not self.rect.colliderect(GAMEAREA):
            self.kill()

    def rotate(self, now):
        x = self.shootBulletPattern(now - self.generateTime)[0]
        y = self.shootBulletPattern(now - self.generateTime)[1]
        v = pygame.math.Vector2(x, y)
        axis = 90 - v.as_polar()[1]
        newImage = pygame.transform.rotate(self.image_origin, axis)
        oldCenter = self.rect.center
        self.image = newImage
        self.rect = self.image.get_rect(center = oldCenter)

    
                

        
        
        


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
enemyBulletSprites = pygame.sprite.Group()

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
    elif 0< time < 60:
        return 4, 2
    else:
        return 0, 0

def enemyPutBulletPattern(time):
    a = b = c = d = e = f = g = h = random.randint(-100, 100)
    return {"numbers" : 4, \
            "position" : ((a, b), (c, d), (e, f), (g, h)), \
            "delateTime" : 60, \
            "intermediateTime" : 3}

    

def enemyshootBulletPattern(number):
    a = b = random.randint(1, 5)
    c = d = random.randint(-5, -1)
    if number == 0:
        return lambda time : (0, a)
    if number == 1:
        return lambda time : (b, 0)
    if number == 2:
        return lambda time : (0, c)
    if number == 3:
        return lambda time : (d, 0)


enemy = Enemy(name = "enemy", \
              Hp = 1000, \
              image = enemyImg, \
              movePattern = enemyMovePattern, \
              enemyBulletImage = enemyBulletImg, \
              putBulletPattern = enemyPutBulletPattern, \
              shootBulletPattern = enemyshootBulletPattern)



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

    for eb in enemyBulletSprites:
        if pygame.sprite.collide_circle(eb, player):
            running = False        
    
    windowSurface.fill(BLACK)
    pygame.draw.rect(windowSurface, BLUE, GAMEAREA)
    allSprites.draw(windowSurface)

    windowSurface.blit(background, background_rect)
    
    pygame.display.update()

    mainClock.tick(FPS)
    timer += 1

pygame.time.delay(1000)
terminate()

