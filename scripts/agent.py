__author__ = "Aybuke Ozturk Suri, Johvany Gustave"
__copyright__ = "Copyright 2023, IN512, IPSA 2024"
__credits__ = ["Aybuke Ozturk Suri", "Johvany Gustave"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"

from network import Network
from my_constants import *

from threading import Thread
import numpy as np
from time import sleep


class Agent:
    """ Class that implements the behaviour of each agent based on their perception and communication with other agents """
    def __init__(self, server_ip):
        #TODO: DEFINE YOUR ATTRIBUTES HERE
        
        self.new_cell_val_ready = False
        self.swimlane_direction = DOWN  # Initial direction for swimlane movement
        self.swimlane_decision = RIGHT
        self.swimlaneH = RIGHT
        self.swimlaneV = DOWN
        self.step_to_move = 0
                
        self.direction_dictionary = {
            LEFT: (-1, 0),   # LEFT
            RIGHT: (1, 0),    # RIGHT
            UP: (0, -1),   # UP
            DOWN: (0, 1),    # DOWN
            UP_LEFT: (-1, -1),  # UP-LEFT
            UP_RIGHT: (1, -1),   # UP-RIGHT
            DOWN_LEFT: (-1, 1),   # DOWN-LEFT
            DOWN_RIGHT: (1, 1)     # DOWN-RIGHT
        }
        
        #DO NOT TOUCH THE FOLLOWING INSTRUCTIONS
        self.network = Network(server_ip=server_ip)
        self.agent_id = self.network.id
        self.running = True
        self.network.send({"header": GET_DATA})
        self.msg = {}
        env_conf = self.network.receive()
        self.nb_agent_expected = 0
        self.nb_agent_connected = 0
        self.x, self.y = env_conf["x"], env_conf["y"]   #initial agent position
        self.w, self.h = env_conf["w"], env_conf["h"]   #environment dimensions
        cell_val = env_conf["cell_val"] #value of the cell the agent is located in
        #print(cell_val)
        Thread(target=self.msg_cb, daemon=True).start()
        #print("hello")
        self.wait_for_connected_agent()
    
        self.cell_memory = [(self.x, self.y)]

        
    def msg_cb(self): 
        """ Method used to handle incoming messages """
        while self.running:
            msg = self.network.receive()
            self.msg = msg
            if msg["header"] == MOVE:
                self.x, self.y =  msg["x"], msg["y"]
                self.new_cell_val_ready = True
                #print(self.x, self.y)
            elif msg["header"] == GET_NB_AGENTS:
                self.nb_agent_expected = msg["nb_agents"]
            elif msg["header"] == GET_NB_CONNECTED_AGENTS:
                self.nb_agent_connected = msg["nb_connected_agents"]

            #print("hellooo: ", msg)
            #print("agent_id ", self.agent_id)
            

    def wait_for_connected_agent(self):
        self.network.send({"header": GET_NB_AGENTS})
        check_conn_agent = True
        while check_conn_agent:
            if self.nb_agent_expected == self.nb_agent_connected:
                #print("both connected!")
                check_conn_agent = False


    #TODO: CREATE YOUR METHODS HERE...
    def wait_for_new_cell_val(self):
        while not self.new_cell_val_ready:
            sleep(0.01)
        self.new_cell_val_ready = False
        return self.msg.get("cell_val", STAND)
    
    def inverse_direction(self,direction):
        if direction == RIGHT:
            self.swimlaneH = LEFT
        elif direction == LEFT:
            self.swimlaneH = RIGHT
        elif direction == UP:
            self.swimlaneV = DOWN
        elif direction == DOWN:
            self.swimlaneV = UP
        return
    
    def Direction_at_start(self):
        if self.x < self.w / 2:
            self.swimlaneH = RIGHT
        else:
            self.swimlaneH = LEFT
        if self.y < self.h / 2:
            self.swimlaneV = DOWN
        else:
            self.swimlaneV = UP

    def swimlane_move_agent(self):
        sleep(0.5)
        step = 4 
        offset = 2
        H,W = self.h-1, self.w-1

        if self.swimlaneH == RIGHT:
            if self.swimlaneV == DOWN:
                if self.x < W-offset and self.y < H-offset:
                    self.step_to_move = 99999
                    self.network.send({"header": MOVE, "direction": self.swimlaneV})
                    self.wait_for_new_cell_val()
            
                elif self.x < H and self.x <= self.step_to_move:
                    if self.step_to_move == 99999:
                        self.step_to_move = self.x+step
                    self.network.send({"header": MOVE, "direction": self.swimlaneH})
                    self.wait_for_new_cell_val()
                
                elif self.x >= self.step_to_move:
                    self.inverse_direction(self.swimlaneV)
            
            elif self.swimlaneV == UP:
                if self.x < W and self.y > offset:
                    self.step_to_move = 99999
                    self.network.send({"header": MOVE, "direction": self.swimlaneV})
                    self.wait_for_new_cell_val()
            
                elif self.x < W and self.x <= self.step_to_move:
                    if self.step_to_move == 99999:
                        self.step_to_move = self.x+step
                    self.network.send({"header": MOVE, "direction": self.swimlaneH})
                    self.wait_for_new_cell_val()
                
                elif self.x >= self.step_to_move:
                    self.inverse_direction(self.swimlaneV)

        elif self.swimlaneH == LEFT:
            if self.swimlaneV == DOWN:
                if self.x > 0 and self.y < H-offset:
                    self.step_to_move = -99999
                    self.network.send({"header": MOVE, "direction": self.swimlaneV})
                    self.wait_for_new_cell_val()
            
                elif self.x > 0 and self.x >= self.step_to_move:
                    if self.step_to_move == -99999:
                        self.step_to_move = self.x-step
                    self.network.send({"header": MOVE, "direction": self.swimlaneH})
                    self.wait_for_new_cell_val()
                
                elif self.x <= self.step_to_move:
                    self.inverse_direction(self.swimlaneV)
            
            elif self.swimlaneV == UP:
                if self.x > 0 and self.y > offset:
                    self.step_to_move = -99999
                    self.network.send({"header": MOVE, "direction": self.swimlaneV})
                    self.wait_for_new_cell_val()
            
                elif self.x > 0 and self.x >= self.step_to_move:
                    if self.step_to_move == -99999:
                        self.step_to_move = self.x-step
                    self.network.send({"header": MOVE, "direction": self.swimlaneH})
                    self.wait_for_new_cell_val()
                
                elif self.x <= self.step_to_move:
                    self.inverse_direction(self.swimlaneV)
        return

    def move_with_item_in_range(self, cell_val):

        valid_cells = []
        for direction, (dx, dy) in self.direction_dictionary.items():
            new_x, new_y = self.x + dx, self.y + dy
            if (new_x, new_y) not in self.cell_memory and 0 <= new_x < self.w and 0 <= new_y < self.h:
                valid_cells.append((direction, new_x, new_y))

        #print("Valid cells to move to:", valid_cells)
        
        if valid_cells:
            if cell_val == 1:
                #print("Key in range!")
                self.network.send({"header": BROADCAST_MSG, "type": KEY_DISCOVERED, "agent_id": self.agent_id})
                owner = self.msg.get('owner_id', self.agent_id)
                print("Owner of the key is agent:", owner)
                for i in range(3):
                    self.wait_for_new_cell_val()
                    self.swimlane_move_agent()
            else:
                move = valid_cells[np.random.randint(len(valid_cells))]
                
                # Send move
                self.network.send({"header": MOVE, "direction": move[0]})
                new_val = self.wait_for_new_cell_val()  # server updates self.x, self.y

                # Check if move was bad
                if new_val <= cell_val:
                    #print("J'ai fait un mauvais move, je reviens en arrière")
                    self.memory_update()
                    
                    # After detecting a bad move:
                    # Original move direction
                    dx, dy = self.direction_dictionary[move[0]]

                    # Find reverse direction
                    reverse_direction = None
                    for d, (rx, ry) in self.direction_dictionary.items():
                        if (rx, ry) == (-dx, -dy):
                            #print("Found reverse direction:", d)
                            reverse_direction = d
                            break

                    if reverse_direction is not None:
                        self.network.send({"header": MOVE, "direction": reverse_direction})
                        self.wait_for_new_cell_val()

                else:
                    #print("J'ai fait un bon move")
                    pass


    def direction_from_target(self, target_x, target_y):
        
        dx = target_x - self.x
        dy = target_y - self.y
        
        for direction, (x, y) in self.direction_dictionary.items():
            if (dx, dy) == (x, y):
                if 0 <= target_x < self.w and 0 <= target_y < self.h:
                    return direction
        return None

    def avoid_wall_move_agent(self):
        last_cell_visited = self.cell_memory[-2]
        direction = self.direction_from_target(last_cell_visited[0], last_cell_visited[1])
        if direction is not None:
            #print("\n\nVoici la direction : ",direction,"\n\n")
            self.network.send({"header": MOVE, "direction": direction})
            self.wait_for_new_cell_val()
            if direction == DOWN or direction == UP:
                self.network.send({"header": MOVE, "direction": self.swimlaneH})
            else:
                if self.x < self.w / 2:
                    self.swimlaneV = DOWN
                else:
                    self.swimlaneV = UP
                self.network.send({"header": MOVE, "direction": self.swimlaneV})
            
            self.wait_for_new_cell_val()

    def memory_update(self):
        """ Update the memory of the agent with the value of the cell it is currently located in """
        cell = (self.x, self.y)
        if cell not in self.cell_memory:
            self.cell_memory.append(cell)



if __name__ == "__main__":
    from random import randint
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--server_ip", help="Ip address of the server", type=str, default="localhost")
    args = parser.parse_args()

    agent = Agent(args.server_ip)
    
    try:
        agent.Direction_at_start()
        _move_count = 0
        while True:
            print(f"-------------------- New Move {_move_count} --------------------")
            cell_val = agent.msg.get("cell_val", 0)
            print(f"cell val for robot {agent.msg.get('owner_id', agent.agent_id)}: ", cell_val)
            if  cell_val == 0:
                print("Swimlane movement")
                agent.swimlane_move_agent()
            elif cell_val < 0:
                print("Avoiding wall")
                agent.avoid_wall_move_agent()
            elif cell_val > 0:
                print("Moving with item in range")
                agent.move_with_item_in_range(cell_val)
            _move_count += 1
            agent.memory_update()
            #sleep(1)


    except KeyboardInterrupt:
        pass
# it is always the same location of the agent first location



