import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for i in range(COLUMNS):
        header += " " + chr(ord('A') + i) + "  "
    print(header)
    # Print board rows with separators
    row_sep = "+" + "---+" * COLUMNS
    for row in board:
        print(row_sep)
        line = "|"
        for cell in row:
            line += " " + cell + " |"
        print(line)
    print(row_sep)

def input_column(player):
    while True:
        inp = input(f"Player {player}, please enter a column: ").strip()
        if len(inp) != 1:
            print("Invalid input. Please enter exactly one letter corresponding to a column.")
            continue
        col_char = inp.upper()
        if not ('A' <= col_char <= chr(ord('A') + COLUMNS - 1)):
            print("Invalid input. Column out of range.")
            continue
        return ord(col_char) - ord('A')

def place_checker(board, col, checker):
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    # Column full
    return False

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, checker):
    # Check all cells if they can start a 4 in a row
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == checker:
                # Horizontal right
                if c + 3 < COLUMNS:
                    if all(board[r][c + i] == checker for i in range(4)):
                        return True
                # Vertical down
                if r + 3 < ROWS:
                    if all(board[r + i][c] == checker for i in range(4)):
                        return True
                # Diagonal down-right
                if r + 3 < ROWS and c + 3 < COLUMNS:
                    if all(board[r + i][c + i] == checker for i in range(4)):
                        return True
                # Diagonal down-left
                if r + 3 < ROWS and c - 3 >= 0:
                    if all(board[r + i][c - i] == checker for i in range(4)):
                        return True
    return False

def check_draw(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current = random.randrange(PLAYERS)
    print_board(board)
    print(f"Player {players_checkers[current]} starts.")

    while True:
        checker = players_checkers[current]
        col = input_column(checker)
        placed = place_checker(board, col, checker)
        if not placed:
            print("Column full! You lose your turn.")
            # lose the turn, continue to next player
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        
        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if check_draw(board):
            print("The game is a draw.")
            break

        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
