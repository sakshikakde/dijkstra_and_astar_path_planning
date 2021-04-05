import numpy as np
from Utils.MiscUtils import *

sizex = 400
sizey = 300
robot_radius = 5
clearance = 10
# total_clearance = robot_radius + clearance
# sizex, sizey, robot_radius, clearance = getParameters()
total_clearance = robot_radius + clearance
# circle
circle_diameter = 70 
circle_offset_x = 90
circle_offset_y = 70
circle_radius = int(circle_diameter/2 + total_clearance)

#ellipse
ellipse_diameter_x = 120
ellipse_diameter_y = 60
ellipse_offset_x = 246
ellipse_offset_y = 145
ellipse_radius_x = int(ellipse_diameter_x/2 + total_clearance)
ellipse_radius_y = int(ellipse_diameter_y/2 + total_clearance)

# C shape
c_offset_x = 200
c_offset_y = 230
c_length_x = 30 
c_length_y = 50
c_width = 10
c_height = 30

# angles rectangle
rect_angle = 35 * np.pi/180
rect_length = 150 + 2 * total_clearance
rect_width = 20 + 2 * total_clearance

rect_offset_x = 48
rect_offset_y = 108

rect_corner1_x = int(rect_offset_x ) #- total_clearance * np.sqrt(2))
rect_corner1_y = int(rect_offset_y - total_clearance * np.sqrt(2))

rect_corner2_x = int(rect_corner1_x + rect_length * np.cos(rect_angle))
rect_corner2_y = int(rect_corner1_y + rect_length * np.sin(rect_angle))

rect_corner3_x = int(rect_corner2_x - rect_width * np.sin(rect_angle))
rect_corner3_y = int(rect_corner2_y + rect_width * np.cos(rect_angle))

rect_corner4_x = int(rect_corner1_x - rect_width * np.sin(rect_angle))
rect_corner4_y = int(rect_corner1_y + rect_width * np.cos(rect_angle))

rect_x_min = np.min([rect_corner1_x, rect_corner2_x, rect_corner3_x, rect_corner4_x])
rect_y_min = np.min([rect_corner1_y, rect_corner2_y, rect_corner3_y, rect_corner4_y])

rect_x_max = np.max([rect_corner1_x, rect_corner2_x, rect_corner3_x, rect_corner4_x])
rect_y_max = np.max([rect_corner1_y, rect_corner2_y, rect_corner3_y, rect_corner4_y])

# c_shape
c_corner1_x = c_offset_x - total_clearance
c_corner1_y = c_offset_y - total_clearance

c_corner2_x = c_corner1_x + c_length_x + 2 * total_clearance
c_corner2_y = c_corner1_y

c_corner3_x = c_corner2_x
c_corner3_y = c_corner2_y + c_width + 2 * total_clearance

c_corner4_x = c_corner3_x - (c_length_x - total_clearance) 
c_corner4_y = c_corner3_y

c_corner5_x = c_corner4_x
c_corner5_y = c_corner4_y + (c_height - 2 * total_clearance)

c_corner6_x = c_corner2_x
c_corner6_y = c_corner5_y

c_corner7_x = c_corner6_x
c_corner7_y = c_corner5_y + c_width + 2 * total_clearance

c_corner8_x = c_corner1_x
c_corner8_y = c_corner7_y

c_max_x = np.max([c_corner1_x, c_corner2_x, c_corner3_x, c_corner4_x, c_corner5_x, c_corner6_x, c_corner7_x, c_corner8_x])
c_min_x = np.min([c_corner1_x, c_corner2_x, c_corner3_x, c_corner4_x, c_corner5_x, c_corner6_x, c_corner7_x, c_corner8_x])
c_max_y = np.max([c_corner1_y, c_corner2_y, c_corner3_y, c_corner4_y, c_corner5_y, c_corner6_y, c_corner7_y, c_corner8_y])
c_min_y = np.min([c_corner1_y, c_corner2_y, c_corner3_y, c_corner4_y, c_corner5_y, c_corner6_y, c_corner7_y, c_corner8_y])