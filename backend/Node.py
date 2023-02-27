import copy # deepcopy
from utils import  * # helper functions

# Node class -- configuration of ship grid at current time
class Node:
    def __init__(self, state, buffer_state, unloads, sequence_type='transfer', parent=None, cost=0):
        self.state = state # container configuration in ship
        self.buffer_state = buffer_state # container configuration in buffer
        self.unloads = unloads # list of containers to be unloaded
        self.sequence_type = sequence_type # operation to perform ('transfer' or 'balance')
        self.parent = parent # pointer to parent node
        self.g = cost # cost from parent to current node
        self.h = 0 # cost to reach goal from current node

        if self.sequence_type == 'transfer':
            self.transfer_heuristic() # updates node with cost to goal state for a transfer sequence
        else:
            self.balance_heuristic() # updates node with cost to goal state for a balance sequence

    # calculates the total time it would take to reach goal state from current state
    # in this case, goal state = all desired containers removed from ship
    def transfer_heuristic(self):
        total_cost = 0
        for cont in self.unloads:
            possible_conts = []

            # finds all containers with desired descriptions (ie. all
            # containers with "Cat" in them)
            for key, value in self.state.items():
                if value[1] == cont[1]:
                    possible_conts.append(key)
        
            if possible_conts:
                # finds least burdened container
                chosen_cont = min([(count_containers_above(self.state, i), i) for i in possible_conts])[1]
                
                # calculates time to fully unload from ship and onto truck
                # manhattan distance + 2 min (time to load onto truck)
                cont_cost = abs(unload_zone[0] - chosen_cont[0]) + abs(unload_zone[1] - chosen_cont[1]) + 2

                total_cost += cont_cost


        # ** TESTING DIFFERENT HEURISTICS **
        # f = len([i for i in self.state.values() if i[1] != 'UNUSED'])
        # f = (ROWS * COLS) // 2 if f > (ROWS * COLS) // 2 else f
        # self.h = (f * total_cost) / ROWS

        # comment this line out if testing other heuristics
        self.h = total_cost

    # calculates the total time it would take to reach goal state from current state
    # in this case, goal state = mass of heavier side / mass of lighter side < 1.1
    # and buffer is empty
    def balance_heuristic(self):
        self.h = 0

    # finds all possible child nodes (moves) from current state
    def children(self):
        child_nodes = [] # holds all child nodes
        for col in range(COLS):
            for row in range(ROWS):
                key = (row + 1, col + 1)
                value = self.state[key]

                # no more valid containers in column
                if value[1] == 'UNUSED':
                    break

                # space holds container
                if value[1] != 'NAN':
                    # top row
                    if key[0] == ROWS:
                        # load/unload operation
                        if self.sequence_type == 'transfer':
                            # container to be unloaded
                            if (value[0], value[1]) in self.unloads:
                                # remove container from ship
                                new_ship = copy.deepcopy(self.state) 
                                new_ship[key][0] = 0
                                new_ship[key][1] = 'UNUSED'

                                # update unload list
                                new_unloads = list(self.unloads)
                                new_unloads.remove((value[0], value[1]))

                                # calculates time to fully unload from ship and onto truck
                                # manhattan distance + 2 min (time to load onto truck)
                                cont_cost = abs(unload_zone[0] - key[0]) + abs(unload_zone[1] - key[1]) + 2

                                # create new node and add it to list of child nodes
                                new_child = Node(new_ship, copy.deepcopy(self.buffer_state), new_unloads, self, self.g + cont_cost)
                                child_nodes.append(new_child)
                            # container to be moved but not unloaded
                            else:
                                # check for valid spots within ship bay
                                for k, v in self.state.items():
                                    # space is not in same column as container
                                    # space is available to be moved into
                                    if k[1] != key[1] and v[1] == 'UNUSED':
                                        # check if space below is occupied
                                        # or on bottom row
                                        if k[0] == 1 or self.state[(k[0] - 1, k[1])][1] != 'UNUSED':
                                            # move container to available space
                                            new_ship = copy.deepcopy(self.state)
                                            new_ship[k] = list(new_ship[key])
                                            new_ship[key][0] = 0
                                            new_ship[key][1] = 'UNUSED'

                                            # calculate cost of move
                                            cont_cost = abs(key[0] - k[0]) + abs(key[1] - k[1])

                                            # create new node and add it to list of child nodes
                                            new_child = Node(new_ship, copy.deepcopy(self.buffer_state), list(self.unloads), self, self.g + cont_cost)
                                            child_nodes.append(new_child)

                                # check for valid spot within buffer
                                spot_found = False
                                for c in range(BUFF_COLS - 1, -1, -1):
                                    for r in range(BUFF_ROWS):
                                        if self.buffer_state[(r + 1, c + 1)][1] == 'UNUSED':
                                            spot_found = True

                                            # move container to open space in buffer
                                            new_ship = copy.deepcopy(self.state)
                                            new_buff = copy.deepcopy(self.buffer_state)
                                            new_buff[(r + 1, c + 1)] = list(new_ship[key])

                                            # mark previous space as empty
                                            new_ship[key][0] = 0
                                            new_ship[key][1] = 'UNUSED'

                                            # calculate cost of move
                                            # ship -> unload_zone -> buff_unload 
                                            # -> buffer
                                            cont_cost = abs(unload_zone[0] - key[0]) + abs(unload_zone[1] - key[1]) + 4 + abs(buff_unload[0] - (r + 1)) + abs(buff_unload[1] - (c + 1))

                                            # create new node and add it to list of
                                            # children
                                            new_child = Node(new_ship, new_buff, list(self.unloads), self, self.g + cont_cost)
                                            child_nodes.append(new_child)
                                            break
                                    if spot_found:
                                        break

                        # balance operation
                        if self.sequence_type == 'balance':
                            # check for valid spots within ship bay
                            for k, v in self.state.items():
                                # space is not in same column as container
                                # space is available to be moved into
                                if k[1] != key[1] and v[1] == 'UNUSED':
                                    # check if space below is occupied
                                    # or on bottom row
                                    if k[0] == 1 or self.state[(k[0] - 1, k[1])][1] != 'UNUSED':
                                        # move container to available space
                                        new_ship = copy.deepcopy(self.state)
                                        new_ship[k] = list(new_ship[key])
                                        new_ship[key][0] = 0
                                        new_ship[key][1] = 'UNUSED'

                                        # calculate cost of move
                                        cont_cost = abs(key[0] - k[0]) + abs(key[1] - k[1])

                                        # create new node and add it to list of child nodes
                                        new_child = Node(new_ship, copy.deepcopy(self.buffer_state), list(self.unloads), self, self.g + cont_cost)
                                        child_nodes.append(new_child)

                            # check for valid spot within buffer
                            spot_found = False
                            for c in range(BUFF_COLS - 1, -1, -1):
                                for r in range(BUFF_ROWS):
                                    if self.buffer_state[(r + 1, c + 1)][1] == 'UNUSED':
                                        spot_found = True

                                        # move container to open space in buffer
                                        new_ship = copy.deepcopy(self.state)
                                        new_buff = copy.deepcopy(self.buffer_state)
                                        new_buff[(r + 1, c + 1)] = list(new_ship[key])

                                        # mark previous space as empty
                                        new_ship[key][0] = 0
                                        new_ship[key][1] = 'UNUSED'

                                        # calculate cost of move
                                        # ship -> unload_zone -> buff_unload 
                                        # -> buffer
                                        cont_cost = abs(unload_zone[0] - key[0]) + abs(unload_zone[1] - key[1]) + 4 + abs(buff_unload[0] - (r + 1)) + abs(buff_unload[1] - (c + 1))

                                        # create new node and add it to list of
                                        # children
                                        new_child = Node(new_ship, new_buff, list(self.unloads), self, self.g + cont_cost)
                                        child_nodes.append(new_child)
                                        break
                                if spot_found:
                                    break

                    # not top row
                    else:
                        # nothing on top of container
                        if self.state[(key[0] + 1, key[1])][1] == 'UNUSED':
                            # load/unload operation
                            if self.sequence_type == 'transfer':
                                # container to be unloaded
                                if (value[0], value[1]) in self.unloads:
                                    # remove container from ship
                                    new_ship = copy.deepcopy(self.state)
                                    new_ship[key][0] = 0
                                    new_ship[key][1] = 'UNUSED'

                                    # update unload list
                                    new_unloads = list(self.unloads)
                                    new_unloads.remove((value[0], value[1]))

                                    # calculates time to fully unload from ship and onto truck
                                    # manhattan distance + 2 min (time to load onto truck)
                                    cont_cost = abs(unload_zone[0] - key[0]) + abs(unload_zone[1] - key[1]) + 2

                                    # create new node and add it to list of child nodes
                                    new_child = Node(new_ship, copy.deepcopy(self.buffer_state), new_unloads, self, self.g + cont_cost)
                                    child_nodes.append(new_child)
                                # container to be moved but not unloaded
                                else:
                                    # check for valid spot within ship bay
                                    for k, v in self.state.items():
                                        # space is not in same column as container
                                        # space is available to be moved into
                                        if k[1] != key[1] and v[1] == 'UNUSED':
                                            # check if space below is occupied
                                            # or on bottom row
                                            if k[0] == 1 or self.state[(k[0] - 1, k[1])][1] != 'UNUSED':
                                                # move container to available space
                                                new_ship = copy.deepcopy(self.state)
                                                new_ship[k] = list(new_ship[key])
                                                new_ship[key][0] = 0
                                                new_ship[key][1] = 'UNUSED'

                                                # calculate cost of move
                                                cont_cost = abs(key[0] - k[0]) + abs(key[1] - k[1])

                                                # create new node and add it to list of child nodes
                                                new_child = Node(new_ship, copy.deepcopy(self.buffer_state), list(self.unloads), self, self.g + cont_cost)
                                                child_nodes.append(new_child)
                                    
                                    # check for valid spot within buffer
                                    spot_found = False
                                    for c in range(BUFF_COLS - 1, -1, -1):
                                        for r in range(BUFF_ROWS):
                                            if self.buffer_state[(r + 1, c + 1)][1] == 'UNUSED':
                                                spot_found = True

                                                # move container to open space in buffer
                                                new_ship = copy.deepcopy(self.state)
                                                new_buff = copy.deepcopy(self.buffer_state)
                                                new_buff[(r + 1, c + 1)] = list(new_ship[key])

                                                # mark previous space as empty
                                                new_ship[key][0] = 0
                                                new_ship[key][1] = 'UNUSED'

                                                # calculate cost of move
                                                # ship -> unload_zone -> buff_unload 
                                                # -> buffer
                                                cont_cost = abs(unload_zone[0] - key[0]) + abs(unload_zone[1] - key[1]) + 4 + abs(buff_unload[0] - (r + 1)) + abs(buff_unload[1] - (c + 1))

                                                # create new node and add it to list of
                                                # children
                                                new_child = Node(new_ship, new_buff, list(self.unloads), self, self.g + cont_cost)
                                                child_nodes.append(new_child)
                                                break
                                        if spot_found:
                                            break

                            # balance operation
                            if self.sequence_type == 'balance':
                                # check for valid spot within ship bay
                                for k, v in self.state.items():
                                    # space is not in same column as container
                                    # space is available to be moved into
                                    if k[1] != key[1] and v[1] == 'UNUSED':
                                        # check if space below is occupied
                                        # or on bottom row
                                        if k[0] == 1 or self.state[(k[0] - 1, k[1])][1] != 'UNUSED':
                                            # move container to available space
                                            new_ship = copy.deepcopy(self.state)
                                            new_ship[k] = list(new_ship[key])
                                            new_ship[key][0] = 0
                                            new_ship[key][1] = 'UNUSED'

                                            # calculate cost of move
                                            cont_cost = abs(key[0] - k[0]) + abs(key[1] - k[1])

                                            # create new node and add it to list of child nodes
                                            new_child = Node(new_ship, copy.deepcopy(self.buffer_state), list(self.unloads), self, self.g + cont_cost)
                                            child_nodes.append(new_child)
                                
                                # check for valid spot within buffer
                                spot_found = False
                                for c in range(BUFF_COLS - 1, -1, -1):
                                    for r in range(BUFF_ROWS):
                                        if self.buffer_state[(r + 1, c + 1)][1] == 'UNUSED':
                                            spot_found = True

                                            # move container to open space in buffer
                                            new_ship = copy.deepcopy(self.state)
                                            new_buff = copy.deepcopy(self.buffer_state)
                                            new_buff[(r + 1, c + 1)] = list(new_ship[key])

                                            # mark previous space as empty
                                            new_ship[key][0] = 0
                                            new_ship[key][1] = 'UNUSED'

                                            # calculate cost of move
                                            # ship -> unload_zone -> buff_unload 
                                            # -> buffer
                                            cont_cost = abs(unload_zone[0] - key[0]) + abs(unload_zone[1] - key[1]) + 4 + abs(buff_unload[0] - (r + 1)) + abs(buff_unload[1] - (c + 1))

                                            # create new node and add it to list of
                                            # children
                                            new_child = Node(new_ship, new_buff, list(self.unloads), self, self.g + cont_cost)
                                            child_nodes.append(new_child)
                                            break
                                    if spot_found:
                                        break

        # a balance operation also considers containers in the buffer that need to be moved back into the ship
        if self.sequence_type == 'balance':
            for col in range(BUFF_COLS - 1, -1 -1):
                empty_space = False
                for row in range(BUFF_ROWS -1, -1, -1):
                    # since buffer is loaded from the rightmost column
                    # once an empty slot is encountered, that is the final column
                    if buffer_grid[(row + 1, col + 1)][1] == 'UNUSED':
                        empty_space = True
                        continue

        return child_nodes