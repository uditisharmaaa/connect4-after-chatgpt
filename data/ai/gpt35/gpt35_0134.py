import os
import random

# Constants (for submission, board is 6 rows x 7 columns, and 2 players)
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']  # max 5 players as per requirements

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(headers))
    # Print separator line
    sep_line = "+---" * len(board[0]) + "+"
    for row in board:
        print(sep_line)
        print("| " + " | ".join(row) + " |")
    print(sep_line)

def input_column(player, columns):
    while True:
        col = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col) != 1:
            print("Invalid input! Please enter a single uppercase letter corresponding to a column.")
            continue
        if not ('A' <= col <= chr(ord('A') + columns - 1)):
            print("Invalid column! Please enter a letter within the board range.")
            continue
        return ord(col) - ord('A')

def place_checker(board, col, checker):
    # from bottom row up, place checker in first empty space in column
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    # column full
    return None, None

def check_win(board, last_row, last_col, checker):
    if last_row is None or last_col is None:
        return False
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # check positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_CONDITION:
            return True
    return False

def is_draw(board):
    # If no empty space left in the top row, it's a draw
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_index]
        col = input_column(player_checker, COLUMNS)
        row, col_placed = place_checker(board, col, player_checker)
        if row is None:
            # column full, player loses turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # still print board, turn lost
            print_board(board)
            continue

        print_board(board)
        if check_win(board, row, col_placed, player_checker):
            print(f"Player {player_checker} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
