from Board import *
import numpy as np

class Agent:
    def __init__(self, board):
        self.board = board

    # Override this method with move selection algorithm
    def get_move(self):
        pass



class RandAgent(Agent):
    def get_move(self):
        moves = self.board.get_valid_moves()

        if len(moves) > 0:
            move = np.random.choice(moves)
        else:
            raise Exception("No moves to choose from")
        return move



class MinimaxAgent(Agent):
    def __init__(self, board, depth=2):
        self.board = board
        self.depth = depth


    def get_move(self):
        moves = self.board.get_valid_moves()
        move, _ = self._minimax(self.depth)

        return move

    def _minimax(self, depth, myturn=True, alpha=-np.inf, beta=np.inf):
        moves = self.board.get_valid_moves()

        # Positive reward on my turn
        # Negative reward on opponents turn
        sign = [-1, 1][myturn]

        # Base case / game end condition
        if depth == 0 or len(moves) == 0:
            if self.board.get_winner() == NO_PIECE:
                return None, 0
            elif self.board.get_winner() == STALEMATE:
                return None, 0
            else:
                # Higher reward for victory in less turns
                reward = depth + 1
                reward = reward * -sign
                return None, reward
        else:
            best_reward = -sign * np.inf
            best_move = None

            # For all the valid moves
            for m in range(len(moves)):
                move = moves[m]
                
                # Play the move
                self.board.play(move)

                # Calculate the reward using minimax
                _, reward = self._minimax(depth - 1, not myturn, alpha, beta)
                
                # Put the board back into original state
                self.board.undo()

                # Maximise score if this is my turn
                if myturn:
                    if reward > best_reward:
                        best_reward = reward
                        best_move = move

                        # Prune alpha
                        alpha = max(alpha, best_reward)
                        if alpha >= beta:
                            break
                # Minimise if this is opponent's turn
                else:
                    if reward < best_reward:
                        best_reward = reward
                        best_move = move

                        # Prune beta
                        beta = min(beta, best_reward)
                        if beta <= alpha:
                            break
                
            return best_move, best_reward


# Run a short test game
if __name__ == "__main__":
    board = Board(8, 8)
    agent1 = MinimaxAgent(board, 3)
    agent2 = MinimaxAgent(board, 3)
    print(board.get_board())

    playing = True
    while playing:
        turn_number = board.get_turn_number()
        print("Turn", turn_number)

        turn = board.get_turn()
        if turn == PIECE1:
            move = agent1.get_move()
        else:
            move = agent2.get_move()
        print(f"Agent {turn} Play column {move}")
        
        board.play(move)
        print(board.get_board())

        if board.get_winner() != NO_PIECE:
            print(f"Winner: {board.get_winner()}")
            playing = False
        print()
