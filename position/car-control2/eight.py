from math import cos, sin, pi, atan2, sqrt

from nav_util import rev, dist

def eightpoint(cy, ang):
    cx = 1.5
    R = 1.0
    x = cx + R*sin(ang*pi/180)
    y = cy + R*cos(ang*pi/180)
    return (x, y)

piece1 = [7, 11, 17, 24, 28, 30, 36]
piece2 = [35, 32, 27, 23, 19, 13, 6]
piece3 = [5, 10, 16, 23, 26, 29, 34]
piece4 = [33, 31, 25, 22, 18, 12, 4]

piece5 = [35, 34]
piece6 = [5, 6]

piece7 = [3, 4]

# 'ways' is not used in nav.py
ways = dict()

nodes = dict()

def fillinlist(l, add):
    n = 3
    for j in range(2*n, 0, -1):
        l[j:j] = [add+l[j]]
    return l

#interleave = 1
interleave = 2

if interleave == 2:
    piece1 = fillinlist(piece1, 100)
    piece2 = fillinlist(piece2, 200)
    piece3 = fillinlist(piece3, 300)
    piece4 = fillinlist(piece4, 400)

piece2a = [35, 32, 27]
piece2a = piece2[0:3*interleave]
# via 23
piece2b = [19, 13, 6]
piece2b = piece2[3*interleave+1:]

piece3a = [5, 10, 16]
piece3a = piece3[0:3*interleave]
# via 23
piece3b = [26, 29, 34]
piece3b = piece3[3*interleave+1:]

ways[1] = piece1 + [35, 34] + piece4 + [5, 6] + [piece1[0]]
ways[3] = piece2
ways[4] = piece3
ways[2] = piece7



# for the geometric 8 only
nodenumbers = piece1 + piece2 + piece3 + piece4

def eightarc(nodenumbers, cy, angleoffset):
    # assume len(nodenumbers) == 7, 2*n+1 == 7
    n = 3
    k = interleave
    for i in range(-n*k, n*k+1):
        ang = 90.0/(n*k)*i
        (x, y) = eightpoint(cy, ang+angleoffset)
        nr = nodenumbers[0]
        nodenumbers = nodenumbers[1:]
        if nr not in nodes:
            nodes[nr] = (x, y)
        else:
            ox = nodes[nr][0]
            oy = nodes[nr][1]
            if abs(x-ox) > 0.01 or abs(y-oy) > 0.01:
                print("node %d already exists: new (%f,%f) old (%f,%f)" % (
                        nr, x, y, ox, oy))
    return nodenumbers

def eightpath(y1, y2, y3):
    R = 1.0

    eightarc(piece1, y1 - R, 0)
    eightarc(piece2, y2 + R, 180)
    eightarc(piece3, y2 - R, 0)
    eightarc(piece4, y3 + R, 180)

    # 0.5 fits with the constants in 'eightpoint'
    nodes[3] = (0.5, 8.0)

    for nr in nodes:
#        print("%d %f %f" % (nr, nodes[nr][0], nodes[nr][1]))
        pass

def makepath(offset, path):
    path1 = []
    x1 = None
    y1 = None
    n = 0
    i1 = None
    for (i, (x0, y0)) in path:
        
        if x1 == None:
            pass
        else:
            dx = x0-x1
            dy = y0-y1
            angle = atan2(dx, -dy)

            x = x1
            y = y1

            path1.append((i1,
                          x+offset*cos(angle),
                          y+offset*sin(angle)))

        i1 = i
        x1 = x0
        y1 = y0
        n += 1

    # use the same angle as for the previous point
    path1.append((i1,
                  x1+offset*cos(angle),
                  y1+offset*sin(angle)))

    return path1

def piece2path(p, offset):
    path1 = [(i, nodes[i]) for i in p]
    path = makepath(offset, path1)
    return path



roadpoints = dict()


def makepathpoints(offset, path):
    path1 = []
    x1 = None
    y1 = None
    n = 0
    i1 = None
    gran = 10

    # make sure our areas overlap
    extra = 2

    for (i, (x0, y0)) in path:
        
        if x1 == None:
            pass
        else:
            dx = x0-x1
            dy = y0-y1
            angle = atan2(dx, -dy)

            for k in range(-extra, gran+1+extra):
                for j in range(-gran, gran+1):
                    px = x1 + k*dx/gran + offset*cos(angle)*j/gran
                    py = y1 + k*dy/gran + offset*sin(angle)*j/gran
                    roadpoints[(px,py)] = True

        i1 = i
        x1 = x0
        y1 = y0
        n += 1

    # use the same angle as for the previous point

    dx = x0-x1
    dy = y0-y1

    for k in range(-extra, gran+1+extra):
        for j in range(-gran, gran+1):
            px = x1 + k*dx/gran + offset*cos(angle)*j/gran
            py = y1 + k*dy/gran + offset*sin(angle)*j/gran
            roadpoints[(px,py)] = True

def piece2pathpoints(p, offset):
    path1 = [(i, nodes[i]) for i in p]
    makepathpoints(offset, path1)

def roaddist(x0, y0):
    dmin = None
    for (x, y) in roadpoints:
        d = dist(x, y, x0, y0)
        if dmin == None or dmin > d:
            dmin = d
    return dmin

# A position of a car in the road network is indicated by what two nodes
# A and B it is between, and how far as a fraction from A.
# From this it is easy to get coordinates, and which piece it is.
def plan(p0, p1):
    return False

def isdecisionpoint(n):
    for (a, b) in pieces:
        if a == n:
            return True
    return False

# A piece goes from a over the list l to b
# n0 is in l
# Sum the distances from a to n0, and from n0 to b
def partdist(n0, a, b, l):
    da = 0
    db = distances[(b, l[-1])]
    before_n0 = True
    lastn = a
    for n in l:
        if before_n0:
            da += distances[(lastn, n)]
        else:
            db += distances[(lastn, n)]
        lastn = n
        if n == n0:
            before_n0 = False
    return (da, db)

# Bug: going only within one piece doesn't work.

# If n0 or n1 are not decision points, n2 and nz are still to be
# decision points.
def paths_p(n0, n1, n2=None, nz=None):
    extra0 = None
    n0x = n0
    for (a, b) in pieces:
        (l, dtot) = pieces[(a, b)]
        if n0 in l:
            (da, db) = partdist(n0, a, b, l)
            #print(("dist", da, db, dtot))
            extra0 = (a, b, da, db)
            n0x = a
            break

    extra1 = None
    n1x = n1
    for (a, b) in pieces:
        (l, dtot) = pieces[(a, b)]
        if n1 in l:
            (da, db) = partdist(n1, a, b, l)
            #print(("dist", da, db, dtot))
            extra1 = (a, b, da, db)
            n1x = b
            break

    #print (extra0, extra1, n0x, n1x)

    pl0 = extendpath_p([n0x], n1x, 0.0, n2, nz, [])
    pl = []
    for (d, l) in pl0:
        if extra0:
            (a, b, da, db) = extra0
            if l[1] == b:
                l = [n0] + l[1:]
                d -= da
            else:
                # we should make sure that (b,a) is also possible
                l = [n0] + l
                d += da
        if extra1:
            (a, b, da, db) = extra1
            if l[-2] == a:
                l = l[:-1] + [n1]
                d -= db
            else:
                l = l + [n1]
                d += db
        pl.append((d, l))

    return pl

def neighbours_p(n):
    l = []
    for (a, b) in pieces:
        if a == n:
            (_, d) = pieces[(a, b)]
            l.append((b, d))
    return l

def extendpath_p(p, goaln, d0, n2, nz, acc):
    nlast1 = p[-1]

    if nlast1 == goaln:
        if nz == None or p[-2] == nz:
            #print("%f %s" % (d0, str(p)))
            return acc + [(d0, p)]

    for (n, d) in neighbours_p(nlast1):
        # Here, we should not look for only p, but for the sequence
        # [p[-1], n]
        if n in p:
            continue

        if len(p) == 1 and n2 != None and n != n2:
            continue

        sharpturns = [[6, 23, 5],
                      [34, 23, 35],
                      [5, 6, 23],
                      [34, 35, 23],
                      [35, 34, 23],
                      [6, 5, 23],
                      [3, 4, 34]]

        newp = p + [n]
        if len(newp) >= 3:
            newp3 = newp[-3:]
            if newp3 in sharpturns or rev(newp3) in sharpturns:
                continue

        acc = extendpath_p(p + [n], goaln, d0 + d,
                           n2, nz, acc)

    return acc

# for the selected segment, the biggest of di and dj must be minimal
def findpos(x, y, ang):
    minq = 1000
    mindidjmax = 1000
    found = None
    if x == None or y == None:
        return None

    for (i, j) in distances:
        d = distances[(i, j)]
        (xi, yi) = nodes[i]
        (xj, yj) = nodes[j]
        di = dist(xi, yi, x, y)
        dj = dist(xj, yj, x, y)
        p = (di+dj)/d
        didjmax = max(di,dj)

        a = atan2(xj-xi, yj-yi)*180/pi

        da = a-ang
        da = da%360
        if da > 180:
            da -= 360

        da1 = abs(da)
        if da1 > 180-30:
            da1 = 180-da1
        q = didjmax/0.5 + da1/30 + (di+dj)

        #print((i, j, q, di, dj, d, (a,ang%360), (xi, yi), (x, y), (xj, yj)))

        if ((found == None or minq > q) and
#            di < 1.2*d and dj < 1.2*d and
            (
                (dj*dj < di*di+d*d and di*di < dj*dj+d*d) or
                (dj < 0.5 or di < 0.5)
                ) and
            (abs(da) < 45 or abs(da) > 180-45)):
            minq = q
            found = (i, j, (i, j, di, dj, d, di+dj, di/(di+dj)))

    if not found:
        return None
    (i, j, p2) = found
    (xi, yi) = nodes[i]
    (xj, yj) = nodes[j]
    a = atan2(xj-xi, yj-yi)*180/pi

    da = a-ang
    da = da%360
    if da > 180:
        da -= 360
    if abs(da) < 45:
        return (i, j, p2)
    elif abs(da) > 180-45:
        return (j, i, p2)
    else:
        return (i, j, "unknown", da)

global distances
global neighbours
global pieces

def eightinit():
    global distances, neighbours, pieces

    eightpath(19.2,15.4,12.5)

    neighbours = dict()

    piecelist = [[6] + piece1 + [35],
                 [5] + rev(piece4) + [34],
                 piece2a + [23],
                 [23] + piece2b,
                 piece3a + [23],
                 [23] + piece3b,
                 [35, 34], # piece5
                 [5, 6], # piece6
                 [3, 4]] # piece7

    distances = dict()
    pieces = dict()

    for piece in piecelist:
        piece2pathpoints(piece, 0.35)

        dtot = 0
        lastn = None
        for n in piece:
            if lastn != None:
                if not n in neighbours:
                    neighbours[n] = []
                neighbours[n] = neighbours[n] + [lastn]
                if not lastn in neighbours:
                    neighbours[lastn] = []
                neighbours[lastn] = neighbours[lastn] + [n]
                d = dist(nodes[n][0], nodes[n][1],
                         nodes[lastn][0], nodes[lastn][1])
                distances[(n, lastn)] = d
                distances[(lastn, n)] = d
                dtot += d
            lastn = n

        pieces[(piece[0],piece[-1])] = (piece[1:-1], dtot)
        pieces[(piece[-1],piece[0])] = (rev(piece[1:-1]), dtot)

#    for (x, y) in roadpoints.keys():
#        print("%f %f" % (x, y))

# a and b are known to be in the same piece
# Return a list l of waypoints where l[0] == a and l[-1] == b
def insert_waypoints(a, b):
    if (a, b) in pieces:
        (l, _) = pieces[(a, b)]
        l = [a] + l + [b]
        return l

    for (a1, b1) in pieces:
        (l, _) = pieces[(a1, b1)]
        l = [a1] + l + [b1]
        if a not in l:
            continue
        if b not in l:
            continue
        ia = l.index(a)
        ib = l.index(b)
        if ia > ib:
            continue
        return l[ia:ib+1]

    # what should we do? throw exception?
    return None

# Apply insert_waypoints to successive pairs in l0
def insert_waypoints_l(l0):
    lastn = l0[0]
    l = [lastn]
    for n in l0[1:]:
        l1 = insert_waypoints(lastn, n)
        l += l1[1:]
        lastn = n

    return l

# We are between nodes a and b, coming from a, proportion q from a
# Return the endpoints of the piece and at what proportion from the
# starting point we are.
def findpiece(a, b, q):
    found = None
    for (a1, b1) in pieces:
        (l, _) = pieces[(a1, b1)]
        l = [a1] + l + [b1]
        if a in l and b in l:
            ia = l.index(a)
            ib = l.index(b)
            d = 0
            if ia < ib:
                lastn = l[0]
                for n in l[1:]:
                    if lastn == a:
                        d += q * distances[(lastn,n)]
                        break
                    d += distances[(lastn,n)]
                    lastn = n
                found = ((a1, b1), d)
            else:
                l = rev(l)
                lastn = l[0]
                for n in l[1:]:
                    if lastn == a:
                        d += q * distances[(lastn,n)]
                        break
                    d += distances[(lastn,n)]
                    lastn = n
                found = ((b1, a1), d)
            break
    return found

if __name__ == "__main__":
    eightinit()
