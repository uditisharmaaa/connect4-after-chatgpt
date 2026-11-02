import random
import os

# Constants
NUM_COLUMNS = 7
NUM_ROWS = 6
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Initialization function to create an empty board
def create_board(num_rows, num_columns):
    board = [[' ' for _ in range(num_columns)] for _ in range(num_rows)]
    return board

# Function to print the board
def print_board(board):
    os.system('clear')
    column_labels = [chr(i) for i in range(ord('A'), ord('A') + len(board[0]))]
    print('  ' + '   '.join(column_labels))
    print('+' + '---+' * len(board[0]))
    
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

# Function to drop a checker into the board
def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

# Function to check for a win condition
def check_winner(board, num_to_win, checkers):
    num_rows = len(board)
    num_columns = len(board[0])

    # Check horizontally
    for row in board:
        for col in range(num_columns - num_to_win + 1):
            if all(row[col + i] == checkers for i in range(num_to_win)):
                return True
                
    # Check vertically
    for col in range(num_columns):
        for row in range(num_rows - num_to_win + 1):
            if all(board[row + i][col] == checkers for i in range(num_to_win)):
                return True
                
    # Check diagonally (/)
    for row in range(num_rows - num_to_win + 1):
        for col in range(num_columns - num_to_win + 1):
            if all(board[row + i][col + i] == checkers for i in range(num_to_win)):
                return True
                
    # Check diagonally (\)
    for row in range(num_rows - num_to_win + 1):
        for col in range(num_to_win - 1, num_columns):
            if all(board[row + i][col - i] == checkers for i in range(num_to_win)):
                return True
                
    return False

# Function to check for a draw condition
def check_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

# Main game function
def connect_four_game(num_players=MIN_PLAYERS, num_rows=NUM_ROWS, num_columns=NUM_COLUMNS):
    checkers = ['X', 'O', 'V', 'H', 'M'][:num_players]
    board = create_board(num_rows, num_columns)
    current_player_idx = random.randint(0, num_players - 1)
    
    print_board(board)
    
    while True:
        current_checker = checkers[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")
        column_input = input().strip().upper()

        if not column_input.isalpha() or len(column_input) != 1:
            print("Invalid input. Please enter a valid column letter.")
            continue

        column_idx = ord(column_input) - ord('A')
        
        if column_idx < 0 or column_idx >= num_columns:
            print("Column out of range. Please enter a valid column letter.")
            continue
        
        if not drop_checker(board, column_idx, current_checker):
            print("Column is full. You lost your turn.")
        else:
            print_board(board)
            
            if check_winner(board, 4, current_checker):
                print(f"Player {current_checker} won!")
                break
                
            if check_draw(board):
                print("The game is a draw!")
                break
                
        current_player_idx = (current_player_idx + 1) % num_players

# Run the game with 2 players and 6x7 board dimensions.
connect_four_game()
