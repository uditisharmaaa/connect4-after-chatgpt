import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players

def clear_screen():
    os.system('clear')

def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    column_labels = " ".join([chr(65 + i) for i in range(COLS)])
    print("  " + "   ".join(column_labels))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_valid_column(board, prompt):
    while True:
        col = input(prompt).strip().upper()
        if len(col) == 1 and col.isalpha() and "A" <= col <= chr(65 + COLS - 1):
            col_index = ord(col) - 65
            if board[0][col_index] == " ":
                return col_index
            else:
                print(f"Column {col} is full. Choose another column.")
        else:
            print("Invalid input. Enter a valid column letter.")

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return

def is_winning_move(board, row, col, checker):
    # Check horizontal
    for i in range(max(0, col - 3), min(COLS - 3, col) + 1):
        if all(board[row][j] == checker for j in range(i, i + 4)):
            return True

    # Check vertical
    if row <= ROWS - 4:
        if all(board[row + i][col] == checker for i in range(4)):
            return True

    # Check diagonal (top-left to bottom-right)
    for i in range(-3, 1):
        if (0 <= row + i < ROWS - 3 and 0 <= col + i < COLS - 3 and
            all(board[row + i + j][col + i + j] == checker for j in range(4))):
            return True

    # Check diagonal (bottom-left to top-right)
    for i in range(-3, 1):
        if (3 <= row + i < ROWS and 0 <= col + i < COLS - 3 and
            all(board[row + i - j][col + i + j] == checker for j in range(4))):
            return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    clear_screen()
    
    # Setup
    board = initialize_board(ROWS, COLS)
    num_players = 2  # Modify this to test more players (up to MAX_PLAYERS)
    current_player_idx = random.randint(0, num_players - 1)
    
    print("Starting Connect 4!")
    print_board(board)
    print(f"Player {PLAYERS[current_player_idx]} starts!\n")

    while True:
        current_checker = PLAYERS[current_player_idx]
        
        # Player's turn
        col = get_valid_column(board, f"Player {current_checker}, please enter a column: ")
        drop_checker(board, col, current_checker)
        
        # Print updated board
        clear_screen()
        print_board(board)
        
        # Check for win
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] == current_checker and is_winning_move(board, r, c, current_checker):
                    print(f"Player {current_checker} won!")
                    return
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            return
        
        # Switch player
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
