from pygame import Surface,draw
import random

import crafting

GrassNoiseMap = []

for x in range(100):
    GrassNoiseMap.append(random.randint(0,10))

def add_to_inventory(inventory,tile):
    index = 0
    if len(inventory) > 30:
        return False
    for x in inventory:
        if x[0] == tile:
            inventory[index][1] +=1
            
            return True
        else:
            index+=1
    inventory.append([tile,1])
    
    return True

def remove_from_inventory(inventory,currentInventorySelected):
    index = 0
    while index < len(inventory):
        if(inventory[currentInventorySelected][1]) == 1:
            del inventory[currentInventorySelected]
            return
        else:
            inventory[currentInventorySelected][1]-=1
            return
        index+=1
    


class Tile(object):

    texture = None
    solid = True
    
    def __init__(self):
        self.texture = Surface((16,16))
    
    def draw(self,world,playerx,playery,worldx,worldy):
        return self.texture
        
    def onClick(self,button,world,x,y,inventory,current):
        if button == 3:
            if add_to_inventory(inventory,world[x][y]):
                world[x][y] = "grass"
        return world,inventory,current
        
class Border(Tile): 
    def __init__(self):
        super().__init__()
        self.texture.fill((0,0,0))
        
    def onClick(self,button,world,x,y,inventory):
        return world,inventory,current
        
class Grass(Tile):
    def __init__(self):
        super().__init__()
        self.texture.fill((101, 67, 33))
        self.solid = False
        
    def draw(self,world,playerx,playery,worldx,worldy):
        color = GrassNoiseMap[(worldx*worldy) % 100]
        
        if color == 0:
            draw.rect(self.texture,(0,245,0),(1,1,14,14))
        elif color == 5:
            draw.rect(self.texture,(0,220,0),(1,1,14,14))
        elif color == 9:
            draw.rect(self.texture,(0,200,5),(1,1,14,14))
        else:
            draw.rect(self.texture,(0,255,0),(1,1,14,14))
            
        return self.texture
        
    def onClick(self,button,world,x,y,inventory,current):
        if button == 1:
            if len(inventory) > 0:
                world[x][y] = inventory[current][0]
                remove_from_inventory(inventory,current)
        return world,inventory,current
        
class Water(Tile):
    def __init__(self):
        super().__init__()
        self.texture.fill((0,0,255))

class DoorClosed(Tile):
    def __init__(self):
        super().__init__()
        self.texture = Surface((16,16))
        self.texture.fill((100,10,0))
        draw.rect(self.texture,(200,100,50),(3,3,12,12))
        
    
    def onClick(self,button,world,x,y,inventory,current):
        if button == 1:
            world[x][y] = "door_open"
        if button == 3:
            if add_to_inventory(inventory,"door_closed"):
                world[x][y] = "grass"
        return world,inventory,current
        
class DoorOpen(Tile):
    def __init__(self):
        super().__init__()
        self.texture.fill((100,10,0))
        draw.rect(self.texture,(200,100,50),(5,1,2,2))
        self.solid = False

    
    def onClick(self,button,world,x,y,inventory,current):
        if button == 1:
            world[x][y] = "door_closed"
        if button == 3:
            if add_to_inventory(inventory,"door_closed"):
                world[x][y] = "grass"
        return world,inventory,current
        
class BrickWall(Tile):
    def __init__(self):
        super().__init__()
        self.texture.fill((200,10,0))
        draw.rect(self.texture,(200,200,200),(7,0,2,15))
        draw.rect(self.texture,(200,200,200),(0,7,15,2))
        
class Tree(Tile):
    def __init__(self):
        super().__init__()
        self.texture.fill((0,255,0))
        draw.polygon(self.texture,(0,60,0),[(0,12),(7,0),(14,12)])
        draw.rect(self.texture,(200,100,50),(6,12,2,14))
        self.solid = False
        
        
class Stone(Tile):
    def __init__(self):
        super().__init__()
        self.texture.fill((100, 100, 100))
        draw.rect(self.texture,(200,200,200),(1,1,14,14))


class Crafting(Tile):
    def __init__(self):
        super().__init__()
        self.texture.fill((200,100,50))

    def onClick(self,button,world,x,y,inventory,current):
        if button == 1:
            if world[x][y-1] == "grass":
                inventory,current = crafting.attemptInvetoryCraft(inventory,current)
                return world,inventory,current
            
        if button == 3:
            if add_to_inventory(inventory,"crafting_table"):
                world[x][y] = "grass"
        return world,inventory,current

class Wood(Tile):
    def __init__(self):
        super().__init__()
        self.texture.fill((100,21,2))

player = Surface((16,16))
player.fill((0,255,0))
draw.rect(player,(255,0,0),(3,3,11,11))

tiles = {"border":Border(),"grass":Grass(),"water":Water(),"door_open":DoorOpen(),"door_closed":DoorClosed(),"brick_wall":BrickWall(),"tree":Tree(),"stone":Stone(),"crafting_table":Crafting(),"wood":Wood()}

