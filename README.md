# Final Project - Bullet Hell
## Instructions
- [Install Pygame](http://kidscancode.org/blog/2015/09/pygame_install/)

```
注意在安裝Python時要將"Add Python to PATH"點選開來，否則建議重灌

點選：Clone or download -> Download ZIP

使用IDLE開啟"main"資料夾的"main.py"，並執行此程式

若遊戲視窗顯示過大，至：顯示設定->縮放與版面配置->變更文字、應用程式與其他項目的大小，
將縮放比例調整成100% (win10)

若有任何技術上的問題，歡迎來信聯絡：leoyeh2013@gmail.com
```
## Key Control
```
z : 射擊
shift : 按住移動速度變慢
方向鍵 : 移動
exc : 退出遊戲
```
## Game Design

- [Flow Chart](https://www.plectica.com/maps/2PZGOB4YP/edit/XVO8LRCRA?fbclid=IwAR2TEoxdSrXTuMBWuuYm5yJp0RdAc9uVFAxQt_G-pHPismyqgdYlE3BYOx0)

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
## Objects Design

### Sprites
```
    png檔, 約100*100左右, 比例最好為整數比例(ex: 1:1, 2:3, 4:3...)

        道中

            小妖精(二到三種款式，各二到三種顏色)
            中妖精(比小妖精大一倍以上，二到三種款式)

        Boss
```
### Bullets
```
    png檔, 約50 * 50左右, 比例最好為整數比例(ex: 1:1, 2:3, 4:3, 5:1...)

	(以下以東方為參考，可依照實際設計有增減)
	每種子彈設計三~四種顏色

		點彈
		小玉
		中玉
		大玉(但實際上會因為透明度問題需要克服，可先不考慮)
		米彈
		鱗彈
		刀彈

		Boss專門彈
			自由發揮
```
## Items
```
	參考東方的Item
		power(紅點)
		point(藍點)
		powerup
```
### Background
```
    註：遊玩範圍約480 * 560
    每面都需要一個背景
    或許可以畫大點(約1000 * 2000)，遊玩過程中移動鏡頭? (技術待克服)
```
### Music
```
    效果音
        射擊聲 (三到五個) (for enemy and player)
        biu (玩家撞彈聲)
        擦彈聲 (技術待克服)

    背景音樂
        起始畫面 (可先不考慮)
        每面道中 + Boss戰
        結尾畫面 (可先不考慮)
```
