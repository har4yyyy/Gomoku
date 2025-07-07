import pygame
import sys
import os

# Settings
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (188, 122, 66)
TEXT_COLOR = (255, 0, 0)

BOARD_SIZE = 15
CELL_SIZE = 40
MARGIN = 16
WIDTH = HEIGHT = BOARD_SIZE * CELL_SIZE + 2 * MARGIN
VALID_RADIUS = 20

FONT_PATH = os.path.join(os.path.dirname(__file__), 'font.ttf')
if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Font file not found at {FONT_PATH}")
    sys.exit(1)
else :
    print(f"Font file found at {FONT_PATH}")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gomoku")

board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
current_player = 'Black'
game_over = False

# Functions
def get_chinese_player(player):
    return 'BLACK' if player == 'Black' else 'WHITE'

def check_winner(rol, col, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 0
        for step in range(-4, 5):
            r = rol + step * dr
            c = col + step * dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0
    return False

def draw_board():
    screen.fill(BOARD_COLOR)
    color = BLACK

    for i in range(BOARD_SIZE):
        ver_start_pos = (MARGIN + i * CELL_SIZE, MARGIN)
        ver_end_pos = (MARGIN + i * CELL_SIZE, HEIGHT - MARGIN)
        pygame.draw.line(screen, color, ver_start_pos, ver_end_pos)
        hor_start_pos = (MARGIN, MARGIN + i * CELL_SIZE)
        hor_end_pos = (WIDTH - MARGIN, MARGIN + i * CELL_SIZE)
        pygame.draw.line(screen, color, hor_start_pos, hor_end_pos)

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col]:
                color = BLACK if board[row][col] == 'Black' else WHITE
                pos = (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE)
                pygame.draw.circle(screen, color, pos, CELL_SIZE // 2 - 2)

def show_status(text):
    font = pygame.font.Font(FONT_PATH, 36)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, MARGIN))
    screen.blit(text_surface, text_rect)

def show_winner_popup(winner):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent
    screen.blit(overlay, (0, 0))

    popup_width = 400
    popup_height = 200
    popup_rect = pygame.Rect((WIDTH - popup_width) // 2, (HEIGHT - popup_height) // 2, popup_width, popup_height)
    pygame.draw.rect(screen, WHITE, popup_rect)

    font = pygame.font.Font(FONT_PATH, 36)
    test = font.render(f"{winner} HAS WON!", True, TEXT_COLOR)
    text_rect = test.get_rect(center=popup_rect.center)
    screen.blit(test, text_rect)

    small_font = pygame.font.Font(FONT_PATH, 24)
    tip_text = small_font.render("PLS Press any Botton to Restart", True, TEXT_COLOR)
    screen.blit(tip_text, tip_text.get_rect(center = (WIDTH // 2, HEIGHT - MARGIN)))

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
                current_player = 'Black'
                game_over = False
            else:
                x, y = event.pos
                col = round((x - MARGIN) / CELL_SIZE)
                row = round((y - MARGIN) / CELL_SIZE)

                cross_x = col * CELL_SIZE + MARGIN
                cross_y = row * CELL_SIZE + MARGIN

                dx = x - cross_x
                dy = y - cross_y
                distance_sq = dx ** 2 + dy ** 2
                if (distance_sq <= VALID_RADIUS ** 2
                        and 0 <= col < BOARD_SIZE
                        and 0 <= row < BOARD_SIZE):
                    if board[row][col] is None:
                        board[row][col] = current_player
                        if check_winner(row, col, current_player):
                            game_over = True
                        else:
                            current_player = 'White' if current_player == 'Black' else 'Black'

    draw_board()
    chinese_player = get_chinese_player(current_player)
    if game_over:
        show_status(f"GAME OVER - {chinese_player} HAS WON!")
        show_winner_popup(chinese_player)
    else:
        show_status(f"{chinese_player}'s Turn")
    pygame.display.flip()