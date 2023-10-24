import pygame
import sys
import random

print("Enter 'r' for 'REPLAY'")
print("Enter 'q' for 'QUIT'")
pygame.init()

WIDTH, HEIGHT = 500, 500
LINE_COLOR = (0, 0, 0)
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE
PLAYER_X = 'X'
PLAYER_O = 'O'

WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

def initialize_game():
    global board, current_player, game_over
    board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = PLAYER_X
    game_over = False

initialize_game()

def draw_grid():
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), 2)
        pygame.draw.line(screen, LINE_COLOR, (row * CELL_SIZE, 0), (row * CELL_SIZE, HEIGHT), 2)

def draw_symbols():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == PLAYER_X:
                pygame.draw.line(screen, LINE_COLOR, (col * CELL_SIZE, row * CELL_SIZE), ((col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE), 2)
                pygame.draw.line(screen, LINE_COLOR, ((col + 1) * CELL_SIZE, row * CELL_SIZE), (col * CELL_SIZE, (row + 1) * CELL_SIZE), 2)
            elif board[row][col] == PLAYER_O:
                pygame.draw.circle(screen, LINE_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5, 2)

def check_win(player):
    for i in range(GRID_SIZE):
        if all(board[i][j] == player for j in range(GRID_SIZE)) or all(board[j][i] == player for j in range(GRID_SIZE)):
            return True
    if all(board[i][i] == player for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - i - 1] == player for i in range(GRID_SIZE)):
        return True
    return False

def check_draw():
    return all(board[i][j] != ' ' for i in range(GRID_SIZE) for j in range(GRID_SIZE))

def make_move(row, col):
    global current_player
    if board[row][col] == ' ':
        board[row][col] = current_player
        current_player = PLAYER_X if current_player == PLAYER_O else PLAYER_O

def minimax(board, depth, is_maximizing):
    scores = {'X': -1, 'O': 1, 'draw': 0}
    
    if check_win(PLAYER_X):
        return scores['X']
    if check_win(PLAYER_O):
        return scores['O']
    if check_draw():
        return scores['draw']

    if is_maximizing:
        best_score = float('-inf')
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == ' ':
                    board[row][col] = PLAYER_O
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == ' ':
                    board[row][col] = PLAYER_X
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ' '
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = float('-inf')
    best_move = None
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == ' ':
                board[row][col] = PLAYER_O
                score = minimax(board, 0, False)
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        make_move(best_move[0], best_move[1])

def draw_end_game_message(winner):
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT))
    font = pygame.font.Font(None, 36)
    text = None
    if winner == PLAYER_X:
        text = font.render("Player X wins!", True, LINE_COLOR)
    elif winner == PLAYER_O:
        text = font.render("Player O wins!", True, LINE_COLOR)
    elif winner == 'draw':
        text = font.render("It's a draw!", True, LINE_COLOR)
    if text:
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
    pygame.display.flip()

play_again = True

while play_again:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE and board[row][col] == ' ':
                    make_move(row, col)
                    if check_win(current_player):
                        game_over = True
                    elif check_draw():
                        game_over = True

        if not game_over and current_player == PLAYER_O:
            ai_move()

        screen.fill(WHITE)
        draw_grid()
        draw_symbols()

        if game_over:
            draw_end_game_message(current_player if check_win(current_player) else 'draw')

        pygame.display.flip()

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    initialize_game()
                    game_over = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        if not game_over:
            break
