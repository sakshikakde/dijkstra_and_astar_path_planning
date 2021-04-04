def intersectionWithCircle(m, c, cx, cy, r):
    determinant = (r**2)*(1 + m**2) - (cy - m*cx -c)**2
    x = 0
    y = 0
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
