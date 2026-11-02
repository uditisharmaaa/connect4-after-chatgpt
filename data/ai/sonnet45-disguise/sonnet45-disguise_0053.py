import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

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
    # Print column letters
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for j in range(COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * COLS + "+")

# Drop checker in column
def drop_checker(board, col, checker):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
            return True
    return False

# Check if column is valid
def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != " ":
        return False
    return True

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

# Check for win diagonally (positive slope)
def check_diagonal_pos(board, checker):
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == checker and board[i+1][j+1] == checker and board[i+2][j+2] == checker and board[i+3][j+3] == checker:
                return True
    return False

# Check for win diagonally (negative slope)
def check_diagonal_neg(board, checker):
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
    if check_diagonal_pos(board, checker):
        return True
    if check_diagonal_neg(board, checker):
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
    checkers = ["X", "O", "V", "H", "M"]
    players = []
    for i in range(NUM_PLAYERS):
        players.append(checkers[i])
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    
    while True:
        checker = players[current_player]
        print("Player " + checker + ", please enter a column: ", end="")
        user_input = input()
        
        # Check if input is valid
        if len(user_input) != 1:
            print("Invalid input. Try again.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Try again.")
            continue
        
        user_input = user_input.upper()
        col = ord(user_input) - 65
        
        if not is_valid_move(board, col):
            print("Invalid move. Try again.")
            continue
        
        # Drop the checker
        drop_checker(board, col, checker)
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print("Player " + checker + " won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

play_game()
