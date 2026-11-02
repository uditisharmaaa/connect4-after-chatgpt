import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board with empty spaces
def create_board():
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

# Print the board with column labels and borders
def print_board(board):
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i), end="   ")
    print()
    
    # Print board with borders
    for row_idx, row in enumerate(board):
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
    print("+---" * COLS + "+")

# Convert column letter to index
def column_letter_to_index(letter):
    return ord(letter) - 65

# Check if input is valid
def is_valid_input(user_input):
    if len(user_input) != 1:
        return False
    
    if not user_input.isalpha():
        return False
    
    col_index = column_letter_to_index(user_input.upper())
    
    if col_index < 0 or col_index >= COLS:
        return False
    
    return True

# Check if column is full
def is_column_full(board, col_index):
    return board[0][col_index] != " "

# Place checker in column
def place_checker(board, col_index, checker):
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_index] == " ":
            board[row_idx][col_index] = checker
            return True
    return False

# Check for win horizontally
def check_horizontal_win(board, checker):
    for row in board:
        for col in range(COLS - WIN_LENGTH + 1):
            if all(row[col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

# Check for win vertically
def check_vertical_win(board, checker):
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False

# Check for win diagonally (top-left to bottom-right)
def check_diagonal_right_win(board, checker):
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

# Check for win diagonally (top-right to bottom-left)
def check_diagonal_left_win(board, checker):
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

# Check if player won
def check_win(board, checker):
    return (check_horizontal_win(board, checker) or
            check_vertical_win(board, checker) or
            check_diagonal_right_win(board, checker) or
            check_diagonal_left_win(board, checker))

# Check if board is full (draw)
def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# Main game loop
def play_game():
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    
    while not game_over:
        current_checker = players[current_player_index]
        
        # Get valid input from player
        valid_move = False
        while not valid_move:
            user_input = input(f"Player {current_checker}, please enter a column: ").upper()
            
            if not is_valid_input(user_input):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = column_letter_to_index(user_input)
            
            if is_column_full(board, col_index):
                print("Column is full. Please choose another column.")
                continue
            
            valid_move = True
        
        # Place checker
        place_checker(board, col_index, current_checker)
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
