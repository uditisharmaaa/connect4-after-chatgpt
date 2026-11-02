import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column headers
    header = "  "
    for i in range(COLUMNS):
        header += chr(ord('A') + i) + "   "
    print(header)
    # Print rows
    for r in range(ROWS):
        print("+---"*COLUMNS + "+")
        row_str = ""
        for c in range(COLUMNS):
            row_str += "| " + board[r][c] + " "
        row_str += "|"
        print(row_str)
    print("+---"*COLUMNS + "+")

def get_valid_column_input(board, player):
    while True:
        col_input = input(f"Player {player}, please enter a column: ")
        if len(col_input) != 1:
            # Invalid length
            continue
        col_letter = col_input.upper()
        if not ('A' <= col_letter <= chr(ord('A') + COLUMNS - 1)):
            # Invalid column letter
            continue
        col = ord(col_letter) - ord('A')
        # Check if column is full
        if board[0][col] != " ":
            # Column full, player loses turn
            return None
        return col

def place_checker(board, col, checker):
    # Place checker in the lowest available row in column col
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    # Should not reach here because we check for full column before
    return None

def check_for_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLUMNS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # Check vertical
    for c in range(COLUMNS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # Check diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True
    # Check diagonal (bottom-left to top-right)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if (board[r][c] == checker and
                board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and
                board[r-3][c+3] == checker):
                return True
    return False

def check_for_draw(board):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)

    print_board(board)
    print(f"Player {players[current_player_index]} starts first!")

    while True:
        player = players[current_player_index]
        col = get_valid_column_input(board, player)
        if col is None:
            # Column full, loses turn
            print(f"Column full. Player {player} loses turn.")
        else:
            place_checker(board, col, player)
            print_board(board)
            if check_for_win(board, player):
                print(f"Player {player} won!")
                break
            if check_for_draw(board):
                print("Game is a draw!")
                break
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
