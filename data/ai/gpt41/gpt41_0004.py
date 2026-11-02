import random
import os
import sys

# ----- Constants -----
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2  # Set 2 for submission
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# ----- Helper functions -----
def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    header = "  " + "   ".join([chr(ord("A") + i) for i in range(len(board[0]))])
    print(header)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_valid_columns(board):
    # Returns list of column indexes that are not full
    valid_cols = []
    for col in range(len(board[0])):
        if board[0][col] == " ":
            valid_cols.append(col)
    return valid_cols

def get_player_input(board, player_checker):
    cols = len(board[0])
    while True:
        col_letter = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_letter) != 1 or not col_letter.isalpha():
            print("Invalid input. Please enter a single uppercase letter.")
            continue
        col_idx = ord(col_letter) - ord("A")
        if not (0 <= col_idx < cols):
            print(f"Invalid column. Valid columns: {[chr(ord('A') + i) for i in get_valid_columns(board)]}")
            continue
        if board[0][col_idx] != " ":
            print("That column is full. You lose your turn!")
            return None  # Lose the turn if column is full
        return col_idx

def drop_checker(board, col, checker):
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # should not reach here if called with a valid col

def is_winning_move(board, row, col, checker):
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    win_count = 4
    for dr, dc in directions:
        count = 1
        # positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= win_count:
            return True
    return False

def is_draw(board):
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def select_first_player(num_players):
    return random.randint(0, num_players - 1)

def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    player = select_first_player(NUM_PLAYERS)
    print_board(board)
    print(f"Player {checkers[player]} will start the game!")

    while True:
        print_board(board)
        col_idx = get_player_input(board, checkers[player])

        if col_idx is None:
            # full column, lose turn
            player = (player + 1) % NUM_PLAYERS
            continue

        row_idx, _ = drop_checker(board, col_idx, checkers[player])

        if is_winning_move(board, row_idx, col_idx, checkers[player]):
            print_board(board)
            print(f"Player {checkers[player]} won!")
            break
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        player = (player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
