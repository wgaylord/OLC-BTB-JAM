import sys, pygame
from pygame import Rect , draw
pygame.init()

size = width, height = 640, 480

screen_center = (width//2,height//2)

screen = pygame.display.set_mode(size)



world_width = 5120
world_height = 3840
        
world = pygame.Surface((world_width,world_height))
world.fill((0,255,0))

draw.circle(world,(255,0,0),(world_width//2,world_height//2),10)

PlayerX = world_width//2
PlayerY = world_height//2


#Delta X and Delta Y
def movePlayer(Dx,Dy):
    PlayerX += Dx
    PlayerY += Dy




while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    for event.type == 
    
    screen.blit(world,(0,0),Rect(PlayerX-screen_center[0],PlayerY-screen_center[1], width, height))
        
    pygame.display.flip()