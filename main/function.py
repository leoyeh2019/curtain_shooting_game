import pygame, random, math
import parameter

def raletivePosition(pointA, pointB):
    """
    raletivePosition(pointA = tuple, pointB = tuple)
        for the bullet generating in raletive position of player or enemy
        will return pointA + pointB
    """
    if (type(pointA) == tuple) and (type(pointB) == tuple):
        x = pointA[0] + pointB[0]
        y = pointA[1] + pointB[1]
        return (x, y)
    else:
        print("PointA and PointB must be 'tuple'.")
        raise TypeError

def distance(pointA, pointB):
    """
    distance(pointA = tuple, pointB = tuple)
        calculating the distance between pointA and pointB
    """
    if (type(pointA) == tuple) and (type(pointB) == tuple):
        x = pointA[0] - pointB[0]
        y = pointA[1] - pointB[1]
        return math.sqrt(x**2 + y**2)
    else:
        print("PointA and PointB must be \"tuple\".")
        raise TypeError

def returnTheComponentOfVectorX(x, y, r):
    return x / distance((x, y), (0, 0)) * r
def returnTheComponentOfVectorY(x, y, r):
    return y / distance((x, y), (0, 0)) * r

def findMostCloseEnemy(playerCenter):
    enemyList = [i for i in parameter.getEnemySprites()]
    enemyDistanceList = [distance(i.rect.center, playerCenter) for i in enemyList]
    minimun = enemyDistanceList[0]
    minimunIndex = 0
    for i in range(len(enemyDistanceList)):
        if enemyDistanceList[i] < minimun:
            minimun = enemyDistanceList[i]
            minimunIndex = i
    return enemyList[minimunIndex].rect.center



if __name__ == "__main__":
    print(distance([8, 7], (-5, 6)))