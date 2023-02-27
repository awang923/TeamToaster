# dimensions of ship bay
ROWS = 4
COLS = 4

# coordinates of unload zone on ship
unload_zone = (ROWS + 1, 1)

manifest_file = '../files/balance_manifest.txt' # needs to be given at runtime

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