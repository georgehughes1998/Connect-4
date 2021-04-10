from Board import *
from Agent import Agent, RandAgent, MinimaxAgent
import numpy as np
import json


class QLearner:
    def __init__(self,
                 board_width = 8,
                 board_height = 8,
                 training_rounds = 10,
                 default_agent = MinimaxAgent,
                 default_reward = 0.0,
                 discount_factor = 0.8,
                 learning_rate = 0.7):
        self.default_reward = default_reward
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate

        self.board_width = board_width
        self.board_height = board_height

        self.default_agent = default_agent

        self.Q = dict()
        self.train(training_rounds)

    def train(self, rounds=10):
        # Play some random games for training
        for game in range(rounds):
            board = Board(self.board_width, self.board_height)
            agent = QAgent(board, self, exploration=0.8)

            # Most games won't have more than 100 turns
            for m in range(100):
                moves = board.get_valid_moves()

                if len(moves) > 0:
                    move = agent.get_move()
                    board.play(move)


    def update_Q(self, board, move):
        state = self.get_board_hash(board)

        old_value = self.default_reward
        if state in self.Q:
            moves = self.Q[state]
            if move in moves:
                old_value = self.Q[state][move]
        else:
            self.Q[state] = dict()
        
        reward = self._calculate_reward(board, move)
        max_q = self._calculate_max_q(board)

        new_value = old_value + self.learning_rate * \
                    (reward + (self.discount_factor * \
                     max_q) - old_value)

        self.Q[state][move] = new_value

##        print("self.Q[state]", self.Q[state])
##        print("Old value", old_value)
##        print("Reward", reward)
##        print("Max Q", max_q)
##        print("New value", new_value)
##        print()


    def get_board_hash(self, board):
        piece = board.get_turn()
        b = board.get_board()
        no_pieces = b == NO_PIECE
        my_pieces = b == piece
        hash_board = no_pieces + my_pieces*2

        hash_tuple = tuple([tuple(c) for c in hash_board])

        hash_value = hash(hash_tuple)
        return hash_value


    def save(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.Q, file)


    def load(self, filename):
        with open(filename, 'r') as file:
            d = json.load(file)
        self.Q = {int(s): {int(m): d[s][m] for m in d[s]} for s in d}

    def _calculate_reward(self, board, move):
        piece = board.get_turn()
        board.play(move)

        if board.get_winner() == piece:
            reward = 10.0
        elif board.get_winner() == STALEMATE:
            reward = -1
        elif board.get_winner() == NO_PIECE:
            # If there was no winner, set the score to be negative the
            # best score achievable by the opponent
            moves = board.get_valid_moves()
            rewards = [0 for m in moves]
            for m in range(len(moves)):
                move = moves[m]
                
                board.play(move)
                winner = board.get_winner()
                board.undo()

                # If the opponent would win
                if winner == board.get_turn():
                    rewards[m] = -100.0
                else:
                    rewards[m] = -1.0
            reward = min(rewards)
                
        board.undo()

        return reward


    def _calculate_max_q(self, board):
        state = self.get_board_hash(board)
        moves = board.get_valid_moves()

        best_reward = -1000
        for move in moves:
            if state in self.Q:
                if move in self.Q[state]:
                    reward = self.Q[state][move]
                    best_reward = max(reward, best_reward)
        if best_reward == -1000:
            best_reward = self.default_reward
        return best_reward



class QAgent(Agent):
    def __init__(self, board, qlearner, exploration=0):
        super().__init__(board)
        self.qlearner = qlearner
        self.exploration = exploration


    def get_move(self, dolearning=True):
        state = self.qlearner.get_board_hash(self.board)

        do_random = False
        do_default = False

        if np.random.uniform(0, 1) >= self.exploration:
            if state in self.qlearner.Q:
                move_reward_dict = self.qlearner.Q[state]

                if len(move_reward_dict) > 0:
                    moves = list(move_reward_dict.keys())
                    rewards = list(move_reward_dict.values())

                    best_ix = np.argmax(rewards)
                    move = moves[best_ix]
                else:
                    do_default = True
            else:
                do_default = True
        else:
            do_random = True

        if do_random:
            moves = self.board.get_valid_moves()
            move = int(np.random.choice(moves))
        elif do_default == True:
            move = int(self.qlearner.default_agent(self.board).get_move())

        # Learn from the move
        if dolearning:
            self.qlearner.update_Q(self.board, move)

        return move


if __name__ == "__main__":
    w, h = 6, 6
    
    qlearner = QLearner(board_width=w, board_height=h, training_rounds=0)

    try:
        qlearner.load("dict.json")
    except:
        pass

    qlearner.train(rounds=100)
    print(len(qlearner.Q))
    print(len(str(qlearner.Q)))

    board = Board(w, h)
    agent1 = QAgent(board, qlearner)
    agent2 = MinimaxAgent(board, depth=5)
    for m in range(1000):
        moves = board.get_valid_moves()

        if len(moves) > 0:
            print(f"Turn {board.get_turn_number()}")

            if m % 2 == 0:
                agent = agent1
            else:
                agent = agent2
            move = agent.get_move()
            print(f"Playing move {move}")

            board.play(move)
            print(board.get_board())
            print()
        else:
            print(f"Winner: {board.get_winner()}")
            break

    print(len(qlearner.Q))
    print(len(str(qlearner.Q)))

    qlearner.save("dict.json")
