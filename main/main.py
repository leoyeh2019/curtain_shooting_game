import pygame, sys, random, math, time, json
from pygame.locals import *
from os import path
import parameter
import classes
import custom 
import function
import sound


# ----------------------Constants----------------------
WINDOWWIDTH = 1280
WINDOWHEIGHT = 960


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 255, 255)

FPS = 60

BACKGROUND_WIDTH = 768
BACKGROUND_HEIGHT = 1440

PLAYER_WIDTH = 100
PLAYER_HEIGHT = 120
PLAYER_COLLISION_BOXSIZE = 15
PLAYER_BULLET_WIDTH = 10
PLAYER_BULLET_HEIGHT = 20

ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
ENEMY_BULLET_WIDTH = 10
ENEMY_BULLET_HEIGHT = 20

BOSS_WIDTH = 200
BOSS_HEIGHT = 200

BOSS_BULLET_1_WIDTH = 51
BOSS_BULLET_1_HEIGHT = 66

ITEM_WIDTH = 20
ITEM_HEIGHT = 20



# ----------------------Pygame Initiate----------------------
pygame.init()
pygame.mixer.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Curtain_Shooting_Game")
pygame.mouse.set_visible(False)


# ----------------------Loading----------------------
img_dir = path.join(path.dirname(__file__), "img")
music_dir = path.join(path.dirname(__file__), "music")
font_dir = path.join(path.dirname(__file__), "font")

coverBackgroundImg = pygame.image.load(path.join(img_dir, 'cover_background.png')).convert()

goodendingImage = pygame.image.load(path.join(img_dir, 'goodending_background.png')).convert()

badendingImage = pygame.image.load(path.join(img_dir, 'badending_background.png')).convert()

background_raw = pygame.image.load(path.join(img_dir, 'background2.png')).convert()
background = pygame.transform.scale(background_raw, (WINDOWWIDTH, WINDOWHEIGHT))
background.set_colorkey(WHITE)
background_rect = background.get_rect()

gameareaBackgroundImg_raw = pygame.image.load(path.join(img_dir, 'background.png')).convert()
gameareaBackgroundImg = pygame.transform.scale(gameareaBackgroundImg_raw, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

playerImg_raw = pygame.image.load(path.join(img_dir, 'player.png')).convert()
playerImg = pygame.transform.scale(playerImg_raw, (PLAYER_WIDTH, PLAYER_HEIGHT))
playerImg.set_colorkey(WHITE)
playerCollisionBoxImg_raw = pygame.image.load(path.join(img_dir, 'playerCollisionBox.png')).convert()
playerCollisionBoxImg = pygame.transform.scale(playerCollisionBoxImg_raw, (PLAYER_COLLISION_BOXSIZE, PLAYER_COLLISION_BOXSIZE))
playerCollisionBoxImg.set_colorkey(WHITE)

playerBulletImg = pygame.image.load(path.join(img_dir, 'player_bullet.png')).convert()
playerBulletImg.set_colorkey(WHITE)
playerBulletImg.set_alpha(128) # Transparent

playerBulletTrackingImg = pygame.image.load(path.join(img_dir, 'player_bullet_tracking.png')).convert()
playerBulletTrackingImg.set_colorkey(WHITE)
playerBulletTrackingImg.set_alpha(128) # Transparent



powerItemImg_raw = pygame.image.load(path.join(img_dir, 'power_item.png')).convert()
powerItemImg = pygame.transform.scale(powerItemImg_raw, (ITEM_WIDTH, ITEM_HEIGHT))

pointItemImg_raw = pygame.image.load(path.join(img_dir, 'point_item.png')).convert()
pointItemImg = pygame.transform.scale(pointItemImg_raw, (ITEM_WIDTH, ITEM_HEIGHT))           

bossImg_raw = pygame.image.load(path.join(img_dir, 'boss.png')).convert()
bossImg = pygame.transform.scale(bossImg_raw, (BOSS_WIDTH, BOSS_HEIGHT))
bossImg.set_colorkey(WHITE)

lifeImg = pygame.image.load(path.join(img_dir, 'life_image.png')).convert()
lifeImg.set_colorkey(WHITE)


enemyImgList = []

for i in range(0, 2):
    image = pygame.image.load(path.join(img_dir, 'enemy_{}.png'.format(i))).convert()
    image.set_colorkey(WHITE)
    enemyImgList.append(image)

enemyBulletImgList = []

for i in range(0, 10):
    image = pygame.image.load(path.join(img_dir, 'enemy_bullet_{}.png'.format(i))).convert()
    image.set_colorkey(WHITE)
    enemyBulletImgList.append(image)

bossBulletImgList = []

for i in range(0, 4):
    image = pygame.image.load(path.join(img_dir, 'boss_bullet_{}.png'.format(i))).convert()
    image.set_colorkey(WHITE)
    bossBulletImgList.append(image)

bossSpellCardBackgroundImgList = []

for i in range(0, 5):
    image = pygame.image.load(path.join(img_dir, 'boss_spell_card_background_{}.png'.format(i))).convert()
    bossSpellCardBackgroundImgList.append(image)

bgmList = []
for i in range(0, 4):
    bgm = path.join(music_dir, 'bgm_{}.mp3'.format(i))
    bgmList.append(bgm)


# ----------------------Fonts----------------------

Helvetica_24 = pygame.font.Font(path.join(font_dir, "Helvetica.ttf"), 24)
Inconsolata_24 = pygame.font.Font(path.join(font_dir, "Inconsolata.otf"), 24)
Inconsolata_32 = pygame.font.Font(path.join(font_dir, "Inconsolata.otf"), 32)
DFXingShu_32 = pygame.font.Font(path.join(font_dir, "DFXingShu-B5 DFFT-S5.TTC"), 32)


# ----------------------Functions----------------------
def terminate():
    pygame.quit()
    sys.exit()


def startGameScreen(background, bgm, topleft):
    background_rect = background.get_rect(topleft = topleft)
    windowSurface.blit(background, background_rect)
    pygame.display.update()
    pygame.mixer.music.load(bgm)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=1)

    waiting = True
    while waiting:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_z:
                    pygame.mixer.music.stop()
                    waiting = False
        
        mainClock.tick(FPS)

    # Clear parameter
    for i in parameter.getAllSprites():
        i.kill()
    parameter.clearTimer()
    parameter.clearPoint()




def generateItem(enemy, number, name, image):
    while True:
        check = True
        itemList = []
        for i in range(number):
            item = classes.Item(name = name, \
                                image = image, \
                                generatePosition = (enemy.rect.center[0] + random.randint(-enemy.rect.width * 1, enemy.rect.width *1), \
                                                    enemy.rect.center[1] + random.randint(-enemy.rect.height *1, enemy.rect.height *1)))
            itemList.append(item)
        for i in range(len(itemList)):
            for j in range(len(itemList) - i - 1):
                if pygame.sprite.collide_rect(itemList[i], itemList[i + j + 1]):
                    check = False
        if check:
            break
    for i in range(len(itemList)):
        parameter.getAllSprites().add(itemList[i])
        parameter.getItemSprites().add(itemList[i])




# ----------------------Main----------------------
if __name__ == "__main__":

    while True:

        startGameScreen(coverBackgroundImg, bgmList[0], (0, 0))
        # Set Gamearea
            # Set in parameter.py

        # Read config

        with open(path.join(path.dirname(__file__), "config.json"), "r") as config:
            config_dic = json.load(config)
        highscore = config_dic["highscore"]

        # Set parameter
        running = True 
        stageInitiated = True


        # Set player, enemy, bullet
        gameareaBackground1 = classes.Background(image = gameareaBackgroundImg, \
                                                topleft = function.raletivePosition(parameter.getGamearea().topleft, (0, -1440)),\
                                                speed = 1)
        gameareaBackground2 = classes.Background(image = gameareaBackgroundImg, \
                                                topleft = parameter.getGamearea().topleft,\
                                                speed = 1)
                                            
        parameter.getBackgroundSprites().add(gameareaBackground1)
        parameter.getBackgroundSprites().add(gameareaBackground2)

        player = classes.Player(name = "player", \
                                lifes = 1, \
                                image = playerImg, \
                                collisionBoxImage = playerCollisionBoxImg, \
                                playerBulletImage = (playerBulletImg, playerBulletTrackingImg), \
                                playerSpeed = (7, 4), \
                                playerDamage = (6, 4), \
                                putBulletPattern = (custom.playerPutbulletPattern, custom.playerPutBulletPattern_tracking), \
                                shootBulletPattern = (custom.playerShootBulletPattern, custom.playerShootBulletPattern_tracking))




        def newEnemy_1():
            enemy = classes.Enemy(name = "enemy", \
                                Hp = 250, \
                                image = enemyImgList[0], \
                                movePattern = custom.enemyMovePattern_1, \
                                enemyBulletImage = [enemyBulletImgList[1]], \
                                putBulletPattern = [custom.enemyPutBulletPattern_1], \
                                shootBulletPattern = [custom.enemyshootBulletPattern_1], \
                                dropItem = (2, 2))
            parameter.getAllSprites().add(enemy)
            parameter.getEnemySprites().add(enemy)

        def newEnemy_2():
            enemy = classes.Enemy(name = "enemy", \
                                Hp = 30, \
                                image = enemyImgList[1], \
                                movePattern = custom.enemyMovePattern_2, \
                                enemyBulletImage = [enemyBulletImgList[8]], \
                                putBulletPattern = [custom.enemyPutBulletPattern_2], \
                                shootBulletPattern = [custom.enemyshootBulletPattern_2], \
                                dropItem = (2, 4))
            parameter.getAllSprites().add(enemy)
            parameter.getEnemySprites().add(enemy)
        def newEnemy_3():
            enemy = classes.Enemy(name = "enemy", \
                                Hp = 30, \
                                image = enemyImgList[1], \
                                movePattern = custom.enemyMovePattern_3, \
                                enemyBulletImage = [enemyBulletImgList[8]], \
                                putBulletPattern = [custom.enemyPutBulletPattern_3], \
                                shootBulletPattern = [custom.enemyshootBulletPattern_3], \
                                dropItem = (1, 4))
            parameter.getAllSprites().add(enemy)
            parameter.getEnemySprites().add(enemy)

        parameter.getAllSprites().add(player)
        parameter.getAllSprites().add(player.collisionBox)

        def newEnemy_4():
            enemy = classes.Enemy(name = "enemy", \
                                Hp = 4000, \
                                image = enemyImgList[0], \
                                movePattern = custom.enemyMovePattern_4, \
                                enemyBulletImage = [enemyBulletImgList[9]], \
                                putBulletPattern = [custom.enemyPutBulletPattern_4], \
                                shootBulletPattern = [custom.enemyshootBulletPattern_4], \
                                dropItem = (8, 10))
            parameter.getAllSprites().add(enemy)
            parameter.getEnemySprites().add(enemy)

        parameter.getAllSprites().add(player)
        parameter.getAllSprites().add(player.collisionBox)


        stageList = []
        boss_stage_1 = classes.BossStage(order = 1, \
                                        time = 60 * 60, \
                                        ifSpellCard = False, \
                                        bonus = 0, \
                                        Hp = 3000, \
                                        bossImage = bossImg, \
                                        bossMovement = custom.bossMovePattern_1, \
                                        bossBulletImage = [bossBulletImgList[0]], \
                                        bossPutBulletPattern = [custom.bossPutBulletPattern_1], \
                                        BossShootBulletPattern = [custom.bossShootBulletPattern_1], \
                                        dropItem = (0, 0), \
                                        background = None)
        stageList.append(boss_stage_1)
        boss_stage_2 = classes.BossStage(order = 2, \
                                        time = 60 * 60, \
                                        ifSpellCard = True, \
                                        bonus = 10000000, \
                                        Hp = 4500, \
                                        bossImage = bossImg, \
                                        bossMovement = custom.bossMovePattern_2, \
                                        bossBulletImage = [enemyBulletImgList[9], enemyBulletImgList[9], enemyBulletImgList[9], enemyBulletImgList[9]], \
                                        bossPutBulletPattern = [custom.bossPutBulletPattern_2_1, custom.bossPutBulletPattern_2_2, custom.bossPutBulletPattern_2_3, custom.bossPutBulletPattern_2_4], \
                                        BossShootBulletPattern = [custom.bossShootBulletPattern_2_1, custom.bossShootBulletPattern_2_1, custom.bossShootBulletPattern_2_3, custom.bossShootBulletPattern_2_3], \
                                        dropItem = (8, 16), \
                                        background = bossSpellCardBackgroundImgList[0], \
                                        spellCardName = "喜形　最是滿城飛絮時")
        stageList.append(boss_stage_2)
        boss_stage_3 = classes.BossStage(order = 3, \
                                        time = 60 * 60, \
                                        ifSpellCard = False, \
                                        bonus = 0, \
                                        Hp = 3000, \
                                        bossImage = bossImg, \
                                        bossMovement = custom.bossMovePattern_3, \
                                        bossBulletImage = [bossBulletImgList[1]], \
                                        bossPutBulletPattern = [custom.bossPutBulletPattern_3], \
                                        BossShootBulletPattern = [custom.bossShootBulletPattern_3], \
                                        dropItem = (0, 0), \
                                        background = None)
        stageList.append(boss_stage_3)
        boss_stage_4 = classes.BossStage(order = 4, \
                                        time = 60 * 60, \
                                        ifSpellCard = True, \
                                        bonus = 10000000, \
                                        Hp = 4500, \
                                        bossImage = bossImg, \
                                        bossMovement = custom.bossMovePattern_4, \
                                        bossBulletImage = [enemyBulletImgList[0], enemyBulletImgList[1]], \
                                        bossPutBulletPattern = [custom.bossPutBulletPattern_4_1, custom.bossPutBulletPattern_4_2], \
                                        BossShootBulletPattern = [custom.bossShootBulletPattern_4_1, custom.bossShootBulletPattern_4_2], \
                                        dropItem = (8, 16), \
                                        background = bossSpellCardBackgroundImgList[1], \
                                        spellCardName = "怒面　夜夢幽回碎月處")
        stageList.append(boss_stage_4)
        boss_stage_5 = classes.BossStage(order = 5, \
                                        time = 60 * 60, \
                                        ifSpellCard = False, \
                                        bonus = 0, \
                                        Hp = 3000, \
                                        bossImage = bossImg, \
                                        bossMovement = custom.bossMovePattern_5, \
                                        bossBulletImage = [bossBulletImgList[2]], \
                                        bossPutBulletPattern = [custom.bossPutBulletPattern_5], \
                                        BossShootBulletPattern = [custom.bossShootBulletPattern_5], \
                                        dropItem = (0, 0), \
                                        background = None)
        stageList.append(boss_stage_5)
        boss_stage_6 = classes.BossStage(order = 6, \
                                        time = 60 * 60, \
                                        ifSpellCard = True, \
                                        bonus = 10000000, \
                                        Hp = 4500, \
                                        bossImage = bossImg, \
                                        bossMovement = custom.bossMovePattern_6, \
                                        bossBulletImage = [(enemyBulletImgList[2], enemyBulletImgList[3])], \
                                        bossPutBulletPattern = [custom.bossPutBulletPattern_6], \
                                        BossShootBulletPattern = [custom.bossShootBulletPattern_6], \
                                        dropItem = (8, 16), \
                                        background = bossSpellCardBackgroundImgList[2], \
                                        spellCardName = "哀意　似水寂情溢於表")
        stageList.append(boss_stage_6)
        boss_stage_7 = classes.BossStage(order = 7, \
                                        time = 60 * 60, \
                                        ifSpellCard = False, \
                                        bonus = 0, \
                                        Hp = 3000, \
                                        bossImage = bossImg, \
                                        bossMovement = custom.bossMovePattern_7, \
                                        bossBulletImage = [bossBulletImgList[3], bossBulletImgList[3]], \
                                        bossPutBulletPattern = [custom.bossPutBulletPattern_7_1, custom.bossPutBulletPattern_7_2], \
                                        BossShootBulletPattern = [custom.bossShootBulletPattern_7_1, custom.bossShootBulletPattern_7_2], \
                                        dropItem = (0, 0), \
                                        background = None)
        stageList.append(boss_stage_7)
        boss_stage_8 = classes.BossStage(order = 8, \
                                        time = 60 * 60, \
                                        ifSpellCard = True, \
                                        bonus = 10000000, \
                                        Hp = 4500, \
                                        bossImage = bossImg, \
                                        bossMovement = custom.bossMovePattern_8_1, \
                                        bossBulletImage = [(enemyBulletImgList[4], enemyBulletImgList[5]), (enemyBulletImgList[6], enemyBulletImgList[7])], \
                                        bossPutBulletPattern = [custom.bossPutBulletPattern_8_1, custom.bossPutBulletPattern_8_1], \
                                        BossShootBulletPattern = [custom.bossShootBulletPattern_8_1, custom.bossShootBulletPattern_8_1], \
                                        dropItem = (8, 16), \
                                        background = bossSpellCardBackgroundImgList[3], \
                                        spellCardName = "樂符　暮色天光落如塵")
        stageList.append(boss_stage_8)

        boss_stage_9 = classes.BossStage(order = 9, \
                                        time = 120 * 60, \
                                        ifSpellCard = True, \
                                        bonus = 30000000, \
                                        Hp = 9, \
                                        bossImage = bossImg, \
                                        bossMovement = custom.bossMovePattern_9, \
                                        bossBulletImage = [bossBulletImgList[0], bossBulletImgList[1], bossBulletImgList[2], bossBulletImgList[3]], \
                                        bossPutBulletPattern = [custom.bossPutBulletPattern_9_1, custom.bossPutBulletPattern_9_1, custom.bossPutBulletPattern_9_1, custom.bossPutBulletPattern_9_1], \
                                        BossShootBulletPattern = [custom.bossShootBulletPattern_9_1, custom.bossShootBulletPattern_9_1, custom.bossShootBulletPattern_9_1, custom.bossShootBulletPattern_9_1], \
                                        dropItem = (8, 16), \
                                        background = bossSpellCardBackgroundImgList[4], \
                                        spellCardName = "終符　紛情亂緒點空明")
        stageList.append(boss_stage_9)

        # Play Music
        pygame.mixer.music.load(bgmList[1])
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=1)

        # Game loop
        while running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        running = False
            # Generate Enemy
            if parameter.getTimer() >= 500 and parameter.getTimer() <= 2000:
                if (parameter.getTimer()  - 500) % 500 == 0:
                    newEnemy_1()
            
            if parameter.getTimer() >= 2600 and parameter.getTimer() <= 3600:
                if (parameter.getTimer()  - 2600) % 50 == 0:
                    newEnemy_2()
                    newEnemy_3()
            
            if parameter.getTimer() == 3900:
                newEnemy_4()
            
            if parameter.getTimer() >= 5000 and stageInitiated:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(bgmList[2])
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(loops=-1)
                stageList[0].isAlive = True
                stageInitiated = False
                
            for i in range(len(stageList)):
                if stageList[i].isDead:
                    if i == len(stageList) - 1:
                        parameter.addPoint(10000000 * player.lifes)
                        goodending = True
                        running = False
                    else:
                        stageList[i+1].isAlive = True
                        stageList[i].isDead = False
                stageList[i].update(player)

            
            
            if parameter.getTimer() > 50 and not bool(parameter.getEnemySprites()):
                for i in parameter.getBackgroundSprites():
                    i.speed = 5
            else:
                for i in parameter.getBackgroundSprites():
                    i.speed = 2
            
            
            parameter.getBackgroundSprites().update()
            parameter.getAllSprites().update()

            # Collidision Destction

            # Player_Bullet v.s. Enemy
            for e in parameter.getEnemySprites():
                for pb in parameter.getPlayerBulletSprites():
                    if pygame.sprite.collide_rect(e, pb):
                        pb.kill()
                        e.Hp -= pb.damage
                        parameter.addPoint(100)
                if e.Hp < 0:
                    sound.enemy_dead_SE.play()
                    generateItem(e, e.dropItem[0], "power", powerItemImg)
                    
                    generateItem(e, e.dropItem[1], "point", pointItemImg)
                    e.kill()
                    parameter.addPoint(10000)
                            
                            
                            

            # Enemy_Bullet v.s. Player
            for eb in parameter.getEnemyBulletSprites():
                if eb.radius > 0:
                    if pygame.sprite.collide_circle(eb, player):
                        sound.player_dead_SE.play()
                        player.hide()
                        player.lifes -= 1

            # Point_Item v.s. Player
            for p in parameter.getItemSprites():
                if pygame.sprite.collide_circle(p, player):
                    sound.pick_item_SE.play()
                    if p.name == "point":
                        parameter.addPoint(100000)
                    if p.name == "power":
                        player.power += 1
                        if player.power > 48:
                            player.power = 48
                    p.kill()
            
            # Check if player die
            if player.lifes == 0:
                goodending = False
                running = False

            # Draw
            windowSurface.fill(BLACK)
            pygame.draw.rect(windowSurface, WHITE, parameter.getGamearea())
            parameter.getBackgroundSprites().draw(windowSurface)
            for i in stageList:
                i.drawBackground(windowSurface)
            """
            check if the bullet just generated
            use 'blit' to draw sprites one by one
            """
            for i in parameter.getAllSprites():
                if i in parameter.getEnemyBulletSprites() or i in parameter.getPlayerBulletSprites():
                    if parameter.getTimer() - i.generateTime > 1:
                        windowSurface.blit(i.image, i.rect)

                else:
                    windowSurface.blit(i.image, i.rect)

        

            windowSurface.blit(background, background_rect)

            for i in stageList:
                i.drawInfo(windowSurface, [Inconsolata_32, DFXingShu_32])

            for i in range(player.lifes):
                rect = lifeImg.get_rect(topleft = (1040 + i * 30, 194))
                windowSurface.blit(lifeImg, rect)

            function.drawText("HighScore  {0:0>12}".format(highscore), Inconsolata_32, BLACK, windowSurface, 864, 64)
            function.drawText("Score      {0:0>12}".format(parameter.getPoint()), Inconsolata_32, BLACK, windowSurface, 864, 128)
            function.drawText("Lifes      ", Inconsolata_32, BLACK, windowSurface, 864, 192)
            function.drawText("Power      {0:0>3}".format(player.power), Inconsolata_32, BLACK, windowSurface, 864, 256)
            
            # Display Update
            pygame.display.update()

            mainClock.tick(FPS)
            parameter.accTimer()
        
        #　Check highscore
        if parameter.getPoint() > highscore:
            config_dic["highscore"] = parameter.getPoint()
            with open(path.join(path.dirname(__file__), "config.json"), "w") as config:
                json.dump(config_dic, config)


        # Game end cover
        if goodending:
            startGameScreen(goodendingImage, bgmList[3], (64, 32))
        else:
            startGameScreen(badendingImage, bgmList[3], (64, 32))

        

