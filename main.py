import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Определение шрифта
font_path = "arial.ttf"
font_size = 33

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (105, 105, 105)

# Определение размеров экрана
screen_width = 800
screen_height = 600

# Создаем экземпляр класса Font
font = pygame.font.Font(font_path, font_size)

# Создание экрана
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Asteroids with Laser")
background_image = pygame.image.load("images/somespace.jpg")


# Создание игровых объектов
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        spaceship_image = pygame.image.load("images/newspace.png").convert_alpha()
        self.image = spaceship_image
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.centery = screen_height // 2
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.right > screen_width:
            self.rect.right = screen_width
        elif self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
        elif self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Генерация случайного радиуса для астероида
        self.radius = random.randint(20, 40)

        # Генерация случайной формы астероида
        self.points = random.randint(5, 12)
        self.angle_offset = random.uniform(0, 2 * math.pi / self.points)
        self.angle_increment = 2 * math.pi / self.points

        # Создание поверхности и отрисовка астероида
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.draw_asteroid()
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.rect.y = random.randrange(-100, -40)
        self.speed_x = random.randrange(-3, 3)
        self.speed_y = random.randrange(1, 8)
        self.rect.x = random.randrange(screen_width - self.rect.width)

    def draw_asteroid(self):
        points = []
        angle = self.angle_offset
        for _ in range(self.points):
            distance = random.uniform(self.radius * 0.8, self.radius)
            x = math.cos(angle) * distance + self.radius
            y = math.sin(angle) * distance + self.radius
            points.append((x, y))
            angle += self.angle_increment

        pygame.draw.polygon(self.image, GREY, points)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top > screen_height + 10 or self.rect.left < -25 or self.rect.right > screen_width + 20:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_x = random.randrange(-3, 3)
            self.speed_y = random.randrange(1, 8)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = ['images/fstexp.png', 'images/secexp.png',
                       'images/threxp.png', 'images/forexp.png',
                       'images/fivexp.png']  # Список изображений для анимации взрыва
        self.current_frame = 0
        self.image = pygame.image.load(self.images[self.current_frame]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.animation_delay = 2  # Задержка между сменой кадров
        self.current_delay = self.animation_delay

    def update(self):
        self.current_delay -= 1
        if self.current_delay <= 0:
            self.current_frame += 1
            if self.current_frame >= len(self.images):
                self.kill()
            else:
                self.image = pygame.image.load(self.images[self.current_frame]).convert_alpha()
                self.current_delay = self.animation_delay


def show_game_over_screen():
    screen.blit(background_image, (0, 0))  # Отрисовка изображения фона
    game_over_text = font.render("Game Over", True, GREY)
    start_again_text = font.render("Press R to start again", True, WHITE)
    score_text = font.render("Final Score: " + str(final_score), True, WHITE)
    quit_text = font.render("Press Q to quit", True, WHITE)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 200))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - 150))
    screen.blit(start_again_text, (screen_width // 2 - start_again_text.get_width() // 2, screen_height // 2))
    screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()


# Создание всех спрайтов и групп
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()
explosions = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for _ in range(8):
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

# Определение положения текста на экране
text_x = 10
text_y = 10

# Переменные для отслеживания уровня и очков
level = 1
score = 0
final_score = score

# Цикл игры
running = True
clock = pygame.time.Clock()

game_started = False

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_started:
                game_started = True
            elif event.key == pygame.K_SPACE:
                player.shoot()

    if game_started:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.speed_x = -5
        elif keys[pygame.K_RIGHT]:
            player.speed_x = 5
        else:
            player.speed_x = 0

        if keys[pygame.K_UP]:
            player.speed_y = -5
        elif keys[pygame.K_DOWN]:
            player.speed_y = 5
        else:
            player.speed_y = 0

        all_sprites.update()

        # Проверка столкновений пуль с астероидами
        hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit_asteroid in hits:
            explosion = Explosion(hit_asteroid.rect.centerx, hit_asteroid.rect.centery)
            all_sprites.add(explosion)
            explosions.add(explosion)

            score += 1
            final_score += 1
            if score % 5 == 0:
                level += 1
                for asteroid in asteroids:
                    asteroid.speed_y += 1

            asteroid = Asteroid()
            all_sprites.add(asteroid)
            asteroids.add(asteroid)

        # Проверка столкновений игрока с астероидами
        hits = pygame.sprite.spritecollide(player, asteroids, False)
        if hits:
            show_game_over_screen()
            all_sprites.empty()
            asteroids.empty()
            bullets.empty()
            explosions.empty()

            player = Player()
            all_sprites.add(player)

            for _ in range(8):
                asteroid = Asteroid()
                all_sprites.add(asteroid)
                asteroids.add(asteroid)

            level = 1
            score = 0
            final_score = 0
            game_started = False

        # Обновление уровня сложности астероидов
        for asteroid in asteroids:
            asteroid.speed_y = random.randrange(1, 8 + level)

        # Отрисовка
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        score_text = font.render("Очки: " + str(score), True, WHITE)
        level_text = font.render("Уровень: " + str(level), True, WHITE)
        screen.blit(score_text, (text_x, text_y))
        screen.blit(level_text, (text_x, text_y + font_size))

    else:
        # Отображение начального меню
        screen.blit(background_image, (0, 0))  # Отрисовка изображения фона
        start_text = font.render("Нажмите любую клавишу для начала игры", True, WHITE)
        screen.blit(start_text, (
        screen_width // 2 - start_text.get_width() // 2, screen_height // 2 - start_text.get_height() // 2))

    pygame.display.flip()

# Завершение игры
pygame.quit()
