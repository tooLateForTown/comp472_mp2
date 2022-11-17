from array import *
from Vehicle import Vehicle
import numpy as np

board = np.full((6, 6), '.')
vehicles = []

def main():
    print("MP2: Rush-Hour")
    valid = False

    while not valid:
        initial_state = input("Enter your game initial state, or (1-3 for samples): ")
        if initial_state == "1":
            initial_state = "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL."
        elif initial_state == "2":
            initial_state = "..I...BBI.K.GHAAKLGHDDKLG..JEEFF.J.."
        elif initial_state == "3":
            initial_state = "JBBCCCJDD..MJAAL.MFFKL.N..KGGN.HH..."
        print(f"Initial State: {initial_state}")
        valid = load_game(initial_state)
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

def letter_val(vehicle):
    return ord(vehicle.letter)

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
                    v.x = col  # top left posit
                    v.y = row
                    # determine length and direction
                    if row < 5 and board[row+1][col] == letter:
                        v.horizontal = False
                        temp_y = row
                        while temp_y <= 5 and board[temp_y][col] == letter:
                            v.length += 1
                            temp_y += 1
                    elif col < 5 and board[row][col+1] == letter:
                        v.horizontal = True
                        temp_x = col
                        while temp_x <= 5 and board[row][temp_x] == letter:
                            v.length += 1
                            temp_x += 1
                    else:
                        print("Cannot determine orientation of " + letter)
                        return False

                    vehicles.append(v)
                vehicles.sort(key=letter_val)


    # determine length orientation of each vehicle.


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
