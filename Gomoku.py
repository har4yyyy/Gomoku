import pygame
import sys
import os

# Settings
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (188, 122, 66)
TEXT_COLOR = (245, 245, 245)

BOARD_SIZE = 16
CELL_SIZE = 40
MARGIN = 22
TOP = 50
HEIGHT = (BOARD_SIZE-1) * CELL_SIZE + 2 * MARGIN + TOP
WIDTH = (BOARD_SIZE-1) * CELL_SIZE + 2 * MARGIN
VALID_RADIUS = 16

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
def get_player(player):
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
        ver_start_pos = (MARGIN + i * CELL_SIZE, MARGIN + TOP)
        ver_end_pos = (MARGIN + i * CELL_SIZE, HEIGHT - MARGIN)
        pygame.draw.line(screen, color, ver_start_pos, ver_end_pos)
        hor_start_pos = (MARGIN, TOP + MARGIN + i * CELL_SIZE)
        hor_end_pos = (WIDTH - MARGIN, TOP + MARGIN + i * CELL_SIZE)
        pygame.draw.line(screen, color, hor_start_pos, hor_end_pos)

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col]:
                color = BLACK if board[row][col] == 'Black' else WHITE
                pos = (MARGIN + col * CELL_SIZE, TOP + MARGIN + row * CELL_SIZE)
                pygame.draw.circle(screen, color, pos, CELL_SIZE // 2 - 3)

def show_status(text):
    font = pygame.font.Font(FONT_PATH, 36)
    text_surface = font.render(text, True, BLACK if current_player == 'Black' else WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, (TOP+MARGIN) // 2))
    screen.blit(text_surface, text_rect)

def show_winner_popup(winner):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent
    screen.blit(overlay, (0, 0))

    popup_width = 400
    popup_height = 200
    popup_rect = pygame.Rect((WIDTH - popup_width) // 2, (HEIGHT - popup_height) // 2, popup_width, popup_height)
    pygame.draw.rect(screen, (52, 95, 161, 0), popup_rect)

    font = pygame.font.Font(FONT_PATH, 40)
    test = font.render(f"{winner} HAS WON!", True, BLACK if current_player == 'Black' else WHITE)
    text_rect = test.get_rect(center=popup_rect.center)
    screen.blit(test, text_rect)

    small_font = pygame.font.Font(FONT_PATH, 20)
    tip_text = small_font.render("PLS Press any Botton to Restart", True, BLACK if current_player == 'Black' else WHITE)
    tip_text_rect = tip_text.get_rect(center=(WIDTH // 2, popup_rect.bottom - 30))
    screen.blit(tip_text, tip_text_rect)

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
                row = round((y - MARGIN - TOP) / CELL_SIZE)

                cross_x = col * CELL_SIZE + MARGIN
                cross_y = row * CELL_SIZE + MARGIN + TOP

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
    player = get_player(current_player)
    if game_over:
        show_status("GAME OVER")
        show_winner_popup(player)
    else:
        show_status(f"{player}'s Turn")
    pygame.display.flip()