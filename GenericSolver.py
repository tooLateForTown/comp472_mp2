from BoardQueue import BoardQueue
from datetime import datetime

class GenericSolver:

    def __init__(self, initial_board, heuristic, lambda_val=5):
        self.initial_board = initial_board
        self.solved_board = None
        self.open = BoardQueue()
        self.closed = BoardQueue()
        self.solved = False
        self.finished = False
        self.solution_path = None
        self.search_path = []
        self.run_time = 0
        self.heuristic = heuristic
        self.lambda_val = 5



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


    def _add_children_to_open(self, board, heuristic):
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
            duplicate_in_closed = self.closed.get_board(c.config_string)  # todo decide if we also care about cost when doing this
            if duplicate_in_closed is not None:
                add_to_open = False
            if add_to_open:
                self.open.add(c)
        self.open.sort_by_heuristic(heuristic)