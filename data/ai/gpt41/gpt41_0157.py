import os
import random
import string

# Constants
ROWS = 6
COLS = 7
MAX_COLUMNS = 26
PLAYERS = 2                   # Set player count here (2 to 5)
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear_screen():
    os.system('clear')  # For Windows use 'cls'

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    sep = "+" + "---+" * cols
    print(header)
    print(sep)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(sep)

def get_valid_column_input(board):
    cols = len(board[0])
    while True:
        choice = input("Please enter a column: ").strip().upper()
        if len(choice) == 1 and choice in string.ascii_uppercase[:cols]:
            col_index = ord(choice) - ord('A')
            if board[0][col_index] != " ":
                print("Column is full! You lose your turn.")
                return None  # Lose turn!
            else:
                return col_index
        else:
            print("Invalid column. Try again.")

def drop_checker(board, col, symbol):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = symbol
            return board.index(row), col  # Return pos for win checking

def check_winner(board, row, col, symbol):
    directions = [(1,0), (0,1), (1,1), (1,-1)]  # vert, horiz, diag \, diag /
    for dr, dc in directions:
        count = 1
        for step in (1, -1):
            r, c = row, col
            while True:
                r += step * dr
                c += step * dc
                if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def is_full(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    curr_player = random.randint(0, PLAYERS-1)
    clear_screen()
    print_board(board)
    print(f"Player {PLAYER_SYMBOLS[curr_player]}, you start!")

    while True:
        print()
        print(f"Player {PLAYER_SYMBOLS[curr_player]},", end=" ")
        col = get_valid_column_input(board)
        if col is None:
            curr_player = (curr_player + 1) % PLAYERS
            continue
        row, col = drop_checker(board, col, PLAYER_SYMBOLS[curr_player])

        clear_screen()
        print_board(board)

        if check_winner(board, row, col, PLAYER_SYMBOLS[curr_player]):
            print(f"Player {PLAYER_SYMBOLS[curr_player]} won!")
            break
        elif is_full(board):
            print("It's a draw!")
            break
        curr_player = (curr_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
