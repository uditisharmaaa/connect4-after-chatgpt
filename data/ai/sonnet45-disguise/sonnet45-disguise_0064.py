import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Create the board
def create_board():
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

# Print the board
def print_board(board):
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        letter = chr(65 + i)
        print(letter + "   ", end="")
    print()
    
    # Print rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for j in range(COLS):
            print(" " + board[i][j] + " |", end="")
        print()
    print("+---" * COLS + "+")

# Place checker in column
def place_checker(board, col, checker):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
            return True
    return False

# Check if column is valid
def is_valid_column(col_letter):
    if len(col_letter) != 1:
        return False
    if col_letter < 'A' or col_letter > chr(65 + COLS - 1):
        return False
    return True

# Check for horizontal win
def check_horizontal(board, checker):
    for i in range(ROWS):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i][j+1] == checker and board[i][j+2] == checker and board[i][j+3] == checker:
                return True
    return False

# Check for vertical win
def check_vertical(board, checker):
    for i in range(ROWS - 3):
        for j in range(COLS):
            if board[i][j] == checker and board[i+1][j] == checker and board[i+2][j] == checker and board[i+3][j] == checker:
                return True
    return False

# Check for diagonal win (down-right)
def check_diagonal_right(board, checker):
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i+1][j+1] == checker and board[i+2][j+2] == checker and board[i+3][j+3] == checker:
                return True
    return False

# Check for diagonal win (down-left)
def check_diagonal_left(board, checker):
    for i in range(ROWS - 3):
        for j in range(3, COLS):
            if board[i][j] == checker and board[i+1][j-1] == checker and board[i+2][j-2] == checker and board[i+3][j-3] == checker:
                return True
    return False

# Check if player won
def check_win(board, checker):
    if check_horizontal(board, checker):
        return True
    if check_vertical(board, checker):
        return True
    if check_diagonal_right(board, checker):
        return True
    if check_diagonal_left(board, checker):
        return True
    return False

# Check if board is full
def is_board_full(board):
    for j in range(COLS):
        if board[0][j] == " ":
            return False
    return True

# Main game
def play_game():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        checker = CHECKERS[current_player]
        
        valid_move = False
        while not valid_move:
            col_input = input("Player " + checker + ", please enter a column: ")
            
            if not is_valid_column(col_input):
                print("Invalid input. Please try again.")
                continue
            
            col = ord(col_input) - 65
            
            if place_checker(board, col, checker):
                valid_move = True
            else:
                print("Column is full. You lose your turn.")
                valid_move = True
        
        print_board(board)
        
        if check_win(board, checker):
            print("Player " + checker + " won!")
            game_over = True
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

play_game()
