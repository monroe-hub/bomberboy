import py5 as p5
import pyautogui as pag #for manipulating player mouse
import numpy as np
from os import path

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

            else:
                p5.push()
                p5.fill(0)
                p5.square(x, y, tile_size)
                p5.pop()


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

    global count
    count = p5.millis
    

    
    # print(test_map)

def draw():
    global test_map
    render_map(test_map, tile_size=64)


    
    
    # if p5.millis() - 5000 < 0: 
    #     test_map = np.random.randint(0, 3, size=(10, 10))

p5.run_sketch()
