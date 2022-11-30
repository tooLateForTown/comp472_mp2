from BoardNode import BoardNode
from BoardQueue import BoardQueue
from datetime import datetime

from GenericSolver import GenericSolver


class SolverGBFS(GenericSolver):
    
    def run(self):

        self.open.add(self.initial_board)
        start_time = datetime.now()
        self._loop_until_end()
        self.run_time = (datetime.now() - start_time).total_seconds()
        print("--- GBFS SEARCH PATH ---")
        for b in self.search_path:
            print(b.move_string)

        print("-- GBFS FINAL SOLUTION-- ")
        print(self.generate_final_solution_string_for_output())


    def _loop_until_end(self):

        first_open = self.open.pop_first()
        
        


    def _check_heuristic_1(self):

        passed_A = False
        carList = {}
        counter = 0
        while counter < 6:
            
            if self.board[2][counter] == "A":
                passed_A = True
                counter += 1

            elif self.board[2][counter] == ".":
                counter += 1

            elif passed_A == True:
                tempCar = self.board[2][counter]
                carList.append(tempCar)
                counter += 1
        
        cost = carList.len()
        return cost

    def _check_heuristic_2(self):

        passed_A = False
        blockedCounter = 0
        counter = 0
        while counter < 6:
            
            if self.board[2][counter] == "A":
                passed_A = True
                counter += 1

            elif self.board[2][counter] == ".":
                counter += 1

            elif passed_A == True:
                blockedCounter += 1
                counter += 1
        
        cost = blockedCounter
        return cost
    
    def _check_heuristic_3(self):

        passed_A = False
        carList = {}
        constantMultiplier = 5
        counter = 0
        while counter < 6:
            
            if self.board[2][counter] == "A":
                passed_A = True
                counter += 1

            elif self.board[2][counter] == ".":
                counter += 1

            elif passed_A == True:
                tempCar = self.board[2][counter]
                carList.append(tempCar)
                counter += 1
        
        cost = constantMultiplier * carList.len()
        return cost
    
    #def _check_heuristic_4(self):
        #