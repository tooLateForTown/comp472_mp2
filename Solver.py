from BoardNode import BoardNode
from BoardQueue import BoardQueue
from datetime import datetime
from globals import ALGORITHM, HEURISTIC
import globals

class Solver:

    def __init__(self, initial_board, heuristic, algorithm, puzzle_id, verbose=False, lambda_val=5):
        self.initial_board = initial_board
        self.solved_board = None
        self.open = BoardQueue()
        self.closed = BoardQueue()
        self.solved = False
        self.finished = False
        self.solution_path = []
        self.search_path = []
        self.run_time = 0
        self.heuristic = heuristic
        self.lambda_val = 5
        self.algorithm = algorithm
        self.verbose = verbose
        self.puzzle_id = puzzle_id

    def run(self):
        self.open.add(self.initial_board)
        start_time = datetime.now()
        self._loop_until_end()
        self.run_time = (datetime.now() - start_time).total_seconds()
        # Generate output files and optionally print to screen
        solution_text = self.generate_final_solution_string_for_output()
        if self.verbose:
            print("--- SEARCH PATH ---")
        for b in self.search_path:
            if self.verbose:
                print(b.string_for_searchpath())
            if b.move_string != "Start":
                self.add_to_search_file(b.string_for_searchpath())
        if self.verbose:
            print("-- FINAL SOLUTION-- ")
            print(solution_text)

        # output result to screen
        print(f"solution_steps={len(self.solution_path)}, search_path={len(self.search_path)}, time={'{:.2f}'.format(self.run_time)} secs")

    def _loop_until_end(self):
        while not self.finished:
            if self.open.is_empty():
                print("Open is empty. No solution found")
                self.finished = True
            else:
                first_open = self.open.pop_first()
                self.search_path.append(first_open)
                success = self._evaluate_board(first_open)
                if success:
                    self.solution_path = BoardNode.path_to_parent(first_open)
                    self.solved_board = first_open
                if not success:
                    self._add_children_to_open(first_open)

    def _evaluate_board(self, board):
        if board.is_goal():
            self.solved = True
            self.finished = True
            # print("Board solved!")
            return True
        else:
            # remove from open list and add to closed
            self.open.remove_board(board)
            self.closed.add(board)
            return False

    def generate_final_solution_string_for_output(self):
        if self.solved:
            s = f"Initial board configuration: {self.initial_board.board_config_string(include_gas=True)}\n"
            s += f"\n{self.initial_board.string_of_board()}"
            s += f"\nCar fuel available: {self.initial_board.car_fuel_for_output()} \n"
            s += f'\nRuntime: {"{:.2f}".format(self.run_time)} seconds'
            s += f"\nSearch path length: {len(self.search_path)} states"
            s += f"\nSolution path length: {len(self.solution_path)} moves"
            s += f"\nSolution path: "
            separator = ""
            for b in self.solution_path:
                s += f"{separator}{b.move_string}"
                separator = "; "
            s += "\n"
            for b in self.solution_path:
                s += f"\n{b.string_for_solution()}"
            s += f"\n\n{self.solved_board.string_of_board()}"
        else:
            s = "no solution"
        
        #output to file
        self.add_to_solution_file(s)
        # Build csv
        self.append_results_to_analysis_csv()
        
        return s

    def _add_children_to_open(self, board):
        # add successor children on board to open
        children = board.get_successor_boards()
        for c in children:
            add_to_open = True
            # print(f"{c.move_string} : {c.config_string}")
            duplicate_in_open = self.open.get_board(c.config_string)
            # UCS specific check
            if duplicate_in_open is not None:
                if duplicate_in_open.cost <= c.cost:
                    add_to_open = False
                else:
                    self.open.remove_board(duplicate_in_open)
            duplicate_in_closed = self.closed.get_board(
                c.config_string)  # todo decide if we also care about cost when doing this
            if duplicate_in_closed is not None:
                add_to_open = False
            if add_to_open:
                if self.heuristic == HEURISTIC.H0_PURELY_COST_FOR_UCS:
                    c.h = 0
                elif self.heuristic == HEURISTIC.H1_NUMBER_BLOCKING_VEHICLES or self.heuristic == HEURISTIC.H3_H1_TIMES_LAMBDA:
                    c.h = c.number_of_blocking_vehicles()
                elif self.heuristic == HEURISTIC.H2_NUMBER_BLOCKED_POSITIONS:
                    c.h = c.number_of_blocked_positions()
                elif self.heuristic == HEURISTIC.H4_CUSTOM:
                    # c.h = c.manhattan_distance()
                    c.h = c.number_of_blocked_positions_in_area_to_right_of_ambulance_edge()

                self.open.add(c)
        self.open.sort_by_heuristic(self.heuristic, self.algorithm, self.lambda_val)

    def add_to_solution_file(self, s):
        # puzzleCounter = 1 #temp variable to make it run, needs to increment

        if self.algorithm.name.lower() == "ucs":

            f = open(f'{globals.OUTPUT_FOLDER}/' + self.algorithm.name.lower() + "-sol-" + str(self.puzzle_id) + ".txt", "a")
            f.write(s + "\n")
            f.close()
        else:
            f = open(f'{globals.OUTPUT_FOLDER}/' + self.algorithm.name.lower() + "-" + self.heuristic.name[0:2].lower() + "-sol-" + str(self.puzzle_id) + ".txt", "a")
            f.write(s + "\n")
            f.close()

    def add_to_search_file(self, b):

        # puzzleCounter = 1 #temp variable to make it run, needs to increment
        if self.algorithm.name.lower() == "ucs":
            f = open(f'{globals.OUTPUT_FOLDER}/' + self.algorithm.name.lower() + "-search-" + str(self.puzzle_id) + ".txt", "a")
            f.write(b + "\n")
            f.close()
        else:
            f = open(f'{globals.OUTPUT_FOLDER}/' + self.algorithm.name.lower() + "-" + self.heuristic.name[0:2].lower() + "-search-" + str(self.puzzle_id) + ".txt", "a")
            f.write(b + "\n")
            f.close()

    def append_results_to_analysis_csv(self):
        if self.algorithm == ALGORITHM.UCS:
            algo = "UCS"
        elif self.algorithm == ALGORITHM.GBFS:
            algo = "GBFS"
        elif self.algorithm == ALGORITHM.A:
            algo = "A/A*"
        if self.heuristic == HEURISTIC.H0_PURELY_COST_FOR_UCS:
            heu = "NA"
        elif self.heuristic == HEURISTIC.H1_NUMBER_BLOCKING_VEHICLES:
            heu = "h1"
        elif self.heuristic == HEURISTIC.H2_NUMBER_BLOCKED_POSITIONS:
            heu = "h2"
        elif self.heuristic == HEURISTIC.H3_H1_TIMES_LAMBDA:
            heu = "h3"
        elif self.heuristic == HEURISTIC.H4_CUSTOM:
            heu = "h4"

        if globals.analysis_csv == "":
            globals.analysis_csv += "Number, Algorithm, Heuristic, Solution Length, Search Length, Execution Time"
        globals.analysis_csv += "\n"
        globals.analysis_csv += f"{self.puzzle_id},{algo},{heu},{len(self.solution_path)}, {len(self.search_path)}, {self.run_time:.2f}"



