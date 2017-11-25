"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    output = []
    for dummy_i in line[::-1]:
        if dummy_i==0:
            output.append(dummy_i)
        else:
            output.insert(0,dummy_i)
    
    for dummy_i in range(len(output) - 1):
        if output[dummy_i] == output[dummy_i+1]:
            output[dummy_i] = 2* output[dummy_i]
            output.pop(dummy_i+1)
            output.append(0)
            dummy_i+=1
        dummy_i+=1
    return output

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._height = grid_height
        self._width = grid_width
        
        self._initial_cells = {
            UP: [(0, x) for x in range(self._width)],
            DOWN: [(self._height-1, x) for x in range(self._width)],
            LEFT: [(x, 0) for x in range(self._height)],
            RIGHT: [(x, self._width-1) for x in range(self._height)],
        }
        
        self.reset()
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # create an empty grid
        self._cells = [[0 for dummy_col in range(self._width)] for dummy_row in range(self._height)]
        # add empty tiles
        self.new_tile()
        self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return str(self._cells)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        changed = False
        tiles = self._initial_cells[direction]
        
        if direction == 1 or direction == 2:
            steps = self._height
        else:
            steps = self._width
        
        for tile in tiles:
            values = []
            for step in range(steps):
                dummy_row = tile[0] + step * OFFSETS[direction][0]
                dummy_col = tile[1] + step * OFFSETS[direction][1]
                values.append(self.get_tile(dummy_row, dummy_col))
            merged_line = merge(values)
            
            for step in range(steps):
                dummy_row = tile[0] + step * OFFSETS[direction][0]
                dummy_col = tile[1] + step * OFFSETS[direction][1]
                if merged_line[step] != self.get_tile(dummy_row, dummy_col):
                    changed	= True
                self.set_tile(dummy_row, dummy_col, merged_line[step])
        
        if changed: 
            self.new_tile()
    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # find the (row, column) indices that are 0
        zeros = []
        for dummy_i, row in enumerate(self._cells):
            for dummy_j, value in enumerate(row):
                if value == 0:
                    zeros.append((dummy_i, dummy_j))
        
        # select a random element from list
        element = zeros[random.randrange(len(zeros))]
        
        # select a value
        value = [2 if random.random() < 0.9 else 4][0]
        self.set_tile(element[0], element[1], value)
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._cells[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._cells[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(3, 4))
