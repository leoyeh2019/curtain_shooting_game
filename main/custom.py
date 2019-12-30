import pygame, sys, random, math
from classes import *
import parameter


# Set player, enemy, bullet
def playerPutbulletPattern(time, power):
    if power in range(0, 24):
        return 0, -30
    if power in range(24, 49):
        return [(-15, -30), (0, -30), (15, -30)]
    
def playerShootBulletPattern(time):
    return 0, -10


def playerPutBulletPattern_tracking(time, power):
    if power in range(8, 49):
        return [(-20, 0), (20, 0)]
def playerShootBulletPattern_tracking(time):
    def findMostCloseEnemy(playerCenter):
        # global parameter.getEnemySprites()
        for i in parameter.getEnemySprites():
            check = 0
            for j in parameter.getEnemySprites():
                if i == j:
                    pass 
                else:
                    distanceI = math.sqrt((i.rect.center[0] - playerCenter[0]) ** 2 + (i.rect.center[0] - playerCenter[0]) **2)
                    distanceJ = math.sqrt((j.rect.center[0] - playerCenter[0]) ** 2 + (i.rect.center[0] - playerCenter[0]) **2)
                    if distanceI < distanceJ:
                        check +=1
            if check == len(parameter.getEnemySprites().sprites()) - 1:
                return i.rect.center

    return {"speed" : 10, "track" : findMostCloseEnemy}

            



def enemyMovePattern(time):
    if time < 0:
        return 0, 0
    elif 0< time < 120:
        return 2, 1
    else:
        return 0, 0

def enemyPutBulletPattern(time):
    r = 50
    θ = (time ** 2) / 120
    ways = 8
    Δθ = 360 / ways 
    positionList = []
    for i in range(ways):
        θ_i = math.radians((θ + (i * Δθ)) % 360)
        positionList.append((r * math.cos(θ_i), r * math.sin(θ_i)))

    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 120, \
            "intermediateTime" : 2}

    

def enemyshootBulletPattern(putPattern):
    speed = 5
    vectorLength = pygame.math.Vector2(putPattern[0], putPattern[1]).length()
    dx = speed / vectorLength * putPattern[0]
    dy = speed / vectorLength * putPattern[1]
    return {"f(x)" : lambda time : (dx * time, dy * time), \
            "f'(x)" : lambda time : (dx, dy)}
    
    





