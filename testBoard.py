from Board import *
import unittest


class GameTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(8, 8, PIECE1)

    """
    o
    o x
    o x
    o x
    """
    def test_winner1_vert(self):
        for i in range(3):
            self.board.play(0)
            self.board.play(1)
        self.board.play(0)

        self.__test_winner(PIECE1)

    """
      x
    o x
    o x
    o x o
    """
    def test_winner2_vert(self):
        for i in range(3):
            self.board.play(0)
            self.board.play(1)
        self.board.play(2)
        self.board.play(1)
        
        self.__test_winner(PIECE2)

    """
    x x x
    o o o o
    """
    def test_winner1_hori(self):
        for i in range(3):
            self.board.play(i)
            self.board.play(i)
        self.board.play(3)

        self.__test_winner(PIECE1)

    """
    o
    o
    o x x x x o
    """
    def test_winner2_hori(self):
        for i in range(3):
            self.board.play(0)
            self.board.play(i+1)
        self.board.play(5)
        self.board.play(4)

        self.__test_winner(PIECE2)


    def test_stalemate(self):
        # List of moves which leads to stalemate
        moves = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 4, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 7, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7]
        for move in moves:
            self.board.play(move)
        self.assertEqual(self.board.get_valid_moves(), [])
        self.assertEqual(self.board.get_winner(), STALEMATE)


    def test_undo(self):
        self.board.play(0)
        self.board.undo()

        # Get bottom of the first column
        value = self.board.get_board()[-1, 0]
        self.assertEqual(value, NO_PIECE)

    def test_undo_win(self):
        for i in range(3):
            self.board.play(0)
            self.board.play(1)
        self.board.play(0)
        
        self.board.undo()
        self.assertGreater(len(self.board.get_valid_moves()), 0)
        self.assertEqual(self.board.get_winner(), NO_PIECE)

    def test_undo_stalemate(self):
        moves = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 4, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 7, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7]
        for move in moves:
            self.board.play(move)
            
        self.board.undo()
        self.assertGreater(len(self.board.get_valid_moves()), 0)
        self.assertEqual(self.board.get_winner(), NO_PIECE)
        
    
    # Generic test for a winner
    def __test_winner(self, piece):
        self.assertEqual(self.board.get_valid_moves(), [])
        self.assertEqual(self.board.get_winner(), piece)



if __name__ == '__main__':
    unittest.main()
