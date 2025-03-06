import py5 as p5
import pyautogui as pag #for manipulating player mouse
import numpy as np
import os

def load_image(file_path):
    #Loads an image without crashing script
    try:
        image = p5.load_image(file_path)
        return image
    except: 
        
        print("Error loading image")
        return None

def load_assets():
    global brick
    os.path()
    break_brick = load_image(os.pardir + os.sep + "destroyable_brick.png")



def render_map():
    
    #This will draw a grid for the corresponding map array.
    pass


def settings():
    p5.size(1500, 1000)

def setup():
    load_assets()
    p5.background(255)

    test_arr = np.random.randint(0, 3, size=(10, 10))
    # print(test_arr)

def draw():

    pass

p5.run_sketch()
