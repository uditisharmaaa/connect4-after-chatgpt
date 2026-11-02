import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players
EMPTY = ' '

# Initialize the board
def create_board():
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLUMNS)

# Check for valid column input
def validate_input(column):
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(64 + COLUMNS)

# Place the checker in the board
def place_checker(player_index, column, board):
    col_idx = ord(column) - 65
    for row in reversed(board):
        if row[col_idx] == EMPTY:
            row[col_idx] = CHECKERS[player_index]
            return True
    return False

# Check for a win condition
def check_win(board, player_index):
    checker = CHECKERS[player_index]
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (
                c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4)) or  # Horizontal
                r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)) or  # Vertical
                r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == checker for i in range(4)) or  # Diagonal /
                r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4))    # Diagonal \
            ):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(cell != EMPTY for row in board for cell in row)

# Main game function
def connect_4():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column = input().strip().upper()
        
        if not validate_input(column):
            print("Invalid input, try again.")
            continue

        if not place_checker(current_player, column, board):
            print("Column is full, try again.")
            continue
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    connect_4()
