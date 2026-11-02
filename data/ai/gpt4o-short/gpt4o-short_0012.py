import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:5]  # Adjust player count based on max 5
COLUMN_LABELS = 'ABCDEFG'

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the console
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|'.join(row))
    print('-' * (2 * COLUMNS - 1))

def get_column_index(label):
    try:
        return COLUMN_LABELS.index(label.upper())
    except ValueError:
        return -1

def make_move(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return True
    return False

def is_valid_move(board, col):
    return 0 <= col < COLUMNS and board[0][col] == ' '

def check_for_winner(board, player):
    # Check horizontal, vertical, and diagonal (both directions) for a win
    ranges = [(0, COLUMNS - 3), (0, ROWS - 3)]
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == player:
                for dr, dc in directions:
                    if all(board[r + dr * i][c + dc * i] == player for i in range(4)):
                        return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def pick_random_player(players):
    return random.choice(players)

def play_game():
    board = create_board()
    current_player = pick_random_player(PLAYERS)
    print(f"Starting player: {current_player}")

    while True:
        print_board(board)
        move = input(f"Player {current_player}, enter column (A-G): ").strip()
        col = get_column_index(move)

        if not is_valid_move(board, col):
            print("Invalid move! Try again.")
            continue

        make_move(board, col, current_player)

        if check_for_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    play_game()
