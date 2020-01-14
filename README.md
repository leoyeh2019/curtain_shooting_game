# Final Project - Curtain Shooting Game
## Introduction
```
此遊戲以經典彈幕遊戲東方project為參考，
希望藉由此遊戲讓大家感受到躲避子彈並欣賞彈幕美感的樂趣。
若對這類遊戲有興趣，歡迎上網搜尋"東方project系列"(如：東方妖妖夢、東方永夜抄......)。
```
## Instructions
- [Install Pygame](http://kidscancode.org/blog/2015/09/pygame_install/)

```
注意在安裝Python時要將"Add Python to PATH"點選開來，否則建議重灌

於github頁面點選：Clone or download -> Download ZIP

使用IDLE開啟"main"資料夾的"main.py"，並執行此程式

若遊戲視窗顯示過大，至：顯示設定->縮放與版面配置->變更文字、應用程式與其他項目的大小，
將縮放比例調整成100% (win10)

若有任何技術上的問題，歡迎來信聯絡：leoyeh2013@gmail.com
```
![](https://datatofish.com/wp-content/uploads/2019/03/000_pyinstaller.png)
![](https://i.imgur.com/BDPzXC9.png)
## Key Control
```
z : 射擊
shift : 按住移動速度變慢
方向鍵 : 移動
exc : 退出遊戲
```
## Update
```
5.1.0 (2020/01/14) : 新增註解
	
```
## Object-Oriented Programming Introduction
- [OOP](https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/117823/?fbclid=IwAR2c-kSx1kGrDHfgfBiEN6_WS506O-G0yl6X2_UfaxPQQUIKCFZQx-eMXtc#outline__1_4_2)
## Pygame Introduction
- [Pygame](http://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/)
- [Pygame Sprites - 1](http://kidscancode.org/blog/2016/08/pygame_1-2_working-with-sprites/)
- [Pygame Sprites - 2](http://kidscancode.org/blog/2016/08/pygame_1-3_more-about-sprites/)

## Game Design

- [Flow Chart](https://www.plectica.com/maps/2PZGOB4YP/edit/XVO8LRCRA?fbclid=IwAR2TEoxdSrXTuMBWuuYm5yJp0RdAc9uVFAxQt_G-pHPismyqgdYlE3BYOx0)

### Main
```
設定遊戲參數
匯入所需圖片、音樂
遊戲主迴圈
	Update -> Draw -> Flip
邏輯判斷
	碰撞偵測
```
### Class
#### Background
```
Update
	遊戲背板的移動控制
	當移動到視窗外時，叫出新的背板並自殺
```
#### Player
```
Update
	當玩家被判定為死亡時 -> 暫時將玩家隱藏，並給予一段無敵時間
	接收鍵盤的Input -> 做出相對應的移動或射擊
	回傳自身位置給parameter.py

Shoot
	當符合條件時生成子彈
	依照自身的power值決定生成多少子彈

Hide
	當玩家撞到子彈死亡時執行此函數 -> 隱藏玩家
```
#### Enemy
```
Update
	由輸入的函數決定移動方式
		move_ip(x, y) : 每幀移動(x, y)格
	當enemy移出螢幕外 -> 自殺

Shoot
	由輸入的函數決定生成的子彈
```
#### Player Bullet
```
Update
	由輸入的函數決定移動方式
```
#### PlayerBullet_tracking
```
Update
	嘗試找到與自身位置最接近的敵人 -> 修正自身的移動方向使得更靠近敵人
Rotate
	依照自身的移動方向進行旋轉
		決定旋轉軸向 -> 紀錄旋轉前中心 -> 由原始圖片旋轉
```
- [Rotate](http://kidscancode.org/blog/2016/08/pygame_shmup_part_6/)
#### EnemyBullet
```
Update
	由輸入的函數決定移動方式
		但由於使用move_ip會無法移動小數點距離，
		因此採用將enemy.rect.center隨時間放到函數設定好的移動軌跡上

Rotate
	依照自身的移動方向進行旋轉
```
#### EnemyBullet_tracking
```
Update
	由玩家的位置決定移動方向

Rotate
	依照自身的移動方向進行旋轉
```
#### EnemyBullet_deathGenerate
```
Update
	繼承EnemyBullet父類別的update()，
	並於接觸到遊戲範圍底部時自殺 

Kill
	當自殺時，生成新的子彈
	繼承pygame.sprite.Sprite父類別的kill()
```
#### EnemyBullet_decay
```
Update
	隨時間生成而從透明(無判定)變不透明(有判定)
	一定時間後開始移動
```
#### Item
```
Update
	控制Item的掉落速度
```
#### BossStage
```
由內部參數控制階段
self.isAlive -> 是否更新此階段
self.isDead -> 是否呼叫下一個階段

GenerateBoss
	生成Boss

Update
	清除上一階段的子彈
	生成Boss
	判斷玩家是否有死亡過(作為給bonus的依據)
	當Boss血量歸零 or 超過時間 -> 結束這個stage
	隨著時間降低bonus

DrawBackground
	於符卡戰時 -> 新增背景

DrawInfo
	畫血條、剩餘血條數、時間、符卡名、bonus
```
### Custom
```
建立玩家、敵人的移動函數、子彈放置函數與子彈移動函數

MovePattern
	每幀移動多少(x, y)

PutBulletPattern 
	numbers : 一次放多少顆子彈
	position : 子彈放在哪裡(相對自己)
	delateTime : enemy生成幾幀才開始放子彈
	intermediateTime : 間隔幾幀放子彈

ShootBulletPattern
	f(x) : 紀錄子彈移動軌跡(x, y 對於t的參數式)
	f'(x) :  紀錄子彈移動方向 -> 作為rotate的依據

DeathGenerate
	判定是否是EnemyBullet_deathGenerate

generateBullet
	EnemyBullet_deathGenerate自殺後生成的子彈pattern

Decay
	判定是否是EnemyBullet_decay
```
### Function
```
存放常用自定義函數
```
### Sound
```
存放音效
```
### Parameter
```
存放各個參數，使得每個程式都能存取
```
### Config
```
紀錄最高分數
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
