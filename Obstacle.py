import numpy as np

sizex = 400
sizey = 300
robot_radius = 10
clearance = 5
total_clearance = 0# robot_radius + clearance
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
c_offset_y = sizey - 20
c_length_x = 30 + (total_clearance * 2)
c_length_y = 50 + (total_clearance * 2)
c_width = 10 + (total_clearance)
c_height = 30 - (total_clearance * 2)

# angles rectangle
rect_angle = 35 * np.pi/180
rect_length = 150 + total_clearance
rect_width = 20 + total_clearance

rect_corner1_x = 48
rect_corner1_y = 108

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

# polygon
poly_angle = 45 * np.pi/180
poly_length = 75
poly_width = 60

poly_corner1_x = sizex - 72
poly_corner1_y = 63

right_tri_height = 55

poly_corner2_x = int(poly_corner1_x + poly_length * np.cos(poly_angle))
poly_corner2_y = int(poly_corner1_y + poly_length * np.sin(poly_angle))

poly_corner4_x = int(poly_corner1_x - poly_width * np.sin(poly_angle))
poly_corner4_y = int(poly_corner1_y + poly_width * np.cos(poly_angle))

poly_corner3_x = int(poly_corner4_x + 56 * np.cos(poly_angle))
poly_corner3_y = int(poly_corner4_y + 56 * np.sin(poly_angle))

poly_corner5_x = poly_corner2_x
poly_corner5_y = poly_corner2_y + right_tri_height

poly_corner6_x = 354
poly_corner6_y = 138

tan65 = (poly_corner5_y - poly_corner6_y) / (poly_corner5_x - poly_corner6_x)
tan36 = (poly_corner6_y - poly_corner3_y) / (poly_corner6_x - poly_corner3_x)

poly_x_min = np.min([poly_corner1_x, poly_corner2_x, poly_corner3_x, poly_corner4_x, poly_corner5_x, poly_corner6_x])
poly_y_min = np.min([poly_corner1_y, poly_corner2_y, poly_corner3_y, poly_corner4_y, poly_corner5_y, poly_corner6_y])

poly_x_max = np.max([poly_corner1_x, poly_corner2_x, poly_corner3_x, poly_corner4_x, poly_corner5_x, poly_corner6_x])
poly_y_max = np.max([poly_corner1_y, poly_corner2_y, poly_corner3_y, poly_corner4_y, poly_corner5_y, poly_corner6_y])

