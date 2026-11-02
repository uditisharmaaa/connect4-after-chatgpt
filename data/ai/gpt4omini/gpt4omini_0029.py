import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+".join("-" for _ in range(COLS)) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+".join("-" for _ in range(COLS)) + "+")

def is_valid_input(col):
    return col.isalpha() and col.isupper() and ord(col) - 65 < COLS

def get_col_index(input_col):
    return ord(input_col) - 65

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for row in board:
        for c in range(COLS - 3):
            if all(row[c + i] == player for i in range(4)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print_board(board)
    
    while True:
        current_player = PLAYERS[current_player_index]
        input_col = input(f"Player {current_player}, please enter a column: ").strip()

        if not is_valid_input(input_col):
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue

        col_index = get_col_index(input_col)
        if not place_checker(board, col_index, current_player):
            print("Column is full. Please choose another column.")
            continue

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
