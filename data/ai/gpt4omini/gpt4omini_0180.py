import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input(player):
    while True:
        col = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if col in [chr(65 + i) for i in range(COLS)]:
            return ord(col) - 65
        print("Invalid input. Please try again.")

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                # Check horizontal
                if c <= COLS - 4 and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Check diagonal down-right
                if r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
                # Check diagonal down-left
                if r <= ROWS - 4 and c >= 3 and all(board[r + i][c - i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(range(len(PLAYERS)))
    
    print_board(board)

    while True:
        col = get_valid_input(PLAYERS[current_player])
        
        if not place_checker(board, col, PLAYERS[current_player]):
            print("Column is full! Try another column.")
            continue
        
        print_board(board)

        if check_win(board, PLAYERS[current_player]):
            print(f"Player {PLAYERS[current_player]} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
