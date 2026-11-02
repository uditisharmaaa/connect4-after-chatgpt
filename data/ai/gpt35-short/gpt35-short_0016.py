import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    # Create an empty board: list of ROWS, each row is a list of COLS filled with ' '
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(COL_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (2*COLS + 1))  # Bottom border

def get_player_count():
    while True:
        count = input(f"Enter number of players (2-{len(PLAYER_SYMBOLS)}): ")
        if count.isdigit():
            count = int(count)
            if 2 <= count <= len(PLAYER_SYMBOLS):
                return count
        print("Invalid number of players. Try again.")

def get_valid_move(board, player):
    while True:
        move = input(f"Player {player}, choose a column (A-G): ").upper()
        if move in COL_LABELS:
            col = COL_LABELS.index(move)
            # Check if column is not full
            if board[0][col] == ' ':
                return col
            else:
                print("That column is full! Try another one.")
        else:
            print("Invalid column. Choose a letter from A to G.")

def make_move(board, col, player):
    # Start from bottom row and place the piece in the first empty spot in col
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_direction(board, start_row, start_col, delta_row, delta_col, player):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == player:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, player):
    # Check all 4 directions: horizontal, vertical, and the two diagonals
    # We count pieces on both sides including the current one,
    # so we subtract 1 to avoid double counting the start position.

    # Horizontal (left + right)
    total = (check_direction(board, row, col, 0, -1, player) +
             check_direction(board, row, col, 0, 1, player) - 1)
    if total >= 4:
        return True

    # Vertical (up + down)
    total = (check_direction(board, row, col, -1, 0, player) +
             check_direction(board, row, col, 1, 0, player) - 1)
    if total >= 4:
        return True

    # Diagonal / (bottom-left to top-right)
    total = (check_direction(board, row, col, 1, -1, player) +
             check_direction(board, row, col, -1, 1, player) - 1)
    if total >= 4:
        return True

    # Diagonal \ (top-left to bottom-right)
    total = (check_direction(board, row, col, -1, -1, player) +
             check_direction(board, row, col, 1, 1, player) - 1)
    if total >= 4:
        return True

    return False

def check_draw(board):
    # If top row has no empty spaces, board is full -> draw
    return all(space != ' ' for space in board[0])

def main():
    player_count = get_player_count()
    players = PLAYER_SYMBOLS[:player_count]

    board = create_board()

    # Pick a random first player index
    current_index = random.randint(0, player_count - 1)

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_index]

        col = get_valid_move(board, current_player)
        row, col = make_move(board, col, current_player)

        if check_win(board, row, col, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("Game ends in a draw!")
            break

        # Next player
        current_index = (current_index + 1) % player_count

if __name__ == "__main__":
    main()
