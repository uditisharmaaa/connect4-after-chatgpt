import os
import random

# Constant global variables
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# Checkers for each player
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with all elements initialized to whitespace"""
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the board with column labels"""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---" * BOARD_COLS)
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS)

def is_valid_input(input_str):
    """Check if the input is a valid column letter"""
    return input_str.isalpha() and input_str.upper() in "ABCDEFG"

def get_player_checker(player_num):
    """Get the checker for the given player number"""
    return CHECKERS[player_num - 1]

def drop_checker(board, player_num, col):
    """Drop the checker in the specified column"""
    checker = get_player_checker(player_num)
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            break

def check_win(board, player_num):
    """Check if the given player has won"""
    checker = get_player_checker(player_num)
    # Check horizontal wins
    for row in board:
        for i in range(BOARD_COLS - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == checker:
                return True
    # Check vertical wins
    for col in range(BOARD_COLS):
        for i in range(BOARD_ROWS - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == checker:
                return True
    # Check diagonal wins
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True
            if board[row][col+3] == board[row+1][col+2] == board[row+2][col+1] == board[row+3][col] == checker:
                return True
    return False

def check_draw(board):
    """Check if the board is full (draw)"""
    return all(all(cell!= " " for cell in row) for row in board)

def game_loop():
    """Main game loop"""
    board = create_board()
    players = list(range(1, NUM_PLAYERS + 1))
    random.shuffle(players)
    current_player = players.pop(0)
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-G):")
        input_str = input().upper()
        if not is_valid_input(input_str):
            print("Invalid input. Please try again.")
            continue
        col = ord(input_str) - ord('A')
        if all(cell!= " " for cell in [row[col] for row in board]):
            print("Column is full. Please try again.")
            continue
        drop_checker(board, current_player, col)
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        players.append(current_player)
        current_player = players.pop(0)

game_loop()
