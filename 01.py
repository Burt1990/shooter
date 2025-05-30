from pygame import *
from random import randint
init()
window = display.set_mode((800, 600))
background = Surface((800, 600))
background.fill((66, 68, 90))
display.set_caption("Platformer")
worldweeds = 5000
worldshift = 0
game = True
font = font.SysFont('Arial', 40)
FPS = 60
lose = font.render('YOU LOSE', True, (90, 25, 70))

clock = time.Clock()
class Player(sprite.Sprite):
    def __init__(self, x, y):        
        sprite.Sprite.__init__(self)
        self.image = Surface((40, 40), SRCALPHA)
        draw.circle(self.image, (255, 234, 59), (20, 20), 20)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (x, y)
        self.speed = 5
        self.jump_power = 15
        self.on_ground = True
        self.velocity_y = 0
        self.gravity = 0.8        
    def update(self):
        keys = key.get_pressed()
        global worldshift
        if keys[K_LEFT] and worldshift > 0:
            worldshift -= self.speed
        if keys[K_SPACE] and self.on_ground:
            self.jump()
        if keys[K_RIGHT] and worldshift < worldweeds - 800:
            worldshift += self.speed
        if not self.on_ground:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
        self.on_ground = False
    def jump(self):
        self.velocity_y = -self.jump_power
        self.on_ground = False
class Platform(sprite.Sprite):
    def __init__(self, x, y, width, height=80):
        sprite.Sprite.__init__(self)
        self.image = Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill((138, 195, 74))
player = Player(100, 100)
start_platform = Platform(50, 400, 200)
current_x = 300
platforms = list()
platforms.append(start_platform)
while current_x < worldweeds:
    width = randint(80, 250)
    gap = randint(50, 200)
    y = randint(100, 500)
    platform = Platform(current_x, y, width)
    platforms.append(platform)
    current_x += gap + width
while game:
    window.blit(background, (0, 0))
    window.blit(player.image, player.rect)
    player.update()
    for platform in platforms:
        window.blit(platform.image, (platform.rect.x - worldshift, platform.rect.y))
        platform_rect = Rect(platform.rect.x - worldshift, platform.rect.y, platform.rect.width, platform.rect.height)
        if player.rect.colliderect(platform_rect):
            player.on_ground = True
            player.rect.bottom = platform.rect.top
    for e in event.get():
        if e.type == QUIT:
            game = False
    if player.rect.y > 600:
        window.blit(lose, (250, 200))
        game = False

    display.update()
    clock.tick(FPS)