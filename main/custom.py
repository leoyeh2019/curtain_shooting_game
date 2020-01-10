import pygame, sys, random, math
from classes import *
import parameter
import function


# Set player, enemy, bullet
def playerPutbulletPattern(time, power):
    if power in range(0, 24):
        return 0, -45
    if power in range(24, 49):
        return [(-25, -45), (0, -45), (25, -45)]
    
def playerShootBulletPattern(time):
    return 0, -15


def playerPutBulletPattern_tracking(time, power):
    if power in range(8, 49):
        return [(-30, 0), (30, 0)]

def playerShootBulletPattern_tracking(time):
    speed = 15
    return (-speed / math.sqrt(2), -speed / math.sqrt(2)), (speed / math.sqrt(2), -speed / math.sqrt(2))



            



# def enemyMovePattern(time):
#     if time < 0:
#         return 0, 0
#     elif 0< time < 120:
#         return 2, 2
#     else:
#         return 0, 0

# def enemyPutBulletPattern(time):
#     r = 50
#     θ = (time ** 2) / 120
#     ways = 4
#     Δθ = 360 / ways 
#     positionList = []
#     for i in range(ways):
#         θ_i = math.radians((θ + (i * Δθ)) % 360)
#         positionList.append((r * math.cos(θ_i), r * math.sin(θ_i)))

#     return {"numbers" : ways, \
#             "position" : positionList, \
#             "delateTime" : 120, \
#             "intermediateTime" : 3}

 

# def enemyshootBulletPattern(putPattern):
#     speed = 5
#     vectorLength = pygame.math.Vector2(putPattern[0], putPattern[1]).length()
#     dx = speed / vectorLength * putPattern[0]
#     dy = speed / vectorLength * putPattern[1]
    
#     return {"f(x)" : lambda time : (dx * time, dy * time), \
#             "f'(x)" : lambda time : (dx, dy)}
    
    
def enemyMovePattern_1(time):
    if time < 0:
        return 384, -10
    elif time < 50:
        return 0, 4
    elif time < 400:
        return 0, 0
    else:
        return 0, -2



def enemyPutBulletPattern_1(time):
    ways = 1
    positionList = [(random.randint(-30, 30), random.randint(20, 40))]
    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 0, \
            "intermediateTime" : 3}



def enemyshootBulletPattern_1(putPattern):
    speed = 8
    vectorLength = pygame.math.Vector2(putPattern[0], putPattern[1]).length()
    dx = speed / vectorLength * putPattern[0]
    dy = speed / vectorLength * putPattern[1]
    
    return {"f(x)" : lambda time : (dx * time, dy * time), \
            "f'(x)" : lambda time : (dx, dy)}


def enemyMovePattern_2(time):
    if time < 0:
        return 0, 10
    
    else:
        return 3, 1



def enemyPutBulletPattern_2(time):
    ways = 3
    positionList = [(-30, 30), (0, 30), (30, 30)]
    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 0, \
            "intermediateTime" : 15}



def enemyshootBulletPattern_2(putPattern):
    speed = 5
    vectorLength = pygame.math.Vector2(putPattern[0], putPattern[1]).length()
    dx = speed / vectorLength * putPattern[0]
    dy = speed / vectorLength * putPattern[1]

    
    return {"f(x)" : lambda time : (dx * time, dy * time), \
            "f'(x)" : lambda time : (dx, dy)}



def enemyMovePattern_3(time):
    if time < 0:
        return 768, 10
    
    else:
        return -3, 1



def enemyPutBulletPattern_3(time):
    ways = 3
    positionList = [(-10, 30), (0, 30), (10, 30)]
    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 0, \
            "intermediateTime" : 15}



def enemyshootBulletPattern_3(putPattern):
    speed = 5
    vectorLength = pygame.math.Vector2(putPattern[0], putPattern[1]).length()
    dx = speed / vectorLength * putPattern[0]
    dy = speed / vectorLength * putPattern[1]

    
    return {"f(x)" : lambda time : (dx * time, dy * time), \
            "f'(x)" : lambda time : (dx, dy)}