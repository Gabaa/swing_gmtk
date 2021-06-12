import pyglet as pg
from pyglet.window import key


class State:
    def __init__(self, window_height) -> None:
        self.points = [
            (20, window_height - 20),
            (20, window_height - 60),
        ]
        self.locked = 0


def main():
    # Make a window
    window = pg.window.Window(caption='Swing')

    # Create game state
    state = State(window.height)

    # Create graphics
    batch = pg.graphics.Batch()
    circles = [
        pg.shapes.Circle(0, 0, 10, batch=batch),
        pg.shapes.Circle(0, 0, 10, batch=batch),
    ]
    # TODO: tilføj linje mellem punkterne

    # Add event handlers
    @window.event
    def on_draw():
        circles[0].x = state.points[0][0]
        circles[0].y = state.points[0][1]
        circles[1].x = state.points[1][0]
        circles[1].y = state.points[1][1]

        window.clear()
        batch.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.SPACE:
            state.locked = (state.locked + 1) % 2

    # Set update function
    def update(dt: float, state: dict):
        l = state.locked
        # TODO: Sæt denne til at svinge nedad
        state.points[l] = (state.points[l][0] + dt * 100, state.points[l][1])

    pg.clock.schedule(update, state)

    # Run the app
    pg.app.run()


if __name__ == '__main__':
    main()
