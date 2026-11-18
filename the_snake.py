from random import choice, randint

import pygame

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

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
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
        pass


class Apple(GameObject):
    """Класс описывающий яблоки"""

    def __init__(self):
        self.position = self.randomize_position([])
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake_positions):
        """Метод для создания яблок
        в рандомных местах поля
        """
        while True:
            free_cell = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if free_cell not in snake_positions:
                self.position = free_cell
                return self.position

    def draw(self):
        """Отрисовка яблок на поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывающий змею"""

    def __init__(
        self
    ):
        self.body_color = SNAKE_COLOR
        self.position = [SCREEN_CENTER]
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Метод для получения координат головы змеи"""
        x_head = self.positions[0][0]
        y_head = self.positions[0][1]
        return (x_head, y_head)

    def move(self):
        """Метод описывает движение головы и удаление хвоста,
        движение змеи по полю
        """
        x_head, y_head = self.get_head_position()
        new_x_head = (x_head + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH
        new_y_head = (y_head + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x_head, new_y_head))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовка головы змейки"""
        for position in self.positions[1:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Инициализация новой игры после столкновения змеи с хвостом."""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice((UP, DOWN, RIGHT, LEFT))
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл"""
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()

        snake.move()

        head_position = snake.get_head_position()

        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        for current_position in snake.positions[1:]:
            if head_position == current_position:
                snake.reset()
                apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
