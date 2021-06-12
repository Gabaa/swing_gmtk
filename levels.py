class Level:
    """Represents a level in the game."""

    def __init__(self, name, points, rectangles, end_rect):
        self.name = name
        self.points = points
        self.rectangles = rectangles
        self.end_rect = end_rect


def level1(window_width, window_height, line_length) -> Level:
    points = [
        (25, window_height - 20),
        (20, window_height - 20 - line_length)
    ]
    rectangles = [
        (200, window_height - 300, 100, 100)
    ]
    end_rect = (window_width - 100, 0, 100, 100)
    return Level("Level 1", points, rectangles, end_rect)


def level2(window_width, window_height, line_length) -> Level:
    points = [
        (25, window_height - 20),
        (20, window_height - 20 - line_length)
    ]
    rectangles = [
        (window_width - 500, window_height - 100, 200, 100),
        (window_width - 300, window_height - 150, 200, 150),
        (window_width - 100, window_height - 200, 100, 200),
        (0, 0, window_width, window_height - 300),
    ]
    end_rect = (window_width - 100, window_height - 300, 100, 100)
    return Level("Level 2", points, rectangles, end_rect)
