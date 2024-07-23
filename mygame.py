import pygame
import numpy as np
#import matplotlib.pyplot as plt
from math import sin, cos, tan
from random import randint


#PhysicsSetup
A=([0.00501, 0.00464, -72.9,  -31.34],
   [-0.0857,  -0.545,   309,    -7.4],
   [0.00185,-0.00767,-0.395, 0.00132],
   [      0,       0,     1,       0])
new=([0],[0],[0],[0])
B=([5.63],[-23.8],[-4.51576],[0])
t=1/720
control=0


#ScreenBgSetup
ScreenX=1920
ScreenY=1020

bg = pygame.image.load('bg.jpeg')
bgY=bg.get_height()
bgRatio=ScreenY/bgY
bg = pygame.transform.scale_by(bg,bgRatio)
bgX=bg.get_width()
bgY=bg.get_height()
scroll=0
tiles=2+(ScreenX//bgX)

#PlayerSetup
player = pygame.image.load('playa.png')
playerX=player.get_width()
playerY=player.get_height()
player=pygame.transform.smoothscale(player, (1*(playerX//playerY)*(bgY//20),bgY//20))
playerX=player.get_width()
playerY=player.get_height()
player_pos = pygame.Vector2((ScreenX//10)-(playerX//2), (ScreenY//3)-(playerY//2))

#TargetSetup
target=pygame.image.load('target.png')
targetX=target.get_width()
targetY=target.get_height()
target=pygame.transform.smoothscale(target, (1*(targetX/targetY)*(bgY//10),bgY//10))
targetX=target.get_width()
targetY=target.get_height()
Hit=True
tScroll=0
boom_pos=pygame.math.Vector2()

#BoomSetup
boomog=pygame.image.load('boom.png')
boom=pygame.transform.smoothscale(boomog,((bgY//9),bgY//9))
boomX=bgY//9
boomY=boomX
frame=0
Explosion=False

#PygameSetup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption('2D Flight Sim')
clock = pygame.time.Clock()
running = True
dt = 0
points=0
font=pygame.font.SysFont("comicsansms",30)
text=font.render(f'Score:{points}', True, 'black')
inp=[]

#GameLoop
while running:
    #Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Physics
    n=np.dot(A,new)+np.dot(control,B)
    new=(np.add(new,np.dot(t,n)))
    u=new[0][-1]
    w=new[1][-1]
    theta=new[3][-1]

    #Control
    stab=True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
            inp.append(1)
    elif keys[pygame.K_DOWN]or keys[pygame.K_s]:
            inp.append(-1)
    else:inp.append(0)
    if abs(control)<=72*dt:
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            control += 1 * dt
            stab=False
        if keys[pygame.K_DOWN]or keys[pygame.K_s]:
            control -= 1 * dt
            stab=False
    if control >0 and stab:
        control-= 0.8*dt
    elif control <0 and stab:
        control+= 0.8*dt
        
    #BackGround
    for i in range(tiles):
        screen.blit(bg,(i*bgX-scroll,0))
    if scroll>=bgX:
        scroll=0
        
    #ContolBar
    barscale=ScreenY//5
    if control >0.003:
        rect=pygame.Rect(player_pos.x//3, (ScreenY//2)-control*barscale, player_pos.x//3,abs(control)*barscale)
        pygame.draw.rect(screen,'green',rect)
    elif control <-0.003:
        rect=pygame.Rect(player_pos.x//3, (ScreenY//2), player_pos.x//3,abs(control)*barscale)
        pygame.draw.rect(screen,'red',rect)
        
    #TargetPlacment
    if Hit:
        tLoc=randint(2,8)
        Hit=False
        tScroll=0
    target_pos=(ScreenX-tScroll, (ScreenY*tLoc)//10-(playerY//2))
    screen.blit(target,target_pos)
    if tScroll>=ScreenX:
        tScroll=0
        Hit=True
    targetBox=pygame.Rect((target_pos),(targetX,targetY))
    #pygame.draw.rect(screen,'red',targetBox)

    #LocationUpdates
    player_pos.y += ((u+A[1][2])*sin(theta)+w*cos(theta))*dt
    hv=((u+A[1][2])*cos(theta)+w*sin(theta))
    scroll+=hv*dt
    tScroll+=hv*dt*0.6
    boom_pos.x-=hv*dt*0.8
    Rplayer=pygame.transform.rotate(player,theta*-57)
    screen.blit(Rplayer,player_pos)

    #PlayerHitbox
    RplayerX=Rplayer.get_width()
    RplayerY=Rplayer.get_height()
    if theta<0:
        playerBox=pygame.Rect((player_pos.x+RplayerX-playerY,player_pos.y+playerY//4),(playerY,playerY//2))
    else:
        playerBox=pygame.Rect((player_pos.x+RplayerX-playerY,player_pos.y+RplayerY-playerY*3//4),(playerY,playerY//2))
    #pygame.draw.rect(screen,'red',playerBox)

    #CollisionCheck
    if targetBox.colliderect(playerBox):
        points+=1
        Hit=True
        Explosion=True
        boom_pos=pygame.math.Vector2(target_pos)
        text=font.render(f'Score:{points}', True, 'black')
    screen.blit((text),(11*ScreenX//12,5))

    #Explosion
    if Explosion:
        if frame<720:
            screen.blit(boom,boom_pos)
            boom=pygame.transform.smoothscale_by(boom,0.98)
            boomX*=0.98
            boom_pos.y+=boomX//100
            frame+=1
        else:
            boom=pygame.transform.smoothscale(boomog,(bgY//9,bgY//9))
            boomX=bgY//9
            frame=0
            Explosion=False
        
    #Render
    if player_pos.y>0 and player_pos.y+RplayerY<ScreenY:
        pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate
    dt = clock.tick(720) / 1000

pygame.quit()
g='''
x = np.linspace(0,len(inp),len(inp))
y = inp
fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
'''
