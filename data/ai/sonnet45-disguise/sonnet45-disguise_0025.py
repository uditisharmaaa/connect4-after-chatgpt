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
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for row in board:
        print("+---" * COLS + "+")
        print("| ", end="")
        for cell in row:
            print(cell + " | ", end="")
        print()
    print("+---" * COLS + "+")

# Place a checker in a column
def place_checker(board, col, checker):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
            return True
    return False

# Check if column is valid
def is_valid_column(col):
    if col >= 0 and col < COLS:
        return True
    return False

# Check for win horizontally
def check_horizontal(board, checker):
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True
    return False

# Check for win vertically
def check_vertical(board, checker):
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    return False

# Check for win diagonally (positive slope)
def check_diagonal_positive(board, checker):
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    return False

# Check for win diagonally (negative slope)
def check_diagonal_negative(board, checker):
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    return False

# Check if a player won
def check_win(board, checker):
    if check_horizontal(board, checker):
        return True
    if check_vertical(board, checker):
        return True
    if check_diagonal_positive(board, checker):
        return True
    if check_diagonal_negative(board, checker):
        return True
    return False

# Check if the board is full (draw)
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# Main game function
def play_game():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        # Get player input
        valid_input = False
        while not valid_input:
            user_input = input("Player " + players[current_player] + ", please enter a column: ")
            
            # Check if input is valid
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            
            if not user_input.isalpha():
                print("Invalid input. Please enter a letter.")
                continue
            
            col_letter = user_input.upper()
            col_index = ord(col_letter) - 65
            
            if not is_valid_column(col_index):
                print("Invalid column. Please enter a valid column letter.")
                continue
            
            # Try to place the checker
            if place_checker(board, col_index, players[current_player]):
                valid_input = True
            else:
                print("Column is full. You lose your turn.")
                valid_input = True
        
        print_board(board)
        
        # Check for win
        if check_win(board, players[current_player]):
            print("Player " + players[current_player] + " won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS

play_game()
