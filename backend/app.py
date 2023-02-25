import copy
import time

# dimensions of ship bay
ROWS = 3
COLS = 3

# coordinates of unload zone on ship
unload_zone = (ROWS + 1, 1)

manifest_file = '../files/small_manifest.txt' # needs to be given at runtime

# contents of ship
# key = (x, y)
# value = [mass, description]
ship = {}

with open(manifest_file) as manifest:
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
    (3450, 'Beer'),
    (2007, 'Balls')
]

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

# Node class -- configuration of ship grid at current time
class Node:
    def __init__(self, state, buffer_state, unloads, parent=None, cost=0):
        self.state = state # container configuration in ship
        self.buffer_state = buffer_state # container configuration in buffer
        self.unloads = unloads # list of containers to be unloaded
        self.parent = parent # pointer to parent node
        self.g = cost # cost from parent to current node
        self.h = 0 # cost to reach goal from current node

        self.heuristic() # updates node with cost to goal state

    # calculates the total time it would take to reach goal state from current
    # state
    # in this case, goal state = all desired containers removed from ship
    def heuristic(self):
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

                    # not top row
                    else:
                        # nothing on top of container
                        if self.state[(key[0] + 1, key[1])][1] == 'UNUSED':
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

        return child_nodes

def a_star(root):
    initial_time = time.time();

    open_nodes = [] # nodes to be visted
    closed_nodes = [] # nodes that have already been visited

    open_nodes.append(root)

    while open_nodes:
        open_nodes.sort(key=lambda x: x.g + x.h) # sort in ascending order based on f score
        
        curr_node = open_nodes.pop(0) # look at node with lowest f score

        if not curr_node.unloads:  # or curr_node.h == 0
            print('time:', (time.time() - initial_time) * 1000)
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

# moves containers from buffer and back onto ship
# returns cost of moves
def unload_buffer(ship_grid, buffer_grid):
    buffer_cost = 0 # total cost of moves from buffer to ship
    ship_space = (ROWS, 1) # first space on ship to begin loading into

    for col in range(BUFF_COLS - 1, -1, -1):
        empty_space = False
        for row in range(BUFF_ROWS - 1, -1 , -1):
            # since buffer is loaded from the rightmost column
            # once an empty slot is encountered, that is the final column
            if buffer_grid[(row + 1, col + 1)][1] == 'UNUSED':
                empty_space = True
                continue

            container_on = False

            # put container back into closest space on ship
            for c in range(ship_space[1] - 1, COLS):
                for r in range(ship_space[0] - 1, -1, -1):
                    # found an empty spot in the ship
                    if ship_grid[(r + 1, c + 1)][1] == 'UNUSED':
                        # either the space is above ground level and there's
                        # something underneath it
                        # or the space is on ground level
                        if (r and ship_grid[(r, c + 1)][1] != 'UNUSED') or not r:
                            # put container onto ship
                            ship_grid[(r + 1, c + 1)] = list(buffer_grid[(row + 1, col + 1)])

                            # mark space in buffer as empty
                            buffer_grid[(row + 1, col + 1)] = [0, 'UNUSED']

                            # calculate cost of move
                            cont_cost = abs(buff_unload[0] - (row + 1)) + abs(buff_unload[1] - (col + 1)) + 4 + abs(unload_zone[0] - (r + 1)) + abs(unload_zone[1] - (c + 1))

                            buffer_cost += cont_cost

                            # mark starting space on ship for next iteration
                            start_row = r + 2 if r + 2 <= ROWS else ROWS
                            ship_space = (start_row, c + 1)

                            container_on = True # successfully loaded container from buffer
                            break

                if container_on:
                    break

        # column contained an empty space, so that is last column to be 
        # unloaded
        if empty_space:
            break

    return buffer_cost

# moves containers from trucks onto ship
def load_ship(ship_grid, loads):
    load_cost = 0 # total cost to move containers from trucks and onto ship

    if loads:
        for c in range(COLS):
            for r in range(ROWS):
                # found an empty spot in the ship
                if ship_grid[(r + 1, c + 1)][1] == 'UNUSED':
                    # either the space is above ground level and there's
                    # something underneath it
                    # or the space is on ground level
                    if (r and ship_grid[(r, c + 1)][1] != 'UNUSED') or not r:
                        ship_grid[(r + 1, c + 1)] = list(loads.pop(0)) # load container

                        cont_cost = 2 + abs(unload_zone[0] - (r + 1)) + abs(unload_zone[1] - (c + 1))

                        load_cost += cont_cost

                # no more containers to load
                if not loads:
                    break

            if not loads:
                break

    return load_cost



# ** MAIN **

node = Node(ship, buffer, unload_list)

goal_node = a_star(node)

i = 1
curr = goal_node
print('goal:', curr.state)
while curr.parent:
    curr = curr.parent
    print(i, curr.state, curr.g)
    i += 1