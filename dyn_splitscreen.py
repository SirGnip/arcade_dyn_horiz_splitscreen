"""
Goal: Trying to use the built in Section class and Manager to handle split screen.
Results: Works (draws stuff from both sections), but there isn't scissoring and it doesn't automatically handle offsets. You have to automatically offset an object's world coordinates.
"""
import arcade

class LeftSect(arcade.Section):
    def __init__(self, left, bottom, width, height, **kwargs):
        super().__init__(left, bottom, width, height, **kwargs)

    def on_draw(self):
        print('draw left', self.left)
        self.view.draw_scene(0)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.close()
class RightSect(arcade.Section):
    def __init__(self, left, bottom, width, height, **kwargs):
        super().__init__(left, bottom, width, height, **kwargs)

    def on_draw(self):
        print('draw right', self.left)
        self.view.draw_scene(1)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.close()
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.lefts = LeftSect(0, 0, 100, 100)
        self.rights = RightSect(400, 400, 100, 100)
        self.sm = arcade.SectionManager(self)
        self.sm.add_section(self.rights)
        self.sm.add_section(self.lefts)

    def on_show_view(self) -> None:
        print('enable')
        self.sm.enable()

    def on_hide_view(self):
        print('disable')
        self.sm.disable()

    def on_draw(self):
        print('view draw')
        self.clear(arcade.color.DARK_BROWN)

    def draw_scene(self, mode):
        bg = arcade.color.YELLOW if mode == 0 else arcade.color.ORANGE
        arcade.draw_lrbt_rectangle_filled(-1000, 1000, -1000, 1000, bg)
        arcade.draw_circle_filled(self.left + 0, self.bottom + 0, 30, arcade.color.RED)
        # arcade.draw_circle_filled(0, 0, 10, arcade.color.GRAY)
        # arcade.draw_text("this is a test", 70, 70, arcade.color.ORANGE, 24)
        # arcade.draw_line(-100, -100, 100, 100, arcade.color.BLUE)
        # arcade.draw_line(-100, 100, 100, -100, arcade.color.BLUE)
        # arcade.draw_line(x, 0, 100, 100, arcade.color.BLUE)

    # def draw_scene2(self):
    #     # bg = arcade.color.YELLOW if mode == 0 else arcade.color.ORANGE
    #     # arcade.draw_lrbt_rectangle_filled(-1000, 1000, -1000, 1000, bg)
    #     arcade.draw_circle_filled(self.left + 0, 20, 10, arcade.color.PURPLE)



if __name__ == '__main__':
    win = arcade.Window(1000, 800, 'test')
    view = GameView()
    win.show_view(view)
    win.run()
