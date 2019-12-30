import pygame, sys, random, math, time
from pygame.locals import *
from os import path
import parameter
import classes
import custom 

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



# Set player, enemy, bullet

player = classes.Player(name = "player", \
                        lifes = 1, \
                        image = playerImg, \
                        collisionBoxImage = playerCollisionBoxImg, \
                        playerBulletImage = playerBulletImg, \
                        playerSpeed = (4, 2), \
                        playerDamage = 10, \
                        putBulletPattern = custom.playerPutbulletPattern, \
                        shootBulletPattern = custom.playerShootBulletPattern, \
                        gamearea = GAMEAREA)





enemy = classes.Enemy(name = "enemy", \
                      Hp = 1000, \
                      image = enemyImg, \
                      movePattern = custom.enemyMovePattern, \
                      enemyBulletImage = enemyBulletImg, \
                      putBulletPattern = custom.enemyPutBulletPattern, \
                      shootBulletPattern = custom.enemyshootBulletPattern, \
                      gamearea = GAMEAREA)



parameter.getAllSprites().add(player)
parameter.getAllSprites().add(player.collisionBox)
parameter.getAllSprites().add(enemy)
parameter.getEnemySprites().add(enemy)


# Game loop
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                running = False
            
    
    
    parameter.getAllSprites().update()

    
    for e in parameter.getEnemySprites():
        for pb in parameter.getPlayerBulletSprites():
            if pygame.sprite.collide_rect(e, pb):
                pb.kill()
                e.Hp -= pb.damage
                if e.Hp < 0:
                    e.kill()

    # for eb in parameter.getEnemyBulletSprites():
    #     if pygame.sprite.collide_circle(eb, player):
    #         running = False


    
    windowSurface.fill(BLACK)
    pygame.draw.rect(windowSurface, BLUE, GAMEAREA)
    parameter.getAllSprites().draw(windowSurface)

    windowSurface.blit(background, background_rect)
    
    pygame.display.update()

    mainClock.tick(FPS)
    parameter.accTimer()


pygame.time.delay(1000)
terminate()

