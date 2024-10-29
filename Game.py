import pygame
import random
import sys
import math

# Инициализируем Pygame
pygame.init()

# Размеры экрана

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GREEN = (0, 128, 0)
WOODEN_BACKGROUND = (165, 42, 42)
BEIGE = (245, 245, 220)

# шрифт
font = pygame.font.Font(None, 36)

# Игровые переменные
balance = 500
bet = 0
bet_type = None
level = 1 # Начальный уровень
recent_results = [] # Список для хранения последних 5 результатов

# Ркзультаты
result = None
spinning = False
spin_angle = 0
result_shown = False

# Функция для отображения текста указанным цветом
def display_text(text, x, y, color=BEIGE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Функция определения цвета кармана
def pocket_color(number):
    if number <= 10:
        return "red" if number % 2 != 0 else "black"
    elif number <= 18:
        return "black" if number % 2 != 0 else "red"
    elif number <= 28:
        return "red" if number % 2 != 0 else "black"
    else:
        return "black" if number % 2 != 0 else "red"

# Функция проверки и обновления уровня
def check_level():
    global level
    if balance >= 1000 and level == 1:
        level = 2
        display_text("Поздравляем, вы достигли 1 уровня.!", 10, 130)
        pygame.display.flip()
        pygame.time.wait(4000)  # Подождите 4 секунды, чтобы отобразилось сообщение
    elif balance >= 2000 and level == 2:
        level = 3
        display_text("Поздравляем, вы достигли 2 уровня.!!", 10, 130)
        pygame.display.flip()
        pygame.time.wait(4000)  # Подождите 4 секунды, чтобы отобразилось сообщение
    elif balance >= 3000 and level == 3:
        level = 4
        display_text("Поздравляем, вы достигли 3 уровня.!!!", 10, 130)
        pygame.display.flip()
        pygame.time.wait(4000)  # Подождите 4 секунды, чтобы отобразилось сообщение
         

# Основной цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not spinning:
                # Крутим рулетку
                spinning = True
                result = random.randint(1, 36)
                result_shown = False
                # Добавить результат в список последних результатов
                recent_results.append(result)
                if len(recent_results) > 5:
                    recent_results.pop(0)
            elif event.key == pygame.K_b:
                # Введите ставку
                bet = int(input("Введите вашу ставку: "))
                if bet > balance:
                    print("Ставка превышает ваш баланс.")
                    bet = 0
            elif event.key == pygame.K_t:
                # Выберите тип ставки
                bet_type = input("Выберите тип ставки (black/red): ")

    # Чистый экран с деревянным фоном
    screen.fill(WOODEN_BACKGROUND)

   # Отображение баланса, ставки и уровня
    display_text(f"Баланс: {balance}", 10, 10)
    display_text(f"Ставка: {bet}", 10, 50)
    display_text(f"Уровень: {level}", 10, 90)

    # Отобразить последние результаты
    display_text("Последние 5 результатов:", 10, 170)
    y = 200
    for result in recent_results:
        color = RED if pocket_color(result) == "red" else BLACK
        display_text(f"{result} ({pocket_color(result)})", 10, y, color)
        y += 40

   # Кнопки дисплея темно-зеленого цвета.
    pygame.draw.rect(screen, DARK_GREEN, (20, 400, 280, 50))
    display_text("Крутить рулетку (R)", 20, 410)
    pygame.draw.rect(screen, DARK_GREEN, (20, 470, 280, 50))
    display_text("Ввести ставку (B)", 20, 480)
    pygame.draw.rect(screen, DARK_GREEN, (20, 540, 280, 50))
    display_text("Выбрать тип ставки (T)", 20, 550)


    # Визуализируем вращающееся колесо
    if spinning:
        spin_angle += 5
        if spin_angle > 360 * 3: # Добавляем 3 оборота для реалистичности
            spin_angle = 0
            spinning = False
            result_shown = True
            # Обновить баланс после вращения
            if bet > 0 and pocket_color(result) == bet_type:
                balance += bet * 2  
                bet = 0
            elif bet > 0:
                balance -= bet
                bet = 0
        for i in range(1, 37):
            angle = (i * 10 + spin_angle) % 360
            
            x = SCREEN_WIDTH // 2 + 235 + int(250 * math.cos(math.radians(angle)))
            y = SCREEN_HEIGHT // 2 + int(250 * math.sin(math.radians(angle)))
            color = pocket_color(i)
            if color == "red":
                pygame.draw.ellipse(screen, RED, (x-25, y-25, 50, 50))
            else:
                pygame.draw.ellipse(screen, BLACK, (x-25, y-25, 50, 50))
            text_surface = font.render(str(i), True, WHITE)
            screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))
    else:
       # Статический дисплей колеса
        for i in range(1, 37):
            angle = i * 10
            x = SCREEN_WIDTH // 2 + 235 + int(250 * math.cos(math.radians(angle)))
            y = SCREEN_HEIGHT // 2 + int(250 * math.sin(math.radians(angle)))
            color = pocket_color(i)
            if color == "red":
                pygame.draw.ellipse(screen, RED, (x-25, y-25, 50, 50))
            else:
                pygame.draw.ellipse(screen, BLACK, (x-25, y-25, 50, 50))
            text_surface = font.render(str(i), True, WHITE)
            screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))

   # Отображение результата после вращения соответствующим цветом
    if result and result_shown:
        color = RED if pocket_color(result) == "red" else BLACK
        display_text(f"Результат: {result} ({pocket_color(result)})", 230, 20, color)

    # Проверка и обновление уровня
    check_level()

  # Экран обновления
    pygame.display.flip()