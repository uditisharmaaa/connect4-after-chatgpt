import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Initialize the board with empty spaces
def create_board(rows, cols):
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board

# Print the board
def print_board(board):
    os.system('clear')
    rows = len(board)
    cols = len(board[0])
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Print top border
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()
        
        # Print row content
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()

# Get valid column input from player
def get_valid_column(board, player_checker):
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        
        # Check if input is a single uppercase letter
        if len(user_input) != 1 or not user_input.isupper() or not user_input.isalpha():
            print("Invalid input. Please enter a single uppercase letter.")
            continue
        
        # Check if column letter is within range
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index

# Place checker on the board
def place_checker(board, col_index, player_checker):
    rows = len(board)
    
    # Find the lowest empty position in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return True
    
    return False

# Check for 4 in a row horizontally
def check_horizontal_win(board, player_checker):
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False

# Check for 4 in a row vertically
def check_vertical_win(board, player_checker):
    rows = len(board)
    cols = len(board[0])
    
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False

# Check for 4 in a row diagonally (top-left to bottom-right)
def check_diagonal_right_win(board, player_checker):
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False

# Check for 4 in a row diagonally (top-right to bottom-left)
def check_diagonal_left_win(board, player_checker):
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False

# Check if a player has won
def check_win(board, player_checker):
    if check_horizontal_win(board, player_checker):
        return True
    if check_vertical_win(board, player_checker):
        return True
    if check_diagonal_right_win(board, player_checker):
        return True
    if check_diagonal_left_win(board, player_checker):
        return True
    
    return False

# Check if the board is full (draw)
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# Main game loop
def play_game():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        # Get current player's checker
        current_player_checker = players[current_player_index]
        
        # Get valid column input
        col_index = get_valid_column(board, current_player_checker)
        
        # Place checker
        place_checker(board, col_index, current_player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
