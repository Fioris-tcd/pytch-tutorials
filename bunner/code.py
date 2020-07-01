import pytch
from pytch import (
    Project,
    Stage,
    Sprite,
    when_key_pressed,
    when_green_flag_clicked,
    create_clone_of,
    when_I_start_as_a_clone,
    when_I_receive,
    when_this_sprite_clicked
)

import random


game_running = False

score = 0

WAITING, PLAYING, SQUISHED = range(3)

class BunnyStage(Stage):
  Backdrops = [ ('world', 'images/bunner-background.png'),
                ('gameover', 'images/gameover-background.png') ]

  def __init__(self):
      Stage.__init__(self)
      self.switch_backdrop('world')

  @when_I_receive('start playing')
  def start_game(self):
    self.switch_backdrop('world')

  @when_I_receive('game over')
  def game_over(self):
    self.switch_backdrop('gameover')

class Bunny(Sprite):
    Costumes = [
        ('up', 'images/sit0.png', 30, 30),
        ('right', 'images/sit1.png', 30, 30),
        ('down', 'images/sit2.png', 30, 30),
        ('left', 'images/sit3.png', 30, 30),
        ('up_squished', 'images/splat0.png', 30, 30),
        ('right_squished', 'images/splat1.png', 30, 30),
        ('down_squished', 'images/splat2.png', 30, 30),
        ('left_squished', 'images/splat3.png', 30, 30)
        ]

    def __init__(self):
        Sprite.__init__(self)
        self.switch_costume('up')
        self.go_to_xy(0, -160)
        self.mode = PLAYING
        self.hide()
        self.mode = WAITING
        self.lives = -1
        self.highest_row_reached = 0
        self.current_row = 0

    @when_I_receive('start playing')
    def start_game(self):
        global game_running, score
        self.lives = 3
        score = 0
        game_running = True
        self.play_one_life()

    def play_one_life(self):
        if self.lives > 0:
          self.lives = self.lives - 1
          pytch.broadcast('lives changed')
          self.switch_costume('up')
          self.go_to_xy(0, -160)
          self.highest_row_reached = 0
          self.current_row = 0
          self.mode = PLAYING
          self.show()
        else:
          global game_running
          game_running = False
          pytch.broadcast('game over')
          self.hide()
          self.move = WAITING



    @when_key_pressed('ArrowUp')
    def move_up(self):
        global score
        if self.mode == PLAYING:
          self.switch_costume('up')
          if self.get_y() < 150:
              self.change_y(40)
              self.current_row = self.current_row + 1
              if self.current_row > self.highest_row_reached:
                  self.highest_row_reached = self.current_row
                  score = score + 1
                  pytch.broadcast('score changed')

    @when_key_pressed('ArrowRight')
    def move_right(self):
        if self.mode == PLAYING:
          self.switch_costume('right')
          if self.get_x() < 210:
              self.change_x(25)

    @when_key_pressed('ArrowDown')
    def move_down(self):
        if self.mode == PLAYING:
          self.switch_costume('down')
          if self.get_y() > -150:
              self.change_y(-40)
              self.current_row = self.current_row - 1

    @when_key_pressed('ArrowLeft')
    def move_left(self):
        if self.mode == PLAYING:
          self.switch_costume('left')
          if self.get_x() > -210:
              self.change_x(-25)

    @when_I_receive('squish bunny')
    def squish(self):
      if self.mode != SQUISHED:
        self.mode = SQUISHED
        self.switch_costume( self._appearance + "_squished" )
        pytch.wait_seconds(0.5)
        self.play_one_life()

    

class Car(Sprite):
    Costumes = [
        ('left0', 'images/car00.png', 45, 30),
        ('right0', 'images/car01.png', 45, 30),
        ('left1', 'images/car20.png', 45, 30),
        ('right1', 'images/car21.png', 45, 30)
        ]

    def __init__(self):
        Sprite.__init__(self)
        self.speed = 3
        self.direction = 'nothing'
        self.set_size(0.65)
        self.hide()

    @when_I_receive('start playing')
    def startTrafficRowOne(self):
        global game_running
        while game_running:
            if random.random() < 0.2:
                self.go_to_xy(-285,-125)
                self.direction = 'right'
                create_clone_of(self)
                pytch.wait_seconds(0.3)
            pytch.wait_seconds(0.1)

    @when_I_receive('start playing')
    def startTrafficRowTwo(self):
        global game_running
        while game_running:
            if random.random() < 0.2:
                self.go_to_xy(285,-80)
                self.direction = 'left'
                create_clone_of(self)
                pytch.wait_seconds(0.3)
            pytch.wait_seconds(0.1)

    @when_I_receive('start playing')
    def startTrafficRowThree(self):
        global game_running
        while game_running:
            if random.random() < 0.2:
                self.go_to_xy(-285,-30)
                self.direction = 'right'
                create_clone_of(self)
                pytch.wait_seconds(0.3)
            pytch.wait_seconds(0.1)

    @when_I_start_as_a_clone
    def drive(self):
        self.switch_costume( self.direction + random.choice(['0','1']) )
        self.show()
        if self.direction == 'right':
            while self.get_x() < 285:
                self.change_x( self.speed )
        else: # Direction should be 'left'
            while self.get_x() > -285:
                self.change_x( -self.speed )
        self.hide()
        self.delete_this_clone()

    @when_I_start_as_a_clone
    def check_for_collision(self):
        while True:
            while not self.hits(Bunny.the_original()):
                pass
            pytch.broadcast('squish bunny')

    @when_I_receive('game over')
    def vanish(self):
      self.delete_this_clone()

    def hits(self, other):
        return abs( self.get_y() - other.get_y() ) <= 10 and\
               abs( self.get_x() - other.get_x() ) <= 40

class StartButton(Sprite):
    Costumes = [ ('start', 'images/start.png', 135, 30) ]

    def __init__(self):
      Sprite.__init__(self)
      self.hide()
      self.go_to_xy(0,120)
      self.switch_costume('start')

    @when_green_flag_clicked
    def start(self):
      self.show()

    @when_I_receive('game over')
    def game_over_try_again(self):
      pytch.wait_seconds(1)
      self.show()

    @when_this_sprite_clicked
    def start_new_game(self):
      pytch.broadcast('start playing')
      self.hide()

score_costumes = [('digit-%d' % n, 'images/digit-%d.png' % n, 14, 14)
                  for n in range(10)]


class Score_1(Sprite):
    Costumes = score_costumes

    @when_green_flag_clicked
    def set_position_and_size(self):
        self.go_to_xy(200, 162)
        self.hide()

    @when_I_receive('score changed')
    def show_correct_digit(self):
        self.switch_costume('digit-%d' % (score % 10) )
        self.show()

class Score_2(Sprite):
    Costumes = score_costumes

    @when_green_flag_clicked
    def set_position_and_size(self):
        self.go_to_xy(175, 162)
        self.hide()

    @when_I_receive('score changed')
    def show_correct_digit(self):
        self.switch_costume('digit-%d' % (score // 10) )
        self.show()

class LivesCounter(Sprite):
    Costumes = score_costumes

    @when_green_flag_clicked
    def set_position_and_size(self):
        self.go_to_xy(20, 162)
        self.hide()

    @when_I_receive('lives changed')
    def show_correct_digit(self):
        self.switch_costume('digit-%d' % (Bunny.the_original().lives % 10))
        self.show()

