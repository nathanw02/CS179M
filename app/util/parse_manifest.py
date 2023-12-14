import os
import random

def parse(manifest):
    grid = [[['0', 'NAN'] for _ in range(12)] for _ in range(8)]
    colors = [
        ['#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#800080', '#4B0082', '#EE82EE', '#FFA500', '#FFFF00', '#008000', '#0000FF'],
        ['#800080', '#4B0082', '#EE82EE', '#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#800080', '#4B0082', '#EE82EE', '#FF0000'],
        ['#FFA500', '#FFFF00', '#008000', '#0000FF', '#800080', '#4B0082', '#EE82EE', '#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF'],
        ['#800080', '#4B0082', '#EE82EE', '#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#800080', '#4B0082', '#EE82EE', '#FF0000'],
        ['#FFA500', '#FFFF00', '#008000', '#0000FF', '#800080', '#4B0082', '#EE82EE', '#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF'],
        ['#800080', '#4B0082', '#EE82EE', '#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#800080', '#4B0082', '#EE82EE', '#FF0000'],
        ['#FFA500', '#FFFF00', '#008000', '#0000FF', '#800080', '#4B0082', '#EE82EE', '#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF'],
        ['#800080', '#4B0082', '#EE82EE', '#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#800080', '#4B0082', '#EE82EE', '#FF0000'],
    ]

    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', manifest)), 'r') as file:
        for line in file:
            coord, weight, name = line.split(', ')

            coord = coord[1:-1].split(',')
            weight = weight[1:-1]
            name = name.strip()
            if name == 'NAN':
                weight = -1
            row, col = 8 - int(coord[0]), int(coord[1]) - 1

            grid[row][col] = [int(weight), name, colors[row][col]]

    return grid
