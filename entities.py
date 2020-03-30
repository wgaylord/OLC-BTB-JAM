from pygame import Surface,draw
import random
from tiles import tiles

class Entity:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.health = 10.0
        self.move_delay = 2
        self.attack_delay = 1
        self.attack_range = 1
        self.attack_damage = 1
        self.texture = Surface((16,16))

    def draw(self):
        return self.texture
        
    def attack(self,playerx,playery):
        return 0

    def hurt(self,inventory,current):
        return


class Zombie(Entity):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.health = 10.0
        self.move_delay = 1
        self.move_time = 0
        self.attack_delay = 10
        self.attack_range = 1
        self.attack_damage = 1
        self.attack_time = 0
        self.texture.fill((128,0,0))
        draw.rect(self.texture,(0,255,0),(6,6,3,3))
        
    def move(self,playerx,playery,world,entitys):
        
        if(self.move_time < self.move_delay):
            self.move_time+=1
            return
        
        def filled(entitys,x,y):
            for z in entitys:
                if z.x == x and z.y == y and z != self:
                    return True
            return False
            
        
        if self.x < playerx:
            self.x+= random.randint(0,1)
            if tiles[world[self.x][self.y]].solid or (self.x == playerx and  self.y == playery) or filled(entitys,self.x,self.y):
                self.x-=1
            else:
                return
                    
        elif self.x > playerx:
            self.x-= random.randint(0,1)
            if tiles[world[self.x][self.y]].solid  or (self.x == playerx and  self.y == playery) or filled(entitys,self.x,self.y):
                self.x+=1
            else:
                return
        if self.y < playery:
            self.y+= random.randint(0,1)
            if tiles[world[self.x][self.y]].solid or (self.x == playerx and  self.y == playery) or filled(entitys,self.x,self.y):
                self.y-=1
            else:
                return
        elif self.y > playery:
            self.y-= random.randint(0,1)
            if tiles[world[self.x][self.y]].solid or (self.x == playerx and  self.y == playery) or filled(entitys,self.x,self.y):
                self.y+=1
            else:
                return
        
        
        
    def attack(self,playerx,playery):
        
        if abs(playerx-self.x) <= self.attack_range and abs(playery - self.y) <= self.attack_range:
            if self.attack_time >= self.attack_delay:
                self.attack_time = 0
                return 1
            else:
                self.attack_time +=1
        return 0
        
    def hurt(self,inventory,current):
        self.health-=5
        return