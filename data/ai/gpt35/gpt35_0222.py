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

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    clear_screen()
    # Print column labels
    header = "  "
    for c in range(cols):
        header += "  " + chr(ord('A') + c) + " "
    print(header)
    # Print the board rows
    for r in range(len(board)):
        print("+" + "---+" * cols)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * cols)

def input_column(player_checker, board):
    cols = len(board[0])
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip()
        if len(inp) != 1:
            continue
        col_char = inp.upper()
        if not ('A' <= col_char <= chr(ord('A') + cols - 1)):
            continue
        col = ord(col_char) - ord('A')
        if board[0][col] != " ":
            # Column full, player loses turn
            return None
        return col

def place_checker(board, col, checker):
    # Place checker in lowest available row in column col
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Should not reach here if column not full
    return None

def check_winner(board, row, col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_dir(r, c, dr, dc):
        count = 0
        rr, cc = r + dr, c + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        return count

    # Directions: horizontal, vertical, diag \, diag /
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]

    for dr, dc in directions:
        total = 1  # The placed checker itself
        total += count_dir(row, col, dr, dc)
        total += count_dir(row, col, -dr, -dc)
        if total >= WIN_COUNT:
            return True
    return False

def board_full(board):
    # If top row has any space, not full
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]

    current_player_index = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        player_checker = players[current_player_index]
        col = input_column(player_checker, board)
        if col is None:
            # Column full -> lose turn
            current_player_index = (current_player_index + 1) % PLAYERS
            continue
        position = place_checker(board, col, player_checker)
        print_board(board)

        if check_winner(board, position[0], position[1], player_checker):
            print(f"Player {player_checker} won!")
            break

        if board_full(board):
            print("The game is a draw.")
            break

        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
