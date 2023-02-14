
manifest_file = '../files/small_manifest.txt' # needs to be given at runtime

ship = [] # holds tuples of container data

with open(manifest_file) as manifest:
    for line in manifest.readlines():
        entries = line.split(' ')

        # parse positional data
        pos = [int(i) for i in entries[0][:-1].strip('][').split(',')]

        # parse weight data
        wt = entries[1][:-1].strip('}{')

        # parse name data
        name = entries[2].strip()

        # add to ship
        ship.append((pos, wt, name))

print(ship)
