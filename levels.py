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


def level3(window_width, window_height, line_length) -> Level:
    points = [
        (100, window_height - 20),
        (100 + line_length, window_height - 20)
    ]
    rectangles = [
        (0, 0, 50, window_height),
        (window_width - 50, 0, 50, window_height),
        (50, window_height - 200, 400, 50),
        (300, 100, 400, 50),
    ]
    end_rect = (window_width - 150, 0, 100, 100)
    return Level("Level 3", points, rectangles, end_rect)


def level4(window_width, window_height, line_length) -> Level:
    points = [
        (30, window_height - 20),
        (30 + line_length, window_height - 20)
    ]
    rectangles = [
        (0, 0, 5, window_height),
        (5, 0, window_width - 5, 5),
        (150, 135, window_width - 150, window_height - 135),
    ]
    end_rect = (window_width - 100, 5, 100, 130)
    return Level("Level 4", points, rectangles, end_rect)


def level5(window_width, window_height, line_length) -> Level:
    points = [
        (25, window_height - 20),
        (20, window_height - 20 - line_length)
    ]
    rectangles = [
        (0, 0, 100, window_height - 150),
        (100, 0, 100, window_height - 250),
        (200, window_height - 100, 100, 100),
        (200, 0, 100, window_height - 350),
        (300, window_height - 200, 100, 200),
        (300, 0, window_width - 300, window_height - 450),
        (400, window_height - 300, 100, 300),
        (500, window_height - 350, window_width - 500, 350),
    ]
    end_rect = (window_width - 100, window_height - 450, 100, 100)
    return Level("Level 5", points, rectangles, end_rect)
