import durdraw.durdraw_movie as movie

class TestSegment:

    def test_flip_horizontal(self):
        'flip_horizontal flips the segment horizontally'

        frame = movie.Frame(5, 5)
        expected_content = [
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
        ]

        frame.content = [
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', '*', ' ', ' '],
            [' ', ' ', '*', ' ', ' '],
            [' ', '*', '*', ' ', ' '],
            ['*', '*', '*', ' ', ' '],
        ]
        frame.newColorMap = [
            [(0, 7), (0, 7), (0, 7), (0, 7), (0, 7)],
            [(0, 7), (0, 7), (0, 11), (0, 7), (0, 7)],
            [(0, 7), (0, 7), (0, 11), (0, 7), (0, 7)],
            [(0, 7), (1, 2), (0, 11), (0, 7), (0, 7)],
            [(1, 7), (3, 4), (0, 11), (0, 7), (0, 7)],
        ]

        start_x, start_y = 1, 1
        end_x, end_y = 3, 4

        segment = movie.FrameSegment(
            content=[row[start_x:end_x+1] for row in frame.content[start_y:end_y+1]],
            colour_map=[row[start_x:end_x+1] for row in frame.newColorMap[start_y:end_y+1]],
        )
        expected_content = [
            [' ', '*', ' '],
            [' ', '*', ' '],
            ['*', '*', ' '],
            ['*', '*', ' '],
        ]
        assert expected_content == segment.content

        flipped = segment.flip(horizontal=True)

        expected = movie.FrameSegment(
            content=[
                [' ', '*', ' '],
                [' ', '*', ' '],
                [' ', '*', '*'],
                [' ', '*', '*'],
            ],
            colour_map=[
                [(0, 7), (0, 11), (0, 7)],
                [(0, 7), (0, 11), (0, 7)],
                [(0, 7), (0, 11), (1, 2)],
                [(0, 7), (0, 11), (3, 4)],
            ],
        )
        assert expected == flipped
