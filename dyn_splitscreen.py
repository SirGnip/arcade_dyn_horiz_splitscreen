"""
Goal: Get basic scrolling working
- x have player start in center of screen move in all directions
- x have simple scroll screen behavior when player gets to edge
"""
import arcade


class Game(arcade.Window):
    def __init__(self, w, h, title):
        super().__init__(w, h, title)
        self.sprites = arcade.SpriteList()
        self.actor = arcade.Sprite(":resources:/images/space_shooter/playerShip1_blue.png")
        self.actor.position = (100, 100)
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
        d = 25
        if symbol == arcade.key.ESCAPE:
            self.close()

        if symbol == arcade.key.W:
            self.actor.center_y += d
        elif symbol == arcade.key.S:
            self.actor.center_y += -d
        elif symbol == arcade.key.D:
            self.actor.center_x += d
        elif symbol == arcade.key.A:
            self.actor.center_x += -d
        print(self.actor.position)
        scroll_view(self.cam, self.actor)

def scroll_view(cam, actor):
    view_in_world_space = cam.scissor.move(cam.position[0], cam.position[1])
    new_view = None  # world-space
    if actor.center_x < view_in_world_space.left:
        # shift the world space view
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
    win = Game(400, 400, "scrolling")
    win.cam = arcade.Camera2D(
        projection=arcade.rect.LRBT(0, 400, 0, 400),
        position=(0, 0),
        scissor=arcade.rect.LRBT(50, 350, 50, 350)  # screenspace
    )
    win.run()
