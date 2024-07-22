import pygame
import numpy as np

#PhysicsSetup
A=([0.00501, 0.00464, -72.9,  -31.34],
   [-0.0857,  -0.545,   309,    -7.4],
   [0.00185,-0.00767,-0.395, 0.00132],
   [      0,       0,     1,       0])
st=([0],[0],[0],[0])
B=([5.63],[-23.8],[-4.51576],[0])
t=0.02
strength=0.01
control=0
x,new=st,st

#ScreenBgSetup
ScreenX=1920
ScreenY=1000
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
player=pygame.transform.scale(player,(1*(playerX//playerY)*(bgY//20),bgY//20))
playerX=player.get_width()
playerY=player.get_height()
player_pos = pygame.Vector2((ScreenX//11)-(playerX//2), (ScreenY//3)-(playerY//2))

#PygameSetup
pygame.init()
screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption('2D Flight Sim')
clock = pygame.time.Clock()
running = True
dt = 0

#GameLoop
while running:
    #Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #BackGround
    for i in range(tiles):
        screen.blit(bg,(i*bgX-scroll,0))
    if scroll>=bgX:
        scroll=0

    #Physics
    n=np.dot(A,new)+np.dot(control,B)
    new=(np.add(new,np.dot(t,n)))
    for i in range(len(x)):
        x[i].append(new[i][-1])

    #Control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        control += 0.1 * dt
    if keys[pygame.K_DOWN]or keys[pygame.K_s]:
        control -= 0.1 * dt
    if control >0:
        control-= 0.05*dt
    elif control <0:
        control+= 0.05*dt
        
    #ContolBar
    if control >0.001:
        rect=pygame.Rect(5, (ScreenY//2)-control*1500, 20,abs(control)*1500)
        pygame.draw.rect(screen,'green',rect)
    elif control <-0.001:
        rect=pygame.Rect(5, (ScreenY//2), 20,abs(control)*1500)
        pygame.draw.rect(screen,'red',rect)

    #LocationUpdates
    player_pos.y += x[1][-1]*dt
    scroll+=(x[0][-1]+309)*dt
    Rplayer=pygame.transform.rotate(player,x[3][-1]*-50)
    screen.blit(Rplayer,player_pos)
        
    #Render
    if player_pos.y>0 and player_pos.y<ScreenY:
        pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate
    dt = clock.tick(50) / 1000

pygame.quit()
