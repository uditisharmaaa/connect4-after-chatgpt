import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Supported checkers for up to 5 players

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+---" + "+---" * (COLS - 1) + "+")  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Rows
        print("+---" + "+---" * (COLS - 1) + "+")  # Row border

def is_valid_input(col):
    return len(col) == 1 and col.isalpha() and 'A' <= col.upper() <= chr(65 + COLS - 1)

def drop_checker(board, col, checker):
    col_index = ord(col.upper()) - 65
    for row in reversed(board):  # Start from bottom row
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal (both) wins
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # Horizontal
                if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Vertical
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Diagonal down-right
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
                # Diagonal up-right
                if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    total_turns = 0

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        col = input(f"Player {current_player}, please enter a column: ")

        if not is_valid_input(col):
            print("Invalid input. Please try again.")
            continue

        if not drop_checker(board, col, current_player):
            print("Column is full. Please try again.")
            continue
        
        total_turns += 1

        # Check for a win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
