import pygame, json
import parameter



def get_parameter(parameter):
    try:
        return parameter
    except NameError:
        return None

class playerCollisionBox(pygame.sprite.Sprite):
    def __init__(self, collisionBoxImage, playerRect):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = collisionBoxImage
        self.image = self.image_origin.copy()
        self.rect = self.image.get_rect(center = playerRect.center)
        self.axis = 0
        self.rotateSpeed = 5 
        self.lastUpdate = parameter.getTimer()
    def rotate(self):
        now = parameter.getTimer()
        if now - self.lastUpdate > 100: 
            self.lastUpdate = now
            self.axis = (self.axis + self.rotateSpeed) % 360
            newImage = pygame.transform.rotate(self.image_origin, self.axis)
            oldCenter = self.rect.center
            self.image = newImage
            self.rect = self.image.get_rect(center = oldCenter)

        

      
        

class Player(pygame.sprite.Sprite):
    def __init__(self, name, lifes, image, collisionBoxImage, playerBulletImage, playerSpeed, playerDamage, putBulletPattern, shootBulletPattern, gamearea):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.lifes = lifes
        self.image = image
        self.collisionBoxImage = collisionBoxImage
        self.playerBulletImage = playerBulletImage
        self.playerDamage = playerDamage
        self.playerFastSpeed = playerSpeed[0]
        self.playerSlowSpeed = playerSpeed[1]
        self.putBulletPattern = putBulletPattern
        self.shootBulletPattern = shootBulletPattern
        self.gamearea = gamearea

        self.rect = self.image.get_rect(center = (self.gamearea.centerx, self.gamearea.bottom - 50))
        
        self.collisionBox = playerCollisionBox(collisionBoxImage = self.collisionBoxImage, playerRect = self.rect)

        self.radius = int(self.collisionBox.rect.width / 2)

        self.lastShootingTime = parameter.getTimer()
        

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LSHIFT]:
            speed = self.playerSlowSpeed
        else:
            speed = self.playerFastSpeed
        if keystate[pygame.K_LEFT] and self.rect.left > self.gamearea.left:
            self.rect.move_ip(-1 * speed, 0)
            if self.rect.left < self.gamearea.left:
                self.rect.left = self.gamearea.left
        if keystate[pygame.K_RIGHT] and self.rect.right < self.gamearea.right:
            self.rect.move_ip(speed, 0)
            if self.rect.right > self.gamearea.right:
                self.rect.right = self.gamearea.right
        if keystate[pygame.K_UP] and self.rect.top > self.gamearea.top:
            self.rect.move_ip(0, -1 * speed)
            if self.rect.top < self.gamearea.top:
                self.rect.top = self.gamearea.top
        if keystate[pygame.K_DOWN] and self.rect.bottom < self.gamearea.bottom:
            self.rect.move_ip(0, speed)
            if self.rect.bottom > self.gamearea.bottom:
                self.rect.bottom = self.gamearea.bottom
        if keystate[pygame.K_z]:
            self.shoot()  
        
        self.collisionBox.rect.center = self.rect.center
        # self.collisionBox.rotate()
        
    def shoot(self):
        now = parameter.getTimer()
        if now - self.lastShootingTime > 6:
            playerBullet = PlayerBullet(name = "playerBullet", \
                                        image = self.playerBulletImage, \
                                        bulletRadius = 1, \
                                        bulletDamage = self.playerDamage, \
                                        putBulletPattern = (self.putBulletPattern(now)[0] + self.rect.center[0], \
                                                            self.putBulletPattern(now)[1] + self.rect.center[1]), \
                                        shootBulletPattern = self.shootBulletPattern, \
                                        gamearea = self.gamearea)
            self.lastShootingTime = now
            parameter.getAllSprites().add(playerBullet)
            parameter.getPlayerBulletSprites().add(playerBullet)
            


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, Hp, image, movePattern, enemyBulletImage, putBulletPattern, shootBulletPattern, gamearea):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.Hp = Hp
        self.image = image
        self.movePattern = movePattern
        self.enemyBulletImage = enemyBulletImage
        self.putBulletPattern = putBulletPattern
        self.shootBulletPattern = shootBulletPattern
        self.gamearea = gamearea

        self.rect = self.image.get_rect(center = (movePattern(-1)[0] + self.gamearea.left, \
                                                  movePattern(-1)[1] + self.gamearea.top))
        self.radius = int((self.rect.width / 2) * 0.5)

        self.generateTime = parameter.getTimer()
        self.lastShootingTime = parameter.getTimer()


    def update(self):
        now = parameter.getTimer()
        self.rect.move_ip(self.movePattern(now - self.generateTime))
        if not self.rect.colliderect(self.gamearea):
            self.kill()

        self.shoot()

    def shoot(self):
        now =  parameter.getTimer()
        if now - self.generateTime > self.putBulletPattern(now - self.generateTime)["delateTime"]:
            if now - self.lastShootingTime > self.putBulletPattern(now - self.generateTime)["intermediateTime"]:
                for i in range(self.putBulletPattern(now)["numbers"]):
                    x = self.putBulletPattern(now)["position"][i][0]
                    y = self.putBulletPattern(now)["position"][i][1]
                    enemyBullet = EnemyBullet(name = "enemyBullet", \
                                              image = self.enemyBulletImage, \
                                              bulletRadius = 1, \
                                              bulletDamage = None, \
                                              putBulletPattern = (x + self.rect.center[0], \
                                                                  y + self.rect.center[1]), \
                                              shootBulletPattern = self.shootBulletPattern((x, y)), \
                                              gamearea = self.gamearea)
                    parameter.getAllSprites().add(enemyBullet)
                    parameter.getEnemyBulletSprites().add(enemyBullet)
                self.lastShootingTime = now
                
                




        
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern, gamearea):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image_origin = image
        self.image = self.image_origin.copy()
        self.radius = bulletRadius
        self.damage = bulletDamage
        self.shootBulletPattern = shootBulletPattern
        self.generateCenter = putBulletPattern
        self.gamearea = gamearea

        self.rect = self.image.get_rect(center = self.generateCenter)

        self.generateTime = parameter.getTimer()
        

    def update(self):
        now = parameter.getTimer()

        self.rect.move_ip(self.shootBulletPattern(now - self.generateTime))

        if not self.rect.colliderect(self.gamearea):
            self.kill()





class EnemyBullet(PlayerBullet):
    def __init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern, gamearea):
        PlayerBullet.__init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern, gamearea)

    def update(self):
        now = parameter.getTimer()

        self.rotate(now)
        self.rect.center = (self.shootBulletPattern["f(x)"](now - self.generateTime)[0] + self.generateCenter[0], \
                            self.shootBulletPattern["f(x)"](now - self.generateTime)[1] + self.generateCenter[1])

        if not self.rect.colliderect(self.gamearea):
            self.kill()
            
    def rotate(self, now):
        if now - self.generateTime == 0:
            time = 1
        else:
            time = now - self.generateTime
        x = self.shootBulletPattern["f'(x)"](time)[0]
        y = self.shootBulletPattern["f'(x)"](time)[1]
        v = pygame.math.Vector2(x, y)
        axis = 90 - v.as_polar()[1]
        newImage = pygame.transform.rotate(self.image_origin, axis)
        oldCenter = self.rect.center
        self.image = newImage
        self.rect = self.image.get_rect(center = oldCenter)