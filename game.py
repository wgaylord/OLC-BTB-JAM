import sys, pygame
from pygame import Rect , draw
pygame.init()

size = width, height = 640, 480

screen_center = (width//2,height//2)

screen = pygame.display.set_mode(size)



world_width = 5120
world_height = 3840
        
worldSurface = pygame.Surface((world_width,world_height))
worldSurface.fill((0,255,0))

#draw.circle(worldSurface,(255,0,0),(world_width//2,world_height//2),10)


world = [[0]*480]*640


grass = pygame.Surface((8,8))
grass.fill((0,255,0))

water = pygame.Surface((8,8))
water.fill((0,0,255))


player = pygame.Surface((8,8))
player.fill((255,0,0))

tiles = [grass,water]


#Delta X and Delta Y
def movePlayer(Dx,Dy):
    global PlayerX,PlayerY,CenterX,CenterY
    PlayerX += Dx
    PlayerY += Dy
    CenterX += Dx*8
    CenterY += Dy*8
    if CenterY+(width//2) > world_width:
        CenterY = world_width - (world_width+1)
    if CenterX+(height//2) > world_height:
        CenterX = world_height - (world_height+1)

    if CenterY-(width//2) < 0:
        CenterY = (world_width+1)
    if CenterX-(height//2) < 0:
        CenterX = (world_height+1)



while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            dx = event.pos[0] - (width//2)
            dy = event.pos[1] - (height//2)
            movePlayer((dx)//8,(dy)//8)
    
    
   
   
    pygame.display.flip()