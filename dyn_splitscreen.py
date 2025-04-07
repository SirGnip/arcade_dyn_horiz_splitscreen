"""
Goal: Show that I can get two separate views/cameras working providing different views into the same "world objects".
Result: Done! Might be easier with View's and Sections. (it isn't easier with View and Sections, unless I need to use an explicit camera?)
"""
import arcade

x = 0


class Game(arcade.Window):
    def __init__(self, w, h, title):
        super().__init__(w, h, title)

    def draw_scene(self, mode):
        bg = arcade.color.YELLOW if mode == 0 else arcade.color.ORANGE
        arcade.draw_lrbt_rectangle_filled(-1000, 1000, -1000, 1000, bg)
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
        with self.cam1.activate():
            self.draw_scene(0)
        with self.cam2.activate():
            self.draw_scene(1)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.close()


if __name__ == '__main__':
    win = Game(600, 400, "test")
    r1 = arcade.rect.LRBT(0, 350, 0, 250)
    win.cam1 = arcade.Camera2D(position=(290, 190), scissor=r1)  # position of camera is world-space point that is shown at center of screen
    r2 = arcade.rect.LRBT(360, 600, 0, 250)
    win.cam2 = arcade.Camera2D(position=(-200, 0), scissor=r2)  # position of camera is world-space point that is shown at center of screen
    win.run()
