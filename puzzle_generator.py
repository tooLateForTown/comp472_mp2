# generate 50 random puzzles. Each puzzles represents a parking lot. The parking lot is a 6 × 6 grid.
# Each vehicle has a size of at least 2 and can only move on the x orthe y axis, depending on its orientation.
#  where A A represents the ambulance, “.” represents an empty cell and a sequence of identical letters (eg. E E) represents a vehicle.
#  The ambulance is always horizontal and has a length of 2. The ambulance is always on row 2 of the grid.

import random
import os

def generate_random_parking_lot(grid):
    car_letters = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
    ambulance_position = random.randint(0, 4)
    # Place ambulance
    grid[2][ambulance_position] = 'A'
    grid[2][ambulance_position + 1] = 'A'
    for i in range(6):
        for j in range(6):
            if grid[i][j] == 0:
                random_token = random.randint(0, 1)
                if random_token == 0:
                    grid[i][j] = '.'
                else:
                    car_length = random.randint(2, 3)
                    car_letter = car_letters.pop()
                    car_orientation = random.randint(0, 1)
                    car_fits = True
                    if car_orientation == 0:
                        # check if the car fits in the row and if there is a car in the way
                        if j + car_length <= 6:
                            # Check if there is a car in the way
                            for k in range(car_length):
                                if grid[i][j + k] != 0:
                                    car_fits = False
                            if car_fits:
                                for k in range(car_length):
                                    grid[i][j + k] = car_letter
                            else:
                                grid[i][j] = '.'
                                car_letters.append(car_letter)
                        else:
                            grid[i][j] = '.'
                            car_letters.append(car_letter)
                    elif car_orientation == 1:
                        # check if the car fits in the column and if there is a car in the way
                        if i + car_length <= 6:
                            # Check if there is a car in the way
                            for k in range(car_length):
                                if grid[i + k][j] != 0:
                                    car_fits = False
                            if car_fits:
                                for k in range(car_length):
                                    grid[i + k][j] = car_letter
                            else:
                                grid[i][j] = '.'
                                car_letters.append(car_letter)
                        else:
                            grid[i][j] = '.'
                            car_letters.append(car_letter)
    # Convert grid to string
    puzzle_string = ''
    for i in range(6):
        for j in range(6):
            puzzle_string += grid[i][j]
    return puzzle_string

os.remove('puzzles.txt')
# Generate 50 random parking lots
for i in range(50):
    grid = [[0 for x in range(6)] for y in range(6)]
    puzzle_string = generate_random_parking_lot(grid)
    # Write puzzle to file
    with open('puzzles.txt', 'a') as f:
        f.write(puzzle_string + '\n')
