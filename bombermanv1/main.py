import py5 as p5
import pyautogui as pag #for manipulating player mouse
import numpy as np
from os import path
from abc import ABC, abstractmethod


class Player:

    def __init__(self, grid_pos, active_map, coordinate_map, size):
        
        self.active_map = active_map
        self.coordinate_map = coordinate_map

        self.position = grid_pos
        self.direction = None 
        self.visual_direction = 'down'

        self.target_coord = None

        self.health = 3
        self.size = size

        self.action_queue = []

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
        self.check_space()

        #If the player is already moving, do not make another move
        if len(self.action_queue) > 0: return

        #If not facing the correct direction, updates visual direction
        if self.visual_direction != self.direction:
            self.visual_direction = self.direction
            if self.target_coord == None: return
            else: return

        #If move was invalid, refuses move
        if self.visual_direction == self.direction:

            if self.target_coord == None: return

            #Adds steps to the action queue
            for i in range(1, 17):
                #Horizontal
                if self.direction == 'left' or self.direction == 'right':

                    if self.direction == 'left': i *= -1
                    #Origin + Step Increment (distance / 64)

                    self.action_queue.append( (self.coordinate_map[self.position][0] + ((self.size / 16) * i), self.coordinate_map[self.position][1]) ) #Tuple

                if self.direction == 'up' or self.direction == 'down':

                    if self.direction == 'up': i *= -1
                    
                    
                    self.action_queue.append( (self.coordinate_map[self.position][0], self.coordinate_map[self.position][1] + ((self.size / 16) * i)) )

            self.position = self.target_coord

            self.check_space()
        
        self.direction = None    
        

    def place_bomb(self, bomb_list):

        if self.target_coord != None and self.active_map[self.target_coord] == 0:\
            bomb_list.append(Bomb(self.target_coord))

class Enemy(ABC):

    def __init__(self, grid_pos, active_map, type=(6, 'crab')):
        
        self.active_map = active_map

        self.position = grid_pos
        self.direction = None 
        self.visual_direction = 'down'

        self.target_coord = None

        self.health = 3

        self.type = type
        self.action = None

        

        


    @abstractmethod
    def decide_action(self):
        pass
        
    @abstractmethod
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

    @abstractmethod      
    def move(self):
        # if self.direction != None: self.visual_direction = self.direction

        self.check_space()

        #If not facing the correct direction, updates visual direction
        if self.visual_direction != self.direction:
            self.visual_direction = self.direction

            #Target coord can begin uninitialized; this handles that
            if self.target_coord == None: return

            else: return

        #If move was invalid, refuses move
        if self.visual_direction == self.direction:

            if self.target_coord == None: return

            self.position = self.target_coord
            self.check_space()
        
        self.direction = None    

class Crab(Enemy):

    def __init__(self, grid_pos, active_map):
        super().__init__(grid_pos, active_map, type=(6, 'crab'))

        self.last_move_time = p5.millis()
        self.move_delay = 1000  # milliseconds between moves (1 second)

        side_spaces = 0
        up_spaces = 0

        for x in range(-1, 1):

            if self.active_map[grid_pos[0] + x, grid_pos[1]] == 0:

                side_spaces += 1

        for y in range(-1, 1):

            if self.active_map[grid_pos[0], grid_pos[1] + y] == 0:

                up_spaces += 1

        if side_spaces >= up_spaces:

            self.crab_walk = 'horizontal'
        else:
            self.crab_walk = 'vertical'

    def decide_action(self):

        if self.crab_walk == 'horizontal':
            directions = ['left', 'right']
        if self.crab_walk == 'vertical':
            directions = ['up', 'down']


        #This checks if a half second has passed since the last move
        current_time = p5.millis()

        if current_time - self.last_move_time < self.move_delay:
            self.action = None  # Wait
            return
        else:

            seed = p5.random_int(1, 3)

            if seed < 3:
                self.action = None
            else: 
                self.action = 'move'
                self.direction = directions[p5.random_int(0, 1)]
            

    def check_space(self):
        return super().check_space()
        
    def move(self):
        self.last_move_time = p5.millis()
        return super().move()

class Bomb:

    #TODO here: create explosion trails and pulsing bombs

    def __init__(self, grid_pos):

        self.grid_pos = grid_pos
        self.bomb_strength = 1
        
        self.spawn_time = p5.millis()  
        self.time_left = 4000  

    def explosion_check(self):

        if p5.millis() - self.spawn_time >= self.time_left:
            return True
        else:
            return False

class Map:

    def __init__(self, array, tile_size=64):
        
        
        self.array = array
        self.tile_size = tile_size

        self.coordinate_map = np.empty(shape=self.array.shape, dtype=object)
        self.active_map = np.copy(self.array)

        self.init_coords = [p5.width/4 + 50, p5.height/8 + 50]

        for row_index in range(0, array.shape[0]):
            for col_index in range(0, array.shape[1]):

                x = self.init_coords[0] + col_index * tile_size
                y = self.init_coords[1] + row_index * tile_size

                self.coordinate_map[row_index, col_index] = (x, y)        

    def render_map(self, player):
        """This will draw a grid for the corresponding map array."""
        
        for row_index, row_values in enumerate(self.active_map):
            for col_index, position in enumerate(row_values):

                x = self.init_coords[0] + col_index * self.tile_size
                y = self.init_coords[1] + row_index * self.tile_size

                #TODO: Decide if converting the array to an object array is worthwhile.
                #If int, convert to list for iterating
                # values = [position] if isinstance(position, int) else position

                # for value in values:
                    #Draws objects based on the values saved within a particular coordinate

                value = position

                #Text color
                p5.fill(0)

                if value == 1:
                    p5.image(steel_brick, x, y, self.tile_size, self.tile_size)
                    p5.text("1", x, y)

                elif value == 2:
                    
                    p5.image(break_brick, x, y, self.tile_size, self.tile_size)
                    p5.text("2", x, y)

                elif value == 3:
                    p5.push()
                    p5.fill(0)
                    p5.square(x, y, self.tile_size)
                    p5.pop()

                    p5.text("3", x, y)

                elif value == 4:

                    if len(player.action_queue) > 0:

                        x, y = player.action_queue[0]
                        player.action_queue.pop(0)

                    if player.visual_direction == 'down' or player.visual_direction == 'up':

                        p5.image(dave_sprites[0], x, y, self.tile_size, self.tile_size)

                    elif player.visual_direction == 'right':
                        p5.image(dave_sprites[1], x, y, self.tile_size, self.tile_size)

                    elif player.visual_direction == 'left':

                        p5.push_matrix()
                        p5.scale(-1 ,1)
                        p5.image(dave_sprites[1], -x, y, self.tile_size, self.tile_size)
                        p5.pop_matrix()

                    p5.text("4", x, y)

                elif value == 5:
                    
                    for bomb in bomb_list:
                        
                        if bomb.grid_pos == (row_index, col_index):

                            progress = p5.constrain((p5.millis() - bomb.spawn_time) / bomb.time_left, 0, 1)
                            
                            p5.push()

                            p5.fill(255 * progress, 0, 0)
                            
                            # p5.fill(0)
                            p5.circle(x, y, self.tile_size)
                            p5.pop()

                    p5.text("5", x, y)

                elif value == 6:

                    for enemy in enemy_list:
                        
                        if enemy.position == (row_index, col_index):
                        
                            p5.push()

                            p5.image(crab_sprite, x, y, self.tile_size, self.tile_size)
                            # p5.fill(255, 0, 0)
                            # p5.circle(x, y, self.tile_size)
                            p5.pop()

                    p5.text("6", x, y)


    def draw_border(self):

        #TODO: this will draw a layer of uninteractable steel bricks (1) around the map
        pass

    def refresh_map(self, player, bomb_list, enemy_list):
        """Recalculates map logic, updating it within the object. Requires a player object as input for various calculations."""


        for row_index in range(0, self.active_map.shape[0]):
            for col_index in range(0, self.active_map.shape[1]):

                x = row_index
                y = col_index

                if (x, y) == player.position: self.active_map[x, y] = 4
                elif self.active_map[x, y] == 4: self.active_map[x, y] = 0

                for i, enemy in enumerate(enemy_list):

                    if enemy.position == (x, y):

                        self.active_map[x, y] = enemy.type[0]

                    enemy.decide_action()

                    if enemy.action == 'move':

                        if enemy.position != None:

                            previous_pos = enemy.position
                            enemy.move()

                            #Do not clear if still
                            if enemy.position != previous_pos:

                                self.active_map[previous_pos[0], previous_pos[1]] = 0

                for i, bomb in enumerate(bomb_list):
                    
                    if bomb.grid_pos == (x, y):

                        # print(bomb.grid_pos, x, y, sep=" ")

                        self.active_map[x, y] = 5

                        if bomb.explosion_check():
                            for i in range(0, bomb.bomb_strength + 1):

                                #This looks digusting but essentially all it does is loop through the neighboring directions, and blow em up
                                p5.push()
                                p5.fill(230, 44, 7)

                                if self.active_map[x + i, y] != 1 and (0 <= x + i <= self.active_map.shape[0] - 1):

                                    if self.active_map[x + i, y] == 4: player.health -= 1

                                    self.active_map[x + i, y] = 0
                                    p5.circle(self.coordinate_map[x + i, y][0], self.coordinate_map[x + i, y][1], self.tile_size)

                                

                                if self.active_map[x - i, y] != 1 and (0 <= x - i <= self.active_map.shape[0] - 1):

                                    if self.active_map[x - i, y] == 4: player.health -= 1

                                    self.active_map[x - i, y] = 0
                                    p5.circle(self.coordinate_map[x - i, y][0], self.coordinate_map[x - i, y][1], self.tile_size)

                                

                                if self.active_map[x, y + i] != 1 and (0 <= y + i <= self.active_map.shape[1] - 1):
                                    
                                    if self.active_map[x, y + i] == 4: player.health -= 1
                                    
                                    self.active_map[x, y + i] = 0
                                    p5.circle(self.coordinate_map[x , y + i][0], self.coordinate_map[x, y + i][1], self.tile_size)

                    

                                if self.active_map[x, y - i] != 1 and (0 <= y - i <= self.active_map.shape[1] - 1):

                                    if self.active_map[x, y - i] == 4: player.health -= 1

                                    self.active_map[x, y - i] = 0
                                    p5.circle(self.coordinate_map[x, y - i][0], self.coordinate_map[x, y - i][1], self.tile_size)

                                if self.active_map[x, y] != 1:
                                    self.active_map[x, y] = 0
                                    p5.circle(self.coordinate_map[x, y][0], self.coordinate_map[x, y][1], self.tile_size)

                                p5.pop()

                            bomb_list.pop(i-1)

    def render_hud(self, player):

        for i in range(0, player.health):
            p5.push()
            p5.image(heart_image, p5.width/8 + (i * self.tile_size), p5.height/8, self.tile_size, self.tile_size)
            p5.pop()


def generate_base_map(size=(10, 10)):

    array = np.zeros(shape=size)
    enemy_coordinates = []

    for row_index in range(0, array.shape[0]):
            for col_index in range(0, array.shape[1]):

                x = row_index
                y = col_index

                if p5.dist(x, y, 1, 1) >= 2: spawn_safe = True
                else: spawn_safe = False

                if x % 2 != 0 and y % 2 != 0:
                    array[x, y] = 1

                elif np.random.randint(0, 6) % 2 == 0 and spawn_safe:
                    array[x, y] = 2

                if stage == 1 and spawn_safe and array[x, y] == 0:

                    if p5.random_int(1, 5) == 5:
                        array[x, y] = 6
                        enemy_coordinates.append((x, y))

    return array, enemy_coordinates

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
    global break_brick, steel_brick, dave_sprites, crab_sprite, heart_image

    image_folder = path.join("bombermanv1", "assets")
    
    # print(image_folder)
    break_brick = load_image(image_folder + path.sep + "destroyable_brick.png")
    steel_brick = load_image(image_folder + path.sep + "steel_brick.png")

    dave_sprites = []
    dave_sprites.append(load_image(image_folder + path.sep + "bomberboy_front.png"))
    dave_sprites.append(load_image(image_folder + path.sep + "bomberboy_side.png"))


    crab_sprite = load_image(image_folder + path.sep + "crab.png")

    heart_image = load_image(image_folder + path.sep + "heart.png")

def settings():
    p5.size(1200, 1000)

    #board size (800x800?)

def setup():
    p5.rect_mode(p5.CENTER)
    p5.image_mode(p5.CENTER)

    # p5.frame_rate(2)

    load_assets()
    p5.background(255)

    global stage
    stage = 1

    returns = generate_base_map((11, 13))

    test_map = returns[0]
    enemy_coordinates = returns[1]

    global maps
    #This is where you should change tile_size
    maps = Map(test_map, 64)

    global dynamite_dave
    dynamite_dave = Player((0, 0), maps.active_map, maps.coordinate_map, 64)
    
    global bomb_list
    bomb_list = []

    global enemy_list 
    enemy_list = []

    for enemy_coords in enemy_coordinates:
        enemy_list.append(Crab(enemy_coords, active_map=maps.active_map))

    


def draw():
    p5.background(255)
    
    maps.refresh_map(dynamite_dave, bomb_list=bomb_list, enemy_list=enemy_list)
    maps.render_map(dynamite_dave)
    maps.render_hud(dynamite_dave)

    #TODO: dave must make movements every couple of frames, with his actions delayed until the first one completes.
    #Do this through internal object timers.
    #player.action_delay


def key_pressed():

    key = str(p5.key).lower()
    
    if key == 'w': 

        dynamite_dave.direction = 'up'
        #Checks if the move entering a valid space
        dynamite_dave.move()

    elif key == 's': 

        dynamite_dave.direction = 'down'
        dynamite_dave.move()

    elif key == 'd': 

        dynamite_dave.direction = 'right'
        dynamite_dave.move()

    elif key == 'a': 

        dynamite_dave.direction = 'left'
        dynamite_dave.move()

    elif key == ' ':
        
        dynamite_dave.place_bomb(bomb_list=bomb_list)
        return
    
    #Debug statement, keep in mind that the coordinate here will not be updated yet
    # print(f"Keypress: |{key}| Direction: {bomberboy.direction} Coordinate: {bomberboy.position}")
    # print(bomberboy.target_coord, len(bomb_list))

p5.run_sketch()
