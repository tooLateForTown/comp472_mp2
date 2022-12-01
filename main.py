#todo add names and id's
import numpy as np
from BoardNode import BoardNode
from datetime import datetime
from Solver import Solver
from globals import HEURISTIC, ALGORITHM
import globals
import InputManager
import os
import puzzle_generator

board = np.full((6, 6), '.')
vehicles = []

# BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL.
# BBB..MCCDD.MAAKL.MJ.KLEEJ.GG..JHHHII B4 J0


# ***********************
RUN_ALL = True
LAMBDA = 5
VERBOSE = False
GENERATE_PUZZLES_FILE = True
QUANTITY_PUZZLES_TO_GENERATE = 1
# or individually if RUN_ALL = False
RUN_UCS = False
RUN_GBFS_H1 = False
RUN_GBFS_H2 = False
RUN_GBFS_H3 = False
RUN_GBFS_H4 = False
RUN_A_H1 = False
RUN_A_H2 = False
RUN_A_H3 = False
RUN_A_H4 = False
SPECIAL_RUN_LAMBDA_TEST = False
# ***********************


def main():
    print("MP2: Rush-Hour")
    if GENERATE_PUZZLES_FILE:
        puzzle_generator.generate_puzzles_file(QUANTITY_PUZZLES_TO_GENERATE)
    puzzles = InputManager.choose_input_file()
    if len(puzzles) == 0:
        print(f"No Puzzles found")
        print(f"Bye")
        exit()
    print(f"{len(puzzles)} puzzles found in file.")

    #reset content of all txt files
    directory = globals.OUTPUT_FOLDER
    # for filename in os.listdir(directory):
    #     fn = os.path.join(directory, filename)
    #     f = open(fn, "w")
    #     f.close()
    # delete contents of folder
    print(f"Deleting files in {directory}...")
    for filename in os.listdir(directory):
        file_to_delete = os.path.join(directory, filename)
        os.remove(file_to_delete)

    counter = 0
    start_time = datetime.now()
    for puzzle in puzzles:
        counter += 1
        print("\n-----------------------------------------------------------")
        print(f" Puzzle {counter} : {puzzle}")
        print("-----------------------------------------------------------")
        run_single_puzzle(puzzle, counter)
    run_time = (datetime.now() - start_time).total_seconds()
    # Save analysis CSV
    csv_file = os.path.join(globals.OUTPUT_FOLDER, "analysis.csv")
    print(f"Analysis CSV saved to {csv_file}")
    with open(csv_file, 'a') as f:
        f.write(globals.analysis_csv)

    print(f'\nTotal Runtime: {"{:.2f}".format(run_time)} seconds')
    print("\n*** The End! *** ")


def run_single_puzzle(puzzle, id):
    initial_board = BoardNode(puzzle)
    initial_board.show_board()


    if SPECIAL_RUN_LAMBDA_TEST == True:
        print(" **** RUNNING SPECIAL LAMBDA TEST!!!  *****")
        for lambda_val in range(2, 20, 2):
            print(f"Lambda={lambda_val}")
            Solver(initial_board, HEURISTIC.H3_H1_TIMES_LAMBDA, ALGORITHM.GBFS, f"{id}-{lambda_val}", VERBOSE, lambda_val).run()
            Solver(initial_board, HEURISTIC.H3_H1_TIMES_LAMBDA, ALGORITHM.A, f"{id}-{lambda_val}", VERBOSE,
                   lambda_val).run()
        return


    if RUN_UCS or RUN_ALL:
        print(f"\n**** RUNNING UCS ******")
        Solver(initial_board, HEURISTIC.H0_PURELY_COST_FOR_UCS, ALGORITHM.UCS, id, VERBOSE).run()
    if RUN_GBFS_H1 or RUN_ALL:
        print(f"\n**** RUNNING GBFS on H1 ******")
        Solver(initial_board, HEURISTIC.H1_NUMBER_BLOCKING_VEHICLES, ALGORITHM.GBFS, id, VERBOSE).run()
    if RUN_GBFS_H2 or RUN_ALL:
        print(f"\n**** RUNNING GBFS on H2 ******")
        Solver(initial_board, HEURISTIC.H2_NUMBER_BLOCKED_POSITIONS, ALGORITHM.GBFS, id, VERBOSE).run()
    if RUN_GBFS_H3 or RUN_ALL:
        print(f"\n**** RUNNING GBFS on H3 ******")
        Solver(initial_board, HEURISTIC.H3_H1_TIMES_LAMBDA, ALGORITHM.GBFS, id, VERBOSE, LAMBDA).run()
    if RUN_GBFS_H4 or RUN_ALL:
        print(f"\n**** RUNNING GBFS on H4 ******")
        Solver(initial_board, HEURISTIC.H4_CUSTOM, ALGORITHM.GBFS, id, VERBOSE).run()
    if RUN_A_H1 or RUN_ALL:
        print(f"\n**** RUNNING A/A* on H1 ******")
        Solver(initial_board, HEURISTIC.H1_NUMBER_BLOCKING_VEHICLES, ALGORITHM.A, id, VERBOSE).run()
    if RUN_A_H2 or RUN_ALL:
        print(f"\n**** RUNNING A/A* on H2 ******")
        Solver(initial_board, HEURISTIC.H2_NUMBER_BLOCKED_POSITIONS, ALGORITHM.A, id, VERBOSE).run()
    if RUN_A_H3 or RUN_ALL:
        print(f"\n**** RUNNING A/A* on H3 ******")
        Solver(initial_board, HEURISTIC.H3_H1_TIMES_LAMBDA, ALGORITHM.A, id, VERBOSE, LAMBDA).run()
    if RUN_A_H4 or RUN_ALL:
        print(f"\n**** RUNNING A/A* on H4 ******")
        Solver(initial_board, HEURISTIC.H4_CUSTOM, ALGORITHM.A, id, VERBOSE).run()

if __name__ == "__main__":
    main()
