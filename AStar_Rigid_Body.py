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
def getBranches(node, step_size, goal_state):
    moves = ["1", "2", "3", "4", "5"]
    state = node.getState()
    branches = []
    branches.append(Node(move30Clock(state, step_size), node, moves[0], node.getCost() + step_size))
    branches.append(Node(move30AntiClock(state, step_size), node, moves[1], node.getCost() + step_size))
    branches.append(Node(move60Clock(state, step_size), node, moves[2], node.getCost() + step_size))
    branches.append(Node(move60AntiClock(state, step_size), node, moves[3], node.getCost() + step_size))
    branches.append(Node(moveStraight(state, step_size), node, moves[4], node.getCost() + step_size))

    #remove None nodes
    b = [branch for branch in branches if branch.getState() is not None]
            
    return b

def move30Clock(state, step_size): #assuming we cat land on the borders
  
    current_theta = state[2]
    new_theta = current_theta - 30
    if new_theta <= -360 :
        new_theta = new_theta + 360

    step_x = step_size * np.cos(np.radians(new_theta))
    step_y = step_size * np.sin(np.radians(new_theta))
    
    new_state = [state[0] + step_x, state[1] + step_y, new_theta]

    if isInObstacleSpace(state, new_state):
        return None
 
    return new_state

def move30AntiClock(state, step_size):

    current_theta = state[2]
    new_theta = current_theta + 30
    if new_theta >= 360:
        new_theta = new_theta - 360

    step_x = step_size * np.cos(np.radians(new_theta))
    step_y = step_size * np.sin(np.radians(new_theta))
    
    new_state = [state[0] + step_x, state[1] + step_y, new_theta]

    if isInObstacleSpace(state, new_state):
        return None
 
    return new_state

def move60Clock(state, step_size):

    current_theta = state[2]
    new_theta = current_theta - 60
    if new_theta <= -360:
        new_theta = new_theta + 360
    
    step_x = step_size * np.cos(np.radians(new_theta))
    step_y = step_size * np.sin(np.radians(new_theta))
    
    new_state = [state[0] + step_x, state[1] + step_y, new_theta]
    if isInObstacleSpace(state, new_state):
        return None
 
    return new_state

def move60AntiClock(state, step_size):

    current_theta = state[2]
    new_theta = current_theta + 60
    if new_theta >= 360:
        new_theta = new_theta - 360

    step_x = step_size * np.cos(np.radians(new_theta))
    step_y = step_size * np.sin(np.radians(new_theta))
    
    new_state = [state[0] + step_x, state[1] + step_y, new_theta]

    if isInObstacleSpace(state, new_state):
        return None
 
    return new_state

def moveStraight(state, step_size):

    current_theta = state[2]
    new_theta = current_theta + 0

    step_x = step_size * np.cos(np.radians(new_theta))
    step_y = step_size * np.sin(np.radians(new_theta))
    
    new_state = [state[0] + step_x, state[1] + step_y, new_theta]

    if isInObstacleSpace(state, new_state):
        return None
 
    return new_state


# %%
def isInObstacleSpace(parent_state, current_state):

    x1, y1 = parent_state[:2]
    x2, y2 = current_state[:2]
    #move line
    move = getLineParam([x1, y1], [x2, y2])

    if (x2 > 399 or x2 < 0 or y2 < 0 or y2 > 299):
        return True

    if rectIntersect(move) or cIntersect(move) or circleIntersect(move) or ellipseIntersect(move):
        return True
    else:
        return False  


# %%
def checkGoalReached(current_node, goal_state, thresh_radius):
    current_state = current_node.getState()
    radius_sq = np.square(current_state[0] - goal_state[0]) + np.square(current_state[1] - goal_state[1])
    if radius_sq < thresh_radius**2:
        return True
    else:
        return False


# %%
def checkVisited(node, node_array, goal_state, threshold=0.5, thetaStep=30):
    result = False
    node_state = node.getState()
    x = node_state[0]
    y = node_state[1]
    theta = node_state[2]
    x = int(halfRound(x)/threshold)
    y = int(halfRound(y)/threshold)
    theta = int(theta/thetaStep)

    if (node.getCost() + computeHeuristicCost(node_state, goal_state) < node_array[x, y, theta]):
        result = True
    return result


# %%
def computeHeuristicCost(current_state, goal_state):
    cost = 0.0
    if current_state is not None:
        cost =  ((current_state[0]-goal_state[0])**2 + (current_state[1]-goal_state[1])**2)**(0.5)
    return cost


# %%
def isInvalidInput(i,j):
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
    Parser.add_argument("--InitState", nargs='+', type=int, default= [0, 0, 0], help = 'init state')
    Parser.add_argument("--GoalState", nargs='+', type=int, default= [350, 250], help = 'goal state')
    Parser.add_argument("--StepSize", type=int, default= 10, help = 'Step size: 1-10')
    Parser.add_argument('--SaveFolderName', default='./', help='Default path to store the video')
    Args = Parser.parse_args()

    init_state = Args.InitState
    goal_state = Args.GoalState
    step_size = Args.StepSize
    save_folder_name = Args.SaveFolderName
    if (not save_folder_name[-1] == '/'):
        save_folder_name = save_folder_name + '/'
    SaveFileName = save_folder_name + "AStar_path.avi"

    if (isInvalidInput(init_state[0], init_state[1])):
        print('Initial state is in obstacle space, please provide new valid state')
        exit()

    if (isInvalidInput(goal_state[0], goal_state[1])):
        print('Goal state is in obstacle space, please provide new valid state')
        exit()

    h = 300
    w = 400
    space_size = [h, w]
    threshold = 0.5
    step_angle = 30

    #visited = np.zeros((int(400/threshold),int(300/threshold),int(360/step_angle)), dtype='int')

    start_point = init_state
    goal_state = goal_state

    result = cv2.VideoWriter(SaveFileName,  
                        cv2.VideoWriter_fourcc(*'MJPG'), 
                        300, (sizex, sizey))


    nodes = queue.PriorityQueue()
    init_node = Node(start_point, None, None, 0)

    nodes.put((init_node.getCost(), init_node))

    root2 = np.sqrt(2)

    goal_reached = False
    node_array = np.array([[[math.inf  for k in range(12)] for j in range(int(300/threshold))] for i in range(int(400/threshold))])

    space_size = [300, 400]
    space_map = np.zeros([space_size[0], space_size[1], 3], dtype=np.uint8)
    space_map = updateMap(space_map, init_node, [0,0,255])
    space_map = addObstacles2Map(space_map)

    full_path = None
    goal_reached = False

    print('Finding path.........')

    while (not nodes.empty()):
        current_node = nodes.get()[1]
        space_map = updateMap(space_map, current_node, [0, 255, 0])
        result.write(space_map)
        # cv2.imshow('frame',space_map)
        # # cv2.waitKey()
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        if checkGoalReached(current_node, goal_state,5):
            print('Goal reached')
            print("The cost of path: ", current_node.getCost())
            full_path, node_path = current_node.getFullPath()
            goal_reached = True

            for node in node_path:
                space_map = updateMap(space_map, node, [0, 0, 255])
                result.write(space_map)

            # keep final frame for 3s
            for i in range(900):
                result.write(space_map)
            #     cv2.imshow('frame',space_map)
            #     if cv2.waitKey(1) & 0xFF == ord('q'):
            #         break
            # cv2.waitKey()
        else:
            branches = getBranches(current_node, step_size, goal_state)    
            for branch_node in branches:

                branch_state = branch_node.getState()
                if checkVisited(branch_node, node_array, goal_state, threshold=0.5, thetaStep=30):
                    node_array[int(halfRound(branch_state[0])/threshold), int(halfRound(branch_state[1])/threshold), int(halfRound(branch_state[2])/30)] = branch_node.getCost() + computeHeuristicCost(branch_state, goal_state)
                    nodes.put((branch_node.getCost() + computeHeuristicCost(branch_state, goal_state), branch_node))

        if (goal_reached): break
            
    cv2.destroyAllWindows()
    print('Goal Reached. Please check the video in the current directory or the path provided as input')
    


# %%
if __name__ == "__main__":
    main()


# %%



