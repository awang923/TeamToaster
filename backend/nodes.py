import copy
from math import dist

# operators of the blocks in the puzzle

# puzzle = [[0, 0, 0],
#           [0, 0, 0],
#           [0, 0, 0]]

def move_up(state):
    new_state = copy.deepcopy(state)
    for i in range(1,4):
        for j in range(3):
            if state[0][j] == ' ':
                return None
            else:
                if state[i][j] == ' ':
                    new_state[i][j] = state[i-1][j]
                    new_state[i-1][j] = ' '
                    return new_state


def move_left(state):
    new_state = copy.deepcopy(state)
    for i in range(1,4):
        for j in range(3):
            if j == 0 and state[i][j] != ' ':
                return None
            else:
                if state[i][j] == ' ':
                    new_state[i][j] = state[i][j+1]
                    new_state[i][j+1] = ' '
                    return new_state

def move_right(state):
    new_state = copy.deepcopy(state)
    for i in range(1,4):
        for j in range(3):
            if j == 2 and state[i][j] != ' ':
                return None
            else:
                if state[i][j] == ' ':
                    new_state[i][j] = state[i][j-1]
                    new_state[i][j-1] = ' '
                    return new_state


def goal_index(goal, val):
    for x, y in enumerate(goal):
        if val in y:
            return x, y.index(val)


class Puzzle_Node:
    def __init__(self, state, parent, gn):
        self.state = state
        self.parent = parent
        # self.action = action
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.hn = 0  # estimated cost from node n to the goal
        self.gn = gn  # cost to get to the node
        self.fn = self.gn + self.hn

    def expand(self):
        frontier = []
        temp = self.state

        up_state = move_up(temp)
        if(up_state != None):
            up_child = Puzzle_Node(up_state, self, self.gn + 1)
            self.up = up_child
            frontier.append(up_child)
        # down_state = move_down(temp)
        # if(down_state != None):
        #     down_child = Puzzle_Node(down_state, self, self.gn + 1)
        #     self.down = down_child
        #     frontier.append(down_child)
        left_state = move_left(temp)
        if(left_state != None):
            left_child = Puzzle_Node(left_state, self, self.gn + 1)
            self.left = left_child
            frontier.append(left_child)
        right_state = move_right(temp)
        if(right_state != None):
            right_child = Puzzle_Node(right_state, self, self.gn + 1)
            self.right = right_child
            frontier.append(right_child)
        return frontier


    def euclidean(self, goal):
        sum = 0
        for i in range(3):
            for j in range(3):
                if(goal[i][j] != self.state[i][j] and self.state[i][j] != 0):
                    i_goal, j_goal = goal_index(goal, self.state[i][j])
                    sum += pow(pow((i - i_goal), 2) + pow(j - j_goal, 2), 0.5)
        self.hn = sum
        self.fn = sum + self.gn









# def move_down(state):
#     new_state = copy.deepcopy(state)
#     for i in range(3):
#         for j in range(3):
#             if state[3][j] == ' ':
#                 return None
#             else:
#                 if state[i][j] == 0:
#                     new_state[i][j] = state[i+1][j]
#                     new_state[i+1][j] = 0
#                     return new_state