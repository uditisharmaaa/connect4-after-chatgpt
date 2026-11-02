import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal before printing the board
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_column():
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1 or ord(col_input) < 65 or ord(col_input) >= 65 + COLS:
            print("Invalid input! Please enter a letter from A to " + chr(65 + COLS - 1) + ".")
        else:
            return ord(col_input) - 65

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                if check_directions(board, r, c, checker):
                    return True
    return False

def check_directions(board, row, col, checker):
    # Check for win in all directions: horizontal, vertical, diagonal right, diagonal left
    return (check_direction(board, row, col, checker, 1, 0) or  # Horizontal
            check_direction(board, row, col, checker, 0, 1) or  # Vertical
            check_direction(board, row, col, checker, 1, 1) or  # Diagonal right
            check_direction(board, row, col, checker, 1, -1)    # Diagonal left
           )

def check_direction(board, row, col, checker, delta_row, delta_col):
    count = 0
    for i in range(4):
        r = row + i * delta_row
        c = col + i * delta_col
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
        else:
            break
    return count == 4

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Game initialization
board = create_board()
players = PLAYER_CHECKERS[:2]  # Set to 2 players for submission
current_player_index = random.randint(0, len(players) - 1)

# Main game loop
while True:
    print_board(board)
    current_player = players[current_player_index]
    col = get_valid_column()
    
    if not place_checker(board, col, current_player):
        print("Column is full! Try again.")
        continue
    
    if check_win(board, current_player):
        print_board(board)
        print(f"Player {current_player} won!")
        break

    if check_draw(board):
        print_board(board)
        print("The game is a draw!")
        break
    
    current_player_index = (current_player_index + 1) % len(players)
