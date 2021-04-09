import numpy as np
from scipy.ndimage import convolve

# Board Constants
DEFAULT_BOARD_WIDTH, DEFAULT_BOARD_HEIGHT = 8, 8

NO_PIECE = 0
PIECE1 = 1
PIECE2 = 2
STALEMATE = -1

CHANGE_TURN = {PIECE1: PIECE2, PIECE2: PIECE1}

NUM_IN_A_ROW = 4


class Board:
    def __init__(self, width=DEFAULT_BOARD_WIDTH, height=DEFAULT_BOARD_HEIGHT, starting_player=PIECE1):
        # Create an empty board
        self._board = np.full((height, width), NO_PIECE).astype(np.uint8)
        self._turn_count = 0
        self._turn = starting_player
        self._winner = NO_PIECE
        self._width, self._height = width, height
        self._move_stack = []


    def play(self, column):
        # Play if no one has won yet
        if self._winner == NO_PIECE:
            # Validate column
            if not np.isscalar(column):
                raise TypeError("column must be of type int.")
            
            # Get a view into selected column
            col = self._board[:, column]

            # Check if there's room in this column for another counter
            if not 0 in col:
                # Todo: Add custom error
                raise Warning("No more room in this column.")

            # Find the last row that doesn't have a counter and play
            # (acts like gravity)
            row = np.max(np.where(col == 0))
            self._board[row, column] = self._turn

            # Add the move to the move stack
            self._move_stack.append((row, column))

            # Check if there's a winner
            self._winner = self._check_end_condition()
            
            # Deal with turns
            self._turn_count += 1
            if self._winner == NO_PIECE:
                self._turn = CHANGE_TURN[self._turn]
            else:
                self._turn = NO_PIECE
        else:
            # Todo: Add custom error
            raise Warning("The game has finished.")


    def undo(self):
        row, column = self._move_stack.pop()
        last_turn = self._board[row, column]
        self._board[row, column] = NO_PIECE
        
        # Remove the winner
        if self._winner != NO_PIECE:
            self._winner = NO_PIECE
            self._winner = self._check_end_condition()
            
        # Deal with turns
        self._turn_count -= 1
        self._turn = last_turn
    

    def get_valid_moves(self):
        moves = np.array([])
        if self._winner == NO_PIECE:
            moves_mask = np.any(self._board == 0, axis=0)
            moves = np.arange(self._width)[moves_mask]
        moves = [int(a) for a in moves]
        return moves


    def get_board(self):
        return self._board


    def get_board_hash(self):
        return hash(str(self._board))


    def get_turn(self):
        return self._turn


    def get_turn_number(self):
        return self._turn_count


    def get_winner(self):
        return self._winner

    
    def _check_end_condition(self):
        # Default no winner
        winner = NO_PIECE

        # Check both colours
        # Consider only this piece
        mask = (self._board == self.get_turn()).astype(np.int8)

        # Set up kernels to count the number of counters
        # in each direction
        kernel_horizontal = np.ones(shape=(1, NUM_IN_A_ROW))
        kernel_vertical = np.ones(shape=(NUM_IN_A_ROW, 1))
        kernel_diag1 = np.eye(NUM_IN_A_ROW)
        kernel_diag2 = np.rot90(kernel_diag1)

        # Convolve the masked board with each kernel
        kernels = [kernel_horizontal, kernel_vertical, kernel_diag1, kernel_diag2]
        counts = [convolve(mask, kernel, mode='constant', cval=0.0) for kernel in kernels]

        # Where the convolved board is equal to the winning number
        # this means that a row of winning counters was found
        res = np.any(np.array(counts) >= NUM_IN_A_ROW)

        # Todo: Identify the winning position(s)

        if res:
            winner = self.get_turn()

        # The result is stalemate if there are no moves
        if winner == NO_PIECE and len(self.get_valid_moves()) == 0:
            winner = STALEMATE
        
        return winner
        




if __name__ == "__main__":
    # Test
    board = Board()
    print(board.get_board())
    print()

    [board.play(0) for i in range(8)]
    [board.play(1) for i in range(8)]
    [board.play(2) for i in range(8)]

    print(board.get_board())
    print(board.get_valid_moves())
    
    [board.play(3) for i in range(1)]

    print(board.get_board())
    print(board.get_valid_moves())


    
    [board.undo() for i in range(7)]

    print(board.get_board())
    print(board.get_valid_moves())    
    
##    for i in range(1000):
##        move = int(np.random.uniform(0, DEFAULT_BOARD_WIDTH))
##        res = board.play(move)
##        print(f"Turn {board.get_turn_number()}")
##        print(board.get_board())
##        if res == PIECE1:
##            print("Blue victory")
##            break
##        print()


