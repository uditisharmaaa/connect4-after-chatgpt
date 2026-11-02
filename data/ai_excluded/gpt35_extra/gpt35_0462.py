import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players allowed
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column headers
    header = "  "
    for i in range(cols):
        header += "  " + chr(ord('A') + i) + " "
    print(header)
    # Print board rows with separators
    line_sep = "+" + "---+" * cols
    for r in range(rows):
        print(line_sep)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line_sep)

def get_valid_column_input(board, player):
    cols = len(board[0])
    while True:
        choice = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(choice) != 1:
            # Invalid length
            continue
        col = ord(choice) - ord('A')
        if col < 0 or col >= cols:
            # Outside board range
            continue
        # Check if column is full
        if board[0][col] != " ":
            # Column full, player loses turn (invalid move)
            return None
        return col

def place_checker(board, col, checker):
    # Place checker at the lowest free spot in a column
    rows = len(board)
    for r in range(rows-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    # Should not reach here if checked before
    return None, None

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0
    # Check diagonal (bottom-left to top-right)
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            win = True
            for i in range(WIN_COUNT):
                if board[r + i][c + i] != checker:
                    win = False
                    break
            if win:
                return True
    # Check diagonal (top-left to bottom-right)
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            win = True
            for i in range(WIN_COUNT):
                if board[r - i][c + i] != checker:
                    win = False
                    break
            if win:
                return True
    return False

def check_draw(board):
    # If top row is all full, board is full
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    checkers = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = checkers[current_player_index]
        col = get_valid_column_input(board, player_checker)
        if col is None:
            # Column full, lose turn, next player
            current_player_index = (current_player_index + 1) % PLAYERS
            continue

        place_checker(board, col, player_checker)
        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        if check_draw(board):
            print("The game is a draw.")
            break
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
