import py5 as p5
import pyautogui as pag #for manipulating player mouse
import numpy as np
from os import path


class Player:

    def __init__(self, grid_pos, active_map):
        
        self.active_map = active_map

        self.position = grid_pos
        self.direction = None 
        self.visual_direction = 'down'

        self.target_coord = None
        self.check_space()


        self.health = 3

    def check_space(self):

        rows, cols = self.active_map.shape

        if self.direction == 'up':

            if 0 <= self.position[0] - 1 <= rows - 1:
                                                                                        
                    if self.active_map[self.position[0] - 1, self.position[1]] == 0:

                        self.target_coord = (self.position[0] - 1, self.position[1])
                        

        if self.direction == 'down':

            if 0 <= self.position[0] + 1 <= rows - 1:

                    if self.active_map[self.position[0] + 1, self.position[1]] == 0:

                        self.target_coord = (self.position[0] + 1, self.position[1])
                        
            
        if self.direction == 'right':

            if 0 <= self.position[1] + 1 <= cols - 1:

                    if self.active_map[self.position[0], self.position[1] + 1] == 0:

                        self.target_coord = (self.position[0], self.position[1] + 1)
                        
            
        if self.direction == 'left':

            if 0 <= self.position[1] - 1 <= cols - 1:

                    if self.active_map[self.position[0], self.position[1] - 1] == 0:
                        self.target_coord = (self.position[0], self.position[1] - 1)
                        
                    
        

    def move(self):
        # if self.direction != None: self.visual_direction = self.direction

        # self.check_space()

        # if self.visual_direction == self.direction and self.target_coord is not None:

        #     self.position = self.target_coord
        # else: 
        #     self.visual_direction = self.visual_direction

        # self.check_space()
        # self.direction = None

        self.check_space()

        # Allow movement only if the direction is valid and the target is not None
        if self.direction is not None and self.target_coord is not None:
            self.position = self.target_coord
            self.visual_direction = self.direction  # Update visual direction only after movement

        self.direction = None  # Reset movement after processing
        

    def place_bomb(self, bomb_list):

        if self.target_coord != None and self.active_map[self.target_coord] == 0:\
            bomb_list.append(Bomb(self.target_coord))

            

class Bomb:

    def __init__(self, grid_pos):

        self.grid_pos = grid_pos
        self.time_left = 4.0

    pass

        
    


class Map:

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

    def render_map(self, player):
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

                    if player.visual_direction == 'down' or player.visual_direction == 'up':
                        p5.image(bomberboy_sprites[0], x, y, self.tile_size, self.tile_size)

                    elif player.visual_direction == 'right':
                        p5.image(bomberboy_sprites[1], x, y, self.tile_size, self.tile_size)

                    elif player.visual_direction == 'left':

                        p5.push_matrix()
                        p5.scale(-1 ,1)
                        p5.image(bomberboy_sprites[1], -x, y, self.tile_size, self.tile_size)
                        p5.pop_matrix()

                elif position == 5:

                    p5.push()
                    p5.fill(0)
                    p5.circle(x, y, self.tile_size)
                    p5.pop()

                    

    def refresh_map(self, player, bomb_list):
        """Recalculates map logic, updating it within the object. Requires a player object as input for various calculations."""


        for row_index in range(0, self.active_map.shape[0]):
            for col_index in range(0, self.active_map.shape[1]):

                x = row_index
                y = col_index

                if (x, y) == player.position: self.active_map[x, y] = 4
                elif self.active_map[x, y] == 4: self.active_map[x, y] = 0

                for bomb in bomb_list:
                    if bomb.grid_pos == (x, y):
                        self.active_map[x, y] = 5

def generate_base_map(size=(10, 10)):

    array = np.zeros(shape=size)

    for row_index in range(0, array.shape[0]):
            for col_index in range(0, array.shape[1]):

                x = row_index
                y = col_index

                if x % 2 != 0 and y % 2 != 0:
                    array[x, y] = 1

                # elif np.random.randint(0, 1) % 1 == 0:
                    # array[x, y] = 2

    return array

def load_image(file_path):
    #Loads an image without crashing script
    try:
        image = p5.load_image(file_path)
        return image
    except: 
        
        print("Error loading image")
        return None

def load_assets():
    """Attempts to load all relevant assets (images, etc.) and places them into the global namespace."""
    global break_brick, steel_brick, bomberboy_sprites

    image_folder = path.join("bombermanv1", "assets")
    
    # print(image_folder)
    break_brick = load_image(image_folder + path.sep + "destroyable_brick.png")
    steel_brick = load_image(image_folder + path.sep + "steel_brick.png")

    bomberboy_sprites = []
    bomberboy_sprites.append(load_image(image_folder + path.sep + "bomberboy_front.png"))
    bomberboy_sprites.append(load_image(image_folder + path.sep + "bomberboy_side.png"))
    # bomberboy_sprites[0]

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
    #This is where you should change file_size
    maps = Map(test_map)

    global bomberboy
    bomberboy = Player((0, 0), maps.active_map)
    
    global bomb_list
    bomb_list = []

def draw():
    p5.background(255)
    
    maps.refresh_map(bomberboy, bomb_list=bomb_list)
    maps.render_map(bomberboy)
  

def key_pressed():

    key = str(p5.key).lower()
    
    if key == 'w': 

        bomberboy.direction = 'up'
        #Checks if the move entering a valid space

    elif key == 's': 

        bomberboy.direction = 'down'

    elif key == 'd': 

        bomberboy.direction = 'right'

    elif key == 'a': 

        bomberboy.direction = 'left'

    elif key == ' ':
        
        bomberboy.place_bomb(bomb_list=bomb_list)
        return
    
    #Default action is movement if not bomb

    bomberboy.move()
    




    #Debug statement, keep in mind that the coordinate here will not be updated yet
    # print(f"Keypress: |{key}| Direction: {bomberboy.direction} Coordinate: {bomberboy.position}")
    # print(bomberboy.target_coord, len(bomb_list))

p5.run_sketch()
