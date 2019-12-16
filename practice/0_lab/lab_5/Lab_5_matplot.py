import random, math 
import matplotlib.pyplot as plot
from matplotlib.patches import Circle

########## Classes and Functions ##########

class circle():
    def __init__(self, name, center, radius, edgecolor):
        self.name = name
        self.center = center
        self.radius = radius
        self.edgecolor = edgecolor

        self.Circle = Circle(xy = center, radius= radius, facecolor = "none", edgecolor = edgecolor)

def distance(centerA, centerB):
    x = abs(centerA[0] - centerB[0])
    y = abs(centerA[1] - centerB[1])
    return math.sqrt(x ** 2 + y ** 2)

def checkIntersection(*circles):
    check = True
    for cA in circles:
        if check == False:
            break
        for cB in circles:
            if cA == cB:
                check = True
            elif distance(cA.center, cB.center) < abs(cA.radius + cB.radius) and \
                 distance(cA.center, cB.center) > abs(cA.radius - cB.radius):
                check = True
            else: 
                check = False
                break
        
    return check


########## Inputs ##########

num = int(input("Please input the number of circles: "))
while True:
    num = int(input("Please input the number of circles: "))
    if num < 2:
        continue
    elif num in [2, 3]:
        break
    elif num > 3:
        print("It's too big. Do you really want to try.(press y to start)")
        if input().lower().startswith("y"):
            break 
        else:
            continue

########## Generate Two Circle ##########


checkA = True 
count = 0
colorList = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']


while checkA:
    count += 1
    circleList = []
    for i in range(1, num + 1):
        c = circle(name = "Circle_{}".format(i), \
                   center = (random.randint(10, 100), random.randint(10, 100)), \
                   radius = random.randint(1, 10), \
                   edgecolor = colorList[i % len(colorList)])
        circleList.append(c)
    
    # if distance(c1.center, c2.center) < abs(c1.radius + c2.radius) and \
    #    distance(c1.center, c2.center) > abs(c1.radius - c2.radius):
    #    checkA = False

    # if checkIntersection(circleList[0], circleList[1], circleList[2]):
    #     checkA = False
    
    if checkIntersection(*(c for c in circleList)):
        checkA = False 
        draw = True

    if count % 500 == 0:
        print("Please wait for a minute.(count = {})".format(count))

    if count == 100000:
        print("Please try again.")
        draw = False
        break


########## Output ##########
if draw:
    print("Iteration of the random processes =",count)

    for c in circleList:
        print("(x, y) of {0} = {1}".format(c.name, c.center))


    ########## Matplot Output ##########
    Lab5_fig = plot.figure("Lab-5")
    figure = Lab5_fig.add_subplot()
        
    for c in circleList:
        figure.add_patch(c.Circle)

    plot.axis('scaled')
    figure.set_xlim(0, 110)
    figure.set_ylim(0, 110)
    plot.show()