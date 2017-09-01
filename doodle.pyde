import random
import time 
add_library('minim')
minim=Minim(this)

class Game:
    def __init__(self, w, h, g):
        self.w=w
        self.h=h
        self.g=g
        self.x=0
        self.y=0
        self.state = 'name'
        self.name = ''
        self.score = ''
        self.enter = {'10': False}
        
        self.platforms=[]
        self.platformY=1
        for num in range (50):
            x = random.randint(1, 4)
            speed = random.uniform (1.1, 2)
            self.platforms.append(Platform('carpet.png', x*100, self.g-100*self.platformY, 50, 10, speed))
            self.platformY += 1  
        
        self.platforms.sort(key=lambda x:x.y)
        
        self.enemies = []
        self.enemiesY=self.g-500
        for num in range(10):
            x = random.randint (50, self.w-50)
            self.enemiesY -= random.randint(100, 200)
            x1 = random.randint (40, 300)
            self.enemies.append(Bomb(x,self.enemiesY,self.enemiesY+40,20,'bomb.png',325, 325, x1, x1+150))

        self.bonus = []
        self.bonusY = self.g-100
        for num in range (100):
            i = random.randint(30,300)
            num = random.randint(0, 2)
            self.bonusY -= random.randint(50, 77)
            for j in range(0,num):
                x = i + 30*j
                reward = Reward(x, self.bonusY, self.bonusY+20, 10, 'coin.png',256, 256, 0, 0)
                self.bonus.append(reward)
        
        self.bombcnt = 0
        self.rewardcnt = 0
        self.platformcnt = 0
        self.bgImage = gameEffect.bgImg
        self.picheight = 3000
        
        gameEffect.bgmusic.loop()
    
    def readScore(self):
        self.scoreFile = open ('doodle.txt', 'r')
        self.scorelist = []
        self.namelist = []
        for line in self.scoreFile:
            string = line.strip()
            templist = string.split(',')
            self.scorelist.append(int(templist[1]))
            self.namelist.append(templist[0])
        self.top3scores = []
        if len(self.scorelist)< 3:
            for n in range(len(self.scorelist)):
                self.top3scores.append([self.namelist[n], self.scorelist[n]])
            print self.top3scores
        else:
            for num in range(3):
                highest_score = max(self.scorelist)
                index = self.scorelist.index(highest_score)
                del self.scorelist[index]
                highest_name = self.namelist.pop(index)
                self.top3scores.append([highest_name, highest_score])
        print (self.top3scores)
        for item in self.top3scores:
            print (item[0], item[1])
        self.scoreFile.close()
        
        
    def recordScore(self):
        self.scoreFile = open('doodle.txt', 'a') 
        self.scoreFile.write(self.name.strip()+','+str(self.score)+'\n')
        self.scoreFile.close()
        
    def namedisplay(self):
        textAlign(LEFT)
        textSize(48)
        text(self.name, game.w/2-80, game.h/2+10)
        fill (10, 50, 240)
        if self.enter['10'] == True:
            self.state = 'menu'
            self.enter['10'] = False
    
    def menudisplay(self):
        textSize(48)
        text(self.name, game.w/2, game.h/2)
        textAlign(CENTER, CENTER)
        
        fill (10, 50, 240)
        if self.enter['10'] == True:
            self.state = 'play'
            self.enter['10'] = False
            doodle = Doodle (game.w/2, game.g, game.g, 20, 'arabdoodle.png', 600, 596)
    
    def playdisplay(self):

        for p in self.platforms:
            if doodle.y < p.y and p.y+self.y > self.h:
                self.platforms.remove(p)
                self.platformcnt += 100
            else:
                p.display()
        
        for e in self.enemies:
            e.display()
        
        for r in self.bonus:
            r.display()
        
            
        
        textSize(24)
        self.score = self.rewardcnt+self.bombcnt+self.platformcnt
        text (self.name+'\n'+str(self.score), 50, 50)
        print (self.name+'\n'+str(self.score))
        fill (10,50,240)
            
    def overdisplay(self):
        self.readScore()
        textSize(36)
        text(self.name, game.w/2, game.h/2-50)
        textAlign(CENTER)
        text(str(self.score), game.w/2, game.h-300)
        fill (10, 50, 240)
        
        cnt=0
        for item in self.top3scores:
            fill(0)
            textSize(24)
            textAlign(CENTER)
            text(item[0]+': '+str(item[1])+'\n', game.w/2,game.h-240+cnt*30)
            cnt +=1
            
        if self.enter['10'] == True:
            self.state = 'play'
            game.__init__(500, 600, 500)
            doodle.__init__ (game.w/2, game.g, game.g, 20, 'arabdoodle.png', 600, 596)
        
            
class Platform:
    def __init__(self,img, x, y, w, h, vx):
        self.x=x
        self.y=y
        self.w=1.5*w
        self.h=1.5*h
        self.vx= vx
        self.img=loadImage(img)
        
    def display(self):
        self.update()
        image(self.img,self.x,self.y+game.y,self.w,self.h)
        
        
    def update(self):
        if self.x < 0 or self.x > game.w-self.w:
            self.vx *=-1
        self.x += self.vx
        
class Object:
    def __init__(self, x, y, g, r,img,w,h, x1, x2):
        self.x=x
        self.y=y
        self.g=g
        self.r=r
        self.vx=-1
        self.vy=0
        self.img=loadImage(img)
        self.dir=1
        self.w=w
        self.h=h
        self.x1=x1
        self.x2=x2
        
    def update(self):
        if self.y+self.r<self.g:
            self.vy += 0.1
        else:
            self.vy = 0
            self.y = self.g - self.r
        
        ## move back and forth
        if self.x < self.x1 or self.x > self.x2:
            self.vx*=-1 

        self.x += self.vx
        self.y += self.vy
        
    def display(self):
        self.update()
        
        if self.vx == 0 and self.dir > 0:
            image(self.img,self.x-self.r,self.y-self.r+game.y,2*self.r,2*self.r, 0,0,self.w,self.h)
        elif self.vx ==0 and self.dir < 0:
            image(self.img,self.x-self.r,self.y-self.r+game.y,2*self.r,2*self.r, self.w, 0, 0, self.h)
        elif self.vx > 0:
            image(self.img,self.x-self.r,self.y-self.r+game.y,2*self.r,2*self.r, 0,0, self.w, self.h)
        else:
            image(self.img,self.x-self.r,self.y-self.r+game.y,2*self.r,2*self.r, self.w,0,0,self.h)                
        
class Doodle(Object):
    def __init__(self,x,y,g,r,img,w,h):
        Object.__init__(self,x,y, g,r,img,w,h,0,0)
        self.Keys={UP:False, RIGHT:False, LEFT:False}
        self.sGame=False
        self.vx=0
        
        
    def update(self):
        ## simulate gravity
        if self.y+self.r<self.g:
            self.vy+=0.1
        else:
            self.vy = 0
            self.y = self.g-self.r
        
        if self.sGame:
            ## set key command
            if self.Keys[LEFT]:
                self.vx = -2
                self.dir=-1
            elif self.Keys[RIGHT]:
                self.vx = 2
                self.dir=1
                
            else:
                self.vx = 0
                
        if self.Keys[UP] and self.y == self.g-self.r:
            self.vy = -6
            
            self.sGame=True
            
        ## update platform ground
        for p in game.platforms:
            if p.y-2*self.r<=self.y+self.r<= p.y  and p.x<=self.x<=p.x+p.w:
                self.g = p.y
                self.vx = p.vx
                if self.Keys[LEFT]:
                    self.vx += -1
                elif self.Keys[RIGHT]:
                    self.vx += 1
                break
            elif not self.sGame:
                self.g = game.g
            else:
                self.g = 2000
        
        ##update enemies dead/alive
        for e in game.enemies:
            if self.distance(self.x, self.y, e.x, e.y) < self.r+e.r:
                if self.vy >0:
                    game.enemies.remove(e)
                    gameEffect.disappearSound.rewind()
                    gameEffect.disappearSound.play()
                    game.bombcnt += 50
                    self.vy = -6
                else:
                    gameEffect.bgmusic.close()
                    gameEffect.explosionSound.rewind()
                    gameEffect.explosionSound.play()
                    time.sleep(1)
                    game.score = game.rewardcnt+game.bombcnt+game.platformcnt
                    game.recordScore()
                    game.state = 'over'
                    gameEffect.gameoverSound.rewind()
                    gameEffect.gameoverSound.play() 
                    return
        
        ##update bonus
        for r in game.bonus:
            if self.distance(self.x,self.y,r.x,r.y)<self.r+r.r:
                game.bonus.remove(r)
                gameEffect.coinSound.rewind()
                gameEffect.coinSound.play()
                game.rewardcnt += 50
            
        self.x += self.vx
        self.y += self.vy
        
        if self.y+game.y > game.h:
            game.score = game.rewardcnt+game.bombcnt+game.platformcnt
            game.recordScore()
            gameEffect.bgmusic.close()
            game.state = 'over'
            gameEffect.gameoverSound.rewind()
            gameEffect.gameoverSound.play() 
            return
            
        ### keep the doodle in the center
        if self.y < game.h/2 and self.vy != 0 and self.vy < 5:
            game.y -= self.vy

        ### keep the doodle in the picture...
        if self.x-self.r<=0: 
            self.x = self.r
        elif self.x+self.r>=game.w:
            self.x = game.w-self.r                
    
    def distance(self, x1,y1,x2,y2):
        return (((x1-x2)**2)+((y1-y2)**2))**0.5
    
class Bomb(Object):
    def __init__(self, x, y, g, r, img, w, h, x1, x2):
        Object.__init__(self, x, y, g, r, img, w, h,x1,x2)
        self.vx =0 
        
class Reward(Object):
    def __init__(self, x, y, g, r, img, w, h, x1, x2):
        Object.__init__(self, x, y, g, r, img, w, h,x1,x2)
        self.vx = 0

class GameEffect:
    def __init__(self):
        self.explosionSound = minim.loadFile('bombE.mp3')
        self.disappearSound = minim.loadFile('bombdisappear.mp3')
        self.coinSound = minim.loadFile('coin.mp3')
        self.bgmusic = minim.loadFile('bgmusic.mp3') 
        self.gameoverSound = minim.loadFile('gameover.mp3')
        
        self.nameImg = loadImage('background.png')
        self.menuImg = loadImage('menu.png')
        self.bgImg = loadImage('burj.jpg')
        self.cloudImg = loadImage('cloud.png')
        self.overImg = loadImage('over.png')
        
gameEffect = GameEffect()
game = Game(500, 600, 500)

doodle = Doodle (game.w/2, game.g, game.g, 20, 'arabdoodle.png', 600, 596)

def setup():
    background(255)
    size(game.w,game.h)
    
def draw():

    if game.state == 'name':
        background(255)
        image(gameEffect.nameImg, 0, 0, game.w, game.h)
        game.namedisplay()
    
    elif game.state == 'menu':
        background(255)
        image(gameEffect.menuImg, 0, 0, game.w, game.h)
        game.menudisplay()
        
    elif game.state == 'play':
        background(255)
        image(game.bgImage,0,0, game.w, game.h, 0, game.picheight-game.h-int(game.y)%(game.picheight-game.h), 250, game.picheight-int(game.y)%(game.picheight-game.h))
        game.playdisplay()
        doodle.display()
    
    elif game.state == 'over':
        background(255)
        image(gameEffect.overImg, 0, 0, game.w, game.h)
        game.overdisplay()


def keyPressed():
    if game.state == 'name':
        if len(game.name) < 6:
            game.name += str(chr(keyCode))
        
        if keyCode == 8:
            game.name = game.name[0: len(game.name)-2]
            
    if keyCode == 10 and game.state == 'over':
        gameEffect.bgmusic = minim.loadFile('bgmusic.mp3')
        
    if keyCode == 10:
        game.enter['10'] = True

    if keyCode in doodle.Keys:
        doodle.Keys[keyCode] = True

def keyReleased():
    if keyCode in doodle.Keys:
        doodle.Keys[keyCode] = False
        

 

