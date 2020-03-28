import sys, pygame
import time
import random
from pygame import Rect , draw
pygame.init()
pygame.font.init()

def text_to_screen(screen, text, x, y, size = 50,color = (200, 000, 000)):
    try:

        text = str(text)
        font = pygame.font.SysFont('Comic Sans MS', size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception as e:
        pass

size = width, height = 640, 480

screen_center = (width//2,height//2)

screen = pygame.display.set_mode(size)

screen_tile_width = width//16
screen_tile_height = height//16

world_width_px = 5120
world_height_px = 3840

world_width = world_width_px//16
world_height = world_height_px//16
        
worldSurface = pygame.Surface((world_width_px,world_height_px))
worldSurface.fill((0,255,0))

#draw.circle(worldSurface,(255,0,0),(world_width//2,world_height//2),10)

PlayerX = world_width//2
PlayerY = world_height//2



world = []
for x in range(world_width):
    world.append([])
    for y in range(world_height):
        tile = 1
        if x < 16 or x > 279:
            tile = 0
        if y < 16 or y >224:
            tile = 0
        world[x].append(tile)
        


border = pygame.Surface((16,16))
border.fill((0,0,0))

grass = pygame.Surface((16,16))
grass.fill((101, 67, 33))
draw.rect(grass,(0,255,0),(1,1,14,14))

grass1 = pygame.Surface((16,16))
grass1.fill((101, 67, 33))
draw.rect(grass1,(0,245,0),(1,1,14,14))

grass2 = pygame.Surface((16,16))
grass2.fill((101, 67, 33))
draw.rect(grass2,(0,220,0),(1,1,14,14))

grass3 = pygame.Surface((16,16))
grass3.fill((101, 67, 33))
draw.rect(grass3,(0,200,5),(1,1,14,14))


water = pygame.Surface((16,16))
water.fill((0,0,255))

door_closed = pygame.Surface((16,16))
door_closed.fill((100,10,0))
draw.rect(door_closed,(200,100,50),(3,3,12,12))

door_open = pygame.Surface((16,16))
door_open.fill((100,10,0))
draw.rect(door_open,(200,100,50),(5,1,2,2))


brick_wall = pygame.Surface((16,16))
brick_wall.fill((100,10,0))

trees = pygame.Surface((16,16))
trees.fill((0,60,0))
draw.rect(trees,(0,255,0),(0,12,14,14))
draw.rect(trees,(200,100,50),(6,12,2,14))


player = pygame.Surface((16,16))
player.fill((0,255,0))
draw.rect(player,(255,0,0),(3,3,11,11))

tiles = [border,grass,grass1,grass2,grass3,water,door_closed,door_open,brick_wall,trees]

#Texture world with random grass variants


inventory = []


for x in range(10000):
    world[random.randint(16,279)][random.randint(16,224)] = 2
    world[random.randint(16,279)][random.randint(16,224)] = 3
    world[random.randint(16,279)][random.randint(16,224)] = 4


world[PlayerX-2][PlayerY-1] = 8
world[PlayerX-1][PlayerY-1] = 8
world[PlayerX][PlayerY-1] = 8
world[PlayerX+1][PlayerY-1] = 8
world[PlayerX+2][PlayerY-1] = 8
world[PlayerX+2][PlayerY] = 8
world[PlayerX+2][PlayerY+1] = 8
world[PlayerX+1][PlayerY+1] = 8
world[PlayerX][PlayerY+1] = 8
world[PlayerX-1][PlayerY+1] = 8
world[PlayerX-2][PlayerY+1] = 8
world[PlayerX-2][PlayerY] = 6


for x in range(100):
    world[random.randint(16,279)][random.randint(16,224)] = 9


def doesCollide():
    if world[PlayerX][PlayerY] in [0,5,6,8]:    
        return True


def add_to_inventory(tile):
    index = 0
    for x in inventory:
        if x[0] == tile:
            inventory[index][1] +=1
            
            return
        else:
            index+=1
    inventory.append([tile,1])

def remove_from_inventory(tile):
    index = 0
    while index < len(inventory):
        if(inventory[currentInventorySelected][1]) == 1:
            del inventory[currentInventorySelected]
            return
        else:
            inventory[currentInventorySelected][1]-=1
            return
        index+=1
    

currentInventorySelected = 0

def do_tile_click(button,x,y):
    if button == 1:
        if world[x][y] == 6:
            world[x][y] = 7
            return
        if world[x][y] == 7:
            world[x][y] = 6
            return
        if world[x][y] in [1,2,3,4,5] and len(inventory) > 0:
            world[x][y] = inventory[currentInventorySelected][0]
            remove_from_inventory(inventory[currentInventorySelected][0])
            
    if button == 3:
        if world[x][y] not in [0,1,2,3,4,5]:
            tile = world[x][y]
            if tile == 7:
                tile = 6
            if(len(inventory) > 32):
                return
            add_to_inventory(tile)
            world[x][y] = random.randint(1,4)

t = time.time()




count = 0
key = 0
while 1:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            key = event.key
        if event.type == pygame.KEYUP:
            if event.key == key:
                key = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(event.pos[1] < height-32):
                x = ((event.pos[0] - (width//2))//16)
                y = ((event.pos[1] - (height//2))//16)
                if abs(x) < 5 or abs(y) < 5:
                    do_tile_click(event.button,PlayerX+x,PlayerY+y)

    if key == 119:
        PlayerY-=1
        if doesCollide():
            PlayerY+=1
    if key == 115:
        PlayerY+=1
        if doesCollide():
            PlayerY-=1
    
    if key == 97:
        PlayerX-=1
        if doesCollide():
            PlayerX+=1
    if key == 100:
        PlayerX+=1
        if doesCollide():
            PlayerX-=1
    if key == 113:
        if currentInventorySelected > 0:
            currentInventorySelected-=1
        key = 0
    if key == 101:
        if currentInventorySelected < len(inventory)-1:
            currentInventorySelected+=1
        key = 0
    if currentInventorySelected > len(inventory)-1: 
        currentInventorySelected = len(inventory)-1
        if currentInventorySelected < 0:
            currentInventorySelected =0




    
    Top = PlayerY-15
    Left = PlayerX-20   

    for x in range(40):
        for y in range(30):
            screen.blit(tiles[world[Left+x][Top+y]],(x*16,y*16))
    
    screen.blit(player,screen_center)
    
    
    draw.rect(screen,(128,128,128),(0,height-32,width,32))
    
    draw.rect(screen,(128,0,128),(((currentInventorySelected+1)*32)-8,height-30,30,30))
    
    
    offset = 32

    for x in inventory:
        screen.blit(tiles[x[0]],(offset,height-24))
        text_to_screen(screen,str(x[1]),offset+14,height-14,10,(0,0,0))
        offset+=32
    
    
    

    count+=1
    if(time.time()-t > 1):
        pygame.display.set_caption(str(count) + " FPS")
        count = 0
        t = time.time()
    pygame.time.wait(40)
    pygame.display.flip()