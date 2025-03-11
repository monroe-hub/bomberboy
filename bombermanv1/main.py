import py5 as p5
import pyautogui as pag #for manipulating player mouse
import numpy as np
from os import path

class Player:

    def __init__(self, grid_pos):
        
        self.position = grid_pos
        self.direction = None 

        self.health = 3

    def try_move(self, active_map):

        rows, cols = active_map.shape

        if self.direction == 'up':

            if 0 <= self.position[0] - 1 <= rows - 1:
                if active_map[self.position[0] - 1, self.position[1]] >= 0: 
                                                                                        
                    if active_map[self.position[0] - 1, self.position[1]] == 0:
                        self.move()

        if self.direction == 'down':

            if 0 <= self.position[0] + 1 <= rows - 1:
                if active_map[self.position[0] + 1, self.position[1]] >= 0:

                    if active_map[self.position[0] + 1, self.position[1]] == 0:
                        self.move()
            
        if self.direction == 'right':

            if 0 <= self.position[1] + 1 <= cols - 1:
                if active_map[self.position[0], self.position[1] + 1] >= 0:

                    if active_map[self.position[0], self.position[1] + 1] == 0:
                        self.move()
            
        if self.direction == 'left':

            if 0 <= self.position[1] - 1 <= cols - 1:
                if active_map[self.position[0], self.position[1] - 1] >= 0:

                    if active_map[self.position[0], self.position[1] - 1] == 0:
                        self.move()
        

    def move(self):

            #This seems inverted, and that's because it is: numpy arrays have the origin in the top left
            
            if self.direction == 'up': 
                self.position = (self.position[0] - 1, self.position[1])
            elif self.direction == 'down': 
                self.position = (self.position[0] + 1, self.position[1])
            elif self.direction == 'right': 
                self.position = (self.position[0], self.position[1] + 1)
            elif self.direction == 'left': 
                self.position = (self.position[0], self.position[1] - 1)
                
            self.direction = None
        

    def throw_bomb():
        pass

def load_image(file_path):
    #Loads an image without crashing script
    try:
        image = p5.load_image(file_path)
        return image
    except: 
        
        print("Error loading image")
        return None

class Map():

    def __init__(self, array, tile_size=64):
        
        self.init_coords = [100, 100]
        self.array = array
        self.tile_size = tile_size

        self.coordinate_map = np.empty(shape=self.array.shape, dtype=object)
        self.active_map = np.copy(self.array)

        for row_index in range(0, array.shape[0]):
            for col_index in range(0, array.shape[1]):

                x = self.init_coords[0] + col_index * tile_size
                y = self.init_coords[1] + row_index * tile_size

                self.coordinate_map[row_index, col_index] = (x, y)

    def render_map(self):
        """This will draw a grid for the corresponding map array."""
        

        for row_index, row_values in enumerate(self.active_map):
            for col_index, position in enumerate(row_values):
                #I know that every tile_size should be a self but I'm lazy
                tile_size = self.tile_size

                x = self.init_coords[0] + col_index * tile_size
                y = self.init_coords[1] + row_index * tile_size

                if position == 1:
                    p5.image(steel_brick, x, y, tile_size, tile_size)

                elif position == 2:
                    
                    p5.image(break_brick, x, y, tile_size, tile_size)

                elif position == 3:
                    p5.push()
                    p5.fill(0)
                    p5.square(x, y, tile_size)
                    p5.pop()

                elif position == 4:

                    p5.push()
                    p5.no_stroke()
                    p5.fill(0, 135, 135)
                    p5.circle(x, y, tile_size)
                    p5.pop()

    def refresh_map(self, player):
        """Recalculates map logic, updating it within the object. Requires a player object as input for various calculations."""


        for row_index in range(0, self.active_map.shape[0]):
            for col_index in range(0, self.active_map.shape[1]):

                x = row_index
                y = col_index

                if (x, y) == player.position: self.active_map[x, y] = 4
                elif self.active_map[x, y] == 4: self.active_map[x, y] = 0

def generate_base_map(size=(10, 10)):

    array = np.zeros(shape=size)

    for row_index in range(0, array.shape[0]):
            for col_index in range(0, array.shape[1]):

                x = row_index
                y = col_index

                if x % 2 == 0 and y % 2 == 0:
                    array[x, y] = 1
                # elif np.random.randint(0, 1) % 1 == 0:
                    # array[x, y] = 2

    return array



def load_assets():
    """Attempts to load all relevant assets (images, etc.) and places them into the global namespace."""
    global break_brick, steel_brick

    image_folder = path.join("bombermanv1", "assets")
    
    # print(image_folder)
    break_brick = load_image(image_folder + path.sep + "destroyable_brick.png")
    steel_brick = load_image(image_folder + path.sep + "steel_brick.png")

def settings():
    p5.size(1000, 1000)
    #board size (800x800?)

def setup():
    p5.rect_mode(p5.CENTER)
    p5.image_mode(p5.CENTER)

    load_assets()
    p5.background(255)

    
    test_map = generate_base_map((11, 13))

    global maps
    maps = Map(test_map)

    global bomberboy
    bomberboy = Player((1, 1))
    # active_map[bomberboy.position[0], bomberboy.position[1]] = 4

def draw():
    p5.background(255)
    

    #Checks to see if a move is queued
    bomberboy.try_move(active_map=maps.active_map)

    maps.refresh_map(bomberboy)
    maps.render_map()

def key_pressed():

    key = str(p5.key).lower()

    # print(key)

    if key == 'w': 
        bomberboy.direction = 'up'
    elif key == 's': 
        bomberboy.direction = 'down'
    elif key == 'd': 
        bomberboy.direction = 'right'
    elif key == 'a': 
        bomberboy.direction = 'left'

    #Debug statement, keep in mind that the coordinate here will not be updated yet
    # print(f"Keypress: {key} Direction: {bomberboy.direction} Coordinate: {bomberboy.position}")


        

    


p5.run_sketch()
