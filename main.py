#1.sprite #2.操控sprite #3.石頭 sprite #4. 子彈sprite & 碰撞處理 #5. 載入圖片 
#6.加強碰撞判斷 #7.石頭動畫 #8.遊戲分數 #9.加入音效(爆炸跟音樂)
#10.增加生命條 #11.增加爆炸動畫 #12.增加復活次數
#13.石頭掉寶 #14.初始畫面 #15.打包遊戲
import pygame
import random #隨機的模組
import os

FPS = 60 #全部用大寫命名 習慣用大寫 代表設定好就"不太會"改變他
WIDTH = 500
HEIGHT = 600

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#遊戲的初始化 和創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("第一個遊戲")
clock = pygame.time.Clock()

#載入圖片
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()#convert 是轉換pygame的格式用
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)
#rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img", "shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img", "gun.png")).convert()
    
#載入音樂、音效
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.2)

font_name = os.path.join("font.ttf")
def draw_text(surf, text, size, x, y):#傳入幾個參數 1.平面上 2.文字 3.文字大小 4.座標
    font = pygame.font.Font(font_name, size)#font 文字的物件 傳入的參數 1.字體 2.文字的大小
    text_surface = font.render(text, True, WHITE)#render 渲染出來
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)# 畫填滿的方形
    pygame.draw.rect(surf, WHITE, outline_rect, 2)# 畫外框

def draw_lives(surf, lives, img, x, y):# 劃出剩下幾條命
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 32*i #做定位 
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0,0))
    draw_text(screen, '太空生存戰!!!', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, '← → 移動飛船 空白鍵發射子彈~', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按任意鍵或是切英 開始遊戲!!', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)#在一秒鐘之內，最多執行()次
        #取得輸入
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               return True
           elif event.type == pygame.KEYUP:# KEYDOWN 是按下去 就直接開始 KEYUP 是雙開的時候 才會開始~
                waiting = False
                return False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))  #但照片太大 還有黑色框框
        self.image.set_colorkey(BLACK)
        #self.image.fill(GREEN  )
        self.rect = self.image.get_rect()
        self.radius = 20 #radius 表示碰撞判斷的半徑
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2 
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2 
            self.rect.bottom = HEIGHT - 10 

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:# RIGHT可以改成鍵盤數字
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()


    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs) #ori 原始
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int (self.rect.width * 0.87 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width) 
        self.rect.y = random.randrange(-180, -100) 
        self.speedy = random.randrange(2, 5)
        self.speedx = random.randrange(-3, 3)
        # 為了不要讓旋轉失偵
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.rot_degree) #rotate 旋轉 但是會失偵數，會一直疊加
        # 寫出重新定位
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx 
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0: 
            self.rect.x = random.randrange(0, WIDTH - self.rect.width) 
            self.rect.y = random.randrange(-100, -40) 
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y 
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
           
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):# 爆炸中心點 , 爆炸大小
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 #代表更新到第幾張圖片
        self.last_update = pygame.time.get_ticks()# 這個函式回傳給我們從初始化經過的毫秒數
        self.frame_rate = 50 #至少要經過幾毫秒 才會更新圖片
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    new_rock()
score = 0 
pygame.mixer.music.play(-1)# (-1)重複無限撥放

#遊戲迴圈
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0

    clock.tick(FPS)#在一秒鐘之內，最多執行()次
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #更新遊戲
    all_sprites.update()
    # 判斷石頭 子彈碰撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:#他會回傳0到1的值喔! 
            pow = Power(hit.rect.center)
            all_sprites.add(pow) 
            powers.add(pow)
        new_rock()
    #判斷石頭 飛船碰撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle) #spritecollide 這個函式 是矩形的碰撞判斷~~
    for hit in hits:
        new_rock()
        player.health -= hit.radius * 3
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()

    #判斷寶物 飛船碰撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 20
            if player.health > 100:
                player.health = 100
            shield_sound.play()
        if hit.type == 'gun':
            player.gunup()
            gun_sound.play()

    if player.lives == 0 and not(death_expl.alive()):
        show_init = True

    #畫面顯示
    screen.fill(BLACK)#元組(R,G,B)
    screen.blit(background_img, (0,0))#blit 畫的意思 #(0,0) xy 座標
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    pygame.display.update()

pygame.quit()