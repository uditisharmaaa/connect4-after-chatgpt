import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']
WINNING_COUNT = 4

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def is_winner(board, checker):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if (c + WINNING_COUNT <= COLS and all(board[r][c + i] == checker for i in range(WINNING_COUNT)) or
                r + WINNING_COUNT <= ROWS and all(board[r + i][c] == checker for i in range(WINNING_COUNT)) or
                r + WINNING_COUNT <= ROWS and c + WINNING_COUNT <= COLS and all(board[r + i][c + i] == checker for i in range(WINNING_COUNT)) or
                r + WINNING_COUNT <= ROWS and c - WINNING_COUNT + 1 >= 0 and all(board[r + i][c - i] == checker for i in range(WINNING_COUNT))):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = initialize_board()
    current_player = random.choice(range(len(PLAYERS)))

    print_board(board)
    while True:
        col = input(f"Player {PLAYERS[current_player]}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        
        if col < 'A' or col >= chr(65 + COLS) or not drop_checker(board, ord(col) - 65, PLAYERS[current_player]):
            print("Invalid input or column full. Please try again.")
            continue
        
        print_board(board)

        if is_winner(board, PLAYERS[current_player]):
            print(f"Player {PLAYERS[current_player]} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
