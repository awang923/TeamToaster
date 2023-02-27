import time # timing search function

from config import * # globals (ship, buffer)

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
# heavier side / lighter side
def mass_ratio(state):
    left = sum([ship[(i + 1, j + 1)][0] for i in range(ROWS) for j in range(COLS // 2)])
    right = sum([ship[(i + 1, j + 1)][0] for i in range(ROWS) for j in range(2, COLS)])

    masses = sorted([left, right])
    lighter, heavier = masses[0], masses[1]

    return heavier / lighter

# a star search algorithm
# root = starting node
# sequence type = 'transfer' or 'balance'
def a_star(root):
    initial_time = time.time();

    open_nodes = [] # nodes to be visted
    closed_nodes = [] # nodes that have already been visited

    open_nodes.append(root)

    while open_nodes:
        open_nodes.sort(key=lambda x: x.g + x.h) # sort in ascending order based on f score
        
        curr_node = open_nodes.pop(0) # look at node with lowest f score

        # for transfer sequence -- goal state: all desired containers are unloaded
        if curr_node.sequence_type == 'transfer' and not curr_node.unloads:  # or curr_node.h == 0
            print('time:', (time.time() - initial_time) * 1000)
            return curr_node

        # for balance sequence -- goal state: heavier side / lighter side = 1.1
        if curr_node.sequence_type == 'balance':
            cont_in_buffer = len([i for i in curr_node.buffer_state.values() if i[1] != 'UNUSED'])
            # check for an empty buffer
            if not cont_in_buffer and mass_ratio(curr_node.state) < 1.1:
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
# returns cost of moves
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