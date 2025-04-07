"""
Goal: Get dynamic split screen, fix jitter on full/split transitions
Result: Jitter was fixed
"""

import sys
import math
import time
import random
import pathlib
from enum import Enum
import arcade

WORLD_X_MIN, WORLD_X_MAX = -5000, 5000
WIN_WIDTH, WIN_HEIGHT = 1200, 800
VIEW_WIDTH, VIEW_HEIGHT = 500, 700
VIEW_OFFSET = (100, 50)
MARGIN = 75
MOUNTAIN_HEIGHT = int(VIEW_HEIGHT * .3)


class SplitMode(Enum):
    FULL = 0
    SPLIT = 1

class FpsCounter:
    def __init__(self):
        self.start_time = time.perf_counter()
        self.ticks = 0

    def tick(self):
        self.ticks += 1

    @property
    def fps(self):
        fps = self.ticks / (time.perf_counter() - self.start_time)
        self.start_time = time.perf_counter()
        self.ticks = 0
        return fps


class Player(arcade.Sprite):
    def __init__(self, udlr: list[int]):
        super().__init__(":resources:/images/space_shooter/playerShip1_blue.png", scale=0.4)
        self.key_up, self.key_down, self.key_left, self.key_right = udlr

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y = arcade.math.clamp(self.center_y + self.change_y, 0, VIEW_HEIGHT)

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
    def __init__(self, w, h, view_width, view_height, view_offset, title):
        super().__init__(w, h, title)
        self.fps = FpsCounter()

        # cameras
        self.caml = arcade.Camera2D(
            projection=arcade.rect.LBWH(0, 0, w, h),
            scissor=arcade.rect.LBWH(view_offset[0], view_offset[1], view_width, view_height)  # in screenspace
        )
        self.camr = arcade.Camera2D(
            projection=arcade.rect.LBWH(0, 0, w, h),
            scissor=arcade.rect.LBWH(view_width + view_offset[0], view_offset[1], view_width, view_height)  # in screenspace
        )
        self.camf = arcade.Camera2D(
            projection=arcade.rect.LBWH(0, 0, w, h),
            position=(0, -50),  # starting position
            scissor=arcade.rect.LBWH(view_offset[0], view_offset[1], view_width * 2, view_height)  # in screenspace
        )
        self.default_cam = arcade.Camera2D()
        self.mode = SplitMode.FULL

        # players
        self.sprites = arcade.SpriteList()
        p = Player([arcade.key.W, arcade.key.S, arcade.key.A, arcade.key.D])
        p.position = (100, 100)
        self.sprites.append(p)
        p = Player([arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT])
        p.position = (200, 150)
        self.sprites.append(p)

        # world geometry
        self.bg_sprites = arcade.SpriteList()
        for _ in range(60):
            x = random.randint(WORLD_X_MIN, WORLD_X_MAX)
            y = random.randint(MOUNTAIN_HEIGHT, VIEW_HEIGHT)
            a = random.uniform(-90, 90)
            scale = random.uniform(0.2, 0.3)
            images = [
                ":resources:images/pinball/bumper.png",
                ":resources:images/space_shooter/meteorGrey_big2.png",
                ":resources:images/space_shooter/meteorGrey_tiny2.png",
                ":resources:images/items/star.png",
            ]
            img = random.choice(images)
            sprite = arcade.Sprite(img, scale, x, y, angle=a)
            self.bg_sprites.append(sprite)
        def my_rand(x, max_val):
            return ((x * 123455) ^ x) % max_val  # quasi-random number generator, repeatable
        self.line_pts = [(x, my_rand(x, 200)) for x in range(WORLD_X_MIN, WORLD_X_MAX, MOUNTAIN_HEIGHT)]
        self.line_pts.append((WORLD_X_MAX, -100))
        self.line_pts.append((WORLD_X_MIN, -100))

    def draw_scene(self):
        arcade.draw_lrbt_rectangle_filled(WORLD_X_MIN, WORLD_X_MAX, -10000, 10000, arcade.color.BLACK)
        self.bg_sprites.draw()
        arcade.draw_polygon_filled(self.line_pts, arcade.color.DARK_BROWN)  # seems slow
        arcade.draw_line_strip(self.line_pts, arcade.color.YELLOW, 2)
        arcade.draw_lrbt_rectangle_filled(-200, 200, -200, 200, arcade.color.YELLOW)
        arcade.draw_circle_filled(0, 0, 30, arcade.color.RED)
        arcade.draw_circle_filled(0, 0, 10, arcade.color.GRAY)
        arcade.draw_circle_filled(300, 300, 20, arcade.color.PINK)
        arcade.draw_text("this is a test", 70, 70, arcade.color.PINK, 24)
        self.sprites.draw()

    def on_draw(self):
        self.clear((25, 25, 25))

        left_actor, right_actor = self.sprites
        left_actor, right_actor = (left_actor, right_actor) if left_actor.center_x < right_actor.center_x else (right_actor, left_actor)
        dist = arcade.get_distance_between_sprites(left_actor, right_actor)

        if dist >= (VIEW_WIDTH * 2) - (MARGIN * 2):
            if self.mode != SplitMode.SPLIT:
                print(f'{self.fps.ticks} transition to split mode')
                self.mode = SplitMode.SPLIT
                self.caml.position = self.camf.position
                self.camr.position = self.camf.position
        elif math.fabs(self.caml.position.x - self.camr.position.x) < 15:
            if self.mode != SplitMode.FULL:
                print(f'{self.fps.ticks} transition to full mode')
                self.mode = SplitMode.FULL
                self.camf.position = self.caml.position

        if self.mode == SplitMode.FULL:
            scroll_view(self.camf, left_actor)
            scroll_view(self.camf, right_actor)
            with self.camf.activate():
                self.draw_scene()
        else:
            scroll_view(self.caml, left_actor)
            scroll_view(self.camr, right_actor)
            with self.caml.activate():
                self.draw_scene()
            with self.camr.activate():
                self.draw_scene()
            with self.default_cam.activate():
                x = VIEW_OFFSET[0] + VIEW_WIDTH
                arcade.draw_line(x, 0, x, WIN_HEIGHT, arcade.color.WHITE, 3)

        self.fps.tick()
        if self.fps.ticks > 60 * 2:
            print(f"{self.fps.fps:.2f}")

    def on_update(self, delta_time):
        self.sprites.update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.close()
        [s.on_key_press(symbol) for s in self.sprites]


def scroll_view(cam, actor):
    # translate the screen view to world space
    view_in_world_space = cam.scissor.move(cam.position[0], cam.position[1])
    new_view = None  # rect in world-space
    if actor.center_x - MARGIN < view_in_world_space.left:
        new_view = view_in_world_space.align_left(actor.center_x - MARGIN)
    if actor.center_x + MARGIN > view_in_world_space.right:
        new_view = view_in_world_space.align_right(actor.center_x + MARGIN)
    if actor.center_y > view_in_world_space.top:
        new_view = view_in_world_space.align_top(actor.center_y)
    if actor.center_y < view_in_world_space.bottom:
        new_view = view_in_world_space.align_bottom(actor.center_y)
    if new_view:
        # offset the camera position to represent the new view in the given screen position
        cam.position = new_view.left - cam.scissor.left, new_view.bottom - cam.scissor.bottom


if __name__ == '__main__':
    win = Game(WIN_WIDTH, WIN_HEIGHT, VIEW_WIDTH, VIEW_HEIGHT, VIEW_OFFSET, pathlib.Path(sys.argv[0]).name)
    win.run()