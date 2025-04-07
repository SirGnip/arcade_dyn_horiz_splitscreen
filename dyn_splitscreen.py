"""
Goal: Get two independently controlled actors
"""
import sys
import pathlib
import arcade

class Player(arcade.Sprite):
    def __init__(self, udlr: list[int]):
        super().__init__(":resources:/images/space_shooter/playerShip1_blue.png")
        self.key_up, self.key_down, self.key_left, self.key_right = udlr

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

    def on_key_press(self, symbol: int):
        d = 4
        if symbol == self.key_up:
            self.angle = 0
            if self.change_y > 0:
                self.change_x = 0
                self.change_y = 0
            else:
                self.change_x = 0
                self.change_y = d
        elif symbol == self.key_down:
            self.angle = 180
            self.change_x = 0
            self.change_y = -d
        elif symbol == self.key_right:
            self.angle = 90
            self.change_x = d
            self.change_y = 0
        elif symbol == self.key_left:
            self.angle = 270
            self.change_x = -d
            self.change_y = 0

class Game(arcade.Window):
    def __init__(self, w, h, title):
        super().__init__(w, h, title)
        self.sprites = arcade.SpriteList()
        p = Player([arcade.key.W, arcade.key.S, arcade.key.A, arcade.key.D])
        p.position = (100, 100)
        self.sprites.append(p)
        p = Player([arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT])
        p.position = (200, 150)
        self.sprites.append(p)


    def draw_scene(self):
        arcade.draw_lrbt_rectangle_filled(-10000, 10000, -10000, 10000, arcade.color.BLACK)
        arcade.draw_lrbt_rectangle_filled(-200, 200, -200, 200, arcade.color.YELLOW)
        arcade.draw_circle_filled(0, 0, 30, arcade.color.RED)
        arcade.draw_circle_filled(0, 0, 10, arcade.color.GRAY)
        arcade.draw_circle_filled(300, 300, 20, arcade.color.PINK)
        arcade.draw_text("this is a test", 70, 70, arcade.color.PINK, 24)
        for i in range(20):
            arcade.draw_text(str(i), i * 50, 0, arcade.color.GREEN, 20)
        self.sprites.draw()

    def on_draw(self):
        self.clear(arcade.color.DARK_BROWN)
        with self.cam1.activate():
            self.draw_scene()
        with self.cam2.activate():
            self.draw_scene()

    def on_update(self, delta_time):
        self.sprites.update(delta_time)
        scroll_view(self.cam1, self.sprites[0])
        scroll_view(self.cam2, self.sprites[1])

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.close()
        [s.on_key_press(symbol) for s in self.sprites]


def scroll_view(cam, actor):
    # translate the screen view to world space
    view_in_world_space = cam.scissor.move(cam.position[0], cam.position[1])
    new_view = None  # rect in world-space
    if actor.center_x < view_in_world_space.left:
        new_view = view_in_world_space.align_left(actor.center_x)
    if actor.center_x > view_in_world_space.right:
        new_view = view_in_world_space.align_right(actor.center_x)
    if actor.center_y > view_in_world_space.top:
        new_view = view_in_world_space.align_top(actor.center_y)
    if actor.center_y < view_in_world_space.bottom:
        new_view = view_in_world_space.align_bottom(actor.center_y)
    if new_view:
        # offset the camera position to represent the new view in the given screen position
        cam.position = new_view.left - cam.scissor.left, new_view.bottom - cam.scissor.bottom


if __name__ == '__main__':
    width, height = 900, 400
    win = Game(width, height, pathlib.Path(sys.argv[0]).name)
    win.cam1 = arcade.Camera2D(
        projection=arcade.rect.LBWH(0, 0, width, height),
        position=(0, 0),
        scissor=arcade.rect.LBWH(50, 80, 350, 300)  # screenspace
    )
    win.cam2 = arcade.Camera2D(
        projection=arcade.rect.LBWH(0, 0, width, height),
        position=(0, 0),
        scissor=arcade.rect.LBWH(450, 10, 150, 350)  # screenspace
    )
    win.run()
