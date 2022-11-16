from array import *
from Vehicle import Vehicle
import numpy as np

board = np.full((6,6), '.')
vehicles = []

def main():
    print("MP2: Rush-Hour")
    valid = False

    while not valid:
        setup = input("Enter your game setup as a string: ")
        valid = load_game(setup)
    print("Valid board loaded")
    show_board()


def show_board():
    print('   a b c d e f')
    print("  -------------")
    count = 1
    for row in board:
        print(count, end='| ')
        count += 1
        for col in row:
            print(col, end=' ')
        print()
    print("  -------------")
    print(f"{len(vehicles)} vehicles: ", end='')
    for v in vehicles:
        print(v, end=' ')
    print()



def load_game(setup) -> bool:
    setup = setup.strip()
    if len(setup) < 36:
        print("Setup needs to be at least 36 characters")
        return False
    # load Board array
    for row in range(0, 6):
        for col in range(0, 6):
            board[row][col] = setup[row*6+col]
    # identify the vehicles
    for row in range(0,6):
        for col in range(0,6):
            letter = board[row][col]
            if letter != '.':
                vehicle = get_vehicle(letter)
                if vehicle is None:
                    v = Vehicle(letter)
                    # print(f"added {v}")
                    vehicles.append(v)
    # load gas
    if len(setup) > 36:
        for gas in setup[36:].split(' '):
            if len(gas) > 1:
                v = get_vehicle(gas[0])
                if v is None:
                    print("Gas setup referring to vehicle not previously found.")
                    return False
                print(f"Gas found for {v.letter}")
                v.gas = int(gas[1:])
    return True

def get_vehicle(letter):
    for v in vehicles:
        if v.letter == letter:
            return v
    return None


if __name__ == "__main__":
    main()
