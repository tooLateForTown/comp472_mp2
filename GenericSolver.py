from BoardQueue import BoardQueue
from datetime import datetime

class GenericSolver:

    def __init__(self, initial_board):
        self.initial_board = initial_board
        self.solved_board = None
        self.open = BoardQueue()
        self.closed = BoardQueue()
        self.solved = False
        self.finished = False
        self.solution_path = None
        self.search_path = []
        self.run_time = 0


    def generate_final_solution_string_for_output(self):
        if self.solved:
            s = f"Initial board configuration: {self.initial_board.board_config_string(include_gas=True)}\n"
            s += f"\n{self.initial_board.string_of_board()}"
            s += "Car fuel available: TO COME \n"
            s += f'\nRuntime: {"{:.2f}".format(self.run_time)} seconds'
            s += f"\nSearch path length: {len(self.search_path)} states"
            s += f"\nSolution path length: {len(self.solution_path)} states"
            s += f"\nSolution path: "
            separator = ""
            for b in self.solution_path:
                s += f"{separator}{b.move_string}"
                separator = "; "
            for b in self.solution_path:
                s += f"\n{b.string_for_solution()}"
            s += f"\n\n{self.solved_board.string_of_board()}"
        else:
            s = "no solution"
        return s