import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]

# Initialize board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print board
def print_board(board):
    os.system('clear')  # or 'cls' for Windows
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+" + "---+" * COLUMNS)

# Validate user input
def is_valid_input(column_input):
    return column_input in COLUMN_LABELS

# Drop checker
def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

# Check for a win
def check_win(board, checker):
    # Horizontal, vertical, positive diagonal, and negative diagonal directions
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == checker:
                for dr, dc in directions:
                    count = 0
                    for step in range(4):
                        r, c = row + step * dr, col + step * dc
                        if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                            count += 1
                        else:
                            break
                    if count == 4:
                        return True

    return False

# Check for draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Play game
def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player]
        move_made = False
        while not move_made:
            column_input = input(f"Player {current_checker}, please enter a column: ").upper()
            if not is_valid_input(column_input):
                print("Invalid input. Please enter a valid column.")
                continue
            
            column_index = ord(column_input) - 65
            if drop_checker(board, column_index, current_checker):
                move_made = True
            else:
                print("Column is full. Please choose another column.")

        print_board(board)
        
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw.")
            break
        
        current_player = (current_player + 1) % PLAYERS

# Start Game
if __name__ == "__main__":
    play_game()
