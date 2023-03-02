import copy
import time

# dimensions of ship bay
ROWS = 3
COLS = 4

# coordinates of unload zone on ship
unload_zone = (ROWS + 1, 1)

manifest_file = '../files/small_manifest.txt' # needs to be given at runtime

# contents of ship
# key = (x, y)
# value = [mass, description]
ship = {}

# ** RUN THIS BEFORE ALL OPERATIONS **
# takes in a manifest text file and populates a ship grid according to its contents
def parse_manifest(ship_grid, filename):
    with open(filename) as manifest:
        for line in manifest.readlines():
            entries = line.split(' ')

            # parse positional data
            pos = [int(i) for i in entries[0][:-1].strip('][').split(',')]
            pos = (pos[0], pos[1])

            # parse weight data
            wt = int(entries[1][:-1].strip('}{'))

            # parse name data
            name = entries[2].strip()

            # add to ship
            ship[pos] = [wt, name]

# containers to be unloaded -- (mass, description)
unload_list = [
    (5, 'Beer'),
    (3, 'Mat')
]

NUM_UNLOADS = len(unload_list)

# containers to be loaded -- (mass, description)
load_list = [
    (6969, 'Taco'),
    (70, 'Dog')
]

# dimensions of buffer
BUFF_ROWS = 4
BUFF_COLS = 24

# buffer
# key = coordinates (row, column)
# value = [mass, description]
buffer = {}

# populate buffer with empty spots
for r in range(BUFF_ROWS):
    for c in range(BUFF_COLS):
        buffer[(r + 1, c + 1)] = [0, 'UNUSED']

# coordinates of unload zone in buffer
buff_unload = (BUFF_ROWS + 1, BUFF_COLS)

# counts occupied spaces above a container
# cont_coords = (x, y)
def count_containers_above(state, cont_coords):
    i = cont_coords[1] + 1 # start at container directly above
    count = 0
    while i <= ROWS:
        cell_above = state[(i, cont_coords[0])]
        if cell_above[1] != 'UNUSED' and cell_above[1] != 'NAN':
            count += 1 # space is occupied by container
        else:
            break
        i += 1
    return count

# returns the ratio of the masses of the halves of a ship configuration
# lighter side / heavier side
def mass_ratio(state):
    left = sum([state[(i + 1, j + 1)][0] for i in range(ROWS) for j in range(COLS // 2)])
    right = sum([state[(i + 1, j + 1)][0] for i in range(ROWS) for j in range(2, COLS)])

    return min((left, right)) / max((left, right))

# Node class -- configuration of ship grid at current time
class Node:
    def __init__(self, state, buffer_state, unloads, sequence_type, parent=None, cost=0, move_str=None):
        self.state = state # container configuration in ship
        self.buffer_state = buffer_state # container configuration in buffer
        self.unloads = unloads # list of containers to be unloaded
        self.sequence_type = sequence_type # operation to perform ('transfer' or 'balance')
        self.parent = parent # pointer to parent node
        self.g = cost # cost from parent to current node
        self.h = 0 # cost to reach goal from current node
        self.move_str = move_str # string containing the move to get to node

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

        self.h = total_cost * (len(self.unloads) / NUM_UNLOADS)

        # self.h = total_cost

    # when balancing, goal is to maximize mass ratio / g score
    def balance_heuristic(self):
        self.h = mass_ratio(self.state) / self.g if self.g > 0 else 0

    def children(self):
        child_nodes = []

        # SHIP -> SHIP
        # look for container in ship
        for col in range(COLS):
            container_found = False
            for row in range(ROWS - 1, -1, -1):
                if self.state[(row + 1, col + 1)][1] == 'UNUSED':
                    continue # go to next row
                elif self.state[(row + 1, col + 1)][1] == 'NAN':
                    break # if NAN found, done with that column
                else:
                    # found an eligible container
                    container_found = True

                    # during a transfer sequence, containers that need to be unloaded will be removed from ship
                    if self.sequence_type == 'transfer' and (self.state[(row + 1, col + 1)][0], self.state[(row + 1, col + 1)][1]) in self.unloads:
                        # move container out of ship and update unload list
                        new_ship = copy.deepcopy(self.state)
                        new_buff = copy.deepcopy(self.buffer_state)

                        new_unloads = list(self.unloads)
                        new_unloads.remove((new_ship[(row + 1, col + 1)][0], new_ship[(row + 1, col + 1)][1]))

                        new_ship[(row + 1, col + 1)] = [0, 'UNUSED']

                        # calculate cost of move
                        cont_cost = abs(unload_zone[0] - (row + 1)) + abs(unload_zone[1] - (col + 1)) + 2

                        # create output string
                        x = str(row + 1) if len(str(row + 1)) > 1 else '0' + str(row + 1)
                        y = str(col + 1) if len(str(col + 1)) > 1 else '0' + str(col + 1)
                        coord = '[' + x + ',' + y + ']'

                        output_str = 'Unload ' + coord + ' ' + self.state[(row + 1, col + 1)][1]

                        # create new child node and add to list of children
                        new_child = Node(new_ship, new_buff, new_unloads, self.sequence_type, self, self.g + cont_cost, output_str)
                        child_nodes.append(new_child)

                        break

                    # look for available space on ship to move container
                    for c in range(COLS):
                        spot_found = False
                        for r in range(ROWS - 1, -1, -1):
                            if c == col:
                                break # no moves to same column
                            if self.state[(r + 1, c + 1)][1] != 'UNUSED' or self.state[(r + 1, c + 1)][1] == 'NAN':
                                break # something in space, done with column

                            # found place in ship to put container
                            spot_found = True

                            # check if something is below available space or it's on the bottom row
                            if (r and self.state[(r, c + 1)][1] != 'UNUSED') or not r:
                                # move container to different space
                                new_ship = copy.deepcopy(self.state)
                                new_buff = copy.deepcopy(self.buffer_state)
                                new_ship[(r + 1, c + 1)] = list(new_ship[(row + 1, col + 1)])

                                # mark old space as empty
                                new_ship[(row + 1, col + 1)] = [0, 'UNUSED']

                                # calculate cost of move
                                cont_cost = abs(row - r) + abs(col - c)

                                # create output string
                                x1 = str(row + 1) if len(str(row + 1)) > 1 else '0' + str(row + 1)
                                y1 = str(col + 1) if len(str(col + 1)) > 1 else '0' + str(col + 1)
                                coord1 = '[' + x1 + ',' + y1 + ']'
                                x2 = str(r + 1) if len(str(r + 1)) > 1 else '0' + str(r + 1)
                                y2 = str(c + 1) if len(str(c + 1)) > 1 else '0' + str(c + 1)
                                coord2 = '[' + x2 + ',' + y2 + ']'

                                output_str = 'Move ' + coord1 + ' ' + self.state[(row + 1, col + 1)][1] + ' to ' + coord2

                                # create new node and add to list of child nodes
                                new_child = Node(new_ship, new_buff, list(self.unloads), self.sequence_type, self, self.g + cont_cost, output_str)
                                child_nodes.append(new_child)

                                break

                # found the topmost container in ship column
                if container_found:
                    break

        # SHIP -> BUFFER
        # look for container in ship
        for col in range(COLS):
            container_found = False
            for row in range(ROWS - 1, -1, -1):
                if self.state[(row + 1, col + 1)][1] == 'UNUSED':
                    continue # go to next row
                elif self.state[(row + 1, col + 1)][1] == 'NAN':
                    break # if NAN found, done with that column
                else:
                    # found an eligible container
                    container_found = True

                    # during a transfer sequence, containers that need to be unloaded will be removed from ship
                    if self.sequence_type == 'transfer' and (self.state[(row + 1, col + 1)][0], self.state[(row + 1, col + 1)][1]) in self.unloads:
                        # done in SHIP -> SHIP operation
                        break
                    
                    # look for available space in buffer to move container
                    for c in range(BUFF_COLS - 1, -1, -1):
                        if self.buffer_state[(BUFF_ROWS, c + 1)][1] != 'UNUSED':
                            continue # column is completely full, go to next one
                        spot_found = False

                        for r in range(BUFF_ROWS):
                            if self.buffer_state[(r + 1, c + 1)][1] != 'UNUSED':
                                continue # space is occupied, go up a row
                            
                            # found available space
                            spot_found = True

                            # move container to buffer
                            new_ship = copy.deepcopy(self.state)
                            new_buff = copy.deepcopy(self.buffer_state)
                            new_buff[(r + 1, c + 1)] = list(new_ship[(row + 1, col + 1)])

                            # mark space in ship as empty
                            new_ship[(row + 1, col + 1)] = [0, 'UNUSED']

                            # calculate cost of move
                            cont_cost = abs(unload_zone[0] - (row + 1)) + abs(unload_zone[1] - (col + 1)) + 4 + abs(buff_unload[0] - (r + 1)) + abs(buff_unload[1] - (c + 1))

                            # create output string
                            x1 = str(row + 1) if len(str(row + 1)) > 1 else '0' + str(row + 1)
                            y1 = str(col + 1) if len(str(col + 1)) > 1 else '0' + str(col + 1)
                            coord1 = '[' + x1 + ',' + y1 + ']'
                            x2 = str(r + 1) if len(str(r + 1)) > 1 else '0' + str(r + 1)
                            y2 = str(c + 1) if len(str(c + 1)) > 1 else '0' + str(c + 1)
                            coord2 = '[' + x2 + ',' + y2 + ']'

                            output_str = 'Move ' + coord1 + ' ' + self.state[(row + 1, col + 1)][1] + ' to BUFFER ' + coord2

                            # create new node and add to list of child nodes
                            new_child = Node(new_ship, new_buff, list(self.unloads), self.sequence_type, self, self.g + cont_cost, output_str)
                            child_nodes.append(new_child)

                            break

                        # found closest space in buffer
                        if spot_found:
                            break

                    # found the topmost container in ship column
                    if container_found:
                        break

        # a balance sequence will check for moves from buffer to ship
        if self.sequence_type == 'balance':
            # BUFFER -> SHIP
            for col in range(BUFF_COLS - 1, -1, -1):
                empty_space = False
                container_found = False
                for row in range(BUFF_ROWS - 1, -1, -1):
                    # since buffer is loaded from the rightmost column
                    # once an empty slot is encountered, that is the final column
                    if self.buffer_state[(row + 1, col + 1)][1] == 'UNUSED':
                        empty_space = True
                        continue

                    # eligible container found
                    container_found = True

                    # look for places in ship to put buffer container
                    for c in range(COLS):
                        for r in range(ROWS - 1, -1, -1):
                            if self.state[(r + 1, c + 1)][1] != 'UNUSED' or self.state[(r + 1, c + 1)][1] == 'NAN':
                                break # something in space, done with column

                            # found place in ship to put container
                            
                            # check if something is below available space or it's on the bottom row
                            if (r and self.state[(r, c + 1)][1] != 'UNUSED') or not r:
                                # put container in ship
                                new_ship = copy.deepcopy(self.state)
                                new_buff = copy.deepcopy(self.buffer_state)
                                new_ship[(r + 1, c + 1)] = list(new_buff[(row + 1, col + 1)])
                                new_buff[(row + 1, col + 1)] = [0, 'UNUSED']

                                # calculate cost of move
                                cont_cost = abs(buff_unload[0] - (row + 1)) + abs(buff_unload[1] - (col + 1)) + 4 + abs(unload_zone[0] - (r + 1)) + abs(unload_zone[1] - (c + 1))

                                # create output string
                                x1 = str(row + 1) if len(str(row + 1)) > 1 else '0' + str(row + 1)
                                y1 = str(col + 1) if len(str(col + 1)) > 1 else '0' + str(col + 1)
                                coord1 = '[' + x1 + ',' + y1 + ']'
                                x2 = str(r + 1) if len(str(r + 1)) > 1 else '0' + str(r + 1)
                                y2 = str(c + 1) if len(str(c + 1)) > 1 else '0' + str(c + 1)
                                coord2 = '[' + x2 + ',' + y2 + ']'

                                output_str = 'Move BUFFER ' + coord1 + ' ' + self.buffer_state[(row + 1, col + 1)][1] + ' to ' + coord2

                                # create new node and add to list of children
                                new_child = Node(new_ship, new_buff, list(self.unloads), self.sequence_type, self, self.g + cont_cost, output_str)
                                child_nodes.append(new_child)

                                break

                    # found the topmost container in the column of buffer
                    if container_found:
                        break

                # last column in buffer
                if empty_space:
                    break
        
        return child_nodes

# search algorithm
# root = starting node
def search(root):
    initial_time = time.time();

    open_nodes = [] # nodes to be visted
    closed_nodes = [] # nodes that have already been visited

    open_nodes.append(root)

    while open_nodes:
        if root.sequence_type == 'transfer':
            # sort in ascending order based on f score
            open_nodes.sort(key=lambda x: x.h)
        else:
            # sort in descending order based on mass ratio / g score
            open_nodes.sort(key=lambda x: x.h, reverse=True)
        
        curr_node = open_nodes.pop(0) # look at node with lowest f score

        # for transfer sequence -- goal state: all desired containers are unloaded
        if curr_node.sequence_type == 'transfer' and not curr_node.unloads:
            print('time:', (time.time() - initial_time) * 1000)
            return curr_node

        # for balance sequence -- goal state: lighter side / heavier side > 0.9
        # and buffer is emptys
        if curr_node.sequence_type == 'balance':
            cont_in_buffer = len([i for i in curr_node.buffer_state.values() if i[1] != 'UNUSED'])
            # check for an empty buffer
            if not cont_in_buffer and mass_ratio(curr_node.state) > 0.9:
                print('time:', (time.time() - initial_time) * 1000)

                # if balancing is not possible, a SIFT operation is done to the containers
                # if not curr_node:
                #    SIFT(root)

                return curr_node

        for child in curr_node.children():
            opened_node = next((i for i in open_nodes if i.state == child.state), None)
            closed_node = next((i for i in closed_nodes if i.state == child.state), None)

            if not closed_node:
                if not opened_node:
                    open_nodes.append(child)
                else:
                    # if node with same state as child node is already in list of nodes to visit
                    # but has a higher cost, replace with child node
                    if child.g + child.h < opened_node.g + opened_node.h:
                        open_nodes.remove(opened_node)
                        open_nodes.append(child)
            else:
                # if node with same state as child node is in the list of visited nodes,
                # but has a higher cost, reopen with child node to explore again
                if child.g + child.h < closed_node.g + closed_node.h:
                    closed_nodes.remove(closed_node)
                    open_nodes.append(child)
        
        closed_nodes.append(curr_node) # close current node

# ** RUN AFTER UNLOADING SHIP **
# moves containers from buffer and back onto ship
# returns cost of moves
def unload_buffer(ship_grid, buffer_grid):
    buffer_cost = 0 # total cost of moves from buffer to ship
    available_spots = [] # potential spaces to load into

    for c in range(COLS):
        for r in range(ROWS):
            # found an empty spot in the ship
            if ship_grid[(r + 1, c + 1)][1] == 'UNUSED':
                # either the space is above ground level and there's
                # something underneath it
                # or the space is on ground level
                if (r and ship_grid[(r, c + 1)][1] != 'UNUSED') or not r:
                    # calculate cost of move
                    cont_cost = 4 + abs(unload_zone[0] - (r + 1)) + abs(unload_zone[1] - (c + 1))

                    available_spots.append((cont_cost, (r + 1, c + 1)))
    
    available_spots.sort() # sort available spaces by lowest time cost

    for c in range(BUFF_COLS - 1, -1, -1):
        empty_space = False
        for r in range(BUFF_ROWS - 1, -1 , -1):
            # since buffer is loaded from the rightmost column
            # once an empty slot is encountered, that is the final column
            if buffer_grid[(r + 1, c + 1)][1] == 'UNUSED':
                empty_space = True
                continue

            # load container in the closest spot in ship
            closest_spot = available_spots.pop(0)
            ship_grid[closest_spot[1]] = buffer_grid[(r + 1, c + 1)]
            buffer_grid[(r + 1, c + 1)] = [0, 'UNUSED']
            
            cont_cost = closest_spot[0] + abs(buff_unload[0] - (r + 1)) + abs(buff_unload[1] - (c + 1))

            buffer_cost += cont_cost

        # column contained an empty space, so that is the last column
        if empty_space:
            break

    return buffer_cost

# ** RUN AFTER UNLOADING SHIP **
# moves containers from trucks onto ship
# returns cost of moves
def load_ship(ship_grid, loads):
    load_cost = 0 # total cost of moves from truck to ship
    available_spots = [] # potential spaces to load into

    for c in range(COLS):
        for r in range(ROWS):
            # found an empty spot in the ship
            if ship_grid[(r + 1, c + 1)][1] == 'UNUSED':
                # either the space is above ground level and there's
                # something underneath it
                # or the space is on ground level
                if (r and ship_grid[(r, c + 1)][1] != 'UNUSED') or not r:
                    # calculate cost of move
                    cont_cost = 2 + abs(unload_zone[0] - (r + 1)) + abs(unload_zone[1] - (c + 1))

                    available_spots.append((cont_cost, (r + 1, c + 1)))
    
    available_spots.sort() # sort available spaces by lowest time cost

    # loads containers starting at space with lowest cost
    for cont in loads:
        closest_spot = available_spots.pop(0)
        ship_grid[closest_spot[1]] = [cont[0], cont[1]]
        load_cost += closest_spot[0]

    return load_cost

# ** RUN AFTER COMPLETING ALL OPERATIONS **
# creates the outbound manifest containing configuration of containers on ship
def update_manifest(ship_grid, filename):
    # isolate filename and append 'OUTBOUND' to it
    name = [i for i in filename.split('/') if '.txt' in i][0][:-4]

    line_counter = 1

    with open(name + 'OUTBOUND.txt', 'w') as outbound:
        for key, value in ship_grid.items():
            # format positional data
            x = str(key[0]) if len(str(key[0])) > 1 else '0' + str(key[0])
            y = str(key[1]) if len(str(key[1])) > 1 else '0' + str(key[1])
            coord = '[' + x + ',' + y + ']'

            # format weight data
            weight = str(value[0])
            while len(weight) < 5:
                weight = '0' + weight
            weight = '{' + weight + '}'

            # name data
            name = value[1]

            # no newline at end of file
            if line_counter == ROWS * COLS:
                outbound.write(coord + ', ' + weight + ', ' + name)
            else:
                outbound.write(coord + ', ' + weight + ', ' + name + '\n')

            line_counter += 1
    
# ** RUN AFTER COMPLETING ALL OPERATIONS **
# creates a list of the sequence of moves taken to reach the goal state
def order_of_operations(node):
    ops = []
    while node.parent:
        ops.append(node.move_str)
        node = node.parent

    return ops[::-1]

# MAIN 

# populate ship grid
parse_manifest(ship, manifest_file)

root = Node(ship, buffer, unload_list, 'transfer')
goal = search(root)
for i in order_of_operations(goal):
    print(i)