import durdraw.durdraw_movie as movie

class TestSegment:

    def test_segment(self):
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
            [[0, 7], [0, 7], [0, 7],  [0, 7], [0, 7]],
            [[0, 7], [0, 7], [0, 11], [0, 7], [0, 7]],
            [[0, 7], [0, 7], [0, 11], [0, 7], [0, 7]],
            [[0, 7], [1, 2], [0, 11], [0, 7], [0, 7]],
            [[1, 7], [3, 4], [0, 11], [0, 7], [0, 7]],
        ]

        start_x, start_y = 1, 1
        end_x, end_y = 3, 4

        segment = movie.FrameSegment(
            content=[row[start_x:end_x+1] for row in frame.content[start_y:end_y+1]],
            color_map=[row[start_x:end_x+1] for row in frame.newColorMap[start_y:end_y+1]],
        )
        expected_content = [
            [' ', '*', ' '],
            [' ', '*', ' '],
            ['*', '*', ' '],
            ['*', '*', ' '],
        ]
        assert expected_content == segment.content
         

    def test_flip_horizontal(self):
        'flip_horizontal flips the segment horizontally'
        content = [
            [' ', '*', ' '],
            [' ', '*', ' '],
            ['*', '*', ' '],
            ['*', '*', ' '],
        ]
        color_map = [
            [[0, 7], [0, 11], [0, 7]],
            [[0, 7], [0, 11], [0, 7]],
            [[1, 2], [0, 11], [0, 7]],
            [[3, 4], [0, 11], [0, 7]],
        ]

        segment = movie.FrameSegment(content=content, color_map=color_map)
        flipped = segment.flip(horizontal=True)

        expected = movie.FrameSegment(
            content=[
                [' ', '*', ' '],
                [' ', '*', ' '],
                [' ', '*', '*'],
                [' ', '*', '*'],
            ],
            color_map=[
                [[0, 7], [0, 11], [0, 7]],
                [[0, 7], [0, 11], [0, 7]],
                [[0, 7], [0, 11], [1, 2]],
                [[0, 7], [0, 11], [3, 4]],
            ],
        )
        assert expected == flipped

    def test_flip_vertical(self):
        'flip_vertical flips the segment vertically'
        content = [
            [' ', '*', ' '],
            [' ', '*', ' '],
            ['*', '*', ' '],
            ['*', '*', ' '],
        ]
        color_map = [
            [[0, 7], [0, 11], [0, 7]],
            [[0, 7], [0, 11], [0, 7]],
            [[1, 2], [0, 11], [0, 7]],
            [[3, 4], [0, 11], [0, 7]],
        ]

        segment = movie.FrameSegment(content=content, color_map=color_map)
        flipped = segment.flip(vertical=True)

        expected = movie.FrameSegment(
            content=[
                ['*', '*', ' '],
                ['*', '*', ' '],
                [' ', '*', ' '],
                [' ', '*', ' '],
            ],
            color_map=[
                [[3, 4], [0, 11], [0, 7]],
                [[1, 2], [0, 11], [0, 7]],
                [[0, 7], [0, 11], [0, 7]],
                [[0, 7], [0, 11], [0, 7]],
            ],
        )
        assert expected == flipped

    def test_flip_both(self):
        'flip_both flips the segment both horizontally and vertically'
        content = [
            [' ', '*', ' '],
            [' ', '*', ' '],
            ['*', '*', ' '],
            ['*', '*', ' '],
        ]
        color_map = [
            [[0, 7], [0, 11], [0, 7]],
            [[0, 7], [0, 11], [0, 7]],
            [[1, 2], [0, 11], [0, 7]],
            [[3, 4], [0, 11], [0, 7]],
        ]

        segment = movie.FrameSegment(content=content, color_map=color_map)
        flipped = segment.flip(horizontal=True, vertical=True)

        expected = movie.FrameSegment(
            content=[
                [' ', '*', '*'],
                [' ', '*', '*'],
                [' ', '*', ' '],
                [' ', '*', ' '],
            ],
            color_map=[
                [[0, 7], [0, 11], [3, 4]],
                [[0, 7], [0, 11], [1, 2]],
                [[0, 7], [0, 11], [0, 7]],
                [[0, 7], [0, 11], [0, 7]],
            ],
        )
        assert expected == flipped

    def test_fill(self):
        'fill fills the segment with a character'
        content = [
            [' ', '*', ' '],
            [' ', '*', ' '],
            ['*', '*', ' '],
            ['*', '*', ' '],
        ]
        color_map = [
            [[0, 7], [0, 11], [0, 7]],
            [[0, 7], [0, 11], [0, 7]],
            [[1, 2], [0, 11], [0, 7]],
            [[3, 4], [0, 11], [0, 7]],
        ]

        segment = movie.FrameSegment(content=content, color_map=color_map)
        filled = segment.fill(char='*', fg=0, bg=7)

        expected = movie.FrameSegment(
            content=[
                ['*', '*', '*'],
                ['*', '*', '*'],
                ['*', '*', '*'],
                ['*', '*', '*'],
            ],
            color_map=[
                [[0, 7], [0, 7], [0, 7]],
                [[0, 7], [0, 7], [0, 7]],
                [[0, 7], [0, 7], [0, 7]],
                [[0, 7], [0, 7], [0, 7]],
            ],
        )
        assert expected == filled