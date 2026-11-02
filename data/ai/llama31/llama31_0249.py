import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
DRAW = "It's a draw!"

def create_board():
    """Create a 2D board with dimensions BOARD_ROWS x BOARD_COLS"""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| " + " | ".join(row) + " |")
    print("+---+---+---+---+---+---+---+")

def get_player_checker(player_num):
    """Get the checker for the current player"""
    return CHECKERS[player_num - 1]

def is_valid_input(input_str):
    """Check if the user input is a valid column letter"""
    return input_str.isalpha() and input_str.upper() in "ABCDEFG"

def get_column_index(input_str):
    """Get the column index from the user input"""
    return ord(input_str.upper()) - ord('A')

def is_valid_move(board, col):
    """Check if the move is valid (column not full)"""
    return board[0][col] == " "

def make_move(board, player, col):
    """Make a move on the board"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = get_player_checker(player)
            break

def check_win(board):
    """Check if there's a win on the board"""
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3]!= " ":
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c]!= " ":
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]!= " ":
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3]!= " ":
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    for col in range(BOARD_COLS):
        if board[0][col] == " ":
            return False
    return True

def game():
    board = create_board()
    player = random.randint(1, NUM_PLAYERS)
    while True:
        print_board(board)
        print("Player", get_player_checker(player), "turn")
        input_str = input("Enter a column (A-G): ")
        if not is_valid_input(input_str):
            print("Invalid input. Please try again.")
            continue
        col = get_column_index(input_str)
        if not is_valid_move(board, col):
            print("Column is full. Please try again.")
            continue
        make_move(board, player, col)
        if check_win(board):
            print_board(board)
            print("Player", get_player_checker(player), "won!")
            break
        elif check_draw(board):
            print_board(board)
            print(DRAW)
            break
        player = (player % NUM_PLAYERS) + 1

game()
