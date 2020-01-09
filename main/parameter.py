import pygame



timer = 0

def accTimer():
    global timer
    timer += 1

def getTimer():
    global timer
    return timer

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


enemyBulletSprites = pygame.sprite.Group()

def getEnemyBulletSprites():
    global enemyBulletSprites
    return enemyBulletSprites

itemSprites = pygame.sprite.Group()

def getItemSprites():
    global itemSprites
    return itemSprites