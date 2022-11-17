from array import *
from Vehicle import Vehicle
import numpy as np
from BoardState import BoardState

board = np.full((6, 6), '.')
vehicles = []


def main():
    print("MP2: Rush-Hour")
    valid = False
    initial_board = None

    while not valid:
        initial_config = input("Enter your game initial state, or (1-3 for samples): ")
        if initial_config == "1":
            initial_config = "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL."
        elif initial_config == "2":
            initial_config = "..I...BBI.K.GHAAKLGHDDKLG..JEEFF.J.."
        elif initial_config == "3":
            initial_config = "JBBCCCJDD..MJAAL.MFFKL.N..KGGN.HH..."
        print(f"Initial State: {initial_config}")
        initial_board = BoardState(initial_config)
        valid = initial_board.valid
    print("Valid board loaded")
    initial_board.show_board()
    print(initial_board.board_config())
    initial_board.get_all_moves()


if __name__ == "__main__":
    main()
