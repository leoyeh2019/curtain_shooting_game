import pygame, random, sys, math

########## Constants##########
WINDOW_WIDTH = 800
WINDOWWINDOW_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
colorList = [RED, GREEN, BLUE] 

class circle(pygame.sprite.Sprite):
    def __init__(self, name, center, radius, color, surface):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.center = center
        self.radius = radius
        self.color = color
        self.surface = surface

        self.rect = pygame.Rect(center[0] - self.radius, center[1] - self.radius, radius * 2, radius * 2)

        self.vector = pygame.math.Vector2(self.center)
    def update(self):
        pygame.draw.circle(self.surface, self.color, self.center, self.radius, 1)





########## Pygame Initialize ##########
pygame.init()
pygame.mixer.init()
WINDOW_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOWWINDOW_HEIGHT))
pygame.display.set_caption("lab_4_pygame")
clock = pygame.time.Clock()


########## Generate Two Circle ##########
check = True
while check:
    circle1 = circle(name = "c1", \
                     center =  (random.randint(50, 500), random.randint(50, 500)), \
                     radius = random.randint(5, 50), \
                     color = random.choice(colorList), \
                     surface = WINDOW_SURFACE)
    circle2 = circle(name = "c2", \
                     center =  (random.randint(50, 500), random.randint(50, 500)), \
                     radius = random.randint(5, 50), \
                     color = random.choice(colorList), \
                     surface = WINDOW_SURFACE)
    
    if not circle1.color == circle2.color:
        if pygame.math.Vector2.length(circle1.vector - circle2.vector) > abs(circle1.radius - circle2.radius) \
           and pygame.math.Vector2.length(circle1.vector - circle2.vector) < abs(circle1.radius + circle2.radius):
            check = False
        

allSprites = pygame.sprite.Group()
allSprites.add(circle1)
allSprites.add(circle2)
print(circle1.center, circle1.radius, circle1.color)
print(circle2.center, circle2.radius, circle2.color)
########## Game Loop ##########
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    
    # Draw / render
    WINDOW_SURFACE.fill(WHITE)
    allSprites.update()
    # *after* drawing everything, flip the display
    pygame.display.update()

pygame.quit()
sys.exit()