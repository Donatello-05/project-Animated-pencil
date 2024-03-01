import pygame
import sys
from pygame.locals import *

pygame.init()

# Настройки окна
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
FPS = 30

# Настройки рисования
drawing = False
brush_size = 5
brush_color = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Mini Pencil2D')

# Цвета и кнопки
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
colors = [BLACK, RED, GREEN, BLUE]
color_buttons = [pygame.Rect(10 + 40 * i, 10, 30, 30) for i in range(len(colors))]
brush_buttons = [pygame.Rect(10, 50 + 40 * i, 30, 30) for i in range(1, 4)]  # Small, Medium, Large
add_layer_button = pygame.Rect(10, 170, 60, 30)  # Button to add a layer
remove_layer_button = pygame.Rect(80, 170, 60, 30)  # Button to remove a layer
animation_button = pygame.Rect(10, 210, 130, 30)  # Button to start animation

LAYERS = [pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)]  # Инициализация первого слоя
current_layer = 0

# Функция рисования
def draw(x, y, color, size):
    pygame.draw.circle(LAYERS[current_layer], color, (x, y), size)

# Функция для обновления экрана
def update_screen():
    screen.fill(WHITE)
    for layer in LAYERS:
        screen.blit(layer, (0, 0))
    # Рисование кнопок
    for i, rect in enumerate(color_buttons):
        pygame.draw.rect(screen, colors[i], rect)
    for i, rect in enumerate(brush_buttons):
        pygame.draw.rect(screen, BLACK, rect, 3)
        pygame.draw.circle(screen, BLACK, rect.center, 5 * (i + 1), 1)
    pygame.draw.rect(screen, BLACK, add_layer_button, 2)
    pygame.draw.rect(screen, BLACK, remove_layer_button, 2)
    pygame.draw.rect(screen, BLACK, animation_button, 2)
    screen.blit(pygame.font.SysFont(None, 24).render('Add', True, BLACK), (20, 175))
    screen.blit(pygame.font.SysFont(None, 24).render('Remove', True, BLACK), (85, 175))
    screen.blit(pygame.font.SysFont(None, 24).render('Animate', True, BLACK), (20, 215))
    pygame.display.update()

# Основной цикл программы
def main():
    global drawing, current_layer, brush_size, brush_color

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Проверка кликов на кнопках выбора цвета и размера кисти
                if event.button == 1:  # Левая кнопка мыши
                    check_buttons(pos)
                drawing = True if event.button == 1 else drawing
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                drawing = False
            elif event.type == MOUSEMOTION and drawing:
                x, y = event.pos
                draw(x, y, brush_color, brush_size)

        update_screen()
        clock.tick(FPS)

def check_buttons(pos):
    global current_layer, brush_size, brush_color
    # Проверка клика на кнопках цвета и размера
    for i, rect in enumerate(color_buttons):
        if rect.collidepoint(pos):
            brush_color = colors[i]
    for i, rect in enumerate(brush_buttons):
        if rect.collidepoint(pos):
            brush_size = 5 * (i + 1)
    # Добавление и удаление слоев
    if add_layer_button.collidepoint(pos):
        LAYERS.append(pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA))
        LAYERS[-1].fill((0, 0, 0, 0))  # Новый слой делаем прозрачным
        current_layer = len(LAYERS) - 1
    if remove_layer_button.collidepoint(pos) and len(LAYERS) > 1:
        LAYERS.pop()
        current_layer = len(LAYERS) - 1
    # Воспроизведение анимации
    if animation_button.collidepoint(pos):
        animate_layers()

def animate_layers():
    for layer in LAYERS:
        screen.fill(WHITE)
        screen.blit(layer, (0, 0))
        pygame.display.update()
        pygame.time.wait(150)  # Время задержки между слоями

if __name__ == '__main__':
    main()
