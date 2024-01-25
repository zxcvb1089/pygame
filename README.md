# pygame - 太空生存戰 

這個遊戲主要讓我學習製作過程中，運用pygame的模組加入文字、圖像、聲音、還有碰撞等等，運用 for迴圈 還有 if判斷 創建類別(class)操作sprite 和定義(def) 各種函式 寫出整個遊戲的架構，以Windows系統開發。

```pip install pygame ```

# pygame - 核心技術

```pygame.Surface```  代表一個矩形的影像，用來繪製在螢幕上

```pygame.Rect```   資料型別，用來定位矩形空間的位置和可以用來偵測物件是否碰撞的

```pygame.event``` 事件模組，用來處理使用者觸發事件，包含自定義事件

```pygame.font``` 文字模組，用來顯示文字，可用來顯示儀表板資料

```pygame.draw``` 繪圖模組，可以畫出多邊形圖形，可當作背景物件

```pygame.image``` 圖片模組，用來處理載入圖片等相關操作，可當作角色精靈（sprite）

```pygame.time``` 時間模組，包含控制遊戲迴圈迭代速率，確保反饋不會太快消逝

# 基礎架構
```
   import pygame

   FPS = 60
   WIDTH =
   HEIGHT = 
```

創間初始化 和 視窗

```
   pygame.init()
   screen = pygame.display.set_mode((WIDTH,HEIGHT))
   clock = pygame.time.Clock() #創建一個物件

   running TRUE
```

遊戲迴圈(Game loop)
![遊戲迴圈過程](https://github.com/zxcvb1089/pygame/assets/152964756/59fd563f-a0a1-4088-a801-119542d654f2)

```
while running:
    clock.tick(FPS) #在一秒鐘之內 最多只能執行()次
# 取得輸入(process input)
    for event pygame.event.get():#回傳發生的所有事件
        if event.type == pygame.QUIT()
            running = False
# 更新遊戲
# 畫面顯示
    screen.fill(R,G,B)
    pygame.display.update()

pygame.quit()
```

# 過程

# 最後
想要建立一個 安裝程式檔
```
pip install auto-py-to-exe
```
在執行
```
python -m auto_py_to_exe
```

把要得檔案放在同一個資料夾，壓縮後再運用了 NSIS 的軟件 創建exe安裝檔 即完成。

