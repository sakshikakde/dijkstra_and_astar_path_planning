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
        print('Determinant = ', determinant)
        if (determinant > 0.0):
            x1 = cx + cy*m - c*m + np.sqrt(determinant)
            x2 = cx + cy*m - c*m - np.sqrt(determinant)
            y1 = m*x1 + c
            y2 = m*x2 + c
        else :
            return None
        points = np.array([[x1, y1], [x2, y2]])
    print('Determinant = ', determinant)
    print('Points = ' ,x1, ', ', y1, ', ', x2, ', ', y2 )
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
    print('Points = ' ,x1, ', ', y1, ', ', x2, ', ', y2 )
    return points

