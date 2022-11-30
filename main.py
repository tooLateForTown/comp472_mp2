from array import *
from Vehicle import Vehicle
import numpy as np
from BoardNode import BoardNode
# from SolverUCS import SolverUCS
# from SolverGBFS import SolverGBFS
# from SolverA import SolverA
from Solver import Solver
from globals import HEURISTIC, ALGORITHM

board = np.full((6, 6), '.')
vehicles = []

# BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL.
# BBB..MCCDD.MAAKL.MJ.KLEEJ.GG..JHHHII B4 J0


# ***********************
RUN_ALL = False
LAMBDA = 5
VERBOSE = True
# or individually if RUN_ALL = False
RUN_UCS = False
RUN_GBFS_H1 = False
RUN_GBFS_H2 = False
RUN_GBFS_H3 = False
RUN_GBFS_H4 = False
RUN_A_H1 = False
RUN_A_H2 = True
RUN_A_H3 = False
RUN_A_H4 = True
# ***********************


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

    if RUN_UCS or RUN_ALL:
        print(f"\n**** RUNNING UCS ******")
        Solver(initial_board, HEURISTIC.H0_PURELY_COST_FOR_UCS, ALGORITHM.UCS, VERBOSE).run()
    if RUN_GBFS_H1 or RUN_ALL:
        print(f"\n**** RUNNING GBFS on H1 ******")
        Solver(initial_board, HEURISTIC.H1_NUMBER_BLOCKING_VEHICLES, ALGORITHM.GBFS, VERBOSE).run()
    if RUN_GBFS_H2 or RUN_ALL:
        print(f"\n**** RUNNING GBFS on H2 ******")
        Solver(initial_board, HEURISTIC.H2_NUMBER_BLOCKED_POSITIONS, ALGORITHM.GBFS, VERBOSE).run()
    if RUN_GBFS_H3 or RUN_ALL:
        print(f"\n**** RUNNING GBFS on H3 ******")
        Solver(initial_board, HEURISTIC.H3_H1_TIMES_LAMBDA, ALGORITHM.GBFS, VERBOSE, LAMBDA).run()
    if RUN_GBFS_H4 or RUN_ALL:
        print(f"\n**** RUNNING GBFS on H4 ******")
        Solver(initial_board, HEURISTIC.H4_CUSTOM, ALGORITHM.GBFS, VERBOSE).run()
    if RUN_A_H1 or RUN_ALL:
        print(f"\n**** RUNNING A/A* on H1 ******")
        Solver(initial_board, HEURISTIC.H1_NUMBER_BLOCKING_VEHICLES, ALGORITHM.A, VERBOSE).run()
    if RUN_A_H2 or RUN_ALL:
        print(f"\n**** RUNNING A/A* on H2 ******")
        Solver(initial_board, HEURISTIC.H2_NUMBER_BLOCKED_POSITIONS, ALGORITHM.A, VERBOSE).run()
    if RUN_A_H3 or RUN_ALL:
        print(f"\n**** RUNNING A/A* on H3 ******")
        Solver(initial_board, HEURISTIC.H3_H1_TIMES_LAMBDA, ALGORITHM.A,VERBOSE, LAMBDA).run()
    if RUN_A_H4 or RUN_ALL:
        print(f"\n**** RUNNING A/A* on H4 ******")
        Solver(initial_board, HEURISTIC.H4_CUSTOM, ALGORITHM.A, VERBOSE).run()


if __name__ == "__main__":
    main()
