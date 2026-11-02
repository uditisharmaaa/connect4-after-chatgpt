import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers A to G
    print("+---" + "---+" * (COLS - 1) + "---+")  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row content
        print("+---" + "---+" * (COLS - 1) + "---+")  # Row border

def choose_first_player(num_players):
    return random.randint(0, num_players - 1)

def is_valid_input(column_input):
    return len(column_input) == 1 and column_input.isalpha() and 'A' <= column_input <= chr(65 + COLS - 1)

def get_column_index(column_input):
    return ord(column_input) - 65

def is_column_full(board, col):
    return board[0][col] != ' '

def find_lowest_empty_row(board, col):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            return row
    return -1  # This technically shouldn't happen if we check for full column

def drop_checker(board, col, player):
    row = find_lowest_empty_row(board, col)
    board[row][col] = player

def check_win(board, player):
    # Check horizontal, vertical and diagonal wins
    # Horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            count = count + 1 if board[r][c] == player else 0
            if count >= 4:
                return True

    # Vertical
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            count = count + 1 if board[r][c] == player else 0
            if count >= 4:
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if r + 3 < ROWS and c - 3 >= 0 and \
                   all(board[r + i][c - i] == player for i in range(4)):
                    return True

    # Diagonal (top-left to bottom-right)
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if r - 3 >= 0 and c - 3 >= 0 and \
                   all(board[r - i][c - i] == player for i in range(4)):
                    return True
    
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def connect4():
    board = initialize_board()
    num_players = min(MAX_PLAYERS, len(PLAYERS))
    current_player_index = choose_first_player(num_players)
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        valid_move = False
        while not valid_move:
            column_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
            if is_valid_input(column_input):
                col = get_column_index(column_input)
                if not is_column_full(board, col):
                    drop_checker(board, col, current_player)
                    valid_move = True
                else:
                    print("Column is full! Please choose another column.")
            else:
                print("Invalid input. Please enter a valid column letter.")

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    connect4()
