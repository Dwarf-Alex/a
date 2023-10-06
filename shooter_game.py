from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
#fire_music = mixer.Sound('fire.ogg')

font.init()
font = font.Font(None,47)
crash = 0
miss = 0
display.set_caption("Star Wars")
window = display.set_mode((1000,700))
fon = transform.scale(image.load('galaxy.jpg'), (1000,700))
class Gamers(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
class Player(Gamers):
    def control(self):
       knopky = key.get_pressed()
       if knopky[K_a] and self.rect.x > 5:
           self.rect.x -= self.speed
       if knopky[K_d] and self.rect.x < 920:
           self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.x+50,self.rect.y,15,20,15)
        bullets.add(bullet)
class Enemy(Gamers):
    def update(self):
        self.rect.y += self.speed
        global miss
        if self.rect.y > 700:
            self.rect.x = randint(80,920)
            self.rect.y = 0
            miss += 1
class Enemy_1(Gamers):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.x = randint(80,920)
            self.rect.y = 0
class Bullet(Gamers):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        
game = True
finish = False
clock = time.Clock()
Vader = Player('rocket.png',480,580,100,100,10)
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy_1('asteroid.png',randint(80,920),0,80,80,randint(1,3))
    asteroids.add(asteroid)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png',randint(80,920),0,80,80,randint(1,5))
    monsters.add(monster)
kol_bullets = 0
r = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if kol_bullets < 15 and r == False:
                    kol_bullets += 1
                    #fire_music.play()
                    Vader.fire()
                if kol_bullets >= 15 and r == False:
                    start_t = timer()
                    r = True
    if finish != True:
        window.blit(fon,(0,0))
        text_1 = font.render('Счёт:'+str(crash), True,(255,255,255))
        window.blit(text_1,(10,20))
        text_2 = font.render('Пропущено:'+str(miss), True,(255,255,255))
        window.blit(text_2,(10,50))
        Vader.reset()
        Vader.control()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        if r == True:
            end_t = timer()
            if end_t-start_t < 2:
                text_r = font.render('Перезарядка!',True,(255,255,255))
                window.blit(text_r,(500,350))
            else:
                r = False
                kol_bullets = 0
        if sprite.spritecollide(Vader,monsters,False)or sprite.spritecollide(Vader,asteroids,False) or miss>=5:
            finish = True
            text_lose = font.render('Вы проиграли!!!',True,(255,255,255))
            window.blit(text_lose,(500,350))
        babah = sprite.groupcollide(bullets,monsters,True,True)
        for i in babah:
            crash +=1
            monster = Enemy('ufo.png',randint(80,920),0,80,80,randint(1,5))
            monsters.add(monster)
        if crash >=50:
            finish = True
            text_win = font.render('Вы выйграли!!!',True,(255,255,255))
            window.blit(text_win,(500,350))
        display.update()
    time.delay(60)