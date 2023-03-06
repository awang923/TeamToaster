from nodes import *
import queue
import heapq

# [container_name, [x,y]]
        #  j=0  j=1  j=2
puzzle = [[' ', ' ', ' '], #i=0
          [' ', ' ', 'c'], #i=1
          ['d', 'e', 'f'], #i=2
          ['g', 'h', 'i']] #i=3



init = [[' ', [1,3]], ['b', [2,3]], ['c', [3,3]], 
        ['d', [1,2]], ['e', [2,2]], ['f', [3,2]], 
        ['g', [1,1]], ['h', [2,1]], ['i', [3,1]]
       ]
to_unload = [['f', [2,3]], 
             ['h', [2,1]]
            ]
goal = [['f', [1,4]],
        ['h', [1,4]]
        ]
# goal = [['', [0,0]], 
#         ['b', [0,0]], 
#         ['c', [0,0]], 
#         ['d', [0,0]], 
#         ['e', [0,0]], 
#         ['f', [1,4]], 
#         ['g', [0,0]], 
#         ['h', [1,4]], 
#         ['i', [0,0]]
#        ]

def pprint(grid):
    for row in grid:
        print(row)


def print_solution(node):
    gn = node.gn
    hn = node.hn
    if node.parent == None:
        print(
            f'The best state to expand with g(n) = {gn} and h(n) = {hn} is ...')
        pprint(node.state)
        return
    print_solution(node.parent)
    print(f'The best state to expand with g(n) = {gn}, and h(n) = {hn} is ...')
    pprint(node.state)


def bfs(start):
    explored = []
    count = 0
    max_queue = 0
    i = 0
    root = Puzzle_Node(start, None, 0)
    q = queue.PriorityQueue()
    q.put((root.fn, i, root))
    while not q.empty():
        temp = q.get()
        temp_state = temp[2]

        # if temp_state.state == goal_puzzle:
        to_unload[0] = temp_state.state[5]
        to_unload[1] = temp_state.state[7]
        if to_unload == goal:
            print_solution(temp_state)
            print('GOAL!!!')
            print(
                f'To solve this problem the search algorithm expanded a total of {count} nodes.')
            print(
                f'The maximum number of nodes in the queue at any one time: {max_queue}')
            return


        explored.append(temp_state.state)
        children = temp_state.expand()
        count += 1
        for c in children:
            if c.state not in explored:
                c.manhattan(goal)
        children = list(q.queue)
        if(len(children) > max_queue):
            max_queue = len(children)



def manhattan_A(start):
    return bfs(start)

manhattan_A(init)






