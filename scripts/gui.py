__author__ = "Aybuke Ozturk Suri, Johvany Gustave"
__copyright__ = "Copyright 2023, IN512, IPSA 2024"
__credits__ = ["Aybuke Ozturk Suri", "Johvany Gustave"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"

import pygame, os
import numpy as np
from my_constants import * 

img_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources", "img")


class GUI:
    def __init__(self, game, fps=10, cell_size=30):
        self.game = game
        self.w, self.h = self.game.map_w, self.game.map_h
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.cell_size = cell_size
        self.screen_res = (self.w*cell_size, self.h*cell_size)      


    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_res)
        pygame.display.set_icon(pygame.image.load(img_folder + "/icon.png"))
        pygame.display.set_caption("IN512 Project")
        self.create_items()        
        self.running = True

    def is_coord_taken(self,x,y):
        robot_pos_encounter = False
        # Check robots' position
        for pos in self.game.agents:
            if pos.x == x and pos.y == y:
                robot_pos_encounter = True
        
        # Check keys' and chests' position
        coord_taken = self.game.map_real[y, x] != 0.0 or robot_pos_encounter
        
        return coord_taken
    
    def available_directions(self,x,y):
        available_directions = dict()
        # Check if left wing available
        if not self.is_coord_taken(x-1,y) and not self.is_coord_taken(x-2,y):
            if 0 <= x-2 and x-2 < self.w:
                print("Left wing available")
                available_directions["LEFT"] = [(x-1,y),(x-2,y)]
        # Check if right wing available
        if not self.is_coord_taken(x+1,y) and not self.is_coord_taken(x+2,y):
            if 0 <= x+2 and x+2 < self.w:
                print("Right wing available")
                available_directions["RIGHT"] = [(x+1,y),(x+2,y)]
        # Check if up wing available
        if not self.is_coord_taken(x,y-1) and not self.is_coord_taken(x,y-2):
            if 0 <= y-2 and y-2 < self.h:
                print("Up wing available")
                available_directions["UP"] = [(x,y-1),(x,y-2)]
        # Check if down wing available
        if not self.is_coord_taken(x,y+1) and not self.is_coord_taken(x,y+2):
            if 0 <= y+2 and y+2 < self.h:
                print("Down wing available")
                available_directions["DOWN"] = [(x,y+1),(x,y+2)]
        print("END AVAILABLE_DIRECTIONS\n________________________")
        return available_directions

    def generate_wall_coord(self):
        rand_x = np.random.randint(self.w)
        rand_y = np.random.randint(self.h)
        
        # Verify if the positions are not yet taken
        while self.is_coord_taken(rand_x,rand_y):
            rand_x = np.random.randint(self.w)
            rand_y = np.random.randint(self.h)
        
        # Check possible wall directions
        #directions = self.available_directions(rand_x,rand_y)
        
        # Check if we can have a L-shape wall without collisions
        # print("len(directions) : ",len(directions))
        # if len(directions) < 2:
        #     print("ARCHEEUEEEEUUUUUUUUUUMM 1 /!\\")
        #     rand_x,rand_y = self.generate_wall_coord()[:1]
        #     directions = self.available_directions(rand_x,rand_y)
        
        # possible_choices = []
        # for direction in DIRECTIONS_COMBINATIONS:
        #     print("direction keys : ",directions.keys())
        #     print("direction[0] : ", direction[0])
        #     print("direction[1] : ", direction[1])
        #     if direction[0] in directions.keys() and direction[1] in directions.keys():
        #         print("direction[0] : ", direction[0])
        #         print("direction[1] : ", direction[1])
        #         possible_choices.append(direction)
        
        # while possible_choices == []:
        #     print("ARCHEEUEEEEUUUUUUUUUUMM 2 /!\\")
        #     rand_x, rand_y = self.generate_wall_coord()[:1]
        #     for direction in DIRECTIONS_COMBINATIONS:
        #         if direction[0] in directions.keys() and direction[1] in directions.keys():
        #             possible_choices.append(direction)
        
        # print("Possible_choices : ",possible_choices)
        # rand_index = np.random.randint(len(possible_choices))
        # print("rand_index : ",rand_index)
        # chosen_direction = possible_choices[rand_index]
        
        # print("chosen_direction : ",chosen_direction)
        
        return rand_x,rand_y #,chosen_direction
        
    
    
    def create_walls(self, wall_img):
        self.walls = [wall_img.copy() for _ in range(self.game.walls_number)]
        self.walls_pos = []
        for wall in range(self.game.walls_number*5):
            print(f"\nGENERATION OF WALL NUMBER {wall} /!\\\n")
            rand_x,rand_y = self.generate_wall_coord()
            
            self.game.add_val(rand_x,rand_y,WALL_PERCENTAGE)
            self.walls_pos.append((rand_x,rand_y))
            
            # for d in direction:
            #     print("d : ",d)
            #     if d == "RIGHT":
            #         self.game.add_val(rand_x+1,rand_y,WALL_PERCENTAGE)
            #         self.walls_pos.append((rand_x+1,rand_y))
            #         self.game.add_val(rand_x+2,rand_y,WALL_PERCENTAGE)
            #         self.walls_pos.append((rand_x+2,rand_y))
            #     elif d == "LEFT":
            #         self.game.add_val(rand_x-1,rand_y,WALL_PERCENTAGE)
            #         self.walls_pos.append((rand_x-1,rand_y))
            #         self.game.add_val(rand_x-2,rand_y,WALL_PERCENTAGE)
            #         self.walls_pos.append((rand_x-2,rand_y))
            #     elif d == "UP":
            #         self.game.add_val(rand_x,rand_y-1,WALL_PERCENTAGE)
            #         self.walls_pos.append((rand_x,rand_y-1))
            #         self.game.add_val(rand_x,rand_y-2,WALL_PERCENTAGE)
            #         self.walls_pos.append((rand_x,rand_y-2))
            #     elif d == "DOWN":
            #         self.game.add_val(rand_x,rand_y+1,WALL_PERCENTAGE)
            #         self.walls_pos.append((rand_x,rand_y+1))
            #         self.game.add_val(rand_x,rand_y+2,WALL_PERCENTAGE)
            #         self.walls_pos.append((rand_x,rand_y+2))
            
            print(f"\n------------------\nwall number : {wall}/{self.game.walls_number}\nrandom wall_position : {self.walls_pos}\n------------------\n")

    def create_items(self):
        #box
        box_img = pygame.image.load(img_folder + "/box.png")
        box_img = pygame.transform.scale(box_img, (self.cell_size, self.cell_size))
        self.boxes = [box_img.copy() for _ in range(self.game.nb_agents)]
        #keys
        key_img = pygame.image.load(img_folder + "/key.png")
        key_img = pygame.transform.scale(key_img, (self.cell_size, self.cell_size))
        self.keys = [key_img.copy() for _ in range(self.game.nb_agents)]
        #agent text number
        font = pygame.font.SysFont("Arial", self.cell_size//4, True)
        self.text_agents = [font.render(f"{i+1}", True, self.game.agents[i].color) for i in range(self.game.nb_agents)]
        #agent_img
        agent_img = pygame.image.load(img_folder + "/robot.png")
        agent_img = pygame.transform.scale(agent_img, (self.cell_size, self.cell_size))
        self.agents = [agent_img.copy() for _ in range(self.game.nb_agents)]
        #wall_img
        wall_img = pygame.image.load(img_folder + "/wall.png")
        wall_img = pygame.transform.scale(wall_img, (self.cell_size, self.cell_size))
        self.create_walls(wall_img)

    
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    
    def on_cleanup(self):
        pygame.event.pump()
        pygame.quit()
    

    def render(self):
        try:
            self.on_init()
            while self.running:
                for event in pygame.event.get():
                    self.on_event(event)    
                self.draw()
                self.clock.tick(self.fps)
            self.on_cleanup()
        except Exception:
            pass
    

    def draw(self):
        self.screen.fill(BG_COLOR)
        #Grid
        for i in range(1, self.h):
            pygame.draw.line(self.screen, BLACK, (0, i*self.cell_size), (self.w*self.cell_size, i*self.cell_size))
        for j in range(1, self.w):
            pygame.draw.line(self.screen, BLACK, (j*self.cell_size, 0), (j*self.cell_size, self.h*self.cell_size))

        for i in range(self.game.nb_agents):
            #agent_paths
            for x, y in self.game.agent_paths[i]:
                pygame.draw.rect(self.screen, self.game.agents[i].color, (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))

        for i in range(self.game.nb_agents):            
            #keys
            pygame.draw.rect(self.screen, self.game.agents[i].color, (self.game.keys[i].x*self.cell_size, self.game.keys[i].y*self.cell_size, self.cell_size, self.cell_size), width=3)
            self.screen.blit(self.keys[i], self.keys[i].get_rect(topleft=(self.game.keys[i].x*self.cell_size, self.game.keys[i].y*self.cell_size)))
            
            #boxes
            pygame.draw.rect(self.screen, self.game.agents[i].color, (self.game.boxes[i].x*self.cell_size, self.game.boxes[i].y*self.cell_size, self.cell_size, self.cell_size), width=3)
            self.screen.blit(self.boxes[i], self.boxes[i].get_rect(topleft=(self.game.boxes[i].x*self.cell_size, self.game.boxes[i].y*self.cell_size)))
            
            #agents
            self.screen.blit(self.agents[i], self.agents[i].get_rect(center=(self.game.agents[i].x*self.cell_size + self.cell_size//2, self.game.agents[i].y*self.cell_size + self.cell_size//2)))
            self.screen.blit(self.text_agents[i], self.text_agents[i].get_rect(center=(self.game.agents[i].x*self.cell_size + self.cell_size-self.text_agents[i].get_width()//2, self.game.agents[i].y*self.cell_size + self.cell_size-self.text_agents[i].get_height()//2)))

        for i in range(self.game.walls_number):
            #walls
            self.screen.blit(self.walls[i], self.walls[i].get_rect(center=(self.walls_pos[i][0]*self.cell_size + self.cell_size//2, self.walls_pos[i][1]*self.cell_size + self.cell_size//2)))
        pygame.display.update()