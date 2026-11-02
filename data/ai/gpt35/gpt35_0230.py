import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    header = "  "
    for i in range(cols):
        header += "  " + chr(ord('A') + i) + "  "
    print(header)
    # Print separator line
    sep_line = "+" + "---+" * cols
    # Print rows
    for row in board:
        print(sep_line)
        row_line = "|"
        for cell in row:
            row_line += " " + cell + " |"
        print(row_line)
    print(sep_line)

def is_valid_column(col_char, cols):
    if len(col_char) != 1:
        return False
    c = col_char.upper()
    return 'A' <= c < chr(ord('A') + cols)

def column_index(col_char):
    return ord(col_char.upper()) - ord('A')

def place_checker(board, col, checker):
    # Place checker in the lowest empty position in the column
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column full

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and board[r][c+1] == checker and
                board[r][c+2] == checker and board[r][c+3] == checker):
                return True
    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == checker and board[r+1][c] == checker and
                board[r+2][c] == checker and board[r+3][c] == checker):
                return True
    # Check diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == checker and board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and board[r+3][c+3] == checker):
                return True
    # Check diagonal up-right
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and board[r-3][c+3] == checker):
                return True
    return False

def board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    rows = ROWS
    cols = COLUMNS
    players = MAX_PLAYERS
    checkers = CHECKERS[:players]

    board = create_board(rows, cols)

    # Randomly pick first player
    current_player = random.randint(0, players -1)

    print_board(board)

    while True:
        player_checker = checkers[current_player]
        prompt = f"Player {player_checker}, please enter a column: "
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column(user_input, cols):
                # Invalid input, repeat
                continue
            col = column_index(user_input)
            row_placed = place_checker(board, col, player_checker)
            if row_placed == -1:
                # Column full, lose turn and break input loop
                break
            else:
                # Valid move, break input loop
                break

        if row_placed == -1:
            # Column full, player loses turn (do nothing)
            pass
        else:
            print_board(board)
            # Check win
            if check_winner(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            # Check draw
            if board_full(board):
                print("The game is a draw!")
                break
        current_player = (current_player + 1) % players

if __name__ == "__main__":
    main()
