import os
import random

# Constants for game setup
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Set between 2 and 5

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print(' A B C D E F G')
    for row in board:
        print('|'.join(row))
        print('-' * (2 * COLUMNS - 1))

def get_column_choice():
    col = input(f"Choose a column (A-G): ").upper()
    return ord(col) - ord('A') if col in 'ABCDEFG' else -1

def place_piece(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return True
    return False

def check_win(board, player):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c + 3 < COLUMNS and all(board[r][c + i] == player for i in range(4)) or
                r + 3 < ROWS    and all(board[r + i][c] == player for i in range(4)) or
                c + 3 < COLUMNS and r + 3 < ROWS and all(board[r + i][c + i] == player for i in range(4)) or
                c - 3 >= 0      and r + 3 < ROWS and all(board[r + i][c - i] == player for i in range(4))):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def start_game():
    board = create_board()
    current_player = random.choice(PLAYERS[:NUM_PLAYERS])
    while True:
        print_board(board)
        col = get_column_choice()
        if col == -1 or not place_piece(board, col, current_player):
            print("Invalid move. Try again.")
            continue
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    start_game()
