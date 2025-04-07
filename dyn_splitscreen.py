"""
Goal: See if I can dynamically move a view/camera around to confirm I understand the math
Result: Yup!
"""
import arcade

x = 0


class Game(arcade.Window):
    def __init__(self, w, h, title):
        super().__init__(w, h, title)

    def draw_scene(self, mode):
        bg = arcade.color.YELLOW if mode == 0 else arcade.color.ORANGE
        arcade.draw_lrbt_rectangle_filled(-200, 200, -200, 200, bg)
        arcade.draw_circle_filled(0, 0, 30, arcade.color.RED)
        arcade.draw_circle_filled(0, 0, 10, arcade.color.GRAY)
        arcade.draw_text("this is a test", 70, 70, arcade.color.ORANGE, 24)
        arcade.draw_line(-100, -100, 100, 100, arcade.color.BLUE)
        arcade.draw_line(-100, 100, 100, -100, arcade.color.BLUE)
        arcade.draw_line(x, 0, 100, 100, arcade.color.BLUE)

    def on_draw(self):
        global x
        x += 0.3

        self.clear(arcade.color.DARK_BROWN)
        with self.cam.activate() as cam:
            self.draw_scene(0)
            print('xxxxxxx')
            print(cam.viewport)
            print(cam.position)
            print(cam.projection)
            print(cam.scissor)

    def on_key_press(self, symbol: int, modifiers: int):
        d = 20

        if symbol == arcade.key.ESCAPE:
            self.close()

        # move camera only
        elif symbol == arcade.key.W:
            self.cam.position = self.cam.position + (0, d)
        elif symbol == arcade.key.S:
            self.cam.position = self.cam.position + (0, -d)
        elif symbol == arcade.key.D:
            self.cam.position = self.cam.position + (d, 0)
        elif symbol == arcade.key.A:
            self.cam.position = self.cam.position + (-d, 0)

        # move view
        elif symbol == arcade.key.U:
            self.cam.position -= (0, d)
            self.cam.scissor = self.cam.scissor.move(0, d)
        elif symbol == arcade.key.J:
            self.cam.position -= (0, -d)
            self.cam.scissor = self.cam.scissor.move(0, -d)
        elif symbol == arcade.key.K:
            self.cam.position -= (d, 0)
            self.cam.scissor = self.cam.scissor.move(d, 0)
        elif symbol == arcade.key.H:
            self.cam.position -= (-d, 0)
            self.cam.scissor = self.cam.scissor.move(-d, 0)

if __name__ == '__main__':
    # I want to be able to set of internal offset, and then position/clip it in screenspace

    win = Game(800, 600, "test")

    win.cam = arcade.Camera2D(
        # viewport=arcade.rect.LRBT(-400, 400, -300, 300),
        projection=arcade.rect.LRBT(0, 800, 0, 600),
        position=(0, 0),
        scissor=arcade.rect.LRBT(0, 200, 0, 200)
    )
    win.run()
