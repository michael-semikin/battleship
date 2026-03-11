from src.models.board import Board, Point


class TestBoard:
    def test_get_neighbors_center_point(self):
        # arrange
        point = Point(5, 5)
        
        expected = {
            Point(4, 5),
            Point(6, 5),
            Point(5, 4),
            Point(5, 6)
        }

        # act
        neighbors = Board.get_neighbors(point)

        # assert
        assert(len(neighbors) == 4)
        assert(neighbors == expected)

    def test_get_surroundings_center_point(self):
        # arrange
        point = Point(5, 5)
        
        expected = {
            Point(4, 4),
            Point(4, 6),
            Point(6, 4),
            Point(6, 6),
            Point(4, 5),
            Point(6, 5),
            Point(5, 4),
            Point(5, 6)            
        }

        # act
        neighbors = Board.get_surroundings(point)

        # assert
        assert(len(neighbors) == 8)
        assert(neighbors == expected)