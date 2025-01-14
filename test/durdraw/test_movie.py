import durdraw.durdraw_movie as movie

class TestSegment:

    def test_segment(self):
        frame = movie.Frame(5, 5)
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

        segment = movie.FrameSegment.from_frame(
            frame, start_x=1, start_y=1, end_x=3, end_y=4,
        )
        expected = movie.FrameSegment(
            content=[
                [' ', '*', ' '],
                [' ', '*', ' '],
                ['*', '*', ' '],
                ['*', '*', ' '],
            ],
            color_map=[
                [[0, 7], [0, 11], [0, 7]],
                [[0, 7], [0, 11], [0, 7]],
                [[1, 2], [0, 11], [0, 7]],
                [[3, 4], [0, 11], [0, 7]],
            ],
        )
        assert expected == segment

class TestFlipSegment:

    def test_flip_horizontal(self):
        'flip_horizontal flips the segment horizontally'
        segment = movie.FrameSegment(
            content=[
                [' ', '*', ' '],
                [' ', '*', ' '],
                ['*', '*', ' '],
                ['*', '*', ' '],
            ],
            color_map=[
                [[0, 7], [0, 11], [0, 7]],
                [[0, 7], [0, 11], [0, 7]],
                [[1, 2], [0, 11], [0, 7]],
                [[3, 4], [0, 11], [0, 7]],
            ]
        )
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
        segment = movie.FrameSegment(
            content=[
                [' ', '*', ' '],
                [' ', '*', ' '],
                ['*', '*', ' '],
                ['*', '*', ' '],
            ],
            color_map=[
                [[0, 7], [0, 11], [0, 7]],
                [[0, 7], [0, 11], [0, 7]],
                [[1, 2], [0, 11], [0, 7]],
                [[3, 4], [0, 11], [0, 7]],
            ],
        )
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

        segment = movie.FrameSegment(
            content=[
                [' ', '*', ' '],
                [' ', '*', ' '],
                ['*', '*', ' '],
                ['*', '*', ' '],
            ],
            color_map=[
                [[0, 7], [0, 11], [0, 7]],
                [[0, 7], [0, 11], [0, 7]],
                [[1, 2], [0, 11], [0, 7]],
                [[3, 4], [0, 11], [0, 7]],
            ]
        )
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

class TestFillSegment:

    def test_fill(self):
        'fills the segment with a specific character and color'
        segment = movie.FrameSegment(
            content=[
                [' ', '*', ' '],
                [' ', '*', ' '],
                ['*', '*', ' '],
                ['*', '*', ' '],
            ],
            color_map=[
                [[0, 7], [0, 11], [0, 7]],
                [[0, 7], [0, 11], [0, 7]],
                [[1, 2], [0, 11], [0, 7]],
                [[3, 4], [0, 11], [0, 7]],
            ]
        )
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

    def test_fill_char(self):
        'fills the segment with a specific character'
        segment = movie.FrameSegment(
            content=[
                [' ', '*', ' '],
                [' ', '*', ' '],
                ['*', '*', ' '],
                ['*', '*', ' '],
            ],
            color_map=[
                [[0, 7], [0, 11], [0, 7]],
                [[0, 7], [0, 11], [0, 7]],
                [[1, 2], [0, 11], [0, 7]],
                [[3, 4], [0, 11], [0, 7]],
            ]
        )
        filled = segment.fillChar(char='*')
        expected = movie.FrameSegment(
            content=[
                ['*', '*', '*'],
                ['*', '*', '*'],
                ['*', '*', '*'],
                ['*', '*', '*'],
            ],
            color_map=segment.color_map,
        )
        assert expected == filled

    def test_fill_color(self):
        'fills the segment with a specific color'
        segment = movie.FrameSegment(
            content=[
                [' ', '*', ' '],
                [' ', '*', ' '],
                ['*', '*', ' '],
                ['*', '*', ' '],
            ],
            color_map=[
                [[0, 7], [0, 11], [0, 7]],
                [[0, 7], [0, 11], [0, 7]],
                [[1, 2], [0, 11], [0, 7]],
                [[3, 4], [0, 11], [0, 7]],
            ]
        )
        filled = segment.fillColor(fg=11, bg=12)
        expected = movie.FrameSegment(
            content=segment.content,
            color_map=[
                [[11, 12], [11, 12], [11, 12]],
                [[11, 12], [11, 12], [11, 12]],
                [[11, 12], [11, 12], [11, 12]],
                [[11, 12], [11, 12], [11, 12]],
            ],
        )
        assert expected == filled
