def intersectionWithCircle(m, r, cx, cy, c):
    determinant = (r**2)*(1 + m**2) - (cy - m*cx -c)**2
    return determinant
