from random import choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Все ячейки поля
ALL_CELLS = set(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
)

# Разрешённые повороты: (текущее направление, клавиша) -> новое направление
TURNS = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов"""

    def __init__(
        self,
        body_color=BOARD_BACKGROUND_COLOR,
        position=SCREEN_CENTER
    ):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Этот метод для дочерних классов
        отвечает за отрисовку объектов на поле
        """
        raise NotImplementedError('Этот метод только для дочерних классов')

    def draw_cell(self, position, color=None):
        """Отрисовка одной ячейки поля"""
        if color is None:
            color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)
        else:
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect, 1)


class Apple(GameObject):
    """Класс описывающий яблоки"""

    def __init__(
        self,
        body_color=APPLE_COLOR,
        position=SCREEN_CENTER,
        occupied=()
    ):
        super().__init__(body_color, position)
        self.randomize_position(occupied)

    def randomize_position(self, occupied=()):
        """Метод для создания яблок
        в рандомных местах поля
        """
        free_cells = ALL_CELLS - set(occupied)
        if free_cells:
            self.position = choice(tuple(free_cells))

    def draw(self):
        """Отрисовка яблок на поле"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс описывающий змею"""

    def __init__(
        self,
        body_color=SNAKE_COLOR,
        position=SCREEN_CENTER
    ):
        super().__init__(body_color, position)
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None

    def get_head_position(self):
        """Метод для получения координат головы змеи"""
        return self.positions[0]

    def move(self):
        """Метод описывает движение головы и удаление хвоста,
        движение змеи по полю
        """
        x_head, y_head = self.get_head_position()
        step_x, step_y = self.direction
        new_x_head = (x_head + GRID_SIZE * step_x) % SCREEN_WIDTH
        new_y_head = (y_head + GRID_SIZE * step_y) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x_head, new_y_head))
        self.last = self.positions.pop()

    def draw(self):
        """Отрисовка головы змейки и стирание хвоста"""
        self.draw_cell(self.positions[0])
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def grow(self):
        """Возвращает съеденный хвост на место: змея удлиняется."""
        if self.last is not None:
            self.positions.append(self.last)
            self.last = None

    def update_direction(self, new_direction):
        """Метод обновления направления после нажатия на кнопку"""
        if new_direction is not None:
            self.direction = new_direction

    def reset(self):
        """Инициализация новой игры после столкновения змеи с хвостом."""
        self.positions = [self.position]
        self.direction = choice((UP, DOWN, RIGHT, LEFT))
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            game_object.update_direction(
                TURNS.get((game_object.direction, event.key))
            )


def main():
    """Основной игровой цикл"""
    pg.init()

    snake = Snake()
    apple = Apple(occupied=snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:

        handle_keys(snake)

        snake.move()

        head_position = snake.get_head_position()

        if head_position == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        if head_position in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()

        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
