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
    


def craftWood(inventory,current):
    if inventory[current][0] == "tree":
        remove_from_inventory(inventory,current)
        add_to_inventory(inventory,"wood")
        return inventory,current,True
    return inventory,current,False
    
def craftBrick(inventory,current):
    if inventory[current][0] == "stone" and inventory[current][1] > 4:
        remove_from_inventory(inventory,current)
        remove_from_inventory(inventory,current)
        remove_from_inventory(inventory,current)
        remove_from_inventory(inventory,current)
        add_to_inventory(inventory,"brick_wall"
        return inventory,current,True
    return inventory,current,False
    
InventoryCrafts = [craftWood,craftBrick]

def attemptInvetoryCraft(inventory,current):
    for x in InventoryCrafts:
        inventory,current,worked = x(inventory,current)
        if worked:
            return inventory,current
    return inventory,current