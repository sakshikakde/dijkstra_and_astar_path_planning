# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import timeit
import argparse
import cv2
import matplotlib.pyplot as plt
import math
import queue
from Obstacle import *
from Utils.MathUtils import *
from Utils.Node import *
from Utils.Viz import *


# %%
def find_moves(current_node):
    i, j = current_node.getState()
    moves = ['N','NE', 'E', 'SE', 'S', 'SW','W', 'NW']
    final_moves = ['N','NE', 'E', 'SE', 'S', 'SW','W', 'NW']
    move_i = [i, i+1, i+1, i+1, i, i-1, i-1, i-1]
    move_j = [j+1, j+1, j, j-1, j-1, j-1, j, j+1]
    for move in range(len(moves)):
        if (isInObstacleSpace(move_i[move], move_j[move]) or current_node.getParentState() == [move_i[move], move_j[move]]):
            final_moves.remove(moves[move])
    # print(final_moves)
    return final_moves


# %%
def isInObstacleSpace(i,j):
    total_clearance = 15
    if (i > 399 or i < 0 or j < 0 or j > 299):
        # print('Tending out of boundary ; avoid')
        return 1

    #condition for cicle
    circle = (i - circle_offset_x)**2 + (j - circle_offset_y)**2
    if circle <= (circle_radius) ** 2:
        # print('Tending towards circle ; avoid')
        return 1

    #condition for ellipse
    ellipse_r_x = ellipse_radius_x
    ellipse_r_y = ellipse_radius_y
    ellipse = ((i - ellipse_offset_x)**2)/(ellipse_r_x*ellipse_r_x) + ((j- ellipse_offset_y)**2)/(ellipse_r_y*ellipse_r_y)
    if ellipse <= 1.0:
        # print('Tending towards ellipse ; avoid')
        return 1

    #condition for rectangle
    d1 = abs((j - 0.7002*i - 74.39) / (1 + (0.7002)**2)**(0.5))
    d2 = abs((j - 0.7002*i - 98.8) / (1 + (0.7002)**2)**(0.5))
    d3 = abs((j + 1.428*i - 176.55) / (1 + (1.428)**2)**(0.5))
    d4 = abs((j + 1.428*i - 439.44) / (1 + (1.428)**2)**(0.5))
    if (d1+d2 <= rect_width and d3+d4 <= rect_length):
        # print('Tending towards rectangle ; avoid')
        return 1

    if ((i - (200 - total_clearance) >= 0 and (230 + total_clearance)-i >=0 and (j >= (230 - total_clearance) and j <= (280 + total_clearance))) and
    ((j- (230 - total_clearance) >= 0 or (280 + total_clearance)-j <=0) and (i >= (200 - total_clearance) and i <= (230 + total_clearance))) and
    not (i-(210 + total_clearance) >=0 and i-230<=0 and j>=(240 + total_clearance) and j<= (270 - total_clearance))):
    # print('Tending towards C shaped object; avoid')
        return 1
    
    return 0


# %%
def main():

    Parser = argparse.ArgumentParser()
    Parser.add_argument("--InitState", nargs='+', type=int, default= [0, 0], help = 'init state')
    Parser.add_argument("--GoalState", nargs='+', type=int, default= [100, 200], help = 'goal state')
    Parser.add_argument('--SaveFolderName', default='./', help='Default path to store the video')
    Args = Parser.parse_args()

    start_point = Args.InitState
    goal_point = Args.GoalState
    save_folder_name = Args.SaveFolderName

    if (not save_folder_name[-1] == '/'):
        save_folder_name = save_folder_name + '/'
    SaveFileName = save_folder_name + "Dijkstra_path.avi"

    if (isInObstacleSpace(start_point[0], start_point[1])):
        print('Initial state is in obstacle space, please provide new valid state')
        exit()

    if (isInObstacleSpace(goal_point[0], goal_point[1])):
        print('Goal state is in obstacle space, please provide new valid state')
        exit()

    nodes = queue.PriorityQueue()
    init_node = Node(start_point, None, None, 0)
    nodes.put((init_node.getCost(), init_node))
    root2 = np.sqrt(2)

    goal_reached = False

    moves_cost = {'N':1, 'NE':root2, 'E':1, 'SE':root2, 'S':1, 'SW':root2, 'W':1, 'NW':root2}
    node_array = np.array([[Node([i,j], None, None, math.inf) for j in range(300)] for i in range(400)])

    space_size = [300, 400]
    sizey, sizex = space_size
    result = cv2.VideoWriter(SaveFileName,  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         300, (sizex, sizey))

    space_map = np.zeros([space_size[0], space_size[1], 3], dtype=np.uint8)
    space_map = updateMapViz(space_map, start_point, [0,0,255])
    space_map = updateMapViz(space_map, goal_point, [0,0,255])
    space_map = addObstacles2Map(space_map)

    full_path = None
    print("Searching................")
    while (not nodes.empty()):

        current_node = nodes.get()[1]
        i, j = current_node.getState()

        space_map = updateMapViz(space_map, current_node.getState(), [0, 255, 0])
        # cv2.imshow('frame',space_map)
        result.write(space_map)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        #define moves list
        moves_i = {'N':i, 'NE':i+1, 'E':i+1, 'SE':i+1, 'S':i, 'SW':i-1, 'W':i-1, 'NW':i-1}
        moves_j = {'N':j+1, 'NE':j+1, 'E':j, 'SE':j-1, 'S':j-1, 'SW':j-1, 'W':j, 'NW':j+1}

        if (current_node.getState() == goal_point):
            print('Goal reached')
            print("The cost of path: ", current_node.getCost())
            full_path, node_path = current_node.getFullPath()
            goal_reached = True

            for node in node_path:
                pos = node.getState()
                space_map = updateMapViz(space_map, pos, [0, 0, 255])
                # cv2.imshow('frame',space_map)
                result.write(space_map)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
            # keep final frame for 3s
            for i in range(900):
                result.write(space_map)

            # cv2.waitKey() 
            # cv2.destroyAllWindows()
            break
        else:
            # find the moves from the current position
            moves = find_moves(current_node)
            parent_cost = current_node.getCost()
            # iterate through each move and find corresponding child
            for move in moves:
                child_state = [moves_i.get(move), moves_j.get(move)]
                new_cost = parent_cost + moves_cost.get(move)
                # if not visited
                if (node_array[child_state[0], child_state[1]].getCost() == math.inf):
                    child_node = Node(child_state, current_node, move, new_cost)
                    node_array[child_state[0], child_state[1]] = child_node
                    nodes.put((child_node.getCost(), child_node))
                else :
                    if (new_cost < node_array[child_state[0], child_state[1]].getCost()):
                        child_node = Node(child_state, current_node, move, new_cost)
                        node_array[child_state[0], child_state[1]] = child_node
                        nodes.put((child_node.getCost(), child_node))
        
        if (goal_reached): break
       


# %%
if __name__ == "__main__":
    main()


# %%



