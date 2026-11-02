import os
import random

# Constants for board size and player count
ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def init_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(i + 65) for i in range(COLS)]))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def is_valid_input(col, cols):
    return col.isalpha() and 0 <= (ord(col) - 65) < cols

def is_column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return

def check_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            # Check horizontal
            if col <= COLS - 4 and all(board[row][c] == checker for c in range(col, col + 4)):
                return True
            # Check vertical
            if row <= ROWS - 4 and all(board[r][col] == checker for r in range(row, row + 4)):
                return True
            # Check diagonal \
            if row <= ROWS - 4 and col <= COLS - 4 and all(board[row + i][col + i] == checker for i in range(4)):
                return True
            # Check diagonal /
            if row >= 3 and col <= COLS - 4 and all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = init_board(ROWS, COLS)
    current_player = random.choice(range(PLAYERS))
    print_board(board)

    while True:
        col_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip()
        if not is_valid_input(col_input, COLS):
            print("Invalid input. Try again.")
            continue
        
        col = ord(col_input) - 65
        if is_column_full(board, col):
            print("Column is full. You lose the turn.")
            current_player = (current_player + 1) % PLAYERS
            continue
        
        place_checker(board, col, CHECKERS[current_player])
        print_board(board)

        if check_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
