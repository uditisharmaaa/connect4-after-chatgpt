import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Only first PLAYERS will be used
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    headers = "  " + "   ".join([chr(ord('A') + i) for i in range(len(board[0]))])
    print(headers)
    # Print the board structure
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def is_valid_column(input_str, board):
    if len(input_str) != 1:
        return False
    col_char = input_str.upper()
    if not ('A' <= col_char <= chr(ord('A') + len(board[0]) -1 )):
        return False
    col_index = ord(col_char) - ord('A')
    # Check if column is full
    if board[0][col_index] != " ":
        return False
    return True

def get_lowest_empty_row(board, col):
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1  # Column full

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            count = 0
            for offset in range(WIN_LENGTH):
                if board[r][c+offset] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            count = 0
            for offset in range(WIN_LENGTH):
                if board[r+offset][c] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    # Diagonal down-right check
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            count = 0
            for offset in range(WIN_LENGTH):
                if board[r+offset][c+offset] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    # Diagonal up-right check
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            count = 0
            for offset in range(WIN_LENGTH):
                if board[r - offset][c + offset] == checker:
                    count += 1
                else:
                    break
            if count == WIN_LENGTH:
                return True

    return False

def is_draw(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]

    current_player_index = random.randint(0, PLAYERS -1)
    print_board(board)

    while True:
        player_checker = players[current_player_index]
        input_valid = False

        while not input_valid:
            move = input(f"Player {player_checker}, please enter a column: ").upper()
            if not is_valid_column(move, board):
                if len(move) == 1 and ('A' <= move <= chr(ord('A') + COLUMNS - 1)):
                    # Valid letter but full column
                    print("Column is full. You lose your turn.")
                    input_valid = True # lose turn
                    move = None
                else:
                    print("Invalid input. Please enter a valid column letter.")
            else:
                input_valid = True

        if move is not None:
            col = ord(move) - ord('A')
            row = get_lowest_empty_row(board, col)
            if row != -1:
                board[row][col] = player_checker
                print_board(board)

                if check_winner(board, player_checker):
                    print(f"Player {player_checker} won!")
                    break

                if is_draw(board):
                    print("The game is a draw!")
                    break
            else:
                # This case theoretically shouldn't occur since is_valid_column checks column full.
                print("Unexpected error: Column full.")
        else:
            print_board(board)

        current_player_index = (current_player_index +1) % PLAYERS

if __name__ == "__main__":
    main()
