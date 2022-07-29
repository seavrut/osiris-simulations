# Triangle.py

import numpy as np

def triangle(n:float, tip1:tuple, tip2:tuple, mirror:float, length:float, theta:float=None) -> str:
    """n: relative plasma density
    tip1: coordinates of tip of 1st triangle
    tip2: coordinates of tip of 2nd triangle
    mirror: x value of mirror point
    length: side length of triangles
    theta: halfangle of prism (in degrees), if not provided defaults to Brewster's angle

    returns: math_func_expr string for 4 triangles"""

    def if_str(x, y, z) -> str:
        """returns 'if(x, y, z)'"""
        return 'if(%s,\n\t %s,\n\t %s)' % (str(x), str(y), str(z))

    def tan_str(X, a, b, c) -> str:
        return '%.1f * tanh(%.3f*(%s)) + %.1f' % (a, b, str(X), c)

    m = np.sqrt(1-n)    # refractive index

    if theta != None:
        theta = np.deg2rad(theta)    # convert to radians
    else:
        brewster = np.arctan2(m, 1)
        theta = np.arcsin(np.sin(brewster) / m)



    alpha = np.pi/2. + theta - np.arcsin(m*np.sin(theta))

    tip3 = (2*mirror - tip2[0], tip2[1])
    tip4 = (2*mirror - tip1[0], tip1[1])
    
    #\tan(\alpha)(x1-c\)+d-x2>0
    #y= \tan (\alpha + theta)(x-a)+b {b-s<y<b}
    t1_left = '%.2f*x1 + %.0f - x2' % (np.tan(alpha - theta), np.tan(alpha - theta)*-1*(tip1[0]-700)+ tip1[1]+700)
    t1_right = '%.2f*x1 + %.0f - x2' % (np.tan(alpha + theta), np.tan(alpha + theta)*-1*(tip1[0]+900) + tip1[1]+900)
    t1_left_ns = '%.2f*x1 + %.0f - x2' % (np.tan(alpha - theta), np.tan(alpha - theta)*-1*tip1[0] + tip1[1])
    t1_right_ns = '%.2f*x1 + %.0f - x2' % (np.tan(alpha + theta), np.tan(alpha + theta)*-1*tip1[0] + tip1[1])
    t1_bottom = 'x2 + %.0f' % (-tip1[1] + length)
    t1_mid = '%.2f*x1 + %.0f - x2' % (np.tan(alpha), np.tan(alpha)*-1*tip1[0] + tip1[1])
    t1 = if_str('(%s > 0) && (%s > 0)' % (t1_left, t1_right),
            if_str(t1_mid + ' > 0',
                    tan_str(t1_left_ns, 0.5, 0.005, 0.5),
                    tan_str(t1_right_ns, 0.5, 0.005, 0.5)),
            0)

    t2_left = '%.2f*x1 + %.0f - x2' % (np.tan(alpha + theta), np.tan(alpha + theta)*-1*(tip2[0]-200) + tip2[1]-200)
    t2_right = '%.2f*x1 + %.0f - x2' % (np.tan(alpha - theta), np.tan(alpha - theta)*-1*(tip2[0]+200) + tip2[1]-200)
    t2_left_ns = '-(%.2f*x1 + %.0f - x2)' % (np.tan(alpha + theta), np.tan(alpha + theta)*-1*tip2[0] + tip2[1])
    t2_right_ns = '-(%.2f*x1 + %.0f - x2)' % (np.tan(alpha - theta), np.tan(alpha - theta)*-1*tip2[0] + tip2[1])
    t2_top = '-x2 + %.0f' % (tip2[1] + length)
    t2_mid = '%.2f*x1 + %.0f - x2' % (np.tan(alpha), np.tan(alpha)*-1*tip2[0] + tip2[1])
    t2 = if_str('(%s < 0) && (%s < 0)' % (t2_left, t2_right),
                 if_str(t2_mid + ' > 0',
                        tan_str(t2_left_ns, 0.5, 0.005, 0.5),
                        tan_str(t2_right_ns, 0.5, 0.005, 0.5)),
                 0)

    t3_left = '%.2f*x1 + %.0f - x2' % (np.tan(-alpha + theta), np.tan(-alpha + theta)*-1*(tip3[0]-200) + tip3[1]-200)
    t3_right = '%.2f*x1 + %.0f - x2' % (np.tan(-alpha-theta), np.tan(-alpha-theta)*-1*(tip3[0]+200) + tip3[1]-200)
    t3_left_ns = '-(%.2f*x1 + %.0f - x2)' % (np.tan(-alpha + theta), np.tan(-alpha + theta)*-1*tip3[0] + tip3[1])
    t3_right_ns = '-(%.2f*x1 + %.0f - x2)' % (np.tan(-alpha-theta), np.tan(-alpha-theta)*-1*tip3[0]+tip3[1])
    t3_top = '-x2 + %.0f' % (tip3[1]+length)
    t3_mid = '%.2f*x1 + %.0f - x2' % (np.tan(-alpha), np.tan(-alpha)*-1*tip3[0] + tip3[1])
    #t3 = 'step(%s) * step(%s) * (%s)\n + step(-(%s)) * step(%s) * (%s)' % (t3_left, t3_mid, tan_str(t3_left_ns, 0.5, 0.01, 0.5), t3_mid, t3_right, tan_str(t3_right_ns, 0.5, 0.01, 0.5))
    t3 = if_str('(%s < 0) && (%s < 0)' % (t3_left, t3_right),
                if_str(t3_mid + ' < 0',
                        tan_str(t3_left_ns, 0.5, 0.005, 0.5),
                        tan_str(t3_right_ns, 0.5, 0.005, 0.5)),
                 0)


    t4_left = '%.2f*x1 + %.1f - x2' % (np.tan(-alpha-theta), np.tan(-alpha-theta)*-1*(tip4[0]-200) + tip4[1]+200)
    t4_right = '%.2f*x1 + %.1f - x2' % (np.tan(-alpha+theta), np.tan(-alpha+theta)*-1*(tip4[0]+200) + tip4[1]+200)
    t4_left_ns = '%.2f*x1 + %.0f - x2' % (np.tan(-alpha-theta), np.tan(-alpha-theta)*-1*tip4[0]+ tip4[1])
    t4_right_ns = '%.2f*x1 + %.0f - x2' % (np.tan(-alpha+theta), np.tan(-alpha+theta)*-1*tip4[0]+tip4[1])
    t4_bottom = 'x2 + %.0f' % (-tip4[1]+length)
    t4_mid = '%.2f*x1 + %.0f - x2' % (np.tan(-alpha), np.tan(-alpha)*-1*tip4[0]+ tip4[1])
    #t4 = 'step(%s) * step(-(%s)) * (%s)\n + step(%s) * step(%s) * (%s)' % (t4_left, t4_mid, tan_str(t4_left_ns, 0.5, 0.01, 0.5), t4_mid, t4_right, tan_str(t4_right_ns, 0.5, 0.01, 0.5))
    t4 = if_str('(%s > 0) && (%s > 0)' % (t4_left, t4_right),
                 if_str( t4_mid + ' < 0',
                        tan_str(t4_left_ns, 0.5, 0.005, 0.5),
                        tan_str(t4_right_ns, 0.5, 0.005, 0.5)),
                 0)


    out = '\"(' + t1 + '\n\n + ' + t2 + '\n\n + ' + t3 + '\n\n + ' + t4 + ')\n\n*step(%s)*step(%s)\",' % (t1_bottom, t2_top)
    out = out.replace('+ -', '- ')
    return out