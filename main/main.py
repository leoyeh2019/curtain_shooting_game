import pygame, sys, random, math, time
from pygame.locals import *
from os import path
import parameter
import classes
import custom 
import function

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

BACKGROUND_WIDTH = 480
BACKGROUND_HEIGHT = 900

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_COLLISION_BOXSIZE = 10
PLAYER_BULLET_WIDTH = 5
PLAYER_BULLET_HEIGHT = 10

ENEMY_WIDTH = 30
ENEMY_HEIGHT = 30
ENEMY_BULLET_WIDTH = 5
ENEMY_BULLET_HEIGHT = 10

ITEM_WIDTH = 10
ITEM_HEIGHT = 10



# ----------------------Pygame Initiate----------------------
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Curtain_Shooting_Game")
pygame.mouse.set_visible(False)


# ----------------------Loading----------------------
img_dir = path.join(path.dirname(__file__), "img")
font_dir = path.join(path.dirname(__file__), "font")

background_raw = pygame.image.load(path.join(img_dir, 'background2.png')).convert()
background = pygame.transform.scale(background_raw, (WINDOWWIDTH, WINDOWHEIGHT))
background.set_colorkey(WHITE)
background_rect = background.get_rect()

gameareaBackgroundImg_raw = pygame.image.load(path.join(img_dir, 'background.png')).convert()
gameareaBackgroundImg = pygame.transform.scale(gameareaBackgroundImg_raw, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

playerImg_raw = pygame.image.load(path.join(img_dir, 'player1.png')).convert()
playerImg = pygame.transform.scale(playerImg_raw, (PLAYER_WIDTH, PLAYER_HEIGHT))
playerCollisionBoxImg_raw = pygame.image.load(path.join(img_dir, 'playerCollisionBox.png')).convert()
playerCollisionBoxImg = pygame.transform.scale(playerCollisionBoxImg_raw, (PLAYER_COLLISION_BOXSIZE, PLAYER_COLLISION_BOXSIZE))
playerCollisionBoxImg.set_colorkey(WHITE)

enemyImg_raw = pygame.image.load(path.join(img_dir, 'enemy1.png')).convert()
enemyImg = pygame.transform.scale(enemyImg_raw, (ENEMY_WIDTH, ENEMY_HEIGHT))

playerBulletImg_raw = pygame.image.load(path.join(img_dir, 'bullet1.png')).convert()
playerBulletImg = pygame.transform.scale(playerBulletImg_raw, (PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT))

playerBulletTrackingImg_raw = pygame.image.load(path.join(img_dir, 'bullet3.png')).convert()
playerBulletTrackingImg = pygame.transform.scale(playerBulletTrackingImg_raw, (PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT))

enemyBulletImg_raw = pygame.image.load(path.join(img_dir, 'bullet2.png')).convert()
enemyBulletImg = pygame.transform.scale(enemyBulletImg_raw, (ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT))
enemyBulletImg.set_colorkey(WHITE)

powerItemImg_raw = pygame.image.load(path.join(img_dir, 'power_item.png')).convert()
powerItemImg = pygame.transform.scale(powerItemImg_raw, (ITEM_WIDTH, ITEM_HEIGHT))

pointItemImg_raw = pygame.image.load(path.join(img_dir, 'point_item.png')).convert()
pointItemImg = pygame.transform.scale(pointItemImg_raw, (ITEM_WIDTH, ITEM_HEIGHT))           
                
 
# ----------------------Fonts----------------------

Helvetica_24 = pygame.font.Font(path.join(font_dir, "Helvetica.ttf"), 24)
Inconsolata_24 = pygame.font.Font(path.join(font_dir, "Inconsolata.otf"), 24)
        


# ----------------------Functions----------------------
def terminate():
    pygame.quit()
    sys.exit()




def generateItem(enemy, number, name, image):
    while True:
        check = True
        itemList = []
        for i in range(number):
            item = classes.Item(name = name, \
                                image = image, \
                                generatePosition = (enemy.rect.center[0] + random.randint(-enemy.rect.width * 1, enemy.rect.width *1), \
                                                    enemy.rect.center[1] + random.randint(-enemy.rect.height *1, enemy.rect.height *1)), \
                                gamearea = GAMEAREA)
            itemList.append(item)
        for i in range(len(itemList)):
            for j in range(len(itemList) - i - 1):
                if pygame.sprite.collide_rect(itemList[i], itemList[i + j + 1]):
                    check = False
        if check:
            break
    for i in range(len(itemList)):
        parameter.getAllSprites().add(itemList[i])
        parameter.getItemSprites().add(itemList[i])


def drawText(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# ----------------------Main----------------------

# Set Gamearea
GAMEAREA = pygame.Rect(40, 20, GAMEAREAWIDTH, GAMEAREAHEIGHT)


# Set parameter
running = True 
point = 0


# Set player, enemy, bullet
gameareaBackground1 = classes.Background(image = gameareaBackgroundImg, \
                                         topleft = function.raletivePosition(GAMEAREA.topleft, (0, -900)),\
                                         speed = 1)
gameareaBackground2 = classes.Background(image = gameareaBackgroundImg, \
                                         topleft = GAMEAREA.topleft,\
                                         speed = 1)
                                    
parameter.getBackgroundSprites().add(gameareaBackground1)
parameter.getBackgroundSprites().add(gameareaBackground2)

player = classes.Player(name = "player", \
                        lifes = 1, \
                        image = playerImg, \
                        collisionBoxImage = playerCollisionBoxImg, \
                        playerBulletImage = (playerBulletImg, playerBulletTrackingImg), \
                        playerSpeed = (4, 2), \
                        playerDamage = (4, 4), \
                        putBulletPattern = (custom.playerPutbulletPattern, custom.playerPutBulletPattern_tracking), \
                        shootBulletPattern = (custom.playerShootBulletPattern, custom.playerShootBulletPattern_tracking), \
                        gamearea = GAMEAREA)




def newEnemy_1():
    enemy = classes.Enemy(name = "enemy", \
                          Hp = 100, \
                          image = enemyImg, \
                          movePattern = custom.enemyMovePattern_1, \
                          enemyBulletImage = enemyBulletImg, \
                          putBulletPattern = custom.enemyPutBulletPattern_1, \
                          shootBulletPattern = custom.enemyshootBulletPattern_1, \
                          dropItem = (2, 2), \
                          gamearea = GAMEAREA)
    parameter.getAllSprites().add(enemy)
    parameter.getEnemySprites().add(enemy)



parameter.getAllSprites().add(player)
parameter.getAllSprites().add(player.collisionBox)



# Game loop
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                running = False
    # Generate Enemy
    if parameter.getTimer() >= 100 and parameter.getTimer() <= 1600:
        if (parameter.getTimer()  - 100) % 500 == 0:
            newEnemy_1()
            
    
    parameter.getBackgroundSprites().update()
    parameter.getAllSprites().update()

    # Collidision Destction
    # Player_Bullet v.s. Enemy
    for e in parameter.getEnemySprites():
        for pb in parameter.getPlayerBulletSprites():
            if pygame.sprite.collide_rect(e, pb):
                pb.kill()
                e.Hp -= pb.damage
                point += 100
        if e.Hp < 0:
            
            generateItem(e, e.dropItem[0], "power", powerItemImg)
            
            generateItem(e, e.dropItem[1], "point", pointItemImg)
            e.kill()
            point += 10000000
                    
                    
                    

    # Enemy_Bullet v.s. Player
    for eb in parameter.getEnemyBulletSprites():
        if pygame.sprite.collide_circle(eb, player):
            running = False

    # Point_Item v.s. Player
    for p in parameter.getItemSprites():
        if pygame.sprite.collide_circle(p, player):
            if p.name == "point":
                point += 100000
            if p.name == "power":
                player.power += 1
                if player.power > 48:
                    player.power = 48
            p.kill()
    
    windowSurface.fill(BLACK)
    pygame.draw.rect(windowSurface, BLUE, GAMEAREA)
    parameter.getBackgroundSprites().draw(windowSurface)

    """
    check if the bullet just generated
    use 'blit' to draw sprites one by one
    """
    for i in parameter.getAllSprites():
        try:
            if parameter.getTimer() - i.generateTime > 1:
                windowSurface.blit(i.image, i.rect)

        except:
            windowSurface.blit(i.image, i.rect)

  

    windowSurface.blit(background, background_rect)

    drawText("Point  {0:0>12}".format(point), Inconsolata_24, BLACK, windowSurface, 540, 40)
    drawText("Power  {0:0>3}".format(player.power), Inconsolata_24, BLACK, windowSurface, 540, 80)

    pygame.display.update()

    mainClock.tick(FPS)
    parameter.accTimer()
    


pygame.time.delay(1000)
terminate()

