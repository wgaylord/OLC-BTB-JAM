import sys, pygame
import time
import random
from pygame import Rect , draw
from tiles import tiles,player
import entities
import json

full = True

pygame.init()
pygame.font.init()
pygame.mouse.set_cursor(*pygame.cursors.diamond)

def text_to_screen(screen1, text, x, y, size = 50,color = (200, 000, 000)):
    try:

        text = str(text)
        font = pygame.font.SysFont('Comic Sans MS', size)
        text = font.render(text, True, color)
        screen1.blit(text, (x, y))

    except Exception as e:
        print(e)

size = width, height = 640, 480

screen_center = (width//2,height//2)


screen = pygame.display.set_mode(size,pygame.FULLSCREEN|pygame.HWSURFACE )

screen_tile_width = width//16
screen_tile_height = height//16

world_width_px = 5120
world_height_px = 3840

world_width = world_width_px//16
world_height = world_height_px//16
        
worldSurface = pygame.Surface((world_width_px,world_height_px))
worldSurface.fill((0,255,0))


PlayerX = world_width//2
PlayerY = world_height//2
PlayerHealth = 10

entitys = []


world = []
for x in range(world_width):
    world.append([])
    for y in range(world_height):
        tile = "grass"
        if x < 16 or x > 279:
            tile = "border"
        if y < 16 or y >224:
            tile = "border"
        world[x].append(tile)
        



#Texture world with random grass variants


inventory = []



world[PlayerX-2][PlayerY-1] = "brick_wall"
world[PlayerX-1][PlayerY-1] = "brick_wall"
world[PlayerX][PlayerY-1] = "brick_wall"
world[PlayerX+1][PlayerY-1] = "brick_wall"
world[PlayerX+2][PlayerY-1] = "brick_wall"
world[PlayerX+2][PlayerY] = "brick_wall"
world[PlayerX+2][PlayerY+1] = "brick_wall"
world[PlayerX+1][PlayerY+1] = "brick_wall"
world[PlayerX][PlayerY+1] = "brick_wall"
world[PlayerX-1][PlayerY+1] = "brick_wall"
world[PlayerX-2][PlayerY+1] = "brick_wall"
world[PlayerX-2][PlayerY] = "door_closed"

world[PlayerX][PlayerY+5] = "crafting_table"


for x in range(200):
    world[random.randint(16,279)][random.randint(16,224)] = "tree"
    
for x in range(100):
    pocket_size = random.randint(2,10)
    x = random.randint(16,279)
    y = random.randint(16,224)
    if abs(PlayerX - x) < (pocket_size+10) or abs(PlayerY - y) < (pocket_size+10):
        continue
    world[x][y] = "stone"
    for z in range(pocket_size):
        for a in range(pocket_size):
            world[x+z][y+a] = "stone"



currentInventorySelected = 0

t = time.time()

overlay = pygame.Surface((width, height-32))

GameOver = pygame.Surface((width, height))
text_to_screen(GameOver,"GAME",200,200,50,(255,0,0))
text_to_screen(GameOver,"OVER",200,250,50,(255,0,0))
text_to_screen(GameOver,"Press x to exit",200,300,30,(255,255,255))
pygame.time.set_timer(25, 50)
count = 0
key = 0
while 1:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key==115 and event.mod==64:
                file = open("save.json","w+")
                data = {}
                data["world"] = world
                data["inventory"] = inventory
                data["PlayerX"] = PlayerX
                data["PlayerY"] = PlayerY
                json.dump(data,file)
                file.close()
            if event.key==108 and event.mod==64:
                file = open("save.json")
                data = json.load(file)
                world = data["world"]
                inventory = data["inventory"]
                PlayerX = data["PlayerX"]
                PlayerY = data["PlayerY"]
                file.close()
            key = event.key
        if event.type == pygame.KEYUP:
            if event.key == key:
                key = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(event.pos[1] < height-32):
                x = ((event.pos[0] - (width//2))//16)
                y = ((event.pos[1] - (height//2))//16)
                if abs(x) < 5 and abs(y) < 5:
                    hit = False
                    for z in entitys:
                        #print(z.x,z.y,x,y)
                        if z.x == PlayerX+x and z.y == PlayerY+y:
                            z.hurt(inventory,currentInventorySelected)
                            hit = True
                    if not hit:
                        world,inventory,currentInventorySelected = tiles[world[PlayerX+x][PlayerY+y]].onClick(event.button,world,PlayerX+x,PlayerY+y,inventory,currentInventorySelected)
        if event.type == 25:
            if key == 119:
                PlayerY-=1
                if tiles[world[PlayerX][PlayerY]].solid:
                    PlayerY+=1
            if key == 115:
                PlayerY+=1
                if tiles[world[PlayerX][PlayerY]].solid:
                    PlayerY-=1
            
            if key == 97:
                PlayerX-=1
                if tiles[world[PlayerX][PlayerY]].solid:
                    PlayerX+=1
            if key == 100:
                PlayerX+=1
                if tiles[world[PlayerX][PlayerY]].solid:
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
            if key == 292:
                if full == False:
                    full = True
                    screen = pygame.display.set_mode(size,pygame.FULLSCREEN|pygame.HWSURFACE)
                else:
                    screen = pygame.display.set_mode(size)
                    full = False
                key = 0
            if key == 120 and PlayerHealth <= 0:
                pygame.quit()
                exit()

            time_of_day = abs(int(((449000+pygame.time.get_ticks()) % 900000) / 2250)-200)
            
            index = 0
            for z in entitys:
                if z.health <=0:
                    del entitys[index]
                    continue
                index+=1
                z.move(PlayerX,PlayerY,world,entitys)
                PlayerHealth-=z.attack(PlayerX,PlayerY)
            
            if len(entitys) < 30 and time_of_day > 100:
                x,y = random.randint(16,279),random.randint(16,220)
                while tiles[world[x][y]].solid:
                    x,y = random.randint(16,279),random.randint(16,220)
                entitys.append(entities.Zombie(x,y))
        
    
            draw.rect(overlay,(time_of_day,time_of_day,time_of_day),(0,0,width,height-32))    

    
    Top = PlayerY-15
    Left = PlayerX-20   

    for x in range(40):
        for y in range(30):
            screen.blit(tiles[world[Left+x][Top+y]].draw(world,PlayerX,PlayerY,Left+x,Top+y),(x*16,y*16))
            for z in entitys:
                if (Left+x) == z.x and (Top+y) == z.y:
                    screen.blit(z.draw(),(x*16,y*16))
            
    
    
    screen.blit(player,screen_center)
    
    
    draw.rect(screen,(128,128,128),(0,height-32,width,32))
    
    draw.rect(screen,(128,0,128),(((currentInventorySelected+1)*32)-8,height-30,30,30))
    
    
    
    screen.blit(overlay,(0,0),special_flags=pygame.BLEND_RGB_SUB)
    text_to_screen(screen,"Health: "+str(PlayerHealth),10,10,20,(255,0,0))
    
    offset = 32

    for x in inventory:
        screen.blit(tiles[x[0]].draw(world,PlayerX,PlayerY,0,0),(offset,height-24))
        text_to_screen(screen,str(x[1]),offset+14,height-14,10,(0,0,0))
        offset+=32
    
    
    

    count+=1
    
    
    if(time.time()-t > 1):
        pygame.display.set_caption(str(count) + " FPS")
        count = 0
        t = time.time()
    if PlayerHealth <=0:
        screen.blit(GameOver,(0,0))
        
        
    pygame.display.flip()
    