import os
import keyboard
import time

EMPTY = '█'


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = EMPTY

    def __str__(self) -> str:
        return self.image


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = dict()
        self.key_pressed = None
        self.make_cells()

    def make_cells(self):
        for x in range(1, self.width + 1):
            for y in range(1, self.height + 1):
                self.cells[(x, y)] = Cell(x, y)

    def get_cell(self, x, y) -> Cell:
        return self.cells[(x, y)]

    def draw(self):
        screen = ''
        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                screen += self.get_cell(x, y).image
            screen += '\n'
        print(screen)

    def on_press(self, event: keyboard.KeyboardEvent):
        self.key_pressed = event.name


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = ''

    def move_player(self):
        pass


class Let:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.image = ''

    def move_let(self):
        pass


screen = Screen(20, 10)
last_update_time = time.time()
keyboard.on_press(screen.on_press)
counter = 0
os.system('cls')
while True:
    print('\033[H', end='')
    print(counter)
    screen.draw()
    if time.time() - last_update_time > 0.5:
        if screen.key_pressed == 'esc':
            counter += 1
            screen.key_pressed = None
            last_update_time = time.time()
    if time.time() - last_update_time > 1:
        if screen.key_pressed == 'esc':
            counter += 1
            screen.key_pressed = None
            last_update_time = time.time()