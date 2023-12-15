import os
import random

def parse(manifest):
    grid = [[['0', 'NAN'] for _ in range(12)] for _ in range(8)]
    colors = [
        ['#FFCCCC', '#FFFFCC', '#CCCCFF', '#CCFFCC', '#CCCCFF', '#CC99CC', '#CC66FF', '#FFCC99', '#CCCCFF', '#FFFFCC', '#CCFFCC', '#FFCCCC'],
        ['#CCFFCC', '#FFCCCC', '#FFFFCC', '#CC99CC', '#FFCC99', '#CCCCFF', '#CCFFCC', '#FFCC99', '#FFFFCC', '#FFCCCC', '#CCFFCC', '#CCCCFF'],
        ['#CCCCFF', '#FFFFCC', '#FFCC99', '#CC66FF', '#CCFFCC', '#CC99CC', '#FFCCCC', '#CCCCFF', '#FFCC99', '#FFFFCC', '#CCFFCC', '#FFCCCC'],
        ['#FFFFCC', '#FFCC99', '#CCCCFF', '#FFCC99', '#FFFFCC', '#CC66FF', '#CC99CC', '#FFFFCC', '#FFCC99', '#CCFFCC', '#CCCCFF', '#FFCCCC'],
        ['#FFCC99', '#CCCCFF', '#CC66FF', '#FFCCCC', '#CC99CC', '#CCFFCC', '#FFCC99', '#FFCCCC', '#CCFFCC', '#FFCC99', '#CCCCFF', '#FFFFCC'],
        ['#CC99CC', '#CCFFCC', '#FFCC99', '#CCCCFF', '#FFFFCC', '#FFCCCC', '#CC66FF', '#FFCC99', '#CCCCFF', '#CCFFCC', '#FFCCCC', '#CC99CC'],
        ['#CC66FF', '#FFCC99', '#CC99CC', '#CCFFCC', '#FFCCCC', '#CCCCFF', '#FFFFCC', '#CCFFCC', '#FFCCCC', '#FFCC99', '#CCCCFF', '#FFFFCC'],
        ['#CCFFCC', '#CCCCFF', '#FFCCCC', '#FFCC99', '#CC66FF', '#FFFFCC', '#CC99CC', '#FFCC99', '#CCCCFF', '#CCFFCC', '#FFCCCC', '#FFFFCC']
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
