import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    
    # Print column letters
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_column(col_letter, board):
    if len(col_letter) != 1:
        return False
    if not col_letter.isalpha():
        return False
    if not col_letter.isupper():
        return False
    
    col_num = ord(col_letter) - 65
    
    if col_num < 0 or col_num >= COLS:
        return False
    
    if board[0][col_num] != " ":
        return False
    
    return True

def place_checker(board, col_letter, checker):
    col_num = ord(col_letter) - 65
    
    for i in range(ROWS - 1, -1, -1):
        if board[i][col_num] == " ":
            board[i][col_num] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for i in range(ROWS):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i][j+1] == checker and board[i][j+2] == checker and board[i][j+3] == checker:
                return True
    
    # Check vertical
    for i in range(ROWS - 3):
        for j in range(COLS):
            if board[i][j] == checker and board[i+1][j] == checker and board[i+2][j] == checker and board[i+3][j] == checker:
                return True
    
    # Check diagonal (down-right)
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i+1][j+1] == checker and board[i+2][j+2] == checker and board[i+3][j+3] == checker:
                return True
    
    # Check diagonal (down-left)
    for i in range(ROWS - 3):
        for j in range(3, COLS):
            if board[i][j] == checker and board[i+1][j-1] == checker and board[i+2][j-2] == checker and board[i+3][j-3] == checker:
                return True
    
    return False

def is_board_full(board):
    for j in range(COLS):
        if board[0][j] == " ":
            return False
    return True

def play_game():
    board = create_board()
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    
    while not game_over:
        checker = CHECKERS[current_player]
        
        print(f"Player {checker}, please enter a column: ", end="")
        col_input = input()
        
        if not is_valid_column(col_input, board):
            print("Invalid input. Try again.")
            continue
        
        place_checker(board, col_input, checker)
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            game_over = True
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

play_game()
