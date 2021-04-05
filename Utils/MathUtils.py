import numpy as np
import math
from Obstacle import *


def halfRound(n):
    return round(2*n)/2

def transformPoint(state, space_map):
    X, Y, _ = space_map.shape
    transformed_y = state[0]
    transformed_x = X - state[1] -1
    return [int(transformed_x), int(transformed_y)]


def checkLineIntersection(m1, c1, m2, c2):
    if m1 == m2:
        return [math.inf, math.inf]
    
    if (m1 == math.inf):
        x = c1
        y = m2 * x + c2
        
    elif (m2 == math.inf):
        x = c2
        y = m1 * x + c1
    else:
        x = (c2 - c1) / (m1 - m2)
        y = (m1 * c2 - m2 * c1) / (m1 - m2)
    return [x, y]


def getLineParam(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    if (round(x2 - x1) == 0):
        m = math.inf
        c = x2
    else:
        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1
    return m, c

# def intersectionWithCircle(m, c, cx, cy, r):
#     determinant = (r**2)*(1 + m**2) - (cy - m*cx -c)**2
#     x = 0
#     y = 0
#     if (determinant > 0.0):
#         x1 = cx + cy*m - c*m + np.sqrt(determinant)
#         x2 = cx + cy*m - c*m - np.sqrt(determinant)
#         y1 = m*x1 + c
#         y2 = m*x2 + c
#     else :
#         return None
#     points = np.array([[x1, y1], [x2, y2]])
#     return points

def intersectionWithCircle(m, c, cx, cy, r):
    x1, y1, x2, y2, determinant = 0.0, 0.0, 0.0, 0.0, 0.0
    if (m == math.inf):
        k = c
        determinant = r**2 - (k - cx)**2
        if (determinant < 0):
            return None
        else:
            x1 = k
            y1 = cy + np.sqrt(determinant)
            x2 = k
            y2 = cy - np.sqrt(determinant)
            points = np.array([[x1, y1], [x2, y2]])
    else:
        determinant = (r**2)*(1 + m**2) - (cy - m*cx -c)**2
        if (determinant > 0.0):
            x1 = (cx + cy*m - c*m + np.sqrt(determinant))/(1+ m**2)
            x2 = (cx + cy*m - c*m - np.sqrt(determinant))/(1+ m**2)
            y1 = m*x1 + c
            y2 = m*x2 + c
        else :
            return None
        points = np.array([[x1, y1], [x2, y2]])
    return points

# function to find the intersection of line with ellipse
# m = slope of line, c = y intercept, a = major axis, b = minor axis, h = x offset, k = y offset
def intersectionWithEllipse(m, c, a, b, h, k):
    x1, y1, x2, y2, determinant = 0.0, 0.0, 0.0, 0.0, 0.0
    if (m == math.inf):
        phy = ((c-h)/a)**2
        determinant = (b**2)*(1-phy)
        if (determinant < 0.0):
            return None
        else:
            x1, x2 = c, c
            y1 = k + np.sqrt(determinant)
            y2 = k - np.sqrt(determinant)
            points = np.array([[x1, y1], [x2, y2]])
    else:
        phy = c - k
        mu = c + m*h
        determinant = b**2 + (a**2)*(m**2) - 2*m*phy*h - phy**2 - (m**2)*(h**2)
        if (determinant < 0.0):
            return None
        else:
            x1 = ((b**2)*h - (a**2)*m*phy + (a*b)*(np.sqrt(determinant))) / (b**2 + (a**2)*(m**2))
            x2 = ((b**2)*h - (a**2)*m*phy - (a*b)*(np.sqrt(determinant))) / (b**2 + (a**2)*(m**2))
            y1 = m*x1 + c
            y2 = m*x2 + c
            points = np.array([[x1, y1], [x2, y2]])
    return points


def rectIntersect(move):
    line1 = getLineParam([rect_corner1_x, rect_corner1_y], [rect_corner2_x, rect_corner2_y])
    line2 = getLineParam([rect_corner2_x, rect_corner2_y], [rect_corner3_x, rect_corner3_y])
    line3 = getLineParam([rect_corner3_x, rect_corner3_y], [rect_corner4_x, rect_corner4_y])
    line4 = getLineParam([rect_corner4_x, rect_corner4_y], [rect_corner1_x, rect_corner1_y])

    I1 = checkLineIntersection(move[0], move[1], line1[0], line1[1])
    I2 = checkLineIntersection(move[0], move[1], line2[0], line2[1])
    I3 = checkLineIntersection(move[0], move[1], line3[0], line3[1])
    I4 = checkLineIntersection(move[0], move[1], line4[0], line4[1])

    I = np.array([I1, I2, I3, I4])
    if ((I[:,0] >= rect_x_min) & (I[:,0] <= rect_x_max) & (I[:,1] >= rect_y_min) & (I[:,1] <= rect_y_max)).any():
        return True
    else:
        return False

def cIntersect(move):
    line1 = getLineParam([c_corner1_x, c_corner1_y], [c_corner2_x, c_corner2_y])
    line2 = getLineParam([c_corner2_x, c_corner2_y], [c_corner7_x, c_corner7_y])
    line3 = getLineParam([c_corner7_x, c_corner7_y], [c_corner8_x, c_corner8_y])
    line4 = getLineParam([c_corner8_x, c_corner8_y], [c_corner1_x, c_corner1_y])

    I1 = checkLineIntersection(move[0], move[1], line1[0], line1[1])
    I2 = checkLineIntersection(move[0], move[1], line2[0], line2[1])
    I3 = checkLineIntersection(move[0], move[1], line3[0], line3[1])
    I4 = checkLineIntersection(move[0], move[1], line4[0], line4[1])

    I = np.array([I1, I2, I3, I4]) 

    if ((I[:,0] >= c_min_x) & (I[:,0] <= c_max_x) & (I[:,1] >= c_min_y) & (I[:,1] <= c_max_y)).any():
        return True
    else:
        return False

def circleIntersect(move):
    I = intersectionWithCircle(move[0], move[1], circle_offset_x, circle_offset_y, circle_radius)
    if I is None:
        return False

    circle = (I[:,0] - circle_offset_x)**2 + (I[:,1] - circle_offset_y)**2
    ratio = (circle/(circle_radius**2)).astype(int)
    if (ratio <= 1).any():
        return True
    else:
        return False

def ellipseIntersect(move):
    
    I = intersectionWithEllipse(move[0], move[1], 75.0, 45.0, 246.0, 145.0)
    if I is None:
        return False

    ellipse = np.square((I[:,0] - 246.0)/75.0) + np.square((I[:,1] - 145.0)/45.0).astype(int)
    # print(ellipse)
    if (ellipse <= 1).any():
        # print(ellipse)
        return True
    else:
        return False
    