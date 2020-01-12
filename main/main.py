import pygame, sys, random, math, time
from pygame.locals import *
from os import path
import parameter
import classes
import custom 
import function


# ----------------------Constants----------------------
WINDOWWIDTH = 1280
WINDOWHEIGHT = 960


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 255, 255)

FPS = 60

BACKGROUND_WIDTH = 768
BACKGROUND_HEIGHT = 1440

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLLISION_BOXSIZE = 15
PLAYER_BULLET_WIDTH = 10
PLAYER_BULLET_HEIGHT = 20

ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
ENEMY_BULLET_WIDTH = 10
ENEMY_BULLET_HEIGHT = 20

BOSS_WIDTH = 100
BOSS_HEIGHT = 100

BOSS_BULLET_1_WIDTH = 51
BOSS_BULLET_1_HEIGHT = 66

ITEM_WIDTH = 20
ITEM_HEIGHT = 20



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
playerBulletImg.set_alpha(192) # Transparent

playerBulletTrackingImg_raw = pygame.image.load(path.join(img_dir, 'bullet3.png')).convert()
playerBulletTrackingImg = pygame.transform.scale(playerBulletTrackingImg_raw, (PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT))
playerBulletTrackingImg.set_alpha(192) # Transparent

enemyBulletImg_raw = pygame.image.load(path.join(img_dir, 'bullet2.png')).convert()
enemyBulletImg = pygame.transform.scale(enemyBulletImg_raw, (ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT))
enemyBulletImg.set_colorkey(WHITE)

powerItemImg_raw = pygame.image.load(path.join(img_dir, 'power_item.png')).convert()
powerItemImg = pygame.transform.scale(powerItemImg_raw, (ITEM_WIDTH, ITEM_HEIGHT))

pointItemImg_raw = pygame.image.load(path.join(img_dir, 'point_item.png')).convert()
pointItemImg = pygame.transform.scale(pointItemImg_raw, (ITEM_WIDTH, ITEM_HEIGHT))           

bossImg_raw = pygame.image.load(path.join(img_dir, 'boss.png')).convert()
bossImg = pygame.transform.scale(bossImg_raw, (BOSS_WIDTH, BOSS_HEIGHT))
bossImg.set_colorkey(WHITE)

bossBullet_1_Img_raw = pygame.image.load(path.join(img_dir, 'boss_bullet_1.png')).convert()
bossBullet_1_Img = pygame.transform.scale(bossBullet_1_Img_raw, (BOSS_BULLET_1_WIDTH, BOSS_BULLET_1_HEIGHT))
bossBullet_1_Img.set_colorkey(WHITE)
 
# ----------------------Fonts----------------------

Helvetica_24 = pygame.font.Font(path.join(font_dir, "Helvetica.ttf"), 24)
Inconsolata_24 = pygame.font.Font(path.join(font_dir, "Inconsolata.otf"), 24)
Inconsolata_32 = pygame.font.Font(path.join(font_dir, "Inconsolata.otf"), 32)


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
                                                    enemy.rect.center[1] + random.randint(-enemy.rect.height *1, enemy.rect.height *1)))
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




# ----------------------Main----------------------

# Set Gamearea
    # Set in parameter.py


# Set parameter
running = True 
stageInitiated = True


# Set player, enemy, bullet
gameareaBackground1 = classes.Background(image = gameareaBackgroundImg, \
                                         topleft = function.raletivePosition(parameter.getGamearea().topleft, (0, -1440)),\
                                         speed = 1)
gameareaBackground2 = classes.Background(image = gameareaBackgroundImg, \
                                         topleft = parameter.getGamearea().topleft,\
                                         speed = 1)
                                    
parameter.getBackgroundSprites().add(gameareaBackground1)
parameter.getBackgroundSprites().add(gameareaBackground2)

player = classes.Player(name = "player", \
                        lifes = 100, \
                        image = playerImg, \
                        collisionBoxImage = playerCollisionBoxImg, \
                        playerBulletImage = (playerBulletImg, playerBulletTrackingImg), \
                        playerSpeed = (7, 4), \
                        playerDamage = (6, 4), \
                        putBulletPattern = (custom.playerPutbulletPattern, custom.playerPutBulletPattern_tracking), \
                        shootBulletPattern = (custom.playerShootBulletPattern, custom.playerShootBulletPattern_tracking))




def newEnemy_1():
    enemy = classes.Enemy(name = "enemy", \
                          Hp = 150, \
                          image = enemyImg, \
                          movePattern = custom.enemyMovePattern_1, \
                          enemyBulletImage = [enemyBulletImg], \
                          putBulletPattern = [custom.enemyPutBulletPattern_1], \
                          shootBulletPattern = [custom.enemyshootBulletPattern_1], \
                          dropItem = (2, 2))
    parameter.getAllSprites().add(enemy)
    parameter.getEnemySprites().add(enemy)

def newEnemy_2():
    enemy = classes.Enemy(name = "enemy", \
                          Hp = 30, \
                          image = enemyImg, \
                          movePattern = custom.enemyMovePattern_2, \
                          enemyBulletImage = [enemyBulletImg], \
                          putBulletPattern = [custom.enemyPutBulletPattern_2], \
                          shootBulletPattern = [custom.enemyshootBulletPattern_2], \
                          dropItem = (2, 4))
    parameter.getAllSprites().add(enemy)
    parameter.getEnemySprites().add(enemy)
def newEnemy_3():
    enemy = classes.Enemy(name = "enemy", \
                          Hp = 30, \
                          image = enemyImg, \
                          movePattern = custom.enemyMovePattern_3, \
                          enemyBulletImage = [enemyBulletImg], \
                          putBulletPattern = [custom.enemyPutBulletPattern_3], \
                          shootBulletPattern = [custom.enemyshootBulletPattern_3], \
                          dropItem = (1, 4))
    parameter.getAllSprites().add(enemy)
    parameter.getEnemySprites().add(enemy)

parameter.getAllSprites().add(player)
parameter.getAllSprites().add(player.collisionBox)

def newEnemy_4():
    enemy = classes.Enemy(name = "enemy", \
                          Hp = 1000, \
                          image = enemyImg, \
                          movePattern = custom.enemyMovePattern_4, \
                          enemyBulletImage = [enemyBulletImg], \
                          putBulletPattern = [custom.enemyPutBulletPattern_4], \
                          shootBulletPattern = [custom.enemyshootBulletPattern_4], \
                          dropItem = (0, 6))
    parameter.getAllSprites().add(enemy)
    parameter.getEnemySprites().add(enemy)

parameter.getAllSprites().add(player)
parameter.getAllSprites().add(player.collisionBox)


stageList = []
boss_stage_1 = classes.BossStage(order = 1, \
                                 time = 60 * 60, \
                                 ifSpellCard = False, \
                                 bonus = 0, \
                                 Hp = 3000, \
                                 bossImage = bossImg, \
                                 bossMovement = custom.bossMovePattern_1, \
                                 bossBulletImage = [bossBullet_1_Img], \
                                 bossPutBulletPattern = [custom.bossPutBulletPattern_1], \
                                 BossShootBulletPattern = [custom.bossShootBulletPattern_1], \
                                 dropItem = (0, 0), \
                                 background = None)
stageList.append(boss_stage_1)
boss_stage_2 = classes.BossStage(order = 2, \
                                 time = 60 * 60, \
                                 ifSpellCard = True, \
                                 bonus = 100000000, \
                                 Hp = 4500, \
                                 bossImage = bossImg, \
                                 bossMovement = custom.bossMovePattern_2, \
                                 bossBulletImage = [enemyBulletImg, enemyBulletImg, enemyBulletImg, enemyBulletImg], \
                                 bossPutBulletPattern = [custom.bossPutBulletPattern_2_1, custom.bossPutBulletPattern_2_2, custom.bossPutBulletPattern_2_3, custom.bossPutBulletPattern_2_4], \
                                 BossShootBulletPattern = [custom.bossShootBulletPattern_2_1, custom.bossShootBulletPattern_2_1, custom.bossShootBulletPattern_2_3, custom.bossShootBulletPattern_2_3], \
                                 dropItem = (8, 16), \
                                 background = pygame.transform.scale(bossBullet_1_Img, (510, 660)))
stageList.append(boss_stage_2)
boss_stage_3 = classes.BossStage(order = 3, \
                                 time = 60 * 60, \
                                 ifSpellCard = False, \
                                 bonus = 0, \
                                 Hp = 3000, \
                                 bossImage = bossImg, \
                                 bossMovement = custom.bossMovePattern_3, \
                                 bossBulletImage = [bossBullet_1_Img], \
                                 bossPutBulletPattern = [custom.bossPutBulletPattern_3], \
                                 BossShootBulletPattern = [custom.bossShootBulletPattern_3], \
                                 dropItem = (0, 0), \
                                 background = None)
stageList.append(boss_stage_3)

# Game loop
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                running = False
    # Generate Enemy
    # if parameter.getTimer() >= 100 and parameter.getTimer() <= 1600:
    #     if (parameter.getTimer()  - 100) % 500 == 0:
    #         newEnemy_1()
    
    # if parameter.getTimer() >= 2200 and parameter.getTimer() <= 3200:
    #     if (parameter.getTimer()  - 2200) % 50 == 0:
    #         newEnemy_2()
    #         newEnemy_3()
    
    # if parameter.getTimer() == 3500:
    #     newEnemy_4()
    
    if parameter.getTimer() >= 50 and stageInitiated:
        stageList[0].isAlive = True
        stageInitiated = False
        
    for i in range(len(stageList)):
        if stageList[i].isDead:
            stageList[i+1].isAlive = True
            stageList[i].isDead = False
        stageList[i].update(player)

    
    
    if parameter.getTimer() > 50 and not bool(parameter.getEnemySprites()):
        for i in parameter.getBackgroundSprites():
            i.speed = 5
    else:
        for i in parameter.getBackgroundSprites():
            i.speed = 2
    
    
    parameter.getBackgroundSprites().update()
    parameter.getAllSprites().update()

    # Collidision Destction

    # Player_Bullet v.s. Enemy
    for e in parameter.getEnemySprites():
        for pb in parameter.getPlayerBulletSprites():
            if pygame.sprite.collide_rect(e, pb):
                pb.kill()
                e.Hp -= pb.damage
                parameter.addPoint(100)
        if e.Hp < 0:
            
            generateItem(e, e.dropItem[0], "power", powerItemImg)
            
            generateItem(e, e.dropItem[1], "point", pointItemImg)
            e.kill()
            parameter.addPoint(10000)
                    
                    
                    

    # Enemy_Bullet v.s. Player
    for eb in parameter.getEnemyBulletSprites():
        if pygame.sprite.collide_circle(eb, player):
            player.hide()
            player.lifes -= 1

    # Point_Item v.s. Player
    for p in parameter.getItemSprites():
        if pygame.sprite.collide_circle(p, player):
            if p.name == "point":
                parameter.addPoint(100000)
            if p.name == "power":
                player.power += 1
                if player.power > 48:
                    player.power = 48
            p.kill()
    
    # Check if player die
    if player.lifes == 0:
        running = False

    # Draw
    windowSurface.fill(BLACK)
    pygame.draw.rect(windowSurface, WHITE, parameter.getGamearea())
    parameter.getBackgroundSprites().draw(windowSurface)
    for i in stageList:
        i.drawBackground(windowSurface)
    """
    check if the bullet just generated
    use 'blit' to draw sprites one by one
    """
    for i in parameter.getAllSprites():
        if i in parameter.getEnemyBulletSprites() or i in parameter.getPlayerBulletSprites():
            if parameter.getTimer() - i.generateTime > 1:
                windowSurface.blit(i.image, i.rect)

        else:
            windowSurface.blit(i.image, i.rect)

  

    windowSurface.blit(background, background_rect)

    for i in stageList:
        i.drawInfo(windowSurface, Inconsolata_32)

    function.drawText("Point  {0:0>12}".format(parameter.getPoint()), Inconsolata_32, BLACK, windowSurface, 864, 64)
    function.drawText("Lifes  {0:0>3}".format(player.lifes), Inconsolata_32, BLACK, windowSurface, 864, 128)
    function.drawText("Power  {0:0>3}".format(player.power), Inconsolata_32, BLACK, windowSurface, 864, 192)
    function.drawText("Timer  {0:0>3}".format(parameter.getTimer()), Inconsolata_32, BLACK, windowSurface, 864, 256)

    pygame.display.update()

    # if parameter.getTimer() % 10 == 0:
    #     print(player.rect.center)
    mainClock.tick(FPS)
    parameter.accTimer()
    


pygame.time.delay(1000)
terminate()

