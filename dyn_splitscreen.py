"""
Goal: Get basic scrolling working
- x have one camera,  a sub-camera (set camera explicitly
- x draw numbers in global
- x have actor that can move
- x scroll view with actor
"""
import arcade


class Game(arcade.Window):
    def __init__(self, w, h, title):
        super().__init__(w, h, title)
        self.sprites = arcade.SpriteList()
        self.actor = arcade.Sprite(":resources:/images/space_shooter/playerShip1_blue.png")
        self.sprites.append(self.actor)

    def draw_scene(self, mode):
        bg = arcade.color.YELLOW if mode == 0 else arcade.color.ORANGE
        arcade.draw_lrbt_rectangle_filled(-10000, 10000, -10000, 10000, arcade.color.BLACK)
        arcade.draw_lrbt_rectangle_filled(-200, 200, -200, 200, bg)
        arcade.draw_circle_filled(0, 0, 30, arcade.color.RED)
        arcade.draw_circle_filled(0, 0, 10, arcade.color.GRAY)
        arcade.draw_circle_filled(300, 300, 20, arcade.color.PINK)
        arcade.draw_text("this is a test", 70, 70, arcade.color.PINK, 24)
        for i in range(20):
            arcade.draw_text(str(i), i * 50, 0, arcade.color.GREEN, 20)
        self.sprites.draw()


    def on_draw(self):
        self.clear(arcade.color.DARK_BROWN)
        with self.cam.activate():
            self.draw_scene(0)

    def on_key_press(self, symbol: int,modifiers: int):
        d = 20
        if symbol == arcade.key.ESCAPE:
            self.close()

        if symbol == arcade.key.W:
            self.actor.center_y += d
            self.cam.position += (0, d)
        elif symbol == arcade.key.S:
            self.actor.center_y += -d
            self.cam.position += (0, -d)
        elif symbol == arcade.key.D:
            self.actor.center_x += d
            self.cam.position += (d, 0)
        elif symbol == arcade.key.A:
            self.actor.center_x += -d
            self.cam.position += (-d, 0)


if __name__ == '__main__':
    win = Game(400, 400, "scrolling")
    win.cam = arcade.Camera2D(
        projection=arcade.rect.LRBT(0, 400, 0, 400),
        position=(0, 0),
        scissor=arcade.rect.LRBT(50, 350, 50, 350)  # screenspace
    )
    win.cam.position -= (50, 50)  # offset camera to account for screenspace adjustment
    win.run()
