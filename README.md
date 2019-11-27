# Final Project - Bullet Hell
## Game Design
```
https://www.plectica.com/maps/2PZGOB4YP/edit/XVO8LRCRA?fbclid=IwAR2TEoxdSrXTuMBWuuYm5yJp0RdAc9uVFAxQt_G-pHPismyqgdYlE3BYOx0
```
```
class(attribute, function...)
state(object) # using JSON
main(load data, logic)
view(draw)
```
```
class body(name, ):
```
```
class bullet(name, rect, image, damage):
	void bulletMove(pattern(x(t), y(t)))
```
```
class player(name, rect, image, hp, fastspeed, slowspeed, bulletList, bulletPattern(x(t), y(t))):
	void playerMove(gamearea, slowModeKeyControl, movingKeyControl(moveLeft, moveRight, moveUp, moveDown))
		self.rect.move_ip(bulletPattern(x(t), y(t)))
	void shootBullet(shootingKeyControl, time, gamearea, movingPattern(x(t), y(t)))
		append bullet in bulletList
	
```
```
class enemy(name, rect, image, hp, movingPattern(x(t), y(t))):
	void enemyMove()
		# self.rect.move_ip(movingPattern(x(t), y(t)))
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
	
