from pygame import *
from random import randint
mixer.init()
window = display.set_mode((700, 500))
display.set_caption("GALAXY")
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
finish = False
mixer.music.load('space.ogg')
mixer.music.play()
clock = time.Clock()
FPS = 60
mixer.init()
font.init()
font = font.SysFont('Arial', 40)
lost = 0
wine = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE(', True, (90, 25, 70))
kills = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, speed, x, y, width, height):
        super().__init__()# ты забыл скобки здесь,
        #поэтому из sprite.Sprite не наследуются атрибуты для помещения спрайта в группу
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
            window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Buller('bullet.png', 15,self.rect.centerx, self.rect.top,  20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def __init__(self, player_image, speed, x, y, width, height):
        super().__init__(player_image, speed, x, y, width, height)
    def update(self):
        self.rect.y += self.speed
        global lost 
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(30, 420)
            lost = lost + 1

class Buller(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
                

bullets = sprite.Group()


asteroids = sprite.Group()
monsters = sprite.Group()
for i in range (5):
    enemy = Enemy('ufo.png', randint(1, 3), randint(30, 670), 30, 50, 50)
    monsters.add(enemy)
for i in range (1):
    enemys = Enemy('asteroid.png', 5, randint(30, 670), 30, 50, 50)
    asteroids.add(enemys)
rocket = Player('rocket.png', 5, 300, 400, 60, 65)
ufo = Enemy('ufo.png', 5, 20, 400, 80, 60)
asteroid = Enemy('asteroid.png', 10, 20, 400, 80, 60)









game = True
while game:
    
        
    
    window.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
            
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
    if finish != True:
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        sprites_lis1t = sprite.groupcollide(asteroids, bullets, True, True)
        for s in sprites_list:
            kills += 1
            enemy = Enemy('ufo.png', randint(1, 3), randint(30, 670), 30, 50, 50)
            monsters.add(enemy)
        for s in sprites_lis1t:
            kills += 2
            enemys = Enemy('asteroid.png', 5, randint(30, 670), 30, 50, 50)
            asteroids.add(enemys) 

        if sprite.spritecollide(rocket, monsters, False):
            window.blit(lose, (250, 200))
            finish = True
        if sprite.spritecollide(rocket, asteroids , False):
            window.blit(lose, (250, 200))
            finish = True
            
        text_lose = font.render('Пропущено: ' + str(lost), 1, (90, 25, 70))
        text_kill = font.render('Убито: ' + str(kills), 1, (90, 25, 70))
        if lost >= 10:
            window.blit(lose, (250, 200))
            finish = True
        rocket.update()
        rocket.reset()
        window.blit(text_lose, (30, 10))
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        window.blit(text_kill, (30, 50))
        if kills >= 10:
            
            window.blit(wine, (250, 200))
            finish = True
        display.update()    
    clock.tick(FPS)
    
