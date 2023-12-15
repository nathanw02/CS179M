import heapq
from copy import deepcopy

def load(load_items, unload_items, manifest):
    res = []

    for r, c in unload_items:
        res.append([r, c, -1, 0])

    unloadSteps = []
    loadSteps = []
    newManifest = manifest

    if unload_items:
        unloadSteps, newManifest = unload(unload_items, manifest)
        loadSteps, newManifest = loadItems(load_items, newManifest)
    else:
        loadSteps, newManifest = loadItems(load_items, manifest)

    return (unloadSteps + loadSteps, newManifest)

def blockingAbove(r, c, manifest):
    count = 0
    for r_ in range(r):
        if manifest[r_][c][1] not in ['UNUSED', 'NAN']:
            count += 1

    return count

def blockingUnder(r, c, items):
    count = 0

    for r_ in range(r, 8):
        if (r_, c) in items:
            count += 1

    return count

def manhattan(r, c, r2, c2):
    return abs(r - r2) + abs(c - c2)

def validCells(r, c, manifest):
    valid = []

    for r2 in range(7, -1, -1):
        for c2 in range(12):
            if manifest[r2][c2][1] == 'UNUSED':
                if r2 == 7:
                    valid.append((r2, c2))
                else:
                    if manifest[r2 + 1][c2][1] != 'UNUSED' and (r2 + 1, c2) != (r, c):
                        valid.append((r2, c2))

    return valid

def findSpot(r, c, manifest, items):
    valid = validCells(r, c, manifest)

    minBlocking = float('inf')
    minDis = float('inf')
    bestMove = (0, 0)

    for r2, c2 in valid:
        if (r2, c2) == (r, c):
            continue

        under = blockingUnder(r, c, items)
        if under <= minBlocking:
            d = manhattan(r, c, r2, c2)
            if d < minDis:
                minDis = d
                minBlocking = under
                bestMove = (r2, c2)
    
    return bestMove

def printManifest(manifest):
    for row in manifest:
        r = ''
        for c in row:
            r += c[1] + ('        ')

        print(r)


def unload(items, manifest):
    items = set(items)
    blocking = {}

    for r, c in items:
        blocking[r, c] = blockingAbove(r, c, manifest)

    q = []

    for k, v in blocking.items():
        r, c = k

        heapq.heappush(q, (v, r, c,))

    steps = []

    removed = set()

    currManifest = deepcopy(manifest)

    for r in range(8):
        for c in range(12):
            currManifest[r][c].append((r, c))

    # i = 0 # use i to debug loop
    while q:
        b, r, c = heapq.heappop(q)
        if r < 0 or r == 8 or c < 0 or c == 12 or currManifest[r][c][3] in removed:
            continue
        
        b = blockingAbove(r, c, currManifest)


        # print(b, r, c, steps)

        if b == 0: # container is movable
            if (r, c) in items:
                steps.append([r, c, -1, 0])
                items.remove((r, c))
                removed.add(currManifest[r][c][3])
                currManifest[r][c] = [0, "UNUSED", manifest[r][c][2]]
                if not items:
                    return (steps, currManifest)
            else:
                under = blockingUnder(r, c, items)
                if under:
                    r2, c2 = findSpot(r, c, currManifest, items)
                    currManifest[r2][c2] = [manifest[r][c][0], manifest[r][c][1], manifest[r][c][2], currManifest[r][c][3]]
                    currManifest[r][c] = [0, "UNUSED", manifest[r][c][2]]

                    steps.append([r, c, r2, c2])

        else:
            heapq.heappush(q, (b - 1, r - 1, c))
            heapq.heappush(q, (b, r, c))

        # i += 1

        # if i == 35: 
        #     break

def findLoadSpot(manifest):
    valid = validCells(-1, 0, manifest)

    minDis = float('inf')
    bestMove = (0, 0)

    for r2, c2 in valid:
        d = manhattan(-1, 0, r2, c2)
        if d < minDis:
            minDis = d
            bestMove = (r2, c2)
    
    return bestMove

def loadItems(items, manifest):
    steps = []

    currManifest = deepcopy(manifest)

    for item in items:
        s = item.split('-')

        name = s[0]
        weight = int(s[1])

        r, c = findLoadSpot(currManifest)
        steps.append([-1, 0, r, c])

        currManifest[r][c] = [weight, name, manifest[r][c][2]]

    return steps, currManifest