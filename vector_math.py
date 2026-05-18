import math
""" THIS MODULE CONTAINS VECTOR OPERATIONS AND
    SOME USEFUL COLLISION DETECTION FUNCTIONS """

#############################################################
                #### VECTORS OPERATIONS ####
#############################################################

def add_vec(v1, v2):
    """ Function to add two vectors """
    nv = [v1[0] + v2[0], 
          v1[1] + v2[1]]
    return nv


def sub_vec(v1, v2):
    """ Function to substract two vectors """
    nv = [v1[0] - v2[0],  # Creates an imaginary "rectangle" between
          v1[1] - v2[1]]   # both vectors/points.
    return nv


def scale_vec(v1, scalar):
    """ Function to multiply x, y of
        a vector by a scalar """
    nv = [v1[0] * scalar,  
          v1[1] * scalar] 
    return nv


def rotate_vec(coords, theta):
    """ Rotate vector to certain angle/theta """
    cos_theta = math.cos(math.radians(theta))
    sin_theta = math.sin(math.radians(theta))
    nv = [[v[0] * cos_theta + v[1] * -sin_theta,
           v[1] * cos_theta + v[0] * sin_theta]]
    return nv


def normalize_vec(v1):
    """ Function to divide vector by its magnitud
        to find the unit base of the vector """
    magn = dist(v1)
    nv = [v1[0] / magn,  
          v1[1] / magn]
    return nv


def dist(vector):
    """ Pythagoras Theorem """
    return ((vector[0]**2) + (vector[1]**2))**0.5 


def distance(v1, v2):
    """ Substracts vectors and calculates the
        distance between them """
    return hypo(sub_vec(v1, v2))


#### #### #### #### #### ####
#### MULTIPLE COORDINATES ####
#### #### #### #### #### ####

def add_vecs(coords, v2):
    nc = []
    for i, v in enumerate(coords):
        nc += [[v[0] + v2[0],
                v[1] + v2[1]]]
    return nc

def sub_vecs(coords, v2):
    nc = []
    for i, v in enumerate(coords):
        nc += [[v[0] - v2[0],
                v[1] - v2[1]]]
    return nc

def scale_vecs(coords, scalar):
    nc = []
    for i, v in enumerate(coords):
        nc += [[v[0] * scalar,
                v[1] * scalar]]
    return nc

def rotate_vecs(coords, theta):
    cos_theta = math.cos(math.radians(theta))
    sin_theta = math.sin(math.radians(theta))
    nc = []
    for i, v in enumerate(coords):
        nc += [[v[0] * cos_theta + v[1] * -sin_theta,
                v[1] * cos_theta + v[0] * sin_theta]]
    return nc



def random_2d(pos=None):
    """ Returns a unit vector with a random direction """
    if pos == None: pos = [0, 0]
    angle = random.randint(-180, 180)
    vx = pos[0] + math.cos(math.radians(angle)) * 1
    vy = pos[1] + math.sin(math.radians(angle)) * 1
    return [vx, vy]


#############################################################
        #### COLLISION DETECTION FUNCTIONS ####
#############################################################


def point_point(v1, v2):
    """ v1 = x, y
        v2 = x, y
    """
    if (v1[0] == v2[0] and v1[1] == v2[1]):
        # Points are in the same place: Collision!
        return True
    else:
        # Not colliding
        return False


def point_circle(v1, v2):
    """ circle v1 = x, y, r
        point  v2 = x, y
    """
    if dist(sub_vec(v1, v2)) < v1[2]:
        return True
    else:
        return False


def circle_circle(v1, v2):
    """ v1 = x, y, r
        v2 = x, y, r
    """
    if dist(sub_vec(v1, v2)) < v1[2]+v2[2]:
        return True
    else:
        return False


def point_rect(v1, v2):
    """ point v1 = x, y
        rect  v2 = x, y, w, h
    """
    # v2[0], v2[1], v2[2], v2[3] = x, y, w, h
    left_edge, right_edge = v2[0], v2[0]+v2[2]
    top_edge, bottom_edge = v2[1], v2[1]+v2[3]

    if (v1[0] >= left_edge and
        v1[0] <= right_edge and
        v1[1] >= top_edge and
        v1[1] <= bottom_edge):
        # The point is inside the rectangle
        return True
    else:
        # The point is outside the rectangle
        return False
        

def rect_rect(v1, v2):
    """ v1 = x, y, w, h
        v2 = x, y, w, h
    """
    # v1[0], v1[1], v1[2], v1[3] = x, y, w, h
    left1, top1 = v1[0], v1[1]
    right1, bottom1 = v1[0]+v1[2], v1[1]+v1[3]

    # v2[0], v2[1], v2[2], v2[3] = x, y, w, h
    left2, right2 = v2[0], v2[0]+v2[2]
    top2, bottom2 = v2[1], v2[1]+v2[3]


    if (right1 >= left2 and
        left1 <= right2 and
        bottom1 >= top2 and
        top1 <= bottom2):
        # The rect1 touches the rect2
        return True

    else:
        # The rect is outside the rectangle
        return False
        

def circle_rect(v1, v2):
    """ circle v1 = x, y, r
        rect   v2 = x, y, w, h
    """

    closestx = v1[0] 
    closesty = v1[1]

    # cx+rad < rx/left                is close to rect left  
    if v1[0]+v1[2] < v2[0]:           closestx = v2[0]
    # cx-rad > rx+rw/right            is close to rect right
    elif v1[0]-v1[2] > v2[0]+v2[2]:   closestx = v2[0]+v2[2]
    # cy+rad < ry/top                 is close to rect top
    elif v1[1]+v1[2] < v2[1]:         closesty = v2[1]
    # cy-rad > ry+rh/bottom           is close to rect bottom
    elif v1[1]-v1[2] > v2[1]+v2[3]:   closesty = v2[1]+v2[3]

    if dist( sub_vec(v1, [closestx, closesty]) ) <= v1[2]:
        return True
    else:
        return False


def line_point(v1, v2):
    """ line  v1 = sx, sy, ex, ey
        point v2 = x, y
    """
    # First the get the len of the line
    line_len = dist(sub_vec( [ v1[0], v1[1] ], [ v1[2], v1[3] ] ))

    # We also need to figure out the distance
    # between the point and the two ends
    d1 = dist(sub_vec(v2, v1))
    d2 = dist(sub_vec(v2, [ v1[2], v1[3] ] ))

    buffer = 0.1 # higher equals less accurate collision

    if (d1+d2 >= line_len-buffer and
        d1+d2 <= line_len+buffer):
        return True
    else:
        return False

    



