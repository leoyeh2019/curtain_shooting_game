import pygame, sys, random, math
from classes import *
import parameter
import function


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
    
    return (-10/math.sqrt(2), -10/math.sqrt(2)), (10/math.sqrt(2), -10/math.sqrt(2))



            



def enemyMovePattern(time):
    if time < 0:
        return 0, 0
    elif 0< time < 120:
        return 2, 2
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
    
    





