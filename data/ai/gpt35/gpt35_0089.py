import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # max 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    board = []
    for _ in range(rows):
        board.append([" "] * columns)
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    headers = "  "
    for i in range(len(board[0])):
        headers += "  " + chr(ord('A') + i) + " "
    print(headers)
    # Print board with lines
    line = "+" + "---+" * len(board[0])
    for row in board:
        print(line)
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print(line)

def get_player_input(player_checker, board):
    columns = len(board[0])
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ")
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter for the column.")
            continue
        col_input = col_input.upper()
        col_index = ord(col_input) - ord('A')
        if col_index < 0 or col_index >= columns:
            print("Invalid column. Please enter a valid column letter.")
            continue
        # Check if column is full
        if board[0][col_index] != " ":
            print("Column is full. You lose your turn.")
            return -1
        return col_index

def place_checker(board, col, checker):
    # Place checker at lowest available spot in column
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Should not reach here because place_checker called only if column not full
    return -1, -1

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Check diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Check diagonal up-right
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    # Use constants, 6x7 board, 2 players
    rows = ROWS
    cols = COLUMNS
    players = PLAYERS
    checkers = CHECKERS[:players]

    board = create_board(rows, cols)
    # Select random starting player
    current_player_index = random.randint(0, players - 1)

    while True:
        print_board(board)
        current_checker = checkers[current_player_index]
        col = get_player_input(current_checker, board)
        if col == -1:
            # Column full: lose turn, next player
            current_player_index = (current_player_index + 1) % players
            continue
        place_checker(board, col, current_checker)
        if check_winner(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        current_player_index = (current_player_index + 1) % players

if __name__ == "__main__":
    main()
