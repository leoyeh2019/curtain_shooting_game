import pygame

GAMEAREAWIDTH = 768
GAMEAREAHEIGHT = 896
GAMEAREA = pygame.Rect(64, 32, GAMEAREAWIDTH, GAMEAREAHEIGHT)

def getGamearea():
    global GAMEAREA
    return GAMEAREA

BULLETGAMEAREA = pygame.Rect(0, 0, GAMEAREAWIDTH * 2, GAMEAREAHEIGHT * 1.5)
BULLETGAMEAREA.center = GAMEAREA.center

def getBulletGamearea():
    global BULLETGAMEAREA
    return BULLETGAMEAREA


timer = 0

def accTimer():
    global timer
    timer += 1

def getTimer():
    global timer
    return timer


point = 0

def getPoint():
    global point
    return point

def addPoint(add):
    global point
    point += add

backgroundSprites = pygame.sprite.Group()

def getBackgroundSprites():
    global backgroundSprites
    return backgroundSprites


allSprites = pygame.sprite.Group()

def getAllSprites():
    global allSprites
    return allSprites




playerBulletSprites =  pygame.sprite.Group()

def getPlayerBulletSprites():
    global playerBulletSprites
    return playerBulletSprites


enemySprites = pygame.sprite.Group()

def getEnemySprites():
    global enemySprites
    return enemySprites

bossSprites = pygame.sprite.Group()

def getBossSprites():
    global bossSprites
    return bossSprites

enemyBulletSprites = pygame.sprite.Group()

def getEnemyBulletSprites():
    global enemyBulletSprites
    return enemyBulletSprites

itemSprites = pygame.sprite.Group()

def getItemSprites():
    global itemSprites
    return itemSprites


playerPosition = [0, 0]

def getPlayerPosition():
    global playerPosition
    return playerPosition

def returnPlayerPosition(center):
    global playerPosition
    playerPosition[0] = center[0]
    playerPosition[1] = center[1]