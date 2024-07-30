#150 pop was good


import pygame, neat
import numpy as np
from math import sin, cos, tan
from random import randint

global t, WIN_WIDTH, WIN_HEIGHT
WIN_WIDTH=1920
WIN_HEIGHT=1000
FPS=60
t=1/FPS

PLAYER_IMG=pygame.image.load('playa.png')
PLAYER_AR=PLAYER_IMG.get_width()/PLAYER_IMG.get_height()
PLAYER_IMG=pygame.transform.scale(PLAYER_IMG,(PLAYER_AR*WIN_HEIGHT//40,WIN_HEIGHT//40))
BG_IMG=pygame.image.load('bg.jpeg')
BG_AR=BG_IMG.get_width()/BG_IMG.get_height()
BG_IMG=pygame.transform.scale(BG_IMG,(BG_AR*WIN_HEIGHT,WIN_HEIGHT))
TARGET_IMG=pygame.image.load('target.png')
TARGET_AR=TARGET_IMG.get_width()/TARGET_IMG.get_height()
TARGET_IMG=pygame.transform.scale(TARGET_IMG,(TARGET_AR*WIN_HEIGHT//10,WIN_HEIGHT//15))
TARGETHEIGHT=TARGET_IMG.get_height()
PLAYERHEIGHT=PLAYER_IMG.get_height()

global A, B
A=([0.00501, 0.00464, -72.9,  -31.34],
   [-0.0857,  -0.545,   309,    -7.4],
   [0.00185,-0.00767,-0.395, 0.00132],
   [      0,       0,     1,       0])
new=([0],[0],[0.1],[0])
B=([5.63],[-23.8],[-4.51576],[0])

global tgs
tgs=1

class Player:
    IMG=PLAYER_IMG

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=0
        self.img=self.IMG
        self.rotated_image=self.img
        self.playerY=self.img.get_height()
        self.control=0
        self.new=([0],[0],[0],[0])
        self.playerBox=pygame.Rect((self.x,self.y),(self.playerY,self.playerY//2))
        self.RplayerY=self.playerY

    def MLIN(self,MLIN):
        self.control=MLIN/5
        

    def move(self):
        self.new=(np.add(self.new,np.dot(t,np.dot(A,self.new)+np.dot(self.control,B))))
        self.u=self.new[0][-1]
        self.w=self.new[1][-1]
        self.theta=self.new[3][-1]
        self.hv=((self.u+A[1][2])*cos(self.theta)+self.w*sin(self.theta))
        self.vv=((self.u+A[1][2])*sin(self.theta)+self.w*cos(self.theta))
        self.y+=self.vv*t
        self.tilt=self.theta*-57
        
    def draw(self,win,coll):
        if abs(self.tilt)<=80:            
            self.rotated_image=pygame.transform.rotate(self.img,self.tilt)
        else:
            self.rotated_image=pygame.transform.rotate(self.img,80*self.tilt/abs(self.tilt))
        win.blit(self.rotated_image,(self.x,self.y))
        pygame.draw.rect(win,coll,self.playerBox)

    def get_mask(self):
        RplayerX=self.rotated_image.get_width()
        self.RplayerY=self.rotated_image.get_height()
        if self.theta<0:
            self.playerBox=pygame.Rect((self.x+RplayerX-self.playerY,self.y+self.playerY//4),(self.playerY,self.playerY//2))
        else:
            self.playerBox=pygame.Rect((self.x+RplayerX-self.playerY,self.y+self.RplayerY-self.playerY*3//4),(self.playerY,self.playerY//2))
        return self.playerBox

class Target:
    IMG=TARGET_IMG
    def __init__(self,x):
        self.x=x
    
        self.y=randint(10,90)*WIN_HEIGHT//100
        
        self.img=self.IMG
        self.targetX=self.img.get_width()
        self.targetY=self.img.get_height()


    def move(self,tgs):
        if self.x>WIN_WIDTH//16:
            self.x-=309*t
        else:
            self.x=14*WIN_WIDTH//15
            self.y=randint(10,90)*WIN_HEIGHT//100
            tgs+=1
        return tgs
        
    def draw(self,win):
        win.blit(self.img,(self.x,self.y))
        #
        pygame.draw.rect(win,'red',self.targetBox)
        
    def collide(self,player,coll):
        self.playerBox=player.get_mask()
        self.targetBox=pygame.Rect((self.x,self.y),(self.targetX,self.targetY))
        if self.targetBox.colliderect(self.playerBox):
            coll='green'
        else: coll='red'
        return self.targetBox.colliderect(self.playerBox),coll

class Bg:
    IMG=BG_IMG
    bgX=IMG.get_width()
    xs=[]

    def __init__(self):
        
        self.y=0
        for i in range((WIN_WIDTH//self.bgX)+2):
            self.xs.append(self.bgX*i)
        self.img=self.IMG

    def move(self):
        for self.x in self.xs:
            self.x-=309*t
            if self.x<=(-1*self.bgX):
                self.x=self.xs[-1]+self.bgX
        
    def draw(self,win):
        for i in self.xs:
            win.blit(self.img,(i,self.y))
    

def draw_win(win,players,target,bg,colls):
    bg.draw(win)
    for x,player in enumerate(players):
        player.draw(win,colls[x])
    target.draw(win)
    pygame.display.update()

def main(genomes, config):
    tgs=1
    cc=0
    nets=[]
    ge=[]
    players=[]
    colls=[]

    for _,g in genomes:
        net=neat.nn.FeedForwardNetwork.create(g,config)##########################################
        nets.append(net)
        players.append(Player(WIN_WIDTH//18,WIN_HEIGHT//2))
        g.fitness=0
        ge.append(g)
        colls.append('red')
                 
    
    bg=Bg()
    target=Target(14*WIN_WIDTH//15)
    win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock=pygame.time.Clock()
    score=0
    run=True
    while run:
        cc+=1/FPS
        clock.tick(FPS)
        #Exit
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False 
                pygame.quit()
                quit()
        if cc>12:
            for j in range((len(players)//2)):
                mini=9999
                for i in range(len(players)):
                    if ge[i].fitness<mini:
                        mini=ge[i].fitness
                        worst=i
               # ge[i].fitness-=FPS//2
                nets.pop(i)
                ge.pop(i)
                players.pop(i)
            cc=0
        if len(players)<3:
            pygame.quit()
            break
                
        tgs=target.move(tgs)
        for x,player in enumerate(players):
            player.move()
            #output=nets[x].activate(((player.y+player.RplayerY/2)-(target.y+TARGETHEIGHT/2),player.vv,target.x))
            output=nets[x].activate(((player.y+player.RplayerY/2)-(target.y+TARGETHEIGHT/2),player.vv,sin(player.tilt)))
            player.MLIN(output[0])

            e,colls[x]=target.collide(player,colls[x])
            if e:
                ge[x].fitness+=FPS*5
            if player.y+player.RplayerY/2>target.y+TARGETHEIGHT and player.y+player.RplayerY/2<target.y:
                ge[x].fitness+=FPS/3
            if player.y>WIN_HEIGHT or player.y<0:
                ge[x].fitness-=FPS
                nets.pop(x)
                ge.pop(x)
                players.pop(x)
            #else:
                #ge[x].fitness+=1*0.009**(abs(player.y+PLAYERHEIGHT/2)-(target.y+TARGETHEIGHT/2)/WIN_HEIGHT)
        
        #bg.move()
        #draw_win(win,players,target,bg,colls)

    pygame.quit()

def run(config_path):
    global config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    p = neat.Population(config)

    
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    global winner
    winner = p.run(main, 5)

    print('\nBest genome:\n{!s}'.format(winner))
    #print(winner)

 
if __name__=="__main__":
    config_path='config-feedforward.txt'
    run(config_path)

pygame.font.init()
points=1
font=pygame.font.SysFont("comicsansms",30)
text=font.render(f'Score:{points}', True, 'black')
text2=font.render(f'Accuracy:{points*100/tgs}%', True, 'black')

net=neat.nn.FeedForwardNetwork.create(winner, config)
player=Player(WIN_WIDTH//18,WIN_HEIGHT//2)

bg=Bg()
target=Target(14*WIN_WIDTH//15)
win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
clock=pygame.time.Clock()
coll='red'
tgs=1
while run:
    clock.tick(FPS)

    #Exit
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False 
            pygame.quit()
            quit()
    player.move()
    output=net.activate(((player.y+PLAYERHEIGHT/2)-(target.y+TARGETHEIGHT/2),player.vv,sin(player.tilt)))
    player.MLIN(output[0])
    tgs=target.move(tgs)
    bg.move()
    e,co=target.collide(player,'red')
    if co!=coll:
        coll=co
        points+=0.5
    text=font.render(f'Score:{round(points)}', True, 'black')
    text2=font.render(f'Accuracy:{(round(round(points)*100/tgs))}%', True, 'black')
    bg.draw(win)
    target.draw(win)
    player.draw(win,coll)
    win.blit((text),(11*WIN_WIDTH//12,5))
    win.blit((text2),(7*WIN_WIDTH//10,10))
    pygame.display.update()
pygame.quit()
print(winner)
