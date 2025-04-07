import arcade

x = 0


class Game(arcade.Window):
    def __init__(self, w, h, title):
        super().__init__(w, h, title)

    def draw_scene(self):
        # self.clear((50, 100, 222))
        arcade.draw_lrbt_rectangle_filled(-100, 100, -100, 100, arcade.color.YELLOW)
        arcade.draw_circle_filled(0, 0, 30, arcade.color.RED)
        arcade.draw_circle_filled(0, 0, 10, arcade.color.GRAY)
        arcade.draw_text("this is a test", 70, 70, arcade.color.ORANGE, 24)
        arcade.draw_line(-100, -100, 100, 100, arcade.color.BLUE)
        arcade.draw_line(-100, 100, 100, -100, arcade.color.BLUE)
        arcade.draw_line(x, 0, 100, 100, arcade.color.BLUE)


    def on_draw(self):
        global x

        self.clear((50, 50, 50))
        with self.cam.activate():
            print('-' * 20)
            print(self.cam.viewport)   # x,y at center
            print(self.cam.position)   # 250, 0
            print(self.cam.projection) # -300,300 -200 200 (center at 0,0)
            print(self.cam.scissor)    # None
            self.draw_scene()

        x += 0.3


if __name__ == '__main__':
    win = Game(600, 400, "test")
    # win.cam = arcade.Camera2D()  # world at bottom left of win
    win.cam = arcade.Camera2D(position=(0, 0))  # world centered in window
    # win.cam = arcade.Camera2D(position=(250, 0))
    # win.cam = arcade.Camera2D(position=(250, 0))
    win.run()
