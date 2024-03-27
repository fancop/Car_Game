from os import system, name
import keyboard
from random import randint
from time import sleep
from sys import exit

# ANSI цвета
BLACK = u'\033[0;30m'
RED = u'\033[0;31m'
GREEN = u'\033[0;32m'
BROWN = u'\033[0;33m'
BLUE = u'\033[0;34m'
PURPLE = u'\033[0;35m'
CYAN = u'\033[0;36m'
LIGHT_GRAY = u'\033[0;37m'
DARK_GRAY = u'\033[1;30m'
LIGHT_RED = u'\033[1;31m'
LIGHT_GREEN = u'\033[1;32m'
YELLOW = u'\033[1;33m'
LIGHT_BLUE = u'\033[1;34m'
LIGHT_PURPLE = u'\033[1;35m'
LIGHT_CYAN = u'\033[1;36m'
LIGHT_WHITE = u'\033[1;37m'
END_COLOR = u'\033[0m'

PLAYER_IMAGE = LIGHT_CYAN + 'P' + END_COLOR
OBSTACLE_IMAGE = LIGHT_PURPLE + 'O' + END_COLOR
CELL_IMAGE = LIGHT_GRAY + '.' + END_COLOR


class GameObject:
    '''
    Объект на игровом поле
    '''

    def __init__(self, y, x, image):
        self.y = y
        self.x = x
        self.image = image


class Player(GameObject):
    def __init__(self, y, x, image=PLAYER_IMAGE):
        self.score = 0
        super().__init__(y, x, image)


class Obstacle(GameObject):
    def __init__(self, y, x, image=OBSTACLE_IMAGE):
        super().__init__(y, x, image)


class Cell:
    def __init__(self, y, x, image):
        self.y = y
        self.x = x
        self.content = None
        self.image = image

    def draw(self):
        if self.content:
            print(self.content.image, end=' ')
        else:
            print(self.image, end=' ')


class Field:
    def __init__(self):
        self.rows = 10
        self.columns = 3
        self.player = Player(y=self.rows - 1, x=self.columns // 2)
        self.obstacles = []
        self.field = self.generate_empty_field()
        self.field[self.player.y][self.player.x].content = self.player

    def spawn_obstacle(self):
        obstacle_y, obstacle_x = 0, randint(0, 2)
        if self.check_neighbours(obstacle_y, obstacle_x):
            obstacle = Obstacle(obstacle_y, obstacle_x)
            self.obstacles.append(obstacle)
            self.field[obstacle.y][obstacle.x].content = obstacle

    def check_neighbours(self, y, x):
        if not self.field[y + 1][x].content and not self.field[y + 2][x].content:
            return True

    def move_obstacles(self):
        for obstacle in self.obstacles:
            this_cell = self.field[obstacle.y][obstacle.x]
            if not self.is_on_field(obstacle.y + 1, obstacle.x):
                this_cell.content = None
                self.obstacles.remove(obstacle)
                continue
            obstacle.y += 1
            new_cell = self.field[obstacle.y][obstacle.x]
            this_cell.content = None
            new_cell.content = obstacle

    def generate_empty_field(self):
        field = [
            [Cell(y=row, x=column, image=CELL_IMAGE) for column in range(self.columns)]
            for row in range(self.rows)
        ]
        return field

    def is_on_field(self, y: int, x: int):
        return (y > -1 and y < self.rows) and (x > -1 and x < self.columns)

    def move_player(self):
        dx = 0
        if keyboard.is_pressed('right'):
            dx = 1
        if keyboard.is_pressed('left'):
            dx = -1
        if keyboard.is_pressed('esc'):
            exit()

        this_cell = self.field[self.player.y][self.player.x]
        new_x = self.player.x + dx

        if not self.is_on_field(self.player.y, new_x):
            return False

        new_cell = self.field[self.player.y][new_x]

        if isinstance(new_cell.content, Obstacle):
            return False

        this_cell.content = None
        new_cell.content = self.player
        self.player.x = new_x
        return True

    def draw(self):
        for row in self.field:
            print('| ', end='')
            for cell in row:
                cell.draw()
            print('|')
        print('')


class Application:
    def __init__(self):
        self.is_running = True
        self.game = Game()
        self.run()

    def run(self):
        self.show_start_screen()
        while self.is_running:
            self.game.start_new_game()
            self.show_end_screen()

    def show_start_screen(self):
        input('Нажмите ENTER чтобы начать игру')

    def show_end_screen(self):
        print('Enter - сыграть еще раз')
        print('Esc - выход')

        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'esc':
                    self.is_running = False
                    return
                elif event.name == 'enter':
                    return

    def clear_screen(self):
        if name == 'nt':
            system('cls')
        else:
            system('clear')


class Game:
    def __init__(self):
        pass

    def start_new_game(self):
        self.field = Field()
        self.is_running = True
        self.run()

    def show_score(self):
        print(f'Очков: {self.field.player.score}')

    def run(self):
        while self.is_running:
            if name == 'nt':
                system('cls')
            else:
                system('clear')

            self.field.draw()

            move = self.field.move_player()
            self.field.spawn_obstacle()
            self.field.move_obstacles()
            self.show_score()
            if not move:
                self.is_running = False
            self.field.player.score += 100
            sleep(1 / 10)


if __name__ == '__main__':
    Application()
