import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" + "+---" * (COLUMNS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLUMNS - 1) + "+")

# Check if a move is valid
def is_valid_move(board, column):
    if column < 0 or column >= COLUMNS:
        return False
    return board[0][column] == " "

# Place a checker in the board
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

# Check for a win (4 in a row)
def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

# Main game loop
def connect4():
    board = create_board()
    players_count = 2
    checkers = PLAYERS[:players_count]
    current_player = random.choice(checkers)
    
    print_board(board)

    while True:
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").strip().upper()
        
        if col_input not in chr(65 + i) for i in range(COLUMNS):
            print("Invalid input. Please enter a valid column (A-G).")
            continue
        
        column = ord(col_input) - 65

        if is_valid_move(board, column):
            place_checker(board, column, current_player)
            print_board(board)

            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            if check_draw(board):
                print("The game is a draw!")
                break
            
            # Switch players
            current_index = checkers.index(current_player)
            current_player = checkers[(current_index + 1) % players_count]
        else:
            print("Column is full! Try a different column.")

if __name__ == "__main__":
    connect4()
