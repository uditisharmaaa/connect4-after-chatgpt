import os
import random

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for players (up to 5)

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    print('  ' + '   '.join(chr(65 + i) for i in range(cols)))
    print('+---' * cols + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * cols + '+')

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def is_valid_column(board, col):
    if col < 0 or col >= len(board[0]) or board[0][col] != ' ':
        return False
    return True

def check_winner(board, player):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] == player:
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == player:
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] == player:
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] == player:
                return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def get_column_input(board):
    while True:
        col_input = input("Please enter a column (A-G): ").strip()
        if len(col_input) == 1 and col_input.isalpha():
            col_index = ord(col_input.upper()) - 65
            if is_valid_column(board, col_index):
                return col_index
        print("Invalid input. Try again!")

def connect_4():
    # Initialization
    num_players = 2
    board = create_board(ROW_COUNT, COLUMN_COUNT)
    players = PLAYERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    
    clear_screen()
    print("Welcome to Connect 4!")
    print(f"Starting with Player {players[current_player_index]}\n")
    print_board(board)

    # Game loop
    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, it's your turn.")
        col = get_column_input(board)
        
        drop_checker(board, col, current_player)
        clear_screen()
        print_board(board)

        # Check for win or draw
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

if __name__ == '__main__':
    connect_4()
