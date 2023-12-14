import itertools
import heapq as hq
import copy

containers = []
containerNames = []
containerDecoys = {}
generatedStates = [] 
traverseStates = []
visitedStates = []

maxSize = 1

class Puzzle:
  def __init__(self):
    self.heavySide = -1
    self.balanceMass = -1

  def readfile(self, filename): 
    with open(filename, "r") as f:
      for line in f:
        line = line.strip()
        if line:
          parts = line.split(", ")
          row, col = map(int, parts[0].strip()[1:-1].split(","))
          row -= 1
          col -= 1
          weight = int(parts[1].strip()[1:-1])
          if parts[-1] == "NAN":
            containerDecoys[row, col] = [-1, ""]
          else:
            containerDecoys[row, col] = [weight, parts[-1]]

  def formatContainers(self):
    rows, cols = zip(*containerDecoys.keys())
    numRows, numCols = max(rows) + 1, max(cols) + 1

    for col in range(numCols):
      temp = [containerDecoys[row, col][0] for row in range(numRows)]
      names = [containerDecoys[row, col][1] for row in range(numRows)]

      containers.append(temp)
      containerNames.append(names)

  def balance(self): 
    while traverseStates:
      node = hq.heappop(traverseStates)

      hq.heappush(visitedStates, node)

      lowerWeightLimit = int(0.9 * self.balanceMass)
      upperWeightLimit = int(1.1 * self.balanceMass)

      rightWithinLimit = lowerWeightLimit < node.right < upperWeightLimit
      leftWithinLimit = lowerWeightLimit < node.left < upperWeightLimit

      if rightWithinLimit and leftWithinLimit:
        moves, names = self.printSolution(node)
        return (moves, names)

      node.astar()

  def path(self, moves, grid): # from harvard
    full_paths = []
    i = 0
    for m in moves:
      temp = []
      startCopy = m[0]
      endCopy = m[1]
      start = m[0]
      end = m[1]
      temp.append(startCopy[:])

      while start != end:
        if start[0] < end[0]:
          test = [start[0] + 1, start[1]]
          if grid[test[0]][test[1]] == 0:
            start = test
          else:
            start[1] += 1

          temp.append(start[:])
          continue

        elif start[0] > end[0]:
          test = [start[0] - 1, start[1]]
          if grid[test[0]][test[1]] == 0:
            start = test
          else:
            start[1] += 1

          temp.append(start[:])
          continue

        elif start[1] > end[1]:
          test = [start[0], start[1] - 1]
          if grid[test[0]][test[1]] == 0:
            start = test
          else:
            start[1] -= 1

          temp.append(start[:])
          continue

      full_paths.append(temp)
      t = grid[startCopy[0]][startCopy[1]]
      grid[startCopy[0]][startCopy[1]] = 0
      grid[endCopy[0]][endCopy[1]] = t

    return full_paths

  def printSolution(self, endNode): 
    nodes = []
    movesNeeded = []
    containerNames = []

    while endNode.parent:
      nodes.append(endNode)
      endNode = endNode.parent

    nodes = nodes[::-1]
    for n in nodes:
      movesNeeded.append(n.movesNeeded)
      containerNames.append(n.containerName)

    return (movesNeeded, containerNames)

class Node:

  def __init__(self, balanceMass, grid, parent,
               names):  
    self.grid = grid
    self.balanceMass = balanceMass

    self.left = 0
    self.right = 0

    self.fn = 0
    self.gn = 0
    self.hn = 0

    self.containerHeld = []
    self.containerName = ""
    self.containerNames = names

    self.movesNeeded = [[], []]
    self.allMoves = []

    self.craneLoc = [12, 0]

    self.parent = parent

  def astar(self): 
    y, x = self.craneLoc

    allMoves = []
    containersToMove = []
    for i in range(0, len(containers)):
      allMoves.append([x + i, y])

    for m in allMoves:
      containerHeld = self.pickupContainer(m, self.grid)
      if containerHeld != None:
        containersToMove.append(containerHeld)

    self.allMoves = allMoves

    for container in containersToMove:

      for move in self.allMoves:
        child = copy.deepcopy(self)

        newNode = Node(self.balanceMass, self.grid, self, child.containerNames)
        newNode.gn = self.gn + 1
        newNode.allMoves = self.availablePositions(container, self.grid)
        if container[0] != move[0]:
          updateMove, newNode.grid = newNode.dropContainer(
              move, container, child.grid)
          newNode.calcMass()

          newNode.hn = self.heuristic(newNode.grid, newNode.left,
                                      newNode.right)
          newNode.fn = newNode.gn + newNode.hn
          visitedShips = [n.grid for n in visitedStates]

          if newNode.grid not in visitedShips and newNode.grid not in generatedStates:
            m = list(container)
            newNode.movesNeeded[0] = m
            newNode.movesNeeded[1] = updateMove

            newNode.containerName = newNode.containerNames[m[0]][m[1]]
            newNode.containerNames = newNode.updateNamesOfContainers(
                m, updateMove)

            hq.heappush(traverseStates, newNode)
            generatedStates.append(newNode.grid)
            global maxSize
            maxSize = max(maxSize, len(traverseStates))

  def updateNamesOfContainers(self, start, end): 
    self.containerNames[start[0]][start[1]], self.containerNames[end[0]][
        end[1]] = (
            self.containerNames[end[0]][end[1]],
            self.containerNames[start[0]][start[1]],
        )
    return self.containerNames

  def dropContainer(self, move, containerHeld, grid): 
    row = move[0]

    locToDrop = next((i for i, val in enumerate(grid[row]) if val == 0), -1)

    if locToDrop == -1:
      return ([-1, -1], grid)

    grid[row][locToDrop] = grid[containerHeld[0]][containerHeld[1]]
    grid[containerHeld[0]][containerHeld[1]] = 0

    return ([row, locToDrop], grid)

  def pickupContainer(self, move, grid):
    row = move[0]
    col = grid[row]

    for col_index in range(len(col) - 1, -1, -1):
      if col[col_index] > 0:
        return (row, col_index)

    return None

  def availablePositions(self, container, grid):  
    availablePosition = []

    for i, col in enumerate(grid):
      if i == container[0]:
        continue

      for j, val in enumerate(col):
        if val == 0:
          availablePosition.append([i, j])
          break

    return availablePosition

  def heuristic(self, grid, left, right): 
    hn = 0
    mid = len(grid) // 2
    relocateWeights = grid[0:mid] if left > right else grid[mid:]
    deficit = self.balanceMass - min(left, right)
    relocateWeightsCopy = list(itertools.chain.from_iterable(relocateWeights))

    for w in relocateWeightsCopy:
      if w <= deficit and w > 0:
        deficit -= w
        hn += 1

    return hn

  def calcMass(self): 
    mid = len(self.grid) // 2

    for col in self.grid[0:mid]:
      self.left += sum(col)

    for col in self.grid[mid:]:
      self.right += sum(col)

  def __lt__(self, other):
    return self.fn < other.fn
  
def calculate(filename):  

  puzzle = Puzzle()
  puzzle.readfile(filename)
  puzzle.formatContainers()
  node = Node(0, containers, None, containerNames)
  node.grid = containers

  mid = len(containers) // 2

  for col in containers[0:mid]:
    node.left += sum(col)

  for col in containers[mid:]:
    node.right += sum(col)

  node.balanceMass = (node.left + node.right) // 2
  puzzle.balanceMass = node.balanceMass
  puzzle.heavySide = 0 if node.left > node.right else 1

  hq.heappush(traverseStates, node)

  moves, names = puzzle.balance()

  full_paths = puzzle.path(moves, node.grid)
  for i, f in enumerate(full_paths):

    print(f"\t{names[i]} --> {f}")

  return [full_paths, names]

calculate(r'app/tests/ShipCase4.txt')