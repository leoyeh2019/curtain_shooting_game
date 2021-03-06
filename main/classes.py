import pygame, json, math
import parameter
import function
import sound


def get_parameter(parameter):
    try:
        return parameter
    except NameError:
        return None



class Background(pygame.sprite.Sprite):
    def __init__(self, image, topleft, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.topleft_origin = topleft
        self.rect = self.image.get_rect(topleft = self.topleft_origin)
        self.speed = speed

    def update(self):
        # Moving Background
        self.rect.move_ip(0, self.speed)

        # Generate new background when out of screen
        if self.rect.top > 928:
            newBackground = Background(image = self.image, \
                                       topleft = (64, -1930), \
                                       speed = self.speed)
            parameter.getBackgroundSprites().add(newBackground)
            self.kill()

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
    def __init__(self, name, lifes, image, collisionBoxImage, playerBulletImage, playerSpeed, playerDamage, putBulletPattern, shootBulletPattern):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.lifes = lifes
        self.image_origin = image
        self.image = self.image_origin.copy()
        self.collisionBoxImage = collisionBoxImage
        self.playerBulletImage = playerBulletImage
        self.playerDamage = playerDamage
        self.playerFastSpeed = playerSpeed[0]
        self.playerSlowSpeed = playerSpeed[1]
        self.putBulletPattern = putBulletPattern
        self.shootBulletPattern = shootBulletPattern


        self.rect = self.image.get_rect(center = (parameter.getGamearea().centerx, parameter.getGamearea().bottom - 50))
        
        self.collisionBox = playerCollisionBox(collisionBoxImage = self.collisionBoxImage, playerRect = self.rect)

        self.radius = int(self.collisionBox.rect.width / 2)
        

        self.lastShootingTime = parameter.getTimer()
        
        self.power = 0

        self.hidden = False
        self.hiddenTime = parameter.getTimer()

    def update(self):
        now = parameter.getTimer()

        #　Hide player for a while when player died
        if self.hidden and now - self.hiddenTime < 30:
            for eb in parameter.getEnemyBulletSprites():
                eb.kill()
        elif self.hidden and now - self.hiddenTime == 30:
            self.radius = 0
            self.rect.center = (parameter.getGamearea().centerx, parameter.getGamearea().bottom - 50)
        elif self.hidden and now - self.hiddenTime < 120:
            self.radius = 0
            if ((now - self.hiddenTime) % 6) in [0, 1, 2]:
                transparentImg = self.image_origin.copy()
                transparentImg.set_alpha(64)
                self.image = transparentImg
            else:
                self.image = self.image_origin
        else:
            self.image = self.image_origin
            self.radius = int(self.collisionBox.rect.width / 2)
            self.hidden = False 
            
        # Key control
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LSHIFT]:
            speed = self.playerSlowSpeed
        else:
            speed = self.playerFastSpeed
        if keystate[pygame.K_LEFT] and self.rect.left > parameter.getGamearea().left:
            self.rect.move_ip(-1 * speed, 0)
            if self.rect.left < parameter.getGamearea().left:
                self.rect.left = parameter.getGamearea().left
        if keystate[pygame.K_RIGHT] and self.rect.right < parameter.getGamearea().right:
            self.rect.move_ip(speed, 0)
            if self.rect.right > parameter.getGamearea().right:
                self.rect.right = parameter.getGamearea().right
        if keystate[pygame.K_UP] and self.rect.top > parameter.getGamearea().top:
            self.rect.move_ip(0, -1 * speed)
            if self.rect.top < parameter.getGamearea().top:
                self.rect.top = parameter.getGamearea().top
        if keystate[pygame.K_DOWN] and self.rect.bottom < parameter.getGamearea().bottom:
            self.rect.move_ip(0, speed)
            if self.rect.bottom > parameter.getGamearea().bottom:
                self.rect.bottom = parameter.getGamearea().bottom
        if keystate[pygame.K_z]:
            self.shoot()  
        
        # Stick player collision box to the player center
        self.collisionBox.rect.center = self.rect.center
        # self.collisionBox.rotate()

        # Return player position
        parameter.returnPlayerPosition(self.rect.center)

    def newPlayerBullet(self, putBulletPattern):
        playerBullet = PlayerBullet(name = "playerBullet", \
                                    image = self.playerBulletImage[0], \
                                    bulletRadius = 5, \
                                    bulletDamage = self.playerDamage[0], \
                                    putBulletPattern = putBulletPattern, \
                                    shootBulletPattern = self.shootBulletPattern[0])
        parameter.getAllSprites().add(playerBullet)
        parameter.getPlayerBulletSprites().add(playerBullet)

    def newPlayerBullet_tracking(self, putBulletPattern, shootBulletPattern):
        playerBullet = PlayerBullet_tracking(name = "playerBullet_tracking", \
                                             image = self.playerBulletImage[1], \
                                             bulletRadius = 5, \
                                             bulletDamage = self.playerDamage[1], \
                                             putBulletPattern = putBulletPattern, \
                                             shootBulletPattern = shootBulletPattern, \
                                             playerRectCenter = self.rect.center)
        parameter.getAllSprites().add(playerBullet)
        parameter.getPlayerBulletSprites().add(playerBullet)

    def shoot(self):
        now = parameter.getTimer()
        if now - self.lastShootingTime > 6:
            sound.bullet_SE_list[0].play()
            # powerups
            if self.power in range(0, 8):
                # line 1 way
                self.newPlayerBullet(putBulletPattern = function.raletivePosition(self.putBulletPattern[0](now, self.power), self.rect.center))
                self.lastShootingTime = now
            
            if self.power in range(8, 24):
                # line 1 way
                self.newPlayerBullet(putBulletPattern = function.raletivePosition(self.putBulletPattern[0](now, self.power), self.rect.center))
                # tracking 2 way
                for i in range(len(self.putBulletPattern[1](now, self.power))):
                    self.newPlayerBullet_tracking(putBulletPattern = function.raletivePosition(self.putBulletPattern[1](now, self.power)[i], self.rect.center), \
                                                  shootBulletPattern = self.shootBulletPattern[1](now)[i])
                
                self.lastShootingTime = now

            if self.power in range(24, 48):
                # line 3 way
                for i in range(len(self.putBulletPattern[0](now, self.power))):
                    self.newPlayerBullet(putBulletPattern = function.raletivePosition(self.putBulletPattern[0](now, self.power)[i], self.rect.center))
                    
                # tracking 2 way
                for i in range(len(self.putBulletPattern[1](now, self.power))):
                    self.newPlayerBullet_tracking(putBulletPattern = function.raletivePosition(self.putBulletPattern[1](now, self.power)[i], self.rect.center), \
                                                  shootBulletPattern = self.shootBulletPattern[1](now)[i])
                
                self.lastShootingTime = now

            if self.power == 48:
                # line 3 way
                for i in range(len(self.putBulletPattern[0](now, self.power))):
                    self.newPlayerBullet(putBulletPattern = function.raletivePosition(self.putBulletPattern[0](now, self.power)[i], self.rect.center))
                    
                # tracking 4 way
                for i in range(len(self.putBulletPattern[1](now, self.power))):
                    self.newPlayerBullet_tracking(putBulletPattern = function.raletivePosition(self.putBulletPattern[1](now, self.power)[i], self.rect.center), \
                                                  shootBulletPattern = self.shootBulletPattern[1](now)[i])
                
                self.lastShootingTime = now


    def hide(self):
        # Hide player
        for eb in parameter.getEnemyBulletSprites():
                eb.kill()
        self.hidden = True 
        self.hiddenTime = parameter.getTimer()
        self.rect.center = (parameter.getGamearea().centerx, parameter.getGamearea().top - 200)
        # Decrease player power
        if self.power > 4:
            self.power -= 4
        else:
             self.power = 0
            


class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, Hp, image, movePattern, enemyBulletImage, putBulletPattern, shootBulletPattern, dropItem):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.Hp = Hp
        self.image = image
        self.movePattern = movePattern
        self.enemyBulletImage = enemyBulletImage
        self.putBulletPattern = putBulletPattern
        self.shootBulletPattern = shootBulletPattern
        self.dropItem = dropItem

        self.rect = self.image.get_rect(center = (movePattern(-1)[0] + parameter.getGamearea().left, \
                                                  movePattern(-1)[1] + parameter.getGamearea().top))
        self.radius = int((self.rect.width / 2) * 0.5)

        self.generateTime = parameter.getTimer()
        self.lastShootingTime = [parameter.getTimer() for i in range(len(self.enemyBulletImage))]


    def update(self):
        now = parameter.getTimer()
        # Moving enemy
        self.rect.move_ip(self.movePattern(now - self.generateTime))
        # Kill enemy if out of screen
        if not self.rect.colliderect(parameter.getGamearea()):
            self.kill()
        # Shoot bullet
        self.shoot()


    def shoot(self):
        now =  parameter.getTimer()
        for j in range(len(self.enemyBulletImage)):
            if now - self.generateTime > self.putBulletPattern[j](now - self.generateTime)["delateTime"]:
                if now - self.lastShootingTime[j] > self.putBulletPattern[j](now - self.generateTime)["intermediateTime"]:
                    sound.bullet_SE_list[2].play()
                    for i in range(self.putBulletPattern[j](now)["numbers"]):
                        x = self.putBulletPattern[j](now)["position"][i][0]
                        y = self.putBulletPattern[j](now)["position"][i][1]
                        if "tracking" in self.putBulletPattern[j](now).keys():
                            enemyBullet = EnemyBullet_tracking(name = "enemyBullet", \
                                                               image = self.enemyBulletImage[j], \
                                                               bulletRadius = 1, \
                                                               bulletDamage = None, \
                                                               putBulletPattern = (x + self.rect.center[0], \
                                                                                   y + self.rect.center[1]), \
                                                               shootBulletPattern = self.shootBulletPattern[j]((x, y)))
                            parameter.getAllSprites().add(enemyBullet)
                            parameter.getEnemyBulletSprites().add(enemyBullet)
                        elif "deathGenerate" in self.putBulletPattern[j](now).keys():
                            enemyBullet = EnemyBullet_deathGenerate(name = "enemyBullet", \
                                                               image = self.enemyBulletImage[j], \
                                                               bulletRadius = 1, \
                                                               bulletDamage = None, \
                                                               putBulletPattern = (x + self.rect.center[0], \
                                                                                   y + self.rect.center[1]), \
                                                               shootBulletPattern = self.shootBulletPattern[j]((x, y)), \
                                                               death = self.putBulletPattern[j](now)["generateBullet"])
                            parameter.getAllSprites().add(enemyBullet)
                            parameter.getEnemyBulletSprites().add(enemyBullet)
                        elif "decay" in self.putBulletPattern[j](now).keys():
                            enemyBullet = EnemyBullet_decay(name = "enemyBullet", \
                                                               image = self.enemyBulletImage[j], \
                                                               bulletRadius = 1, \
                                                               bulletDamage = None, \
                                                               putBulletPattern = (x + self.rect.center[0], \
                                                                                   y + self.rect.center[1]), \
                                                               shootBulletPattern = self.shootBulletPattern[j]((x, y)))
                            parameter.getAllSprites().add(enemyBullet)
                            parameter.getEnemyBulletSprites().add(enemyBullet)
                        else:
                            enemyBullet = EnemyBullet(name = "enemyBullet", \
                                                      image = self.enemyBulletImage[j], \
                                                      bulletRadius = 1, \
                                                      bulletDamage = None, \
                                                      putBulletPattern = (x + self.rect.center[0], \
                                                                          y + self.rect.center[1]), \
                                                      shootBulletPattern = self.shootBulletPattern[j]((x, y)))
                            parameter.getAllSprites().add(enemyBullet)
                            parameter.getEnemyBulletSprites().add(enemyBullet)
                    self.lastShootingTime[j] = now
    def kill(self):
        super().kill()
                
                



        
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image_origin = image
        self.image = self.image_origin.copy()
        self.radius = bulletRadius
        self.damage = bulletDamage
        self.shootBulletPattern = shootBulletPattern
        self.generateCenter = putBulletPattern

        self.rect = self.image.get_rect(center = self.generateCenter)

        self.generateTime = parameter.getTimer()
        

    def update(self):
        now = parameter.getTimer()

        self.rect.move_ip(self.shootBulletPattern(now - self.generateTime))

        if not self.rect.colliderect(parameter.getGamearea()):
            self.kill()

     


class PlayerBullet_tracking(PlayerBullet):
    def __init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern, playerRectCenter):
        PlayerBullet.__init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern)
        self.playerRectCenter = playerRectCenter
        self.speed = function.distance(self.shootBulletPattern, (0, 0))
        self.dx = self.shootBulletPattern[0]
        self.dy = self.shootBulletPattern[1]

    def update(self):
        now = parameter.getTimer()
        # Find the nearest enemy
        try:
            enemyCenter = function.findMostCloseEnemy(self.playerRectCenter)
            self.dx += (enemyCenter[0] - self.rect.center[0]) / 5000 * (now - self.generateTime) ** 2
            self.dy += (enemyCenter[1] - self.rect.center[1]) / 5000 * (now - self.generateTime) ** 2
            
        except:
            pass
            
        self.rotate()
        
        self.rect.move_ip(function.returnTheComponentOfVectorX(self.dx, self.dy, self.speed), \
                          function.returnTheComponentOfVectorY(self.dx, self.dy, self.speed))

        if not self.rect.colliderect(parameter.getGamearea()):
            self.kill() 
    
    def rotate(self):
        v = pygame.math.Vector2(self.dx, self.dy)
        axis = 90 - v.as_polar()[1]
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.image_origin, axis)
        self.rect = self.image.get_rect(center = oldCenter)




class EnemyBullet(PlayerBullet):
    def __init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern):
        PlayerBullet.__init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern)
        self.radius = int(self.rect.width / 2 * 0.75)

    def update(self):
        now = parameter.getTimer()

        self.rotate(now)
        # Placing bullet on the orbit that caculated by functions
        self.rect.center = (self.shootBulletPattern["f(x)"](now - self.generateTime)[0] + self.generateCenter[0], \
                            self.shootBulletPattern["f(x)"](now - self.generateTime)[1] + self.generateCenter[1])

        if not self.rect.colliderect(parameter.getBulletGamearea()):
            self.kill()
            
    def rotate(self, now):
        time = now - self.generateTime
        x = self.shootBulletPattern["f'(x)"](time)[0]
        y = self.shootBulletPattern["f'(x)"](time)[1]
        v = pygame.math.Vector2(x, y)
        axis = 90 - v.as_polar()[1]
        newImage = pygame.transform.rotate(self.image_origin, axis)
        oldCenter = self.rect.center
        self.image = newImage
        self.rect = self.image.get_rect(center = oldCenter)

class EnemyBullet_tracking(EnemyBullet):
    def __init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern):
        EnemyBullet.__init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern)
        self.speed = shootBulletPattern
        # Get player position from parameter.py
        self.playerPosition = parameter.getPlayerPosition()

        vectorLength = pygame.math.Vector2(self.playerPosition[0] - self.generateCenter[0], self.playerPosition[1] - self.generateCenter[1]).length()
        self.dx = self.speed / vectorLength * (self.playerPosition[0] - self.generateCenter[0])
        self.dy = self.speed / vectorLength * (self.playerPosition[1] - self.generateCenter[1])


    def update(self):
        now = parameter.getTimer()

        self.rotate()
        self.rect.center = (self.dx * (now - self.generateTime) + self.generateCenter[0], \
                            self.dy * (now - self.generateTime) + self.generateCenter[1])

        if not self.rect.colliderect(parameter.getGamearea()):
            self.kill()
    def rotate(self):
        v = pygame.math.Vector2(self.dx, self.dy)
        axis = 90 - v.as_polar()[1]
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.image_origin, axis)
        self.rect = self.image.get_rect(center = oldCenter)

class EnemyBullet_deathGenerate(EnemyBullet):
    def __init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern, death):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image_origin = image[0]
        self.image = self.image_origin.copy()
        
        self.damage = bulletDamage
        self.shootBulletPattern = shootBulletPattern
        self.generateCenter = putBulletPattern

        self.rect = self.image.get_rect(center = self.generateCenter)
        self.radius = int(self.rect.width / 2 * 0.75)
        
        self.generateTime = parameter.getTimer()

        self.deathGenerateImage = image[1]
        self.deathGenerate = death
        self.generateBulletNumber = self.deathGenerate["generateBulletNumber"]


    def update(self):
        super().update()
        if self.rect.bottom > parameter.getGamearea().bottom:
            self.kill()

    def kill(self):
        # Generate new bullet when killed
        for i in range(self.generateBulletNumber):
            x = self.deathGenerate["putPattern"][0]
            y = self.deathGenerate["putPattern"][1]
            enemyBullet = EnemyBullet(name = "enemyBullet", \
                                    image = self.deathGenerateImage, \
                                    bulletRadius = 1, \
                                    bulletDamage = None, \
                                    putBulletPattern = (x + self.rect.center[0], \
                                                        y + self.rect.center[1]), \
                                    shootBulletPattern = self.deathGenerate["shootPattern"]((x, y)))
            parameter.getAllSprites().add(enemyBullet)
            parameter.getEnemyBulletSprites().add(enemyBullet)
        super().kill()
    
class EnemyBullet_decay(EnemyBullet):
    def __init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern):
        EnemyBullet.__init__(self, name, image, bulletRadius, bulletDamage, putBulletPattern, shootBulletPattern)
        self.radius = 0
        self.radius_origin = int(self.rect.width / 2 * 0.5)
        self.px = self.rect.centerx
        self.py = self.rect.centery
        self.dx = self.shootBulletPattern["f'(x)"](self.generateTime)[0]
        self.dy = self.shootBulletPattern["f'(x)"](self.generateTime)[1]

    
    def update(self):
        self.rotate(self.generateTime)
        now = parameter.getTimer()
        # Becoming non-transparent by time
        if now - self.generateTime < 128:
            self.image.set_alpha((now - self.generateTime) * 2)
            self.radius = 0
        # Can collide detect with player as  being opaque
        else:
            self.image.set_alpha(255)
            self.radius = self.radius_origin

        if now - self.generateTime > 300:
            self.px += self.dx
            self.py += self.dy
            self.rect.center = (self.px, self.py)

        if not self.rect.colliderect(parameter.getGamearea()):
            self.kill()
            


class Item(pygame.sprite.Sprite):
    def __init__(self, name, image, generatePosition):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = image
        self.generatePosition = generatePosition
        self.rect = self.image.get_rect(center = self.generatePosition)

        self.generateTime = parameter.getTimer()

        self.radius = self.rect.width * 3

    def update(self):
        now = parameter.getTimer()
        time = now - self.generateTime

        def itemMovement(time):
            v0 = -3
            g = 0.1
            v = v0 + g * time
            if v < 3:
                oldCenterX = self.rect.center[0]
                self.rect.center = (oldCenterX, v0 * time + 0.5 * g * (time **2) + self.generatePosition[1])
            else:
                self.rect.move_ip(0, 3)
            
        
        itemMovement(time)
        if self.rect.top > parameter.getGamearea().bottom:
            self.kill()
        


class BossStage():
    def __init__(self, order, time, ifSpellCard, bonus, Hp, bossImage, bossMovement, bossBulletImage, bossPutBulletPattern, BossShootBulletPattern, dropItem, background, spellCardName = None):
        self.order = order 
        self.time = time
        self.ifSpellCard = ifSpellCard
        self.spellCardName = spellCardName
        self.bonus_origin = bonus
        self.bonus = self.bonus_origin
        self.Hp = Hp
        self.bossImage = bossImage
        self.bossMovement = bossMovement
        self.bossBulletImage = bossBulletImage
        self.bossPutBulletPattern = bossPutBulletPattern
        self.bossShootBulletPattern = BossShootBulletPattern
        self.dropItem = dropItem
        self.background = background
        
        if not self.background == None:
            self.background_rect = self.background.get_rect(topleft = parameter.getGamearea().topleft)


        self.isAlive = False
        self.isDead = False
        self.ifGenerateBoss = False
        self.ifBonus = True
        self.timer = 0


    def generateBoss(self):
        if not self.ifGenerateBoss:
            self.boss = Enemy(name = self.order, \
                            Hp = self.Hp, \
                            image = self.bossImage, \
                            movePattern = self.bossMovement, \
                            enemyBulletImage = self.bossBulletImage, \
                            putBulletPattern = self.bossPutBulletPattern, \
                            shootBulletPattern = self.bossShootBulletPattern, \
                            dropItem = self.dropItem)
            parameter.getEnemySprites().add(self.boss)
            parameter.getBossSprites().add(self.boss)
            parameter.getAllSprites().add(self.boss)
            self.ifGenerateBoss = True

    def update(self, player):
        # execute if this stage isAlive
        if self.isAlive:
            # Thoroughly kill the bullet generated by last stage
            if self.timer < 10:
                for i in parameter.getEnemyBulletSprites():
                    i.kill()
            # Generate Boss
            self.generateBoss()
            
            # If player has dead in this stage, no bonus
            if player.rect.top < 0 and self.timer > 100:
                self.ifBonus = False
                self.bonus = 0

            # Turn of this stage if boss's Hp < 0 or run out of time
            if self.boss.Hp <= 0 :
                self.isAlive = False
                self.isDead = True
                for i in (parameter.getEnemySprites() or parameter.getEnemyBulletSprites()):
                    i.kill()
                if self.ifBonus:
                    parameter.addPoint(self.bonus)
            elif self.timer > self.time:
                self.isAlive = False
                self.isDead = True
                for i in (parameter.getEnemySprites() or parameter.getEnemyBulletSprites()):
                    i.kill()
            # bonus decay by time
            if self.ifBonus:
                self.bonus -= int(self.bonus_origin / 4000)
            self.timer += 1


    def drawBackground(self, surface):
        if self.isAlive:
            # Draw background in spell card
            if not self.background == None:
                # Background fade in 
                if self.timer < 150:
                    alpha = self.timer
                else:
                    alpha = 150
                self.background.set_alpha(alpha)
                surface.blit(self.background, self.background_rect) 


    def drawInfo(self, surface, font):
        if self.isAlive:
            percentage = self.boss.Hp / self.Hp
            HpBar = pygame.Rect(128, 64, 640 * percentage, 8)
            if self.ifSpellCard:
                HpBarColor = (245, 168, 140)
            else:
                HpBarColor = (255, 255, 255)
            pygame.draw.rect(surface, HpBarColor, HpBar)

            if self.time - self.timer <= 10 * 60:
                textColor = (255, 0, 0)
            else:
                textColor = (255, 255, 255)
            function.drawText(str(int(self.order)), font[0], (255, 255, 255), surface, 80, 48)
            function.drawText("{0:2}".format(int((self.time - self.timer) / 60)), font[0], textColor, surface, 784, 48)
            if self.ifSpellCard:
                function.drawText(str(self.spellCardName), font[1], (255, 255, 255), surface, 824, 80, topRight = True)
                function.drawText(("bonus : {0:>7}".format(self.bonus)), font[0], (255, 255, 255), surface, 824, 112, topRight = True)


