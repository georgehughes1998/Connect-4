from Board import *
from Agent import RandAgent, MinimaxAgent
import unittest


class testMinimaxAgent(unittest.TestCase):
    def setUp(self, board_size=(8, 8), agent_depth=4):
        self.board = Board(*board_size, PIECE1)
        self.agent = MinimaxAgent(self.board, depth=agent_depth)

    """
    ?
    o x
    o x
    o x
    """
    def test_vert_win(self):
        self.setUp(agent_depth=3)
        for i in range(3):
            self.board.play(0)
            self.board.play(1)

        move = self.agent.get_move()
        self.assertEqual(0, move)

    """
    x x x
    o o o ?
    """
    def test_hori_win(self):
        self.setUp(agent_depth=3)

        for i in range(3):
            self.board.play(i)
            self.board.play(i)

        move = self.agent.get_move()
        self.assertEqual(3, move)

    """
    ?
    o
    o x
    o x
    """
    def test_vert_block(self):
        self.setUp(agent_depth=3)
        for i in range(2):
            self.board.play(0)
            self.board.play(1)
        self.board.play(0)

        move = self.agent.get_move()
        self.assertEqual(0, move)

    """
    x x
    o o o ?
    """
    def test_hori_block(self):
        self.setUp(agent_depth=3)

        for i in range(2):
            self.board.play(i)
            self.board.play(i)
        self.board.play(2)
        
        move = self.agent.get_move()
        self.assertEqual(3, move)



if __name__ == "__main__":
    unittest.main()
        
