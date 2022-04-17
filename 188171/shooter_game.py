#Create your own shooter
from pygame import *
from random import randint
window=display.set_mode((700,500))
background=transform.scale(image.load('galaxy.jpg'),(700,500))
font.init()
font1=font.SysFont('Arial',36)
bullets=sprite.Group()
loss=0
scored=0
mixer.init()
'''mixer.music.load('space.ogg')
mixer.music.set_volume(0.05)
mixer.music.play()'''
class GameSprite(sprite.Sprite):
    def __init__(self,images,x,y,speed):
        super().__init__()
        self.image=transform.scale(image.load(images),(80,80))
        self.speed=speed
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class player(GameSprite):
    def update(self):
        keyp=key.get_pressed()
        if keyp[K_a] and self.rect.x>=0:
            self.rect.x-=self.speed
        if keyp[K_d] and self.rect.x<=635:
            self.rect.x+=self.speed
    def fire(self):
        bullet=Bullet('bullet.png',self.rect.centerx-5,self.rect.top,-15)
        bullets.add(bullet)
        fires=mixer.Sound('fire.ogg')
        fires.play()
        fires.set_volume(0.05)
class enemy(GameSprite):
    def update(self):
        global loss
        self.image=transform.scale(self.image,(100,50))
        self.rect.y+=self.speed
        if self.rect.y>=500:
            self.rect.y=0
            self.rect.x=randint(50,650)
            self.speed=randint(5,10)
            loss+=1
class Bullet(GameSprite):
    def update(self):
        self.image=transform.scale(self.image,(10,15))
        self.rect.y+=self.speed
        if self.rect.y<=0:
                self.kill()
            
clock=time.Clock()
FPS=60
clock.tick(FPS)
rocket=player('rocket.png',325,400,20)
ufos=sprite.Group()
for i in range(5):
    ufo=enemy('ufo.png',randint(50,650),0,randint(5,10))
    ufos.add(ufo)




game=True
while game:
    window.blit(background,(0,0))
    text=font1.render('Missed:'+str(loss),1,(255,255,255))
    scores=font1.render('Score:'+str(scored),1,(255,255,255))
    youwin=font1.render('YOU WIN',1,(255,255,255))
    youlose=font1.render('YOU LOSE',1,(255,255,255))
    window.blit(text,(10,10))
    window.blit(scores,(10,50))
    collide=sprite.groupcollide(ufos,bullets,True,True)
    for i in collide:
        scored+=1
        ufo=enemy('ufo.png',randint(50,650),0,randint(5,10))
        ufos.add(ufo)
    if scored==10:
        window.blit(youwin,(350,250))
        time.wait(500)
        break
        
        '''#youwin.hide()
        loss=0
        scored=0'''

    if loss==3 or sprite.spritecollide(rocket,ufos,False,False):
        window.blit(youlose,(350,250))
        time.wait(500)
        break
        
        '''#youlose.hide()
        loss=0
        scored=0'''
    rocket.reset()
    rocket.update()
    bullets.update()
    bullets.draw(window)
    ufos.update()
    ufos.draw(window)
    keyp=key.get_pressed()
    for e in event.get():
        if e.type==QUIT:
            game=False
        if e.type==KEYDOWN:
            if e.key==K_SPACE:
                rocket.fire()
    display.update()
    clock.tick(FPS)
    time.delay(50)