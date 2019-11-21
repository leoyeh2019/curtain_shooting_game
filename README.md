# Final Project - Bullet Hell
## Game Design
```
class body:
	name
	box
	image
	speed
	hp
	movement()     #player: 以鍵盤操控；enemy: 以時間對位置函數決定 
	placeBullet()  #在哪個位置放出子彈
	deathAnimate() #死亡動畫
	dropItem()     #要噴幾個item，放置在何處
```
```
class player:
	highSpeedPlayer
		body         #*
		bomb         #*
	lowSpeedPlayer #低速模式
		body         #*
		bomb         #*
	switchType()
    life           #有幾條命
	bombQuantity   #一條life有幾個bomb
```
```
class enemy:
	body           #*
	timer          #紀錄在場上時間
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
class bullet:
	name
	box
	image
	damage
	timer          #紀錄在場上時間
	pattern()      #決定移動軌跡: 建立一個x = f(t), y = g(t)的函數
```
```
class bomb:
	damage
	timer          #紀錄放bomb時間
	animate()      #放bomb動畫
```
	
