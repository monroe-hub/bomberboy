import py5 as p5
import pyautogui as pag #for manipulating player mouse
import numpy as np
from os import path

class Player:

    def __init__(self, grid_pos):
        
        self.position = grid_pos
        self.direction = None

        self.health = 3


    def conjure(coords):

        p5.push()
        p5.no_stroke()
        p5.fill(0, 135, 135)
        p5.circle(coords[0], coords[1], 64)
        p5.pop()

    def move(self):

        if self.direction == None: pass
        elif self.direction == 'up': 
            self.position = (self.position[0], self.position[1] + 1)
        elif self.direction == 'down': 
            self.position = (self.position[0], self.position[1] - 1)
        elif self.direction == 'right': 
            self.position = (self.position[0] + 1, self.position[1])
        elif self.direction == 'left': 
            self.position = (self.position[0] - 1, self.position[1])

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

def load_assets():
    """Attempts to load all relevant assets (images, etc.) and places them into the global namespace."""
    global break_brick, steel_brick

    image_folder = path.join("bombermanv1", "assets")
    
    # print(image_folder)
    break_brick = load_image(image_folder + path.sep + "destroyable_brick.png")
    steel_brick = load_image(image_folder + path.sep + "steel_brick.png")



def render_map(array, tile_size = 80):
    """This will draw a grid for the corresponding map array."""

    init_coords = [100, 100]
    

    for row_index, row_values in enumerate(array):
        for col_index, position in enumerate(row_values):
            
            x = init_coords[0] + col_index * tile_size
            y = init_coords[1] + row_index * tile_size

            if position == 2:
                
                p5.image(break_brick, x, y, tile_size, tile_size)
            elif position == 1:
                p5.image(steel_brick, x, y, tile_size, tile_size)

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

def create_coordinate_space(array, tile_size = 80):
    """Creates from a given array two returned arrays: a coordinate map, where each cartesian grid coordinate in the array corresponds to its drawn position in 
        Processing's screen-space, and an active map, where each cartesian grid coordinate in the array 
        corresponds to a possible data value; this begins with the values of the parameterized array.
    """


    init_coords = [100, 100]

    coordinate_map = np.empty(shape=array.shape, dtype=object)
    active_map = np.copy(array)

    for row_index in range(0, array.shape[0]):
        for col_index in range(0, array.shape[1]):

            x = init_coords[0] + col_index * tile_size
            y = init_coords[1] + row_index * tile_size

            coordinate_map[row_index, col_index] = (x, y)


    return active_map, coordinate_map



def settings():
    p5.size(1000, 1000)
    #board size (800x800?)

def setup():
    p5.rect_mode(p5.CENTER)
    p5.image_mode(p5.CENTER)

    load_assets()
    p5.background(255)

    global test_map
    test_map = np.random.randint(0, 3, size=(11, 13))
    
    global coordinate_map, active_map
    coordinate_map = create_coordinate_space(test_map, tile_size=64)[1]
    active_map = create_coordinate_space(test_map, tile_size=64)[0]
    
    global bomberboy
    bomberboy = Player((1, 1))
    active_map[bomberboy.position[0], bomberboy.position[1]] = 4

def draw():
    global active_map
    #recalculates active map, looking for changes
    active_map = create_coordinate_space(active_map, tile_size=64)[0]


    global test_map
    render_map(active_map, tile_size=64)

def key_pressed(key):

    key = str(key).lower()

    if key == 'w': bomberboy.direction = 'up'
    elif key == 's': bomberboy.direction = 'down'
    elif key == 'd': bomberboy.direction = 'right'
    elif key == 'a': bomberboy.direction = 'left'
        

    


p5.run_sketch()
