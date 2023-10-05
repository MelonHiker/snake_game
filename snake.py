import pygame
from random import randint
from os import path

pygame.init()

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

SCALE = 30  # pixel/block, (x, y) = (pos[0] * SCALE, pos[1] * SCALE)
SPEED_UP = 0.5
GET_SCORE = 10
INCREASE_BODY_SIZE = 1

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (80, 78, 81)
clock = pygame.time.Clock()


class Snake:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self):
        self.body_size = 0
        self.head_pos = [0, 0]
        self.bodys_pos = []
        self.direction = self.RIGHT
        self.speed = 4  # block/sec

    def move(self):
        self.bodys_pos.append(self.head_pos[:])

        if len(self.bodys_pos) > self.body_size:
            self.bodys_pos.pop(0)

        if self.direction == self.RIGHT:
            self.head_pos[0] += 1
        elif self.direction == self.LEFT:
            self.head_pos[0] -= 1
        elif self.direction == self.UP:
            self.head_pos[1] -= 1
        elif self.direction == self.DOWN:
            self.head_pos[1] += 1

        self.draw()

    def draw(self):
        head_rect = pygame.Rect(self.head_pos[0] * SCALE, self.head_pos[1] * SCALE, SCALE, SCALE)
        pygame.draw.rect(WIN, GREEN, head_rect)

        for body_pos in self.bodys_pos:
            body_rect = pygame.Rect(body_pos[0] * SCALE, body_pos[1] * SCALE, SCALE, SCALE)
            pygame.draw.rect(WIN, GREEN, body_rect)

    def restart(self):
        self.body_size = 0
        self.head_pos = [0, 0]
        self.bodys_pos = []
        self.direction = self.RIGHT
        self.speed = 4  # block/sec


class Food:
    def __init__(self):
        self.pos = [randint(0, WIDTH // SCALE - 1), randint(0, HEIGHT // SCALE - 1)]
        self.radius = SCALE * 0.3
        self.color = (randint(180, 255), randint(180, 255), randint(180, 255))

    def draw(self):
        x = self.pos[0] * SCALE + SCALE / 2
        y = self.pos[1] * SCALE + SCALE / 2
        pygame.draw.circle(WIN, self.color, (x, y), self.radius)

    def recreate(self):
        self.pos = [randint(0, WIDTH // SCALE - 1), randint(0, HEIGHT // SCALE - 1)]
        self.color = (randint(180, 255), randint(180, 255), randint(180, 255))


def draw_text(text, size, x, y):
    font = pygame.font.SysFont("comicsans", size)
    font_text = font.render(text, True, WHITE)
    x -= font_text.get_width() / 2
    y -= font_text.get_height() / 2
    WIN.blit(font_text, (x, y))


def draw_background():
    WIN.fill(BLACK)
    for i in range(1, HEIGHT // SCALE):
        pygame.draw.line(WIN, DARK_GREY, (0, i * SCALE), (WIDTH, i * SCALE))

    for i in range(1, WIDTH // SCALE):
        pygame.draw.line(WIN, DARK_GREY, (i * SCALE, 0), (i * SCALE, HEIGHT))


def draw_init(best_score):
    WIN.fill(BLACK)
    draw_text("Snake!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text("Arrow keys to move~~~", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(f"best score: {best_score}", 22, WIDTH / 2, HEIGHT * 5 / 8)
    draw_text("Press any bottom to start!", 18, WIDTH / 2, HEIGHT * 3 / 4)

    pygame.display.update()
    waiting = True

    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                waiting = False

    return False


def main():
    run = True
    snake = Snake()
    food = Food()
    
    score = 0
    best_score = 0

    # 讀取最佳分數
    if (path.exists("best_score.txt")):
        with open("best_score.txt", "r") as file:
            best_score = int(file.read())
    
    # 初始畫面
    if draw_init(best_score):
        run = False

    while run:
        clock.tick(snake.speed)
        draw_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, ord("w")) and snake.direction != snake.DOWN:
                    snake.direction = snake.UP
                elif event.key in (pygame.K_DOWN, ord("s")) and snake.direction != snake.UP:
                    snake.direction = snake.DOWN
                elif event.key in (pygame.K_LEFT, ord("a")) and snake.direction != snake.RIGHT:
                    snake.direction = snake.LEFT
                elif event.key in (pygame.K_RIGHT, ord("d")) and snake.direction != snake.LEFT:
                    snake.direction = snake.RIGHT
                else:
                    continue
                break

        food.draw()
        snake.move()
        draw_text(f"Score: {score}", 16, 40, 10)
        pygame.display.update()

        # 吃到食物
        if snake.head_pos == food.pos:
            score += GET_SCORE
            food.recreate()
            snake.body_size += INCREASE_BODY_SIZE
            snake.speed += SPEED_UP

        # 碰到身體或是牆
        head_x = snake.head_pos[0] * SCALE
        head_y = snake.head_pos[1] * SCALE

        if (
            (snake.head_pos in snake.bodys_pos)
            or (head_x >= WIDTH)
            or (head_y >= HEIGHT)
            or (head_x < 0)
            or (head_y < 0)
        ):
            if draw_init(best_score):
                break

            snake.restart()
            food.recreate()
            score = 0

        best_score = max(score, best_score)

    with open("best_score.txt", "w") as file:
        file.write(str(best_score))

    pygame.quit()


if __name__ == "__main__":
    main()