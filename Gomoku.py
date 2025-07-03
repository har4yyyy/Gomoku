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
MARGIN = 20
WIDTH = HEIGHT = BOARD_SIZE * CELL_SIZE + 2 * MARGIN
VALID_RADIUS = 15

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

# Function to Draw the Board
def draw_board():
    screen.fill(BOARD_COLOR)

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
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - MARGIN // 2))
    screen.blit(text_surface, text_rect)

def show_winner_popup(winner):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent
    screen.blit(overlay, (0, 0))

    popup_width = 400
    popup_height = 200
    popup_rect = pygame.Rect((WIDTH - popup_width) // 2, (HEIGHT - popup_height) // 2, popup_width, popup_height)
    pygame.draw.rect(screen, WHITE, popup_rect)