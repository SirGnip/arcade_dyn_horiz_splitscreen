"""
Goal: See if I can dynamically move a view/camera around to confirm I understand the math
Result: Yes! Not too bad. Using the position of the camera is necessary to position the view on the screen. So any scrolling I'll need to take this into account.
"""
import arcade

x = 0


class Game(arcade.Window):
    def __init__(self, w, h, title):
        super().__init__(w, h, title)

    def draw_scene(self, mode):
        global x
        x += 0.3

        bg = arcade.color.YELLOW if mode == 0 else arcade.color.ORANGE
        arcade.draw_lrbt_rectangle_filled(-200, 200, -200, 200, bg)
        arcade.draw_circle_filled(0, 0, 30, arcade.color.RED)
        arcade.draw_circle_filled(0, 0, 10, arcade.color.GRAY)
        arcade.draw_text("this is a test", 70, 70, arcade.color.PINK, 24)
        arcade.draw_line(-100, -100, 100, 100, arcade.color.BLUE)
        arcade.draw_line(-100, 100, 100, -100, arcade.color.BLUE)
        arcade.draw_line(x, 0, 100, 100, arcade.color.BLUE)

    def on_draw(self):
        self.clear(arcade.color.DARK_BROWN)
        with self.cam1.activate():
            self.draw_scene(0)
        with self.cam2.activate():
            self.draw_scene(1)

    def on_key_press(self, symbol: int, modifiers: int):
        d = 20

        if symbol == arcade.key.ESCAPE:
            self.close()

        # move camera only
        elif symbol == arcade.key.W:
            self.cam1.position = self.cam1.position + (0, d)
        elif symbol == arcade.key.S:
            self.cam1.position = self.cam1.position + (0, -d)
        elif symbol == arcade.key.D:
            self.cam1.position = self.cam1.position + (d, 0)
        elif symbol == arcade.key.A:
            self.cam1.position = self.cam1.position + (-d, 0)

        # move cam1 view
        elif symbol == arcade.key.U:
            self.cam1.position -= (0, d)
            self.cam1.scissor = self.cam1.scissor.move(0, d)
        elif symbol == arcade.key.J:
            self.cam1.position -= (0, -d)
            self.cam1.scissor = self.cam1.scissor.move(0, -d)
        elif symbol == arcade.key.K:
            self.cam1.position -= (d, 0)
            self.cam1.scissor = self.cam1.scissor.move(d, 0)
        elif symbol == arcade.key.H:
            self.cam1.position -= (-d, 0)
            self.cam1.scissor = self.cam1.scissor.move(-d, 0)

        # move cam2 view
        elif symbol == arcade.key.P:
            self.cam2.position -= (0, d)
            self.cam2.scissor = self.cam2.scissor.move(0, d)
        elif symbol == arcade.key.SEMICOLON:
            self.cam2.position -= (0, -d)
            self.cam2.scissor = self.cam2.scissor.move(0, -d)
        elif symbol == arcade.key.APOSTROPHE:
            self.cam2.position -= (d, 0)
            self.cam2.scissor = self.cam2.scissor.move(d, 0)
        elif symbol == arcade.key.L:
            self.cam2.position -= (-d, 0)
            self.cam2.scissor = self.cam2.scissor.move(-d, 0)


if __name__ == '__main__':
    # I want to be able to set of internal offset, and then position/clip it in screenspace

    win = Game(800, 600, "test")

    win.cam1 = arcade.Camera2D(
        projection=arcade.rect.LRBT(0, 800, 0, 600),
        position=(0, 0),
        scissor=arcade.rect.LRBT(0, 200, 0, 200)
    )
    win.cam2 = arcade.Camera2D(
        projection=arcade.rect.LRBT(0, 800, 0, 600),
        position=(0, 0),
        scissor=arcade.rect.LRBT(0, 200, 0, 200)
    )
    win.cam2.position -= (300, 0)
    win.cam2.scissor = win.cam2.scissor.move(300, 0)
    win.run()
