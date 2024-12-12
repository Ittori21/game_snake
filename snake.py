import pygame
import random
import logging
import sys

logging.basicConfig(filename="./loging.log", level=logging.INFO,
                    format="%(asctime)s - %(message)s")
WIDTH, HEIGHT = 1000, 800
CELL_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
LIGHT_GRAY = (200, 200, 200)

pygame.init()
FONT = pygame.font.SysFont("comicsansms", 35)

class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Food(GameObject):
    def __init__(self):
        super().__init__(
            round(random.randrange(0, WIDTH - CELL_SIZE) / CELL_SIZE) * CELL_SIZE,
            round(random.randrange(0, HEIGHT - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
        )

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, [self.x, self.y, CELL_SIZE, CELL_SIZE])

class Snake(GameObject):
    def __init__(self):
        super().__init__(WIDTH // 2, HEIGHT // 2)
        self.body = [[self.x, self.y]]
        self.direction = (0, 0)
        self.length = 1

    def move(self):
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.body.append([self.x, self.y])
        if len(self.body) > self.length:
            del self.body[0]

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, WHITE, [segment[0], segment[1], CELL_SIZE, CELL_SIZE])

    def check_collision(self):
        if self.x < 0 or self.x >= WIDTH or self.y < 0 or self.y >= HEIGHT:
            return True
        if self.body[-1] in self.body[:-1]:
            return True
        return False

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Змейка")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.running = True

    def display_score(self):
        score_text = FONT.render(f"Ваш счет: {self.score}", True, BLUE)
        self.screen.blit(score_text, [10, 10])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.snake.direction != (CELL_SIZE, 0):
                    self.snake.direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and self.snake.direction != (-CELL_SIZE, 0):
                    self.snake.direction = (CELL_SIZE, 0)
                elif event.key == pygame.K_UP and self.snake.direction != (0, CELL_SIZE):
                    self.snake.direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and self.snake.direction != (0, -CELL_SIZE):
                    self.snake.direction = (0, CELL_SIZE)

    def restart_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        logging.info("Игра перезапущена")

    def game_over(self):
        self.screen.fill(WHITE)
        msg = FONT.render("Вы проиграли!", True, RED)
        self.screen.blit(msg, [WIDTH // 3, HEIGHT // 4])

        restart_button = pygame.Rect(WIDTH // 3, HEIGHT // 2, 200, 50)
        quit_button = pygame.Rect(WIDTH // 3 + 250, HEIGHT // 2, 200, 50)

        pygame.draw.rect(self.screen, LIGHT_GRAY, restart_button)
        pygame.draw.rect(self.screen, LIGHT_GRAY, quit_button)

        restart_text = FONT.render("Перезапуск", True, BLACK)
        quit_text = FONT.render("Выход", True, BLACK)

        self.screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))
        self.screen.blit(quit_text, (quit_button.x + 10, quit_button.y + 10))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        self.restart_game()
                        return
                    if quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

    def run(self):
        logging.info("Игра началась")
        while self.running:
            self.handle_events()
            self.snake.move()

            if self.snake.check_collision():
                logging.warning("Змейка столкнулась")
                self.game_over()

            if self.snake.x == self.food.x and self.snake.y == self.food.y:
                self.food = Food()
                self.snake.length += 1
                self.score += 1
                logging.info(f"Счет: {self.score}")

            self.screen.fill(BLACK)
            self.food.draw(self.screen)
            self.snake.draw(self.screen)
            self.display_score()
            pygame.display.update()
            self.clock.tick(15)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()