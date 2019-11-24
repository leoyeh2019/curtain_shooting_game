# Final Project - Bullet Hell
## Game Design
```
class body():
	
```
```
class bullet(name, rect, image, damage):
	void bulletMove(patternX, patternY)
	
```
```
class player(name, rect, image, hp, bulletList, bulletPatternX, bulletPatternY, fastspeed, slowspeed):
	void playerMove(gamearea, slowMode, moveLeft, moveRight, moveUp, moveDown)
		# self.rect.move_ip(bulletPatternX, bulletPatternY)
	void shootBullet(shooting, time, gamearea, patternX, patternY)
		# append bullet in bulletList
	
```
```
class enemy(name, rect, image, hp, movingPatternX, movingPatternY):
	void enemyMove()
		# self.rect.move_ip(movingPatternX, movingPatternY)
```
```
class boss:
	enemy          #*
	stage          #記錄不同符卡
```
```
class item:
	name
	box
	speed          #掉落速度
```
```
class bomb:
	damage
	timer          #紀錄放bomb時間
	animate()      #放bomb動畫
```
	
