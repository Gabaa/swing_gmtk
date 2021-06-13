from math import sqrt
from time import time
from typing import NamedTuple

import pyglet as pg
from pyglet.graphics import Batch, OrderedGroup
from pyglet.shapes import Circle, Line, Rectangle
from pyglet.window import key
from pyglet.text import Label

import levels

Point = NamedTuple('Point', [('x', float), ('y', float)])
Vector = NamedTuple('Vector', [('x', float), ('y', float)])
Rect = NamedTuple('Rect', [('x', float), ('y', float), ('w', float), ('h', float)])


RADIUS = 10
LINE_LENGTH = 75


class State:
    """Holds all game state."""

    def __init__(self, level: levels.Level, window_width, window_height, restart) -> None:
        # Define the player thingy
        self.batch = Batch()
        self.game_group = OrderedGroup(0)
        self.mid_group = OrderedGroup(1)
        self.text_group = OrderedGroup(2)

        self.line = Line(0, 0, 0, 0, width=5, batch=self.batch, group=self.game_group)
        self.circles = [
            Circle(point[0], point[1], RADIUS, batch=self.batch, group=self.game_group) for point in level.points
        ]
        self.rectangles = [
            Rectangle(rect[0], rect[1], rect[2], rect[3], color=(255, 0, 0), batch=self.batch, group=self.game_group) for rect in level.rectangles
        ]
        self.end_rect = Rectangle(level.end_rect[0], level.end_rect[1], level.end_rect[2], level.end_rect[3], color=(0, 255, 0), batch=self.batch, group=self.game_group)

        self.velocity = Vector(0.0, 0.0)
        self.unlocked = 0

        # Define the win/lose state
        self.background = Rectangle(0, 0, window_width, window_height, batch=self.batch, group=self.mid_group)
        self.background.opacity = 0

        self.won = False
        self.won_text = pg.text.Label(
            'You won!',
            font_size=64, bold=True, color=(0, 200, 0, 255),
            x=window_width / 2, y=window_height / 2,
            anchor_x='center', anchor_y='center', group=self.text_group
        )

        self.lost = False
        self.lost_text = pg.text.Label(
            'You lost!',
            font_size=64, bold=True, color=(200, 0, 0, 255),
            x=window_width / 2, y=window_height / 2,
            anchor_x='center', anchor_y='center', group=self.text_group
        )

        # Restart function
        self.restart = restart

    def circle_rect_collision(self, c: Circle, r: Rectangle) -> bool:
        test_x = c.x
        test_y = c.y

        # Check if left or right of rect
        if c.x < r.x:
            test_x = r.x
        elif c.x > r.x + r.width:
            test_x = r.x + r.width

        # Check if above or below rect
        if c.y < r.y:
            test_y = r.y
        elif c.y > r.y + r.height:
            test_y = r.y + r.height

        dist_x = c.x - test_x
        dist_y = c.y - test_y
        dist = sqrt(dist_x ** 2 + dist_y ** 2)

        return dist <= RADIUS

    def check_for_collisions(self):
        for c in self.circles:
            # Check if colliding with end rect
            if self.circle_rect_collision(c, self.end_rect):
                self.won = True
                pg.clock.unschedule(self.update)
                pg.clock.schedule_once(self.restart, 2, True)
                self.won_text.batch = self.batch
                self.background.opacity = 64
                return True

            for r in self.rectangles:
                if self.circle_rect_collision(c, r):
                    self.lost = True
                    pg.clock.unschedule(self.update)
                    pg.clock.schedule_once(self.restart, 1, False)
                    self.lost_text.batch = self.batch
                    self.background.opacity = 64
                    return True

        return False

    def update(self, dt: float):
        if dt == 0:
            return

        if self.check_for_collisions():
            return

        moving = self.circles[self.unlocked]
        locked = self.circles[(self.unlocked + 1) % 2]

        # Add gravity to velocity
        self.velocity = Vector(self.velocity.x, self.velocity.y - 600 * dt)
        # Find next point
        moving_next = Point(moving.x + self.velocity.x * dt, moving.y + self.velocity.y * dt)
        # Move to lie on circle around stationary point
        stat_to_next_vec = Vector(moving_next.x - locked.x, moving_next.y - locked.y)
        stat_to_next_norm = sqrt(stat_to_next_vec.x ** 2 + stat_to_next_vec.y ** 2)
        moving_next_circle = Point(
            locked.x + (LINE_LENGTH * stat_to_next_vec.x / stat_to_next_norm),
            locked.y + (LINE_LENGTH * stat_to_next_vec.y / stat_to_next_norm)
        )
        # Get new velocity
        self.velocity = Vector(
            (moving_next_circle.x - moving.x) / dt,
            (moving_next_circle.y - moving.y) / dt
        )

        # Update circle position
        moving.x, moving.y = moving_next_circle

    def update_line(self):
        self.line.x = self.circles[0].x
        self.line.y = self.circles[0].y
        self.line.x2 = self.circles[1].x
        self.line.y2 = self.circles[1].y


class Window(pg.window.Window):
    state: State

    def __init__(self):
        super().__init__(caption='Swing!')
        self.all_levels = [
            levels.level1(self.width, self.height, LINE_LENGTH),
            levels.level2(self.width, self.height, LINE_LENGTH),
            levels.level3(self.width, self.height, LINE_LENGTH),
            levels.level4(self.width, self.height, LINE_LENGTH),
            levels.level5(self.width, self.height, LINE_LENGTH),
        ]
        self.current_level = 0
        self.state = None

        self.start_time = time()
        self.resets = 0

        self.congrats_label = Label(
            'Congratulations!',
            font_size=32, bold=True, color=(200, 200, 200, 255),
            x=self.width / 2, y=3 * self.height / 4,
            anchor_x='center', anchor_y='center'
        )
        self.time_label = Label(
            '',
            font_size=28, color=(200, 200, 200, 255),
            x=self.width / 2, y=2 * self.height / 4,
            anchor_x='center', anchor_y='center'
        )
        self.resets_label = Label(
            '',
            font_size=28, color=(200, 200, 200, 255),
            x=self.width / 2, y=self.height / 4,
            anchor_x='center', anchor_y='center'
        )

    def start_new(self, dt: float, next_level: bool):
        if next_level:
            self.current_level += 1
        if self.current_level >= len(self.all_levels):
            self.time_label.text = f"Time: {round(time() - self.start_time, 4)} seconds"
            self.resets_label.text = f"Resets: {self.resets}"
            return

        if self.state is not None:
            pg.clock.unschedule(self.state.update)
            pg.clock.unschedule(self.start_new)
            if not next_level:
                self.resets += 1

        level = self.all_levels[self.current_level]
        self.set_caption(f"Swing - {level.name}")
        self.state = State(level, self.width, self.height, self.start_new)
        pg.clock.schedule(self.state.update)

    def on_draw(self):
        self.state.update_line()

        # Render to the window
        self.clear()

        if self.current_level >= len(self.all_levels):
            self.congrats_label.draw()
            self.time_label.draw()
            self.resets_label.draw()
            return

        self.state.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pg.app.exit()

        if self.current_level >= len(self.all_levels):
            return

        if symbol == key.SPACE:
            self.state.unlocked = (self.state.unlocked + 1) % 2
            self.state.velocity = Vector(0.0, 0.0)
        if symbol == key.R and not (self.state.won or self.state.lost):
            pg.clock.unschedule(self.start_new)
            self.start_new(0, False)


def main():
    window = Window()
    window.start_new(0, False)
    pg.app.run()


if __name__ == '__main__':
    main()
