import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input(player):
    while True:
        user_input = input(f"Player {player}, please enter a column: ").upper()
        if len(user_input) != 1 or user_input not in [chr(65 + i) for i in range(COLS)]:
            print("Invalid input. Please choose a valid column (A-G).")
        else:
            return ord(user_input) - 65  # Convert 'A' to 0, 'B' to 1, etc.

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    def check_direction(start_row, start_col, delta_row, delta_col):
        count = 0
        for _ in range(4):
            if 0 <= start_row < ROWS and 0 <= start_col < COLS and board[start_row][start_col] == checker:
                count += 1
                start_row += delta_row
                start_col += delta_col
            else:
                break
        return count
    
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                if (check_direction(r, c, 0, 1) >= 4 or  # Horizontal
                    check_direction(r, c, 1, 0) >= 4 or  # Vertical
                    check_direction(r, c, 1, 1) >= 4 or  # Diagonal down-right
                    check_direction(r, c, 1, -1) >= 4): # Diagonal down-left
                    return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def connect4_game():
    board = create_board()
    current_player = random.choice(range(len(PLAYERS)))
    
    while True:
        print_board(board)
        column = get_valid_input(PLAYERS[current_player])
        
        if not place_checker(board, column, PLAYERS[current_player]):
            print("Column full! Try a different column.")
            continue
        
        if check_win(board, PLAYERS[current_player]):
            print_board(board)
            print(f"Player {PLAYERS[current_player]} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % len(PLAYERS)  # Switch to next player

if __name__ == "__main__":
    connect4_game()
