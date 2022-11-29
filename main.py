from array import *
from Vehicle import Vehicle
import numpy as np
from BoardNode import BoardNode
from SolverUCS import SolverUCS
from SolverA import SolverA

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
        initial_board = BoardNode(initial_config)
        valid = initial_board.valid
    print("Valid board loaded")
    initial_board.show_board()

    heuristic = input("Enter your heuristic (1-3): 1: number of blocking vehicles, 2: number of blocked positions, 3: heuristic * alpha: ")
    if heuristic == "1":
        heuristic = "number_of_blocking_vehciles"
    elif heuristic == "2":
        heuristic = "number_of_blocked_positions"
    elif heuristic == "3":
        heuristic = "heuristic_multiplied"
        alpha = input("Enter your alpha: ")
    print(f"Heuristic: {heuristic}")
    #ucs = SolverUCS(initial_board)
    #ucs.run()
    a = SolverA(initial_board, heuristic, alpha if heuristic == "heuristic_multiplied" else None)
    a.run()

    # first_level_moves = initial_board.get_all_moves()
    # for m in first_level_moves:
    #     print(m)
    #     m.board.show_board()


if __name__ == "__main__":
    main()
