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


def enemyMovePattern_4(time):
    if time < 0:
        return 384, -10
    elif time < 50:
        return 0, 4
    elif time < 1000:
        return 0, 0
    else:
        return 0, -2

def enemyPutBulletPattern_4(time):
    r = 50
    θ = (time ** 2) / 60
    ways = 4
    Δθ = 360 / ways 
    positionList = []
    for i in range(ways):
        θ_i = math.radians((θ + (i * Δθ)) % 360)
        positionList.append((r * math.cos(θ_i), r * math.sin(θ_i)))

    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 50, \
            "intermediateTime" : 2}

 

def enemyshootBulletPattern_4(putPattern):
    speed = 8
    vectorLength = pygame.math.Vector2(putPattern[0], putPattern[1]).length()
    dx = speed / vectorLength * putPattern[0]
    dy = speed / vectorLength * putPattern[1]
    
    return {"f(x)" : lambda time : (dx * time, dy * time), \
            "f'(x)" : lambda time : (dx, dy)}

def bossMovePattern_1(time):
    if time < 0:
        return 384, -50
    if time <= 50:
        return 0, 5
    else:
        return 0, 0

def bossPutBulletPattern_1(time):
    r = 10
    θ = time * 10
    ways = 1
    Δθ = random.randint(-15, 15)
    positionList = []
    for i in range(ways):
        θ_i = math.radians((θ + ((i+1) * Δθ)) % 360)
        positionList.append((r * math.cos(θ_i), r * math.sin(θ_i)))

    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 150, \
            "intermediateTime" : 1}

 

def bossShootBulletPattern_1(putPattern):
    speed = random.randint(10, 20)
    vectorLength = pygame.math.Vector2(putPattern[0], putPattern[1]).length()
    dx = speed / vectorLength * putPattern[0]
    dy = speed / vectorLength * putPattern[1]
    
    return {"f(x)" : lambda time : (dx * time, dy * time), \
            "f'(x)" : lambda time : (dx, dy)}


def bossMovePattern_2(time):
    if time < 0:
        return 384, 200
    else:
        return 0, 0

def bossPutBulletPattern_2_1(time):
    ax = 1
    ay = 2
    b = -300
    ways = 20
    difficulty = time // 150
    if difficulty > 5:
        difficulty = 5
    Δ = 15
    
    positionList = []
    for i in range(ways):
        entropy = random.randint(-difficulty * 15, difficulty * 15)
        positionList.append((i * Δ * ax + entropy, i * Δ * ay + b + entropy))

    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 0, \
            "intermediateTime" : 150}

def bossPutBulletPattern_2_2(time):
    ax = 1
    ay = 2
    b = -150
    ways = 20
    difficulty = time // 150
    if difficulty > 5:
        difficulty = 5
    Δ = 15
    
    positionList = []
    for i in range(ways):
        entropy = random.randint(-difficulty * 15, difficulty * 15)
        positionList.append((i * Δ * ax + entropy, i * Δ * ay + b + entropy))

    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 0, \
            "intermediateTime" : 150}

def bossPutBulletPattern_2_3(time):
    ax = -1
    ay = 2
    b = -300
    ways = 20
    difficulty = time // 150
    if difficulty > 5:
        difficulty = 5
    Δ = 15
    
    positionList = []
    for i in range(ways):
        entropy = random.randint(-difficulty * 15, difficulty * 15)
        positionList.append((i * Δ * ax + entropy, i * Δ * ay + b + entropy))

    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 0, \
            "intermediateTime" : 150}

def bossPutBulletPattern_2_4(time):
    ax = -1
    ay = 2
    b = -150
    ways = 20
    difficulty = time // 150
    if difficulty > 5:
        difficulty = 5
    Δ = 15
    
    positionList = []
    for i in range(ways):
        entropy = random.randint(-difficulty * 15, difficulty * 15)
        positionList.append((i * Δ * ax + entropy, i * Δ * ay + b + entropy))

    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 0, \
            "intermediateTime" : 150}

def bossShootBulletPattern_2_1(putPattern):
    speed = 10
    dx1 = speed / math.sqrt(5) * -2
    dy1 = speed / math.sqrt(5) * 1
    dx2 = speed / math.sqrt(5) * 1
    dy2 = speed / math.sqrt(5) * 2
    
    return {"f(x)" : lambda time : (dx1 * time, dy1 * time) if time < 50 else  (dx2 * (time - 50) + dx1 * 50, dy2 * (time - 50) + dy1 * 50), \
            "f'(x)" : lambda time : (dx1, dy1) if time < 50 else  (dx2, dy2)}

def bossShootBulletPattern_2_3(putPattern):
    speed = 10
    dx1 = speed / math.sqrt(5) * 2
    dy1 = speed / math.sqrt(5) * 1
    dx2 = speed / math.sqrt(5) * -1
    dy2 = speed / math.sqrt(5) * 2
    
    return {"f(x)" : lambda time : (dx1 * time, dy1 * time) if time < 50 else  (dx2 * (time - 50) + dx1 * 50, dy2 * (time - 50) + dy1 * 50), \
            "f'(x)" : lambda time : (dx1, dy1) if time < 50 else  (dx2, dy2)}

def bossMovePattern_3(time):
    if time < 0:
        return 384, 200
    else:
        return 0, 0

def bossPutBulletPattern_3(time):
    r = 10
    ways = 36
    θ = 360 / ways
    Δθ = random.randint(10, 20)
    positionList = []
    for i in range(ways):
        θ_i = math.radians((θ * i + Δθ)) % 360
        positionList.append((r * math.cos(θ_i), r * math.sin(θ_i)))

    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 150, \
            "intermediateTime" : 30}

 

def bossShootBulletPattern_3(putPattern):
    speed = random.randint(5, 15)
    vectorLength = pygame.math.Vector2(putPattern[0], putPattern[1]).length()
    dx = speed / vectorLength * putPattern[0]
    dy = speed / vectorLength * putPattern[1]
    
    return {"f(x)" : lambda time : (dx * time, dy * time), \
            "f'(x)" : lambda time : (dx, dy)}


def bossMovePattern_4(time):
    if time < 0:
        return 384, 200
    else:
        return 0, 0

def bossPutBulletPattern_4_1(time):
    ways = 1
    positionList = []
    for i in range(ways):
        positionList.append((0, 50))

    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 150, \
            "intermediateTime" : 100, \
            "tracking" : True}

 

def bossShootBulletPattern_4_1(putPattern):

    speed = 5
    
    return speed

def bossPutBulletPattern_4_2(time):
    ways = 40
    Δ = 64
    positionList = []
    for i in range(ways):
        entropy = random.randint(-15, 15)
        if i <= 13:
            positionList.append((-384, -200 + Δ * i + entropy))
        elif i >= 14 and i <= 25:
            positionList.append((-384 + Δ * (i - 14) + entropy, -200 ))
        else:
            positionList.append((384, -200 + Δ * (i - 26) + entropy))

    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 280, \
            "intermediateTime" : 130, \
            "tracking" : True}

 

def bossShootBulletPattern_4_2(putPattern):

    speed = 1
    
    return speed


def bossMovePattern_5(time):
    if time < 0:
        return 384, 200
    else:
        return 0, 0

def bossPutBulletPattern_5(time):
    r = 10
    ways = 3
    θ = 360 / ways
    Δθ = random.randint(-60, 60)
    positionList = []
    for i in range(ways):
        θ_i = math.radians((θ * i + Δθ)) % 360
        positionList.append((r * math.cos(θ_i), r * math.sin(θ_i)))

    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 150, \
            "intermediateTime" : 3}

 

def bossShootBulletPattern_5(putPattern):
    speed = random.randint(2, 5)
    vectorLength = pygame.math.Vector2(putPattern[0], putPattern[1]).length()
    dx = speed / vectorLength * putPattern[0]
    dy = speed / vectorLength * putPattern[1]
    
    return {"f(x)" : lambda time : (dx * time, dy * time), \
            "f'(x)" : lambda time : (dx, dy)}


def bossMovePattern_6(time):
    if time < 0:
        return 384, 200
    else:
        return 0, 0

def bossPutBulletPattern_6(time):
    ways = 1
    generateRangeX = 300
    generateRangeY = 100
    positionList = []
    for i in range(ways):
        positionList.append((random.randint(-generateRangeX, generateRangeX), random.randint(-generateRangeY, generateRangeY)))

    deathGenerateBullet = {}
    deathGenerateBullet["generateBulletNumber"] = 5
    deathGenerateBullet["putPattern"] = (0, 0)
    deathGenerateBullet["shootPattern"] = bossShootBulletPattern_6_1
    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 150, \
            "intermediateTime" : 20, \
            "deathGenerate" : True, \
            "generateBullet" : deathGenerateBullet}

def bossShootBulletPattern_6_1(putPattern):
    speed = 1
    θ = random.randint(0, 180)
    vectorLength = pygame.math.Vector2(function.form_polar_degree(speed, θ)).length()
    dx = - speed / vectorLength * function.form_polar_degree(speed, θ)[0]
    dy = - speed / vectorLength * function.form_polar_degree(speed, θ)[1]
    
    return {"f(x)" : lambda time : (dx * time, dy * time), \
            "f'(x)" : lambda time : (dx, dy)}

def bossShootBulletPattern_6(putPattern):
    speed = 10
    return {"f(x)" : lambda time : (0, speed * time), \
            "f'(x)" : lambda time : (0, speed)}


def bossMovePattern_7(time):
    if time < 0:
        return 384, 200
    else:
        return 0, 0

def bossPutBulletPattern_7_1(time):
    r = 10
    θ = time * 10
    ways = 1
    Δθ = random.randint(-15, 15)
    positionList = []
    for i in range(ways):
        θ_i = math.radians((θ + ((i+1) * Δθ)) % 360)
        positionList.append((r * math.cos(θ_i), r * math.sin(θ_i)))

    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 150, \
            "intermediateTime" : 1}

def bossPutBulletPattern_7_2(time):
    r = 10
    θ = time * 10
    ways = 1
    Δθ = random.randint(-15, 15)
    positionList = []
    for i in range(ways):
        θ_i = - math.radians((θ + ((i+1) * Δθ)) % 360)
        positionList.append((r * math.cos(θ_i), r * math.sin(θ_i)))

    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 150, \
            "intermediateTime" : 1}

def bossShootBulletPattern_7_1(putPattern):
    speed = random.randint(10, 20)
    vectorLength = pygame.math.Vector2(putPattern[0], putPattern[1]).length()
    dx = speed / vectorLength * putPattern[0]
    dy = speed / vectorLength * putPattern[1]
    
    return {"f(x)" : lambda time : (dx * time, dy * time), \
            "f'(x)" : lambda time : (dx, dy)}

def bossShootBulletPattern_7_2(putPattern):
    speed = random.randint(5, 10)
    vectorLength = pygame.math.Vector2(putPattern[0], putPattern[1]).length()
    dx = speed / vectorLength * putPattern[0]
    dy = speed / vectorLength * putPattern[1]
    
    return {"f(x)" : lambda time : (dx * time, dy * time), \
            "f'(x)" : lambda time : (dx, dy)}


def bossMovePattern_8_1(time):
    if time < 0:
        return 384, 200
    else:
        return 0, 0


def bossPutBulletPattern_8_1(time):
    ways = 1
    generateRangeX = 400
    generateRangeY = 200
    positionList = []
    for i in range(ways):
        positionList.append((random.randint(-generateRangeX, generateRangeX), random.randint(-generateRangeY, 0)))

    deathGenerateBullet = {}
    deathGenerateBullet["generateBulletNumber"] = 1
    deathGenerateBullet["putPattern"] = (0, 0)
    deathGenerateBullet["shootPattern"] = bossShootBulletPattern_8_1_1
    return {"numbers" : ways, \
            "position" : positionList, \
            "delateTime" : 150, \
            "intermediateTime" : 15, \
            "deathGenerate" : True, \
            "generateBullet" : deathGenerateBullet}

def bossShootBulletPattern_8_1_1(putPattern):
    speed = - math.sqrt(700 * 2 * 0.20)
    g = 0.25
    return {"f(x)" : lambda time : (0, speed * time + 0.5 * g * (time ** 2)), \
            "f'(x)" : lambda time : (0, speed + g * time)}
def bossShootBulletPattern_8_1(putPattern):
    speed = 0
    g = 0.20
    return {"f(x)" : lambda time : (0, speed * time + 0.5 * g * (time ** 2)), \
            "f'(x)" : lambda time : (0, speed + g * time)}