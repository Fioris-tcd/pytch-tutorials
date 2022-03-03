import pytch
import random


class GameBackground(pytch.Stage):
    Backdrops = ["solid-green.png"]


class Fruit(pytch.Sprite):
    Costumes = ["apple.png"]

    @pytch.when_this_sprite_clicked
    def hit_fruit(self):
        self.hide()
        pytch.wait_seconds(1)

        appear_x = random.randint(-200, 200)

        self.show()
