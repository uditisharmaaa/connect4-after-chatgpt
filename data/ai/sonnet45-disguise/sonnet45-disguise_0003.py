import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Create empty board
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
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows with borders
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for j in range(COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * COLS + "+")

# Check if column is valid and not full
def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != " ":
        return False
    return True

# Place checker in column
def place_checker(board, col, checker):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
            return i
    return -1

# Check for win horizontally
def check_horizontal(board, checker):
    for i in range(ROWS):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i][j+1] == checker and board[i][j+2] == checker and board[i][j+3] == checker:
                return True
    return False

# Check for win vertically
def check_vertical(board, checker):
    for i in range(ROWS - 3):
        for j in range(COLS):
            if board[i][j] == checker and board[i+1][j] == checker and board[i+2][j] == checker and board[i+3][j] == checker:
                return True
    return False

# Check for win diagonally (bottom-left to top-right)
def check_diagonal1(board, checker):
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i+1][j+1] == checker and board[i+2][j+2] == checker and board[i+3][j+3] == checker:
                return True
    return False

# Check for win diagonally (top-left to bottom-right)
def check_diagonal2(board, checker):
    for i in range(3, ROWS):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i-1][j+1] == checker and board[i-2][j+2] == checker and board[i-3][j+3] == checker:
                return True
    return False

# Check if player won
def check_win(board, checker):
    if check_horizontal(board, checker):
        return True
    if check_vertical(board, checker):
        return True
    if check_diagonal1(board, checker):
        return True
    if check_diagonal2(board, checker):
        return True
    return False

# Check if board is full (draw)
def check_draw(board):
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
        user_input = input()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Try again.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Try again.")
            continue
        
        col_letter = user_input.upper()
        col = ord(col_letter) - 65
        
        if col < 0 or col >= COLS:
            print("Invalid column. Try again.")
            continue
        
        if not is_valid_move(board, col):
            print("Column is full. Try again.")
            continue
        
        # Place the checker
        place_checker(board, col, checker)
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print("Player " + checker + " won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

play_game()
