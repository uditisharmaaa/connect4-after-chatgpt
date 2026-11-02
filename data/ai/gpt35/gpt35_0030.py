import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(labels))
    # Print the board with borders
    for r in range(rows):
        print("+" + "---+" * cols)
        print("|" + "|".join(" {} ".format(board[r][c]) for c in range(cols)) + "|")
    print("+" + "---+" * cols)

def get_column_index(column_char, cols):
    # Convert a column letter to index (A->0, B->1,...)
    if len(column_char) != 1:
        return -1
    c = column_char.upper()
    if c < 'A' or c >= chr(ord('A') + cols):
        return -1
    return ord(c) - ord('A')

def is_valid_column(board, col):
    # Check if column is not full
    return board[0][col] == " "

def place_checker(board, col, checker):
    # Place checker in the lowest available row in column col
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column full

def check_line(line, checker):
    # Check if there is WIN_LENGTH consecutive checkers in a line
    count = 0
    for c in line:
        if c == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c+i] == checker for i in range(WIN_LENGTH)):
                return True
    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r+i][c] == checker for i in range(WIN_LENGTH)):
                return True
    # Diagonal /
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    # Diagonal \
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_draw(board):
    # If no empty space on top row, board is full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]

    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        player = players[current_player_index]
        print(f"Player {player}, please enter a column:")
        col_input = input().strip()

        col = get_column_index(col_input, COLS)
        if col == -1:
            print("Invalid input. Please enter a valid column letter.")
            continue

        if not is_valid_column(board, col):
            print("Column is full, you lose your turn.")
            current_player_index = (current_player_index + 1) % PLAYERS
            print_board(board)
            continue

        place_checker(board, col, player)
        print_board(board)

        if check_win(board, player):
            print(f"Player {player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
