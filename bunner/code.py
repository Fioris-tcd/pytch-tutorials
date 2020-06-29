import pytch
from pytch import (
    Project,
    Stage,
    Sprite,
    when_key_pressed
)

class BunnyStage(Stage):
  Backdrops = [ ('world', 'images/bunner-background.png') ]

  def __init__(self):
      Stage.__init__(self)
      self.switch_backdrop('world')

class Bunny(Sprite):
    Costumes = [
        ('up', 'images/sit0.png', 30, 30),
        ('right', 'images/sit1.png', 30, 30),
        ('down', 'images/sit2.png', 30, 30),
        ('left', 'images/sit3.png', 30, 30)
        ]

    def __init__(self):
        Sprite.__init__(self)
        self.switch_costume('up')
        self.go_to_xy(0, -160)
        self.show()

    @when_key_pressed('ArrowUp')
    def move_up(self):
        self.switch_costume('up')
        if self.get_y() < 150:
            self.change_y(40)

    @when_key_pressed('ArrowRight')
    def move_right(self):
        self.switch_costume('right')
        if self.get_x() < 210:
            self.change_x(25)

    @when_key_pressed('ArrowDown')
    def move_down(self):
        self.switch_costume('down')
        if self.get_y() > -150:
            self.change_y(-40)

    @when_key_pressed('ArrowLeft')
    def move_left(self):
        self.switch_costume('left')
        if self.get_x() > -210:
            self.change_x(-25)
