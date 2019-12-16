import random, math 
import matplotlib.pyplot as plot
from matplotlib.patches import Circle

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


########## Generate Two Circle ##########
check = True 
count = 0

while check:
    count += 1
    c1 = circle(name = "Circle_1", \
                center = (random.randint(10, 100), random.randint(10, 100)), \
                radius = random.randint(1, 10), \
                edgecolor = "r")
    c2 = circle(name = "Circle_2", \
                center = (random.randint(10, 100), random.randint(10, 100)), \
                radius = random.randint(1, 10), \
                edgecolor = "b")
    if distance(c1.center, c2.center) < abs(c1.radius + c2.radius) and \
       distance(c1.center, c2.center) > abs(c1.radius - c2.radius):
       check = False


print("(x, y) of {0} = {1}".format(c1.name, c1.center))
print("(x, y) of {0} = {1}".format(c2.name, c2.center))
print("Iteration of the random processes =", count)

########## Matplot Output ##########
Lab5_fig = plot.figure("Lab-5")
figure = Lab5_fig.add_subplot()
    
figure.add_patch(c1.Circle)
figure.add_patch(c2.Circle)
plot.axis('scaled')
figure.set_xlim(0, 110)
figure.set_ylim(0, 110)
plot.show()