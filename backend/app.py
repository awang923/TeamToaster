
# dimensions of ship bay
ROWS = 3
COLS = 3

# coordinates of unload zone
unload_zone = (1, ROWS + 1)

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
        wt = entries[1][:-1].strip('}{')

        # parse name data
        name = entries[2].strip()

        # add to ship
        ship[pos] = [wt, name]

# containers to be unloaded -- (mass, description)
unload_list = [
    (3450, 'Beer'),
    (2007, 'Balls')
]

# counts occupied spaces above a container
# cont_coords = (x, y)
def count_containers_above(cont_coords):
    i = cont_coords[1] + 1 # start at container directly above
    count = 0
    while i <= ROWS:
        cell_above = ship[(cont_coords[0], i)]
        if cell_above[1] != 'UNUSED' and cell_above[1] != 'NAN':
            count += 1 # space is occupied by container
        else:
            break
        i += 1
    return count

# Node class -- configuration of ship grid at current time
class Node:
    def __init__(self, state, parent, cost):
        self.parent = parent # pointer to parent node
        self.state = state # container configuration
        self.g = cost # cost from parent to current node
        self.h = 0 # cost to reach goal from current node

        self.heuristic() # updates node with cost to goal state

    # calculates the total time it would take to reach goal state from current
    # state
    # in this case, goal state = all desired containers removed from ship
    def heuristic(self):
        total_cost = 0
        for cont in unload_list:
            possible_conts = []

            # finds all containers with desired descriptions (ie. all
            # containers with "Cat" in them)
            for key, value in ship.items():
                if value[1] == cont[1]:
                    possible_conts.append(key)
        
            # finds least burdened container
            chosen_cont = min([(count_containers_above(i), i) for i in possible_conts])[1]
            
            # calculates time to fully unload from ship and onto truck
            # manhattan distance + 2 (time to load onto truck)
            cont_cost = abs(unload_zone[0] - chosen_cont[0]) + abs(unload_zone[1] - chosen_cont[1]) + 2

            total_cost += cont_cost

        self.h = total_cost
            

node = Node(ship, None, 0)
print(node.h)



                


