import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))

    # Print horizontal separator and rows
    for row in range(len(board)):
        print("+---" * len(board[0]) + "+")
        print("| " + " | ".join(board[row]) + " |")
    print("+---" * len(board[0]) + "+")

def get_valid_columns(board):
    valid = []
    for col in range(len(board[0])):
        if board[0][col] == " ":
            valid.append(chr(ord('A') + col))
    return valid

def input_column(player_checker, board):
    valid_columns = get_valid_columns(board)
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            # Not a single char
            continue
        if col_input not in valid_columns:
            # Either full column or invalid letter
            if col_input < 'A' or col_input >= chr(ord('A') + len(board[0])):
                continue
            # If column is full (not in valid_columns) player loses turn (just return None)
            return None
        return col_input

def place_checker(board, col_letter, checker):
    col = ord(col_letter) - ord('A')
    # Start from bottom row to top
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full, should not reach here as input_column prevents but in case
    return None

def check_win(board, row, col, checker):
    directions = [
        (0,1),   # horizontal right
        (1,0),   # vertical down
        (1,1),   # diagonal down-right
        (1,-1)   # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])
    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row+dr, col+dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row-dr, col-dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]

    # Choose a random starting player index
    current_player_i = random.randint(0, PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_i]
        col_letter = input_column(player_checker, board)

        if col_letter is None:
            # Column is full, player loses turn
            # Advance turn
            current_player_i = (current_player_i + 1) % PLAYERS
            print_board(board)
            continue

        pos = place_checker(board, col_letter, player_checker)

        if pos is None:
            # Should not occur due to input validation
            current_player_i = (current_player_i + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        row, col = pos
        if check_win(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("Game is a draw!")
            break

        current_player_i = (current_player_i + 1) % PLAYERS

if __name__ == "__main__":
    main()
