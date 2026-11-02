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

# Place checker in column
def place_checker(board, col, checker):
    # Find the lowest available row
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
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        checker = players[current_player]
        print("Player " + checker + ", please enter a column: ", end="")
        col_input = input().upper()
        
        # Validate input
        while not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column: ", end="")
            col_input = input().upper()
        
        col = ord(col_input) - 65
        
        # Try to place checker
        if place_checker(board, col, checker):
            print_board(board)
            
            # Check for win
            if check_win(board, checker):
                print("Player " + checker + " won!")
                game_over = True
            elif is_board_full(board):
                print("It's a draw!")
                game_over = True
            else:
                # Next player
                current_player = (current_player + 1) % NUM_PLAYERS
        else:
            print("Column is full. You lose your turn.")
            print_board(board)
            current_player = (current_player + 1) % NUM_PLAYERS

play_game()
